# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-13 16:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('upvote', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submission',
            name='pub_date',
        ),
        migrations.AddField(
            model_name='submission',
            name='published_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]