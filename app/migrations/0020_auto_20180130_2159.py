# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-01-30 21:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_auto_20180111_2306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ponto',
            name='pedido',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Pedido'),
        ),
    ]