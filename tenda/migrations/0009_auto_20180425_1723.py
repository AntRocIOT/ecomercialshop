# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-25 17:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenda', '0008_auto_20180425_1721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.FloatField(default=None),
        ),
    ]
