# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-10 14:06
from __future__ import unicode_literals

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_auto_20161210_1517'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='picture',
            field=models.FileField(default='settings.MEDIA_ROOT/default/default.png', storage=django.core.files.storage.FileSystemStorage(location='F:\\Projects\\www\\media'), upload_to='default'),
        ),
    ]
