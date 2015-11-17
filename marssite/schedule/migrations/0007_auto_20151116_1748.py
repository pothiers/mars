# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0006_auto_20151102_1011'),
    ]

    operations = [
        migrations.CreateModel(
            name='Proposal',
            fields=[
                ('propid', models.CharField(help_text='YYYYs-nnnn (s[emester]:: A|B)', primary_key=True, serialize=False, max_length=12)),
                ('title', models.CharField(max_length=256)),
                ('pi_name', models.CharField(help_text='Principal Investigator name', max_length=80)),
                ('pi_affiliation', models.CharField(max_length=160)),
            ],
        ),
        migrations.RemoveField(
            model_name='slot',
            name='frozen',
        ),
        migrations.RemoveField(
            model_name='slot',
            name='pi_affiliation',
        ),
        migrations.RemoveField(
            model_name='slot',
            name='pi_name',
        ),
        migrations.RemoveField(
            model_name='slot',
            name='propid',
        ),
        migrations.RemoveField(
            model_name='slot',
            name='title',
        ),
        migrations.AlterField(
            model_name='slot',
            name='telescope',
            field=models.CharField(choices=[('ct09m', 'ct09m'), ('ct13m', 'ct13m'), ('ct15m', 'ct15m'), ('ct1m', 'ct1m'), ('ct4m', 'ct4m'), ('gem_n', 'gem_n'), ('gem_s', 'gem_s'), ('het', 'het'), ('keckI', 'keckI'), ('keckII', 'keckII'), ('kp09m', 'kp09m'), ('kp13m', 'kp13m'), ('kp21m', 'kp21m'), ('kp4m', 'kp4m'), ('kpcf', 'kpcf'), ('magI', 'magI'), ('magII', 'magII'), ('mmt', 'mmt'), ('soar', 'soar'), ('wiyn', 'wiyn')], max_length=10),
        ),
        migrations.AddField(
            model_name='slot',
            name='proposals',
            field=models.ManyToManyField(to='schedule.Proposal'),
        ),
    ]
