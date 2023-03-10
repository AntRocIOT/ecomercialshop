# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-05-14 11:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import tenda.models


class Migration(migrations.Migration):

    dependencies = [
        ('tenda', '0015_auto_20180513_2035'),
    ]

    operations = [
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=tenda.models.get_image_filename, verbose_name='Image')),
            ],
        ),
        migrations.RemoveField(
            model_name='product',
            name='avatar',
        ),
        migrations.AddField(
            model_name='images',
            name='post',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='tenda.Product'),
        ),
    ]
