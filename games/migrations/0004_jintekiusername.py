# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-08 01:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0003_auto_20170430_1716'),
    ]

    operations = [
        migrations.CreateModel(
            name='JintekiUsername',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jinteki_username', models.CharField(max_length=32)),
                ('site_username', models.CharField(max_length=32)),
            ],
        ),
    ]
