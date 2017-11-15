# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20160728_1812'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subItem_order', models.IntegerField()),
                ('subItem_title', models.CharField(max_length=400)),
                ('subItem_link', models.CharField(max_length=400)),
                ('subItem_function', models.CharField(max_length=300)),
            ],
        ),
    ]
