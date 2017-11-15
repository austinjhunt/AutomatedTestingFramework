# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_quizquestion_python_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='expand',
            field=models.BooleanField(default=False),
        ),
    ]
