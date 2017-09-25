# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-25 08:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vpc', '0012_auto_20170925_1019'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='createip',
            name='project_id',
        ),
        migrations.AddField(
            model_name='createip',
            name='bandwidth_id',
            field=models.CharField(blank=True, help_text='共享带宽必须填写共享带宽ID，独享带宽不填写', max_length=40, null=True, verbose_name='共享带宽ID'),
        ),
        migrations.AlterField(
            model_name='createip',
            name='account_name',
            field=models.CharField(help_text='填写云账户中已经配置的帐户名', max_length=20, null=True, verbose_name='账户'),
        ),
        migrations.AlterField(
            model_name='createip',
            name='bandwidth_name',
            field=models.CharField(blank=True, help_text='独享带宽必须填写带宽名称，共享带宽不填写', max_length=128, null=True, verbose_name='带宽名称'),
        ),
        migrations.AlterField(
            model_name='createip',
            name='bandwidth_size',
            field=models.IntegerField(help_text='填写数字，范围1~300，单位默认M', null=True, verbose_name='带宽大小'),
        ),
        migrations.AlterField(
            model_name='createip',
            name='publicip',
            field=models.GenericIPAddressField(blank=True, help_text='指定ip地址创建，留空则随机创建ip', null=True, verbose_name='弹性IP'),
        ),
        migrations.AlterField(
            model_name='createip',
            name='region',
            field=models.CharField(choices=[('cn-north-1', '华北1'), ('cn-south-1', '华南1'), ('cn-east-2', '华东2')], max_length=32, verbose_name='区域'),
        ),
    ]
