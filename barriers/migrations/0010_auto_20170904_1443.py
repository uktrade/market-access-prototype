# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-04 14:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barriers', '0009_auto_20170904_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='barriertype',
            name='ec_barrier_code',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='barriertype',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
