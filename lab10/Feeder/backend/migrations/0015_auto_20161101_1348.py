# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-01 13:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0014_feedback_question'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedback',
            name='course',
        ),
        migrations.RemoveField(
            model_name='question',
            name='feedback',
        ),
        migrations.DeleteModel(
            name='Feedback',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
    ]
