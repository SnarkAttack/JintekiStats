# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-17 04:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0004_jintekiusername'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='corp_credits',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='corp_draws',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='corp_installs',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='corp_mulligan',
            field=models.NullBooleanField(default=None),
        ),
        migrations.AddField(
            model_name='game',
            name='runner_credits',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='runner_draws',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='runner_installs',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='runner_mulligan',
            field=models.NullBooleanField(default=None),
        ),
    ]
