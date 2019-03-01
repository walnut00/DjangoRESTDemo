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
        filtered_values = filter(lambda v: not isinstance(v[0], UpdatedDateTimeField), values)
        return super(MyModel, self)._do_update(base_qs, using, pk_val, filtered_values, update_fields, forced_update)

    def _do_insert(self, manager, using, fields, update_pk, raw):
        # 不更新创建时间
        filtered_fields = filter(lambda v: not isinstance(v, CreatedDateTimeField), fields)
        return super(MyModel, self)._do_insert(manager, using, filtered_fields, update_pk, raw)


class User(MyModel):
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=128)
    email = models.CharField(max_length=128, null=True)
    created_at = CreatedDateTimeField()
    updated_at = UpdatedDateTimeField()

    class Meta:
        db_table = 'user'

    def __unicode__(self):
        return '{}.{}'.format(self.id, self.name)


class Blog(MyModel):
    # 一个user对应对个blog
    user = models.ForeignKey(to=User, help_text=u'作者', on_delete=models.CASCADE, related_name='user_blogs')
    title = models.CharField(max_length=128, help_text=u'标题', null=True)
    abstract = models.CharField(max_length=512, help_text=u'摘要', null=True)
    content = models.TextField(help_text=u'内容', null=True)
    click = models.IntegerField(null=True)
    created_at = CreatedDateTimeField()
    updated_at = UpdatedDateTimeField()

    class Meta:
        db_table = 'blog'

    def __unicode__(self):
        return '{}.{}'.format(self.id, self.title)


class Comment(MyModel):
    # 一个blog对应多个comment
    blog = models.ForeignKey(to=Blog, help_text=u'被评论的博客', on_delete=models.CASCADE, related_name='blog_comments')
    # 一个user有多个comment
    user = models.ForeignKey(to=User, help_text=u'评论者', on_delete=models.CASCADE, related_name='user_comments')
    comment = models.TextField(help_text=u'评论', null=True)
    created_at = CreatedDateTimeField()

    class Meta:
        db_table = 'comment'

    def __unicode__(self):
        return '{}.{}'.format(self.id, self.comment)

