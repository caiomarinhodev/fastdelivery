# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-12-15 16:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_auto_20171215_1341'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='btn_finalizado',
            field=models.BooleanField(default=False),
        ),
    ]