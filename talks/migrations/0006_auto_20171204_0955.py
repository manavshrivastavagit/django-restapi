# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-12-04 07:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('talks', '0005_auto_20171120_1950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meetup',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
