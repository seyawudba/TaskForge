from django.contrib import admin
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode

from .models import Membership, Project, Task, Workspace

# Register your models here.


class ProjectInline(admin.TabularInline):
    model = Project
    extra = 0


class TaskInline(admin.TabularInline):
    model = Task
    extra = 0


@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ["owner", "name", "projects_count"]
    list_select_related = ["owner"]
    search_fields = ["name", "owner__username"]
    autocomplete_fields = ["owner"]
    inlines = [
        ProjectInline,
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request).select_related("owner")

        qs = qs.annotate(projects_count=Count("projects", distinct=True))

        return qs

    @admin.display(description="Projects Count")
    def projects_count(self, obj):
        url = reverse("admin:taskbar_project_changelist")
        url = f"{url}?{urlencode({'workspace__id': obj.id})}"
        projects_count = obj.projects_count
        return format_html('<a href="{}">{}</a>', url, projects_count)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["name", "workspace", "status"]
    list_select_related = ["workspace"]
    search_fields = ["name", "workspace__name"]
    list_filter = ["status", "workspace"]
    autocomplete_fields = ["workspace"]

    inlines = [
        TaskInline,
    ]


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ["user", "workspace", "role"]
    list_select_related = ["workspace"]
    search_fields = ["user__username", "workspace__name"]
    list_filter = ["role", "workspace"]
    autocomplete_fields = ["user", "workspace"]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["title", "status", "project", "workspace", "severity"]
    list_select_related = ["project", "workspace"]
    search_fields = ["title", "project__name"]
    list_filter = ["status", "project"]
    autocomplete_fields = ["project"]
