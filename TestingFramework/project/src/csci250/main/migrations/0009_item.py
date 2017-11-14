# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20160725_1719'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('model_order', models.IntegerField()),
                ('model_content', models.CharField(max_length=400)),
                ('topic', models.ForeignKey(to='main.Topic')),
            ],
        ),
    ]
