# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-01 15:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0005_auto_20170131_0501'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='corp_name',
            field=models.CharField(default=None, max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='runner_name',
            field=models.CharField(default=None, max_length=32, null=True),
        ),
    ]