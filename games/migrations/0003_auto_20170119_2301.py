# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-19 23:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0002_auto_20170119_2257'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OldGame',
            new_name='Game',
        ),
    ]
