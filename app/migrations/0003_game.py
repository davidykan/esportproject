# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-16 23:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newapp', '0002_auto_20160416_0219'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('source_id_game', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('game', models.CharField(max_length=40)),
                ('entry', models.ManyToManyField(to='newapp.Entry')),
            ],
        ),
    ]
