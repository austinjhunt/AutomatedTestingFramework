# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_pimsleur_lesson'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Pimsleur_Lesson',
        ),
        migrations.DeleteModel(
            name='Week',
        ),
    ]
