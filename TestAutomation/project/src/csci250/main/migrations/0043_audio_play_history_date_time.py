# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-14 20:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0042_audio_play_history'),
    ]

    operations = [
        migrations.AddField(
            model_name='audio_play_history',
            name='date_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]