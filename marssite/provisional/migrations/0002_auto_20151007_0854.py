# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('provisional', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fitsname',
            old_name='dtnsanam',
            new_name='id',
        ),
        migrations.RemoveField(
            model_name='fitsname',
            name='dtacqnam',
        ),
        migrations.AddField(
            model_name='fitsname',
            name='source',
            field=models.CharField(null=True, max_length=256),
        ),
    ]
