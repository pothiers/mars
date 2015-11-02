# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0005_auto_20151020_1459'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='slotset',
            name='begin',
        ),
        migrations.RemoveField(
            model_name='slotset',
            name='end',
        ),
        migrations.AddField(
            model_name='slotset',
            name='comment',
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AlterField(
            model_name='slot',
            name='frozen',
            field=models.BooleanField(default=False, help_text='Protect against changing this slot during a batch operation.'),
        ),
        migrations.AlterField(
            model_name='slot',
            name='obsdate',
            field=models.DateField(help_text='Observation date'),
        ),
        migrations.AlterField(
            model_name='slot',
            name='pi_name',
            field=models.CharField(help_text='Principal Investigator name', max_length=80),
        ),
        migrations.AlterField(
            model_name='slot',
            name='propid',
            field=models.CharField(help_text='YYYYs-nnnn (s:: A|B)', max_length=12),
        ),
        migrations.AlterField(
            model_name='slot',
            name='telescope',
            field=models.CharField(choices=[('ct09m', 'ct09m'), ('ct13m', 'ct13m'), ('ct15m', 'ct15m'), ('ct1m', 'ct1m'), ('ct4m', 'ct4m'), ('gem_n', 'gem_n'), ('gem_s', 'gem_s'), ('het', 'het'), ('keckI', 'keckI'), ('keckII', 'keckII'), ('kp09m', 'kp09m'), ('kp13m', 'kp13m'), ('kp21m', 'kp21m'), ('kp4m', 'kp4m'), ('kpcf', 'kpcf'), ('magI', 'magI'), ('magII', 'magII'), ('mmt', 'mmt'), ('soar', 'soar'), ('wiyn', 'wiyn')], max_length=80),
        ),
    ]
