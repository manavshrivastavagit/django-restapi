# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-04 13:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0057_auto_20170104_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='profile_image_url',
            field=models.URLField(default='http://elsyser.herokuapp.com/static/default.png'),
        ),
    ]
