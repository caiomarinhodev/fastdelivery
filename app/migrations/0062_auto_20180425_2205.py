# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-04-25 22:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0061_auto_20180412_1235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='troco',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]