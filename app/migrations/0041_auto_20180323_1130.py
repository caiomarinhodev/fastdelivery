# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-03-23 11:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0040_auto_20180323_1049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bairro',
            name='valor',
            field=models.CharField(blank=True, default='6', max_length=3, null=True),
        ),
    ]
