# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-01-14 07:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edwin', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='click',
            field=models.IntegerField(null=True),
        ),
    ]