# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0003_slotset'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmptySlot',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('telescope', models.CharField(max_length=80)),
                ('obsdate', models.DateField()),
            ],
        ),
        migrations.AlterField(
            model_name='slotset',
            name='xmlfile',
            field=models.FileField(upload_to='mars/%Y%m%d/schedule.xml'),
        ),
        migrations.AlterUniqueTogether(
            name='emptyslot',
            unique_together=set([('telescope', 'obsdate')]),
        ),
        migrations.AlterIndexTogether(
            name='emptyslot',
            index_together=set([('telescope', 'obsdate')]),
        ),
    ]
