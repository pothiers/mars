# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-20 20:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audit', '0015_auditrecord_fstop_host'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auditrecord',
            name='dome_host',
        ),
        migrations.RemoveField(
            model_name='auditrecord',
            name='mountain_host',
        ),
        migrations.RemoveField(
            model_name='auditrecord',
            name='valley_host',
        ),
        migrations.AlterField(
            model_name='auditrecord',
            name='errcode',
            field=models.CharField(blank=True, default='', help_text='Error code for error reported from dataq, tada, archive', max_length=10),
        ),
        migrations.AlterField(
            model_name='auditrecord',
            name='fstop',
            field=models.CharField(blank=True, help_text='Most downstream stop of FITS file', max_length=25),
        ),
    ]
