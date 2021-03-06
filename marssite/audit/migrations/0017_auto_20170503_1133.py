# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-03 18:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from natica.models import Site,Telescope,Instrument



class Migration(migrations.Migration):

    dependencies = [
        ('audit', '0016_auto_20160920_1355'),
        ('natica', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auditrecord',
            name='instrument',
            field=models.ForeignKey(to='natica.Instrument'),
        ),
        migrations.AlterField(
            model_name='auditrecord',
            name='telescope',
            field=models.ForeignKey(to='natica.Telescope'),
        ),
    ]
