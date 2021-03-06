# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-20 16:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audit', '0005_auto_20160615_1407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sourcefile',
            name='instrument',
            field=models.CharField(choices=[('90prime', '90prime'), ('mosaic3', 'mosaic3'), ('goodman', 'goodman')], max_length=25),
        ),
        migrations.AlterField(
            model_name='sourcefile',
            name='telescope',
            field=models.CharField(choices=[('soar', 'soar'), ('ct4m', 'ct4m'), ('ct15m', 'ct15m'), ('kp4m', 'kp4m'), ('bok23m', 'bok23m')], max_length=10),
        ),
    ]
