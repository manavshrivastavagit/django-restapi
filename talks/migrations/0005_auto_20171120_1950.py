# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-11-20 17:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('talks', '0004_auto_20171118_1944'),
    ]

    operations = [
        migrations.CreateModel(
            name='Meetup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
            ],
            options={
                'ordering': ['date'],
            },
        ),
        migrations.AlterModelOptions(
            name='talk',
            options={'ordering': ['vote_score']},
        ),
        migrations.RemoveField(
            model_name='talk',
            name='date',
        ),
        migrations.AddField(
            model_name='talk',
            name='meetup',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='talks', to='talks.Meetup'),
        ),
    ]
