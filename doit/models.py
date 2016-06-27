from __future__ import unicode_literals

from django.db import models
from authentication.models import Account


class Task(models.Model):
    '''
    '''
    user_id = models.IntegerField(null=True)
    description = models.TextField(blank=False)
    due_date = models.DateTimeField(null=True, blank=True)
    task_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,  null=True)
