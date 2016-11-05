# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-01 13:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0015_auto_20161101_1348'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=30)),
                ('due_date', models.DateTimeField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('q', models.CharField(max_length=50)),
                ('opinion', models.IntegerField(choices=[(1, 'Strongly Agree'), (2, 'Agree'), (3, 'Neutral'), (4, 'Disagree'), (5, 'Strongly Disagree')], default=1)),
                ('feedback', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.Feedback')),
            ],
        ),
    ]