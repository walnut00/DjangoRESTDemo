# -*- coding: utf8 -*-

from django.db import models


class MyDateTimeField(models.Field):
    def __init__(self, **kwargs):
        super(MyDateTimeField, self).__init__(null=True)


class CreatedDateTimeField(MyDateTimeField):
    def db_type(self, connection):
        typ = ['DATETIME']
        if self.null:
            typ += ['NULL']
        typ += ['default CURRENT_TIMESTAMP']
        return ' '.join(typ)


class UpdatedDateTimeField(MyDateTimeField):
    def db_type(self, connection):
        typ = ['DATETIME']
        if self.null:
            typ += ['NULL']
        typ += ['default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP']
        return ' '.join(typ)