# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-11-18 16:59
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('talks', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='talk',
            options={'ordering': ['votes__up', 'date']},
        ),
        migrations.AddField(
            model_name='talk',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 18, 16, 59, 47, 415813, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='talk',
            name='video_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]