# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0011_auto_20151202_1007'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='slot',
            name='half',
        ),
        migrations.RemoveField(
            model_name='slot',
            name='instrument',
        ),
    ]
