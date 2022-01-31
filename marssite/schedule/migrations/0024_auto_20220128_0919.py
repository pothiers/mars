# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2022-01-28 16:19
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0023_auto_20170928_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='defaultpropid',
            name='propids',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), size=None),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='propid',
            field=models.CharField(help_text='YYYYs-nnnn (s[emester]:: A|B)', max_length=20, primary_key=True, serialize=False),
        ),
    ]
