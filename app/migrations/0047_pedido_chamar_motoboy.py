# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-03-24 10:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0046_logger'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='chamar_motoboy',
            field=models.BooleanField(default=True),
        ),
    ]
