# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-07 22:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audit', '0002_auto_20160516_1622'),
    ]

    operations = [
        migrations.AddField(
            model_name='sourcefile',
            name='staged',
            field=models.BooleanField(default=False, help_text='Marked for subsequent action.'),
        ),
        migrations.AlterField(
            model_name='sourcefile',
            name='obsday',
            field=models.DateField(help_text='Observation Day', null=True),
        ),
    ]