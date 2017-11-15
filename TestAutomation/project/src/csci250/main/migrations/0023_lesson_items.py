# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_item_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson_items',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lesson_item_text', models.TextField()),
                ('lesson_item_stop_after', models.BooleanField(default=False)),
                ('lesson_item_append_at_once', models.BooleanField(default=False)),
                ('lesson_item_duration', models.IntegerField()),
                ('item', models.ForeignKey(to='main.Item')),
            ],
        ),
    ]
