# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-25 09:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vpc', '0014_auto_20170925_1626'),
    ]

    operations = [
        migrations.AddField(
            model_name='createip',
            name='bandwidth_charge_mode',
            field=models.CharField(choices=[('traffic', '按流量计费'), ('bandwidth', '按带宽计费')], max_length=10, null=True, verbose_name='带宽计费方式'),
        ),
    ]
