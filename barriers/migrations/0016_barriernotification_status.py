# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-09 09:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barriers', '0015_auto_20171004_1056'),
    ]

    operations = [
        migrations.AddField(
            model_name='barriernotification',
            name='status',
            field=models.CharField(blank=True, choices=[('Inactive', 'Inactive'), ('Active', 'Active')], default=None, max_length=20, null=True),
        ),
    ]
