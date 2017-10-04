# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-04 10:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barriers', '0013_auto_20171004_1023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='barriercountry',
            name='govuk_index_entry_code',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='GOV.UK index code'),
        ),
    ]