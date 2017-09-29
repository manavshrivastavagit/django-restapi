# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-09-19 19:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0005_auto_20170802_1524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grade',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grades', to='students.Student'),
        ),
        migrations.AlterField(
            model_name='grade',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grades', to='students.Subject'),
        ),
        migrations.AlterField(
            model_name='student',
            name='clazz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='students.Class'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teachers', to='students.Subject'),
        ),
    ]