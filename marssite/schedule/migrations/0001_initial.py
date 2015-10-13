# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Slot',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('telescope', models.CharField(max_length=80)),
                ('obsdate', models.DateField()),
                ('propid', models.CharField(max_length=12)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='slot',
            unique_together=set([('telescope', 'obsdate')]),
        ),
        migrations.AlterIndexTogether(
            name='slot',
            index_together=set([('telescope', 'obsdate')]),
        ),
    ]
