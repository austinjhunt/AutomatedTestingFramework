# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_subitem_show'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizquestion',
            name='author_id',
            field=models.IntegerField(default=-1),
        ),
    ]
