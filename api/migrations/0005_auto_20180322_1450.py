# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-22 14:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20180322_0829'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientanketa',
            name='partner',
            field=models.ForeignKey( on_delete=django.db.models.deletion.CASCADE, to='api.Partner'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='zayavkicreditorg',
            name='predlogenie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Predlogenie'),
            preserve_default=False,
        ),
    ]
