#-*- coding: utf-8 -*-
from rest_framework.permissions import BasePermission
from rest_framework.authentication import BaseAuthentication

class IsAdminUser(BasePermission):
    message = u'需要admin用户权限'
    def has_permission(self, request, view):
        return request.user and request.user.name == 'admin'


class IsSysUser(BasePermission):
    message = u'需要sys用户权限'
    def has_permission(self, request, view):
        return request.user and request.user.name == 'sys'


# 调用request.user时会调用authenticate方法
class MyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        pass