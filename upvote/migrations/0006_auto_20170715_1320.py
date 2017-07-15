# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-15 20:20
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import upvote.models


class Migration(migrations.Migration):

    dependencies = [
        ('upvote', '0005_auto_20170714_1032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='word',
            field=models.CharField(max_length=50, unique=True, validators=[django.core.validators.RegexValidator('^[a-zA-Z]*$', 'Only letters are allowed.'), upvote.models.validate_profanity]),
        ),
    ]
