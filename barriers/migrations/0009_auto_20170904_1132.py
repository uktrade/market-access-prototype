# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-04 11:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('barriers', '0008_auto_20170830_1025'),
    ]

    operations = [
        migrations.CreateModel(
            name='BarrierType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('ec_barrier_code', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('is_sps', models.BooleanField(default=False)),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='barriers.BarrierType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BarrierTypes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='marketaccessbarrier',
            name='core_symbol',
            field=models.CharField(blank=True, max_length=500, verbose_name='Core Symbol'),
        ),
        migrations.AlterField(
            model_name='marketaccessbarrier',
            name='mab_type',
            field=models.CharField(blank=True, max_length=500, verbose_name='Barrier type'),
        ),
        migrations.AddField(
            model_name='barriertypes',
            name='barrier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='barriers', to='barriers.MarketAccessBarrier'),
        ),
        migrations.AddField(
            model_name='barriertypes',
            name='barrier_type',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='barrier_types', to='barriers.BarrierTypes'),
        ),
    ]
