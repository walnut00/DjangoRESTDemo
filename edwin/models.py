# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.timezone import now
from fields import *

# Create your models here.


class MyModel(models.Model):
    """
    自定义model基类，便于显示的设置id等字段
    也可以不自定义model基类，django默认为每个model设置了一个id字段
    """
    # id， 这里自定义了一个model基类
    id = models.AutoField(primary_key=True, auto_created=True)

    class Meta:
        # 抽象基类
        abstract = True

    def _do_update(self, base_qs, using, pk_val, values, update_fields, forced_update):
        # 不覆盖更新时间
        filted_values = filter(lambda v: not isinstance(v[0], UpdatedDateTimeField), values)
        return super(MyModel, self)._do_update(base_qs, using, pk_val, filted_values, update_fields, forced_update)


class User(MyModel):
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=128)
    email = models.CharField(max_length=128)
    created_at = CreatedDateTimeField()
    updated_at = UpdatedDateTimeField()

    class Meta:
        db_table = 'user'

    def __unicode__(self):
        return '{}.{}'.format(self.id, self.name)

class Blog(MyModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs')
    title = models.CharField(max_length=128)
    content = models.TextField()
    click = models.IntegerField(null=True)
    created_at = CreatedDateTimeField()
    updated_at = UpdatedDateTimeField()

    class Meta:
        db_table = 'blog'

    def __unicode__(self):
        return '{}.{}'.format(self.id, self.title)