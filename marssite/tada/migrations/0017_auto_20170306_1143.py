# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-06 18:43
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tada', '0016_auto_20170301_2002'),
    ]

    operations = [
        migrations.CreateModel(
            name='ErrorCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=8, unique=True)),
                ('regexp', models.CharField(help_text='Regular expression to match against long error string.', max_length=80)),
                ('shortdesc', models.CharField(blank=True, max_length=40)),
            ],
        ),
        migrations.AlterField(
            model_name='hdrfunc',
            name='documentation',
            field=models.TextField(blank=True, help_text='Function description.'),
        ),
        migrations.AlterField(
            model_name='hdrfunc',
            name='inkeywords',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=8), default=list, help_text='FITS keywords used by func', size=None),
        ),
        migrations.AlterField(
            model_name='hdrfunc',
            name='outkeywords',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=8), default=list, help_text='FITS keywords added or modified by func', size=None),
        ),
    ]
