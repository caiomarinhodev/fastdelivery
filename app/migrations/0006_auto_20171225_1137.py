# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-12-25 14:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='type_message',
            field=models.CharField(choices=[('NOVO_PEDIDO', 'NOVO_PEDIDO'), ('DELETE_LOJA', 'DELETE_LOJA'), ('ACCEPT_ORDER', 'ACCEPT_ORDER'), ('CANCEL_ORDER', 'CANCEL_ORDER'), ('ENABLE_ROTA', 'ENABLE_ROTA'), ('ORDER_DELIVERED', 'ORDER_DELIVERED'), ('ADMIN_MESSAGE', 'ADMIN_MESSAGE'), ('ALL_DELIVERED', 'ALL_DELIVERED'), ('LOJA_MESSAGE', 'LOJA_MESSAGE'), ('MOTORISTA_MESSAGE', 'MOTORISTA_MESSAGE')], max_length=100),
        ),
    ]
