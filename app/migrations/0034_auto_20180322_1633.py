# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-03-22 16:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0033_auto_20180322_1627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuration',
            name='chamar_motoboy',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='configuration',
            name='has_cozinha',
            field=models.BooleanField(default=True),
        ),
    ]
