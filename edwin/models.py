# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=128)
    email = models.CharField(max_length=128)

    def __unicode__(self):
        return '{}.{}'.format(self.id, self.name)

class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs')
    title = models.CharField(max_length=128)
    content = models.TextField()
    click = models.IntegerField(null=True)

    def __unicode__(self):
        return '{}.{}'.format(self.id, self.title)