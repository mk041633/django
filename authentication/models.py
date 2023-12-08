from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
   project_name = models.CharField(max_length=20, default='')


class YourModel(models.Model):
    field_name = models.CharField(max_length=100)