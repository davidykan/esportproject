# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-17 12:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newapp', '0005_auto_20160417_1210'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='status',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
