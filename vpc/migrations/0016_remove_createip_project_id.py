# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-25 09:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vpc', '0015_createip_bandwidth_charge_mode'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='createip',
            name='project_id',
        ),
    ]
