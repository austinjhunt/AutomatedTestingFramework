# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_subitem_subitem_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuizQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('questionText', models.TextField()),
                ('candidateAnswer1', models.CharField(max_length=200)),
                ('candidateAnswer2', models.CharField(max_length=200)),
                ('candidateAnswer3', models.CharField(max_length=200)),
                ('candidateAnswer4', models.CharField(max_length=200)),
                ('correctAnswer', models.CharField(max_length=200)),
                ('subItem', models.ForeignKey(to='main.SubItem')),
            ],
        ),
    ]
