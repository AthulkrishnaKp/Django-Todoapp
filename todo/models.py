from email.policy import default
from enum import auto
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model):
    task_name=models.CharField(max_length=200)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_date=models.DateTimeField(auto_now_add=True)
    status=models.BooleanField(default=False)

    def __str__(self):
        return self.task_name