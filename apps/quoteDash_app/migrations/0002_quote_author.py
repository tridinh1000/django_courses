# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-22 17:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quoteDash_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='author',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]