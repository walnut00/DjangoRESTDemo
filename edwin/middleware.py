# -*- coding: utf8 -*-

from django.utils.deprecation import MiddlewareMixin
from django.http.response import JsonResponse
from rest_framework.response import Response
from models import User

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


# 认证中间件
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
