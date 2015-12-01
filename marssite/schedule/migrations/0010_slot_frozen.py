# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0009_slot_modified'),
    ]

    operations = [
        migrations.AddField(
            model_name='slot',
            name='frozen',
            field=models.BooleanField(help_text='Protect against changing this slot during a batch operation.', default=False),
        ),
    ]
