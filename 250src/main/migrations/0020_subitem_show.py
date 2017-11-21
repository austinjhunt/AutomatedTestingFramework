# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_item_expand'),
    ]

    operations = [
        migrations.AddField(
            model_name='subitem',
            name='show',
            field=models.BooleanField(default=True),
        ),
    ]
