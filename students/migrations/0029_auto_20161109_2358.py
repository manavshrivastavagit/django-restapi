# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-09 21:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0028_auto_20161109_2343'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='news',
            options={'ordering': ['-posted_on'], 'verbose_name_plural': 'news'},
        ),
        migrations.AlterField(
            model_name='news',
            name='posted_on',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
