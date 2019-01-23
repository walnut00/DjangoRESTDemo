# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class User(models.Model):
    name = models.fields.CharField(max_length=32)
    password = models.fields.CharField(max_length=128)
    email = models.fields.CharField(max_length=128)


class Blog(models.Model):
    title = models.fields.CharField(max_length=128)
    author = models.fields.CharField(max_length=32)
    content = models.fields.TextField()
    click = models.fields.IntegerField(null=True)