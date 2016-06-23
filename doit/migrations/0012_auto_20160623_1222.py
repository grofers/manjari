# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-23 12:22
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doit', '0011_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='user_info',
            field=models.ForeignKey(default=0, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
