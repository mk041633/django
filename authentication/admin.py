from django.contrib import admin
from . models import User


@admin.register(User)
class volunteerInfo(admin.ModelAdmin):
    list_display = ('username', 'is_staff', 'id', 'email', 'first_name', 'last_name', 'project_name', 'date_joined')