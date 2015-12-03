# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0010_slot_frozen'),
    ]

    operations = [
        migrations.AddField(
            model_name='slot',
            name='half',
            field=models.CharField(default='1', choices=[('1', '1'), ('2', '2')], max_length=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='slot',
            name='instrument',
            field=models.CharField(default='none', max_length=30),
            preserve_default=False,
        ),
    ]
