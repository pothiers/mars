# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0002_slot_frozen'),
    ]

    operations = [
        migrations.CreateModel(
            name='SlotSet',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('xmlfile', models.FileField(upload_to='')),
                ('begin', models.DateField()),
                ('end', models.DateField()),
            ],
        ),
    ]
