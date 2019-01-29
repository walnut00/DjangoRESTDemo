# -*- coding: utf8 -*-
import json
from collections import OrderedDict
from django.utils.deprecation import MiddlewareMixin
from django.http.response import JsonResponse
from django.conf import settings
from rest_framework.response import Response

from models import User
from sessions import Session

class UncaughtExceptionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        print 'process request:', request

    def process_response(self, request, response):
        print 'process response:', response.reason_phrase
        return response

    def process_view(self, request, callback, callback_args, callback_kwargs):
        print 'process view:', callback

    def process_exception(self, request, exception):
        data = {'uncaught exception': exception.message}
        return JsonResponse(data=data)


# 认证中间件，根据cookie从session中解析出user信息
# 需要配合django自带的session中间件
class MyAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if hasattr(request, '_cached_user'):
            request.user = request._cached_user
            return

        request.user = None

        # token和session
        user_token = request.COOKIES.get('user_token')
        session = request.session
        if session is None:
            return

        # 解析user信息
        request._cached_user = User()
        request._cached_user.id = session.get('user_id')
        request._cached_user.name = session.get('name')
        request.user = request._cached_user
        print 'Auth Middleware:', user_token, request._cached_user.name


# 自定义session中间件
class MySessionMiddlereare(MiddlewareMixin):
    def process_request(self, request):
        # 解析token
        user_token = request.COOKIES.get('user_token')
        # 解析session
        request.session = Session.load(key=user_token)

    def process_response(self, request, response):
        session = request.session

        if session is not None and len(session) > 0:
            user_token = session.get('user_token')
            session.save(user_token)

        return response