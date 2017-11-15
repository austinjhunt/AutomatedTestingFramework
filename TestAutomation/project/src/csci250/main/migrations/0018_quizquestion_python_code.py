# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_quizquestion_quiztype'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizquestion',
            name='python_code',
            field=models.TextField(default=b''),
        ),
    ]
