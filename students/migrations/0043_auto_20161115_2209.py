# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-15 22:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0042_exam_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='details',
            field=models.TextField(blank=True, max_length=1000),
        ),
    ]