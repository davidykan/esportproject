# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-16 02:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]
