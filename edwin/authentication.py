#-*- coding: utf-8 -*-
from rest_framework.permissions import BasePermission
from rest_framework.authentication import BaseAuthentication

class IsAdminUser(BasePermission):
    message = u'the administrator permission is required'
    def has_permission(self, request, view):
        return request.user and request.user.name == 'admin'


class IsSysUser(BasePermission):
    message = u'the system permission is required'
    def has_permission(self, request, view):
        return request.user and request.user.name == 'sys'


class IsLogin(BasePermission):
    message = u'please login first'
    def has_permission(self, request, view):
        return request.user not in (None, '')


# 调用request.user时会调用authenticate方法
class MyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        pass