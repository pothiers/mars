# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-10-10 20:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tada', '0021_auto_20171006_0617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tacinstrumentalias',
            name='tac',
            field=models.CharField(help_text='Name used by Dave Bells TAC Schedule', max_length=20, primary_key=True, serialize=False),
        ),
        migrations.AlterUniqueTogether(
            name='tacinstrumentalias',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='tacinstrumentalias',
            name='id',
        ),
    ]
