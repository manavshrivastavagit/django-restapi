# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-07 16:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0019_auto_20161107_1838'),
    ]

    operations = [
        migrations.AddField(
            model_name='homework',
            name='materials',
            field=models.FileField(blank=True, null=True, upload_to='homework_materials/'),
        ),
    ]