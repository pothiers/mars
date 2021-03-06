# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-01 16:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tada', '0007_hdrfunc_documentation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hdrfunc',
            name='documentation',
            field=models.TextField(blank=True, help_text='Function description.'),
        ),
        migrations.AlterField(
            model_name='hdrfunc',
            name='name',
            field=models.CharField(help_text='Function name as used in personality.', max_length=40, unique=True),
        ),
    ]
