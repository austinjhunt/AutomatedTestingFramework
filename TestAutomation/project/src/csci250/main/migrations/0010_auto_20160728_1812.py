# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_item'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='model_content',
            new_name='item_content',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='model_order',
            new_name='item_order',
        ),
    ]
