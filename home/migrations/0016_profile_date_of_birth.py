# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-10 13:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_remove_profile_date_of_birth'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='date_of_birth',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
