# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-04 10:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barriers', '0012_auto_20171002_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='barriersource',
            name='remote_url',
            field=models.URLField(blank=True, max_length=300, null=True),
        ),
    ]
