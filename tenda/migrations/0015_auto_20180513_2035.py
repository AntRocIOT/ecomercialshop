# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-05-13 20:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tenda', '0014_bill_city'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bill',
            options={'ordering': ['data']},
        ),
    ]