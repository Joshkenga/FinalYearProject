from django.contrib import admin
from .models import CustomUser, Project, ProjectGroup, Category, GroupMember, ProjectSupervisor

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Project)
admin.site.register(ProjectGroup)
admin.site.register(Category)
admin.site.register(GroupMember)
admin.site.register(ProjectSupervisor)
