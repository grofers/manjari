# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-23 11:32
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doit', '0004_task_user_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='user_info',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
