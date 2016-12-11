# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-10 20:40
from __future__ import unicode_literals

import django.core.files.storage
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0020_auto_20161210_1609'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'ordering': ['-date_created']},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-date_created']},
        ),
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.CharField(blank=True, max_length=5000),
        ),
        migrations.AlterField(
            model_name='profile',
            name='date_of_birth',
            field=models.DateField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='profile',
            name='picture',
            field=models.FileField(default='default/default.png', storage=django.core.files.storage.FileSystemStorage(location='F:\\Projects\\www\\media'), upload_to='default'),
        ),
    ]