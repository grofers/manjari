from __future__ import unicode_literals

from django.db import models
from authentication.models import Account


class Task(models.Model):
    '''
    '''
    user_info = models.ForeignKey('authentication.Account', on_delete=models.CASCADE, default=0, null=True)
    description = models.TextField(blank=False)
    due_date = models.DateTimeField()
    task_status = models.BooleanField(default=False)
