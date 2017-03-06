# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-01 19:44
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tada', '0009_auto_20170301_0925'),
    ]

    operations = [
        migrations.AddField(
            model_name='hdrfunc',
            name='inkeywords',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(help_text='FITS keywords needed by func', max_length=8), default=list, size=None),
        ),
        migrations.AddField(
            model_name='hdrfunc',
            name='outkeywords',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(help_text='FITS keywords added or modified by func', max_length=8), default=list, size=None),
        ),
        migrations.AlterField(
            model_name='hdrfunc',
            name='definition',
            field=models.TextField(help_text='Python function BODY'),
        ),
        migrations.AlterField(
            model_name='hdrfunc',
            name='documentation',
            field=models.TextField(blank=True, help_text='Function description.', max_length=80),
        ),
    ]