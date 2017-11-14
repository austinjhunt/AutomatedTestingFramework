# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_topic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='week',
            name='week_title',
            field=models.CharField(max_length=600),
        ),
    ]
