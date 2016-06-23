from __future__ import unicode_literals

from django.db import models


class Task(models.Model):
    '''
    '''
    description = models.CharField(max_length=256)
    due_date = models.DateTimeField(max_length=128)
    task_status = models.BooleanField(default=False)
