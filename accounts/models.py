from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    timezone = models.CharField(max_length=40)
    reset_time = models.IntegerField()

