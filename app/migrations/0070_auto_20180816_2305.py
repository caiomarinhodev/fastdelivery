# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-08-16 23:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0069_estabelecimento_motoboys'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='pedido',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='request', to='app.Pedido'),
        ),
    ]