# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-25 15:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vpc', '0018_auto_20170925_2217'),
    ]

    operations = [
        migrations.AddField(
            model_name='createip',
            name='result',
            field=models.CharField(choices=[('200', '状态码200，弹性IP创建成功'), ('409', '错误码409，IP地址已被占用，创建失败'), ('400', '错误码400，参数错误，请检查填写项')], max_length=128, null=True, verbose_name='创建结果'),
        ),
        migrations.AlterField(
            model_name='createip',
            name='region',
            field=models.CharField(choices=[('cn-north-1', '华北1'), ('cn-south-1', '华南1'), ('cn-east-2', '华东2')], max_length=32, null=True, verbose_name='区域'),
        ),
    ]
