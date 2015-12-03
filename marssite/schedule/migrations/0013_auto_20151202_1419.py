# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0012_auto_20151202_1054'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proposal',
            name='pi_affiliation',
        ),
        migrations.RemoveField(
            model_name='proposal',
            name='pi_name',
        ),
        migrations.RemoveField(
            model_name='proposal',
            name='title',
        ),
        migrations.AlterField(
            model_name='slot',
            name='telescope',
            field=models.CharField(choices=[('aat', 'aat'), ('ct09m', 'ct09m'), ('ct13m', 'ct13m'), ('ct15m', 'ct15m'), ('ct1m', 'ct1m'), ('ct4m', 'ct4m'), ('gem_n', 'gem_n'), ('gem_s', 'gem_s'), ('gemn', 'gemn'), ('gems', 'gems'), ('het', 'het'), ('keckI', 'keckI'), ('keckII', 'keckII'), ('kp09m', 'kp09m'), ('kp13m', 'kp13m'), ('kp21m', 'kp21m'), ('kp4m', 'kp4m'), ('kpcf', 'kpcf'), ('magI', 'magI'), ('magII', 'magII'), ('mmt', 'mmt'), ('soar', 'soar'), ('wiyn', 'wiyn')], max_length=10),
        ),
    ]
