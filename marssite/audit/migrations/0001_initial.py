# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Submittal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source', models.CharField(max_length=256, help_text='Path of file as submitted')),
                ('archive', models.CharField(max_length=80, help_text='Basename of FITS file in Archive')),
                ('status', models.TextField(help_text='From Archive HTTP response')),
                ('metadata', models.TextField(help_text='As JSON')),
                ('when', models.DateTimeField(help_text='When submitted', auto_now_add=True)),
            ],
            options={
                'ordering': ('when',),
            },
        ),
    ]
