from random import choices

from django.db import models

from django.conf import settings

from taskbar.choices import SeverityChoices, StatusChoices, WorkspaceMembershipRole

# Create your models here.


class Timer(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
    

class Workspace(Timer):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='owned_workspaces')
    description = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.name

class Project(Timer):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50,db_index=True, default=StatusChoices.TASK_TO_DO, choices=StatusChoices.choices)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, db_index=True, related_name='projects')


    def __str__(self):
        return self.name
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["workspace", "name"],
                name="unique_project_per_workspace"
            )
        ]

class Membership(Timer):
    workspace = models.ForeignKey(Workspace,db_index=True, on_delete=models.CASCADE, related_name='memberships')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,db_index=True, on_delete=models.CASCADE, related_name='memberships')
    role = models.CharField(max_length=50,db_index=True, default=WorkspaceMembershipRole.MEMBER, choices=WorkspaceMembershipRole.choices)

    def __str__(self):
        return f'{self.user} is a {self.role} in {self.workspace}'
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["workspace", "user"],
                name="unique_workspace_membership"
            )
        ]
    
class Task(Timer):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50,db_index=True, default=StatusChoices.TASK_TO_DO, choices=StatusChoices.choices)
    assignee = models.ManyToManyField(Membership, db_index=True, blank=True, related_name='assigned_tasks')
    workspace = models.ForeignKey(Workspace,on_delete=models.CASCADE,db_index=True, related_name='tasks')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, db_index=True, related_name='tasks')
    severity = models.CharField(max_length=50, db_index=True, choices=SeverityChoices.choices,default=SeverityChoices.MEDIUM)
    due_date = models.DateField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_tasks')


    def __str__(self):
        return self.title

    class Meta:
        indexes = [
            models.Index(
                fields=["project", "-created_at"]
            ),
            models.Index(
                fields=["assignees", "-created_at"]
            ),
            models.Index(
                fields=["status", "-created_at"]
            ),
            models.Index(
                fields=["severity", "-created_at"]
            ),
            models.Index(
                fields=["workspace", "-created_at"]
            ),
        ]
    

class ActivityLog(Timer):
    workspace = models.ForeignKey(Workspace,db_index=True, on_delete=models.CASCADE, related_name='activity_logs')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='activity_logs')
    action_event_type = models.CharField(max_length=255,db_index=True)
    object_type = models.CharField(max_length=255,db_index=True)
    object_id = models.PositiveIntegerField(db_index=True)
    metadata = models.JSONField(db_index=True,blank=True, null=True)

    def __str__(self):
        return f'{self.user} {self.action_event_type} on {self.object_type} {self.object_id} at {self.created_at}'
    
    class Meta:
        indexes = [
            models.Index(
                fields=["workspace", "-created_at"]
            )
        ]
    



# class Comment(Timer):
#     task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
#     author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
#     content = models.TextField()


#     def __str__(self):
#         return f'Comment by {self.author} on {self.task}'
    
