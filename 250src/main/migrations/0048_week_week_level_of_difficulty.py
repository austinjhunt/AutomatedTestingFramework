# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-25 12:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0047_auto_20170812_1432'),
    ]

    operations = [
        migrations.AddField(
            model_name='week',
            name='week_level_of_difficulty',
            field=models.CharField(default=b'', max_length=100),
        ),
    ]
