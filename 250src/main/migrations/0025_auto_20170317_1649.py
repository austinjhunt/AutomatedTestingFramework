# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_auto_20170316_1742'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment_question_mltiple4',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('python_code', models.TextField(default=b'')),
                ('candidateAnswer1', models.CharField(max_length=200)),
                ('candidateAnswer2', models.CharField(max_length=200)),
                ('candidateAnswer3', models.CharField(max_length=200)),
                ('candidateAnswer4', models.CharField(max_length=200)),
                ('correctAnswer', models.CharField(max_length=200)),
            ],
        ),
        migrations.DeleteModel(
            name='AssignmentMultipleQuestion',
        ),
    ]
