# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-30 12:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenda', '0010_auto_20180425_1728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='data',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='bill',
            name='total',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
    ]
