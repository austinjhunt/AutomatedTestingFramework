# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_week'),
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('topic_order', models.IntegerField()),
                ('topic_title', models.CharField(max_length=200)),
                ('topic_date', models.DateField()),
                ('week_id', models.ForeignKey(to='main.Week')),
            ],
        ),
    ]
