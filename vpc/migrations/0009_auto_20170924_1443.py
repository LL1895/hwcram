# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-24 06:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vpc', '0008_auto_20170924_0016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vpc',
            name='create_time',
            field=models.CharField(max_length=40, null=True, verbose_name='创建时间(UTC)'),
        ),
    ]
