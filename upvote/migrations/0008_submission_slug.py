# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-17 17:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upvote', '0007_auto_20170717_1021'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='slug',
            field=models.SlugField(default='test', editable=False),
            preserve_default=False,
        ),
    ]
