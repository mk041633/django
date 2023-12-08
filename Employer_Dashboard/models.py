from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.conf import settings

class Department(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dept = models.TextField(max_length=20)
    def _str_(self):
        return self.owner


class Project(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.TextField(max_length=20)
    def _str_(self):
        return self.owner



class YourModel(models.Model):
    field_name = models.CharField(max_length=100)