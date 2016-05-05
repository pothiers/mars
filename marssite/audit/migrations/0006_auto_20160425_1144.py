# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-25 18:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audit', '0005_auto_20160420_1658'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sourcefile',
            old_name='source',
            new_name='srcpath',
        ),
        migrations.AddField(
            model_name='sourcefile',
            name='instrument',
            field=models.CharField(choices=[('mosaic3', 'mosaic3'), ('mop/ice', 'mop/ice'), ('arcon', 'arcon'), ('spartan', 'spartan'), ('decam', 'decam'), ('90prime', '90prime'), ('falmingos', 'falmingos'), ('gtcam', 'gtcam'), ('wildfire', 'wildfire'), ('chiron', 'chiron'), ('osiris', 'osiris'), ('arcoiris', 'arcoiris'), ('andicam', 'andicam'), ('echelle', 'echelle'), ('flamingos', 'flamingos'), ('sam', 'sam'), ('newfirm', 'newfirm'), ('goodman', 'goodman'), ('y4kcam', 'y4kcam'), ('minimo/ice', 'minimo/ice'), ('ice', 'ice'), ('ispi', 'ispi'), ('mosaic', 'mosaic'), ('goodman spectrograph', 'goodman spectrograph'), ('hdi', 'hdi'), ('bench', 'bench'), ('kosmos', 'kosmos'), ('spartan ir camera', 'spartan ir camera'), ('soi', 'soi'), ('(p)odi', '(p)odi'), ('whirc', 'whirc'), ('cosmos', 'cosmos'), ('unknown', 'unknown')], default='unknown', max_length=20),
        ),
        migrations.AddField(
            model_name='sourcefile',
            name='telescope',
            field=models.CharField(choices=[('aat', 'aat'), ('ct09m', 'ct09m'), ('ct13m', 'ct13m'), ('ct15m', 'ct15m'), ('ct1m', 'ct1m'), ('ct4m', 'ct4m'), ('gem_n', 'gem_n'), ('gem_s', 'gem_s'), ('gemn', 'gemn'), ('gems', 'gems'), ('het', 'het'), ('keckI', 'keckI'), ('keckII', 'keckII'), ('kp09m', 'kp09m'), ('kp13m', 'kp13m'), ('kp21m', 'kp21m'), ('kp4m', 'kp4m'), ('kpcf', 'kpcf'), ('magI', 'magI'), ('magII', 'magII'), ('mmt', 'mmt'), ('soar', 'soar'), ('wiyn', 'wiyn'), ('unknown', 'unknown')], default='unknown', max_length=10),
        ),
    ]
