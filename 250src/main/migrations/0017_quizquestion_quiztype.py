# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_quizquestion_repeat'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizquestion',
            name='quizType',
            field=models.CharField(default=b'multiple4', max_length=100),
        ),
    ]
