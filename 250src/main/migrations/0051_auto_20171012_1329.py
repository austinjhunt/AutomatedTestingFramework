# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-12 13:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0050_section'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='section',
            name='section_time',
        ),
        migrations.AlterField(
            model_name='section',
            name='section_id',
            field=models.CharField(max_length=600),
        ),
    ]
