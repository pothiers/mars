# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audit', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submittal',
            name='metadata',
            field=models.TextField(help_text='As JSON', blank=True),
        ),
        migrations.AlterField(
            model_name='submittal',
            name='status',
            field=models.TextField(help_text='From Archive HTTP response', blank=True),
        ),
    ]
