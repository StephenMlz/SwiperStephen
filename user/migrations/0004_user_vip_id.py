# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-03-25 03:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20190323_1432'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='vip_id',
            field=models.IntegerField(default=1, verbose_name='会员信息'),
        ),
    ]
