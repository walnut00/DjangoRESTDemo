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
        if not hasattr(request, '_cached_user'):
            user_token = request.COOKIES.get('user_token')
            user_id = request.session.get('user_id')
            user_id = User._meta.pk.to_python(user_id)
            if user_id is not None:
                request._cached_user = User._default_manager.get(id=user_id)
                print 'Auth Middleware:', user_token, request._cached_user.name
            else:
                request._cached_user = None

        request.user = request._cached_user

# 自定义session中间件
class MySessionMiddlereare(MiddlewareMixin):
    def process_request(self, request):
        # 解析token
        user_token = request.COOKIES.get('user_token')

        # 解析session
        session = Session()
        if user_token is not None:
            session.load(user_token)

        request.session = session

    def process_response(self, request, response):
        session = request.session
        if session is not None:
            user_token = session.get('user_token')

            # 保存session至redis
            if user_token is not None:
                session.save(user_token)

        return response