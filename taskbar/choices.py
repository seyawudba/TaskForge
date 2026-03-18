from django.db import models
from django.utils.translation import gettext_lazy as _


class StatusChoices(models.TextChoices):
    TASK_TO_DO = "todo", _("To Do")
    TASK_IN_PROGRESS = "in progress", _("In Progress")
    TASK_DONE = "done", _("Done")
    TASK_REVIEW = "review", _("Review")


class SeverityChoices(models.TextChoices):
    LOW = "low", _("Low")
    MEDIUM = "medium", _("Medium")
    HIGH = "high", _("High")


class WorkspaceMembershipRole(models.TextChoices):
    OWNER = "owner", _("Owner")
    ADMIN = "admin", _("Admin")
    MEMBER = "member", _("Member")
    VIEWER = "viewer", _("Viewer")


class EventTypeChoices(models.TextChoices):
    TASK_CREATED = "task_created", _("Task Created")
    TASK_UPDATED = "task_updated", _("Task Updated")
    TASK_DELETED = "task_deleted", _("Task Deleted")
    PROJECT_CREATED = "project_created", _("Project Created")
    PROJECT_UPDATED = "project_updated", _("Project Updated")
    PROJECT_DELETED = "project_deleted", _("Project Deleted")
    WORKSPACE_CREATED = "workspace_created", _("Workspace Created")
    WORKSPACE_UPDATED = "workspace_updated", _("Workspace Updated")
    WORKSPACE_DELETED = "workspace_deleted", _("Workspace Deleted")
    TASK_ASSIGNED = "task_assigned", _("Task Assigned")
    TASK_STATUS_CHANGED = "task_status_changed", _("Task Status Changed")
    COMMENT_ADDED = "comment_added", _("Comment Added")
    MEMBER_INVITED = "member_invited", _("Member Invited")
