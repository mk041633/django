from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Tasks(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE )
    Description = models.TextField()
    Type = models.CharField(max_length=21)
    StartTime = models.DateTimeField()
    StartDate = models.DateField()
    TimeTaken = models.IntegerField()
    def __str__(self):
        return self.owner.username
    