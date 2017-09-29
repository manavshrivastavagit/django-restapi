# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-09-19 19:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0002_auto_20170807_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='materials', to='students.Subject'),
        ),
    ]