# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-08-09 09:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeworks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='homework',
            name='topic',
            field=models.CharField(default='Homework', max_length=50),
        ),
    ]