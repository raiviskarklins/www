# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-07 13:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20161207_1549'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='picture',
            field=models.FileField(blank=True, upload_to=''),
        ),
    ]