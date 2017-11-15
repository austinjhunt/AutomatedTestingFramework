# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_lesson_items'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment_question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question_title', models.TextField()),
                ('question_type', models.CharField(max_length=200)),
                ('question_order', models.IntegerField()),
                ('question_detail_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='AssignmentMultipleQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question_title', models.TextField()),
                ('python_code', models.TextField(default=b'')),
                ('candidateAnswer1', models.CharField(max_length=200)),
                ('candidateAnswer2', models.CharField(max_length=200)),
                ('candidateAnswer3', models.CharField(max_length=200)),
                ('candidateAnswer4', models.CharField(max_length=200)),
                ('correctAnswer', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Assignments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('assignment_title', models.CharField(max_length=300)),
            ],
        ),
        migrations.AddField(
            model_name='assignment_question',
            name='assignment',
            field=models.ForeignKey(to='main.Assignments'),
        ),
    ]
