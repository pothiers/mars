# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0007_auto_20151116_1748'),
    ]

    operations = [
        migrations.AddField(
            model_name='emptyslot',
            name='modified',
            field=models.DateTimeField(help_text='When modified', default=datetime.datetime(2015, 11, 18, 0, 13, 15, 68369, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='proposal',
            name='modified',
            field=models.DateTimeField(help_text='When modified', default=datetime.datetime(2015, 11, 18, 0, 13, 48, 159533, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
