# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-10 11:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_remove_profile_occupation'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='occupation',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]