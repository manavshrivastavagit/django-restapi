# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-17 20:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0046_auto_20161119_2124'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homework',
            name='materials',
        ),
    ]
