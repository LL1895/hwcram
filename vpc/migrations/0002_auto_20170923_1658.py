# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-23 08:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vpc', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vpc',
            name='bandwidth_size',
            field=models.IntegerField(null=True, verbose_name='带宽大小'),
        ),
    ]