# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_week'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Week',
        ),
    ]
