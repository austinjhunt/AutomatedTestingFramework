# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_quizquestion'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizquestion',
            name='repeat',
            field=models.IntegerField(default=1),
        ),
    ]
