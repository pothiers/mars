# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(max_length=80)),
                ('prop_id', models.CharField(max_length=80)),
                ('dtpropid', models.CharField(max_length=80)),
                ('dtnsanam', models.CharField(max_length=80)),
                ('dtacqnam', models.CharField(max_length=80)),
            ],
            options={
                'db_table': 'voi.siap',
            },
        ),
    ]
