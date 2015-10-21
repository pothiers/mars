# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0004_auto_20151020_1415'),
    ]

    operations = [
        migrations.AddField(
            model_name='slot',
            name='pi_affiliation',
            field=models.CharField(max_length=160, default='NONE GIVEN'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='slot',
            name='pi_name',
            field=models.CharField(max_length=80, default='NONE GIVEN'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='slot',
            name='title',
            field=models.CharField(max_length=256, default='NONE GIVEN'),
            preserve_default=False,
        ),
    ]
