# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0008_auto_20151117_1713'),
    ]

    operations = [
        migrations.AddField(
            model_name='slot',
            name='modified',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2015, 11, 18, 0, 15, 44, 412425, tzinfo=utc), help_text='When modified'),
            preserve_default=False,
        ),
    ]
