# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Fitsname',
            fields=[
                ('dtnsanam', models.CharField(primary_key=True, max_length=80, serialize=False)),
                ('dtacqnam', models.CharField(max_length=80)),
            ],
        ),
    ]
