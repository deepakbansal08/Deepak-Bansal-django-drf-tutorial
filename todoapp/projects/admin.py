from django.contrib import admin

from projects.models import Project, ProjectMember

class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "max_members", "status")
    list_filter = ("name", "status")

class ProjectMemberAdmin(admin.ModelAdmin):
    list_display = ("project", "member")
    list_filter = ("project", "member")

admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectMember, ProjectMemberAdmin)
