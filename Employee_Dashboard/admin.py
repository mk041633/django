from django.contrib import admin
from . models import Tasks
@admin.register(Tasks)
class ProjectInfo(admin.ModelAdmin):
    list_display = ('owner', 'Description', 'Type', 'StartTime', 'StartDate', 'TimeTaken')