# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-07 15:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0065_submission_checked'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='submission',
            options={'ordering': ['-posted_on']},
        ),
    ]
