# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-31 19:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0008_delete_myadmin'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyAdmin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=30)),
                ('logged_in', models.BooleanField(default=False)),
            ],
        ),
    ]
