# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-17 20:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0013_auto_20151202_1419'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposal',
            name='propid',
            field=models.CharField(help_text='YYYYs-nnnn (s[emester]:: A|B)', max_length=10, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='slot',
            name='frozen',
            field=models.BooleanField(default=False, help_text='Protect against changing this slot during a bulk operation.'),
        ),
    ]
