# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-03-10 08:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_motorista_configuration'),
    ]

    operations = [
        migrations.AddField(
            model_name='ponto',
            name='itens',
            field=models.TextField(blank=True, null=True),
        ),
    ]
