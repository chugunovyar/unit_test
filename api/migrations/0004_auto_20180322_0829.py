# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-22 08:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20180322_0456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientanketa',
            name='passport_num',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]