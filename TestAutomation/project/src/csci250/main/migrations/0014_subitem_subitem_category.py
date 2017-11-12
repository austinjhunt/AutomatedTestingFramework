# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_subitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='subitem',
            name='subItem_category',
            field=models.CharField(default=b'PDF', max_length=200),
        ),
    ]
