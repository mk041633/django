from django.contrib import admin
from . models import Department, Project

@admin.register(Department)
class departmentInfo(admin.ModelAdmin):
    list_display = ('owner', 'dept')



@admin.register(Project)
class ProjectInfo(admin.ModelAdmin):
    list_display = ('owner', 'project')