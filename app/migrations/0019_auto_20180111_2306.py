# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-01-11 23:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_auto_20180109_2324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estabelecimento',
            name='complemento',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Ponto de Refer\xeancia'),
        ),
        migrations.AlterField(
            model_name='estabelecimento',
            name='endereco',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Endere\xe7o'),
        ),
        migrations.AlterField(
            model_name='estabelecimento',
            name='photo',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='motorista',
            name='complemento',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Ponto de Refer\xeancia'),
        ),
        migrations.AlterField(
            model_name='motorista',
            name='endereco',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Endere\xe7o'),
        ),
        migrations.AlterField(
            model_name='motorista',
            name='photo',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ponto',
            name='complemento',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Ponto de Refer\xeancia'),
        ),
        migrations.AlterField(
            model_name='ponto',
            name='endereco',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Endere\xe7o'),
        ),
    ]
