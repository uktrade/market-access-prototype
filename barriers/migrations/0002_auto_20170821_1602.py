# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-21 16:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barriers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marketaccessbarrier',
            name='comments_due_date',
            field=models.DateField(blank=True, null=True, verbose_name='Final date for comments'),
        ),
        migrations.AlterField(
            model_name='marketaccessbarrier',
            name='distribution_date',
            field=models.DateField(blank=True, null=True, verbose_name='Distribution Date'),
        ),
    ]
