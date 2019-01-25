# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from werkzeug.security import check_password_hash

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import generics
from rest_framework import exceptions
from rest_framework.response import Response

from django.http import *
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.core.cache import caches # caches['default'], the same as django.core.cache
from django.utils.translation import LANGUAGE_SESSION_KEY

from serializers import UserModelSerializer, BlogModelSerializer, \
    LoginSerializer, LogoutSerializer
from models import User, Blog
from request import MyRequest

from authentication import IsAdminUser, IsSysUser, IsLogin
# Create your views here.

class MyGenericViewSet(viewsets.GenericViewSet):
    # def perform_authentication(self, request):
    #     if request.path in ('/edwin/', '/edwin/login/'):
    #         pass
    #     elif request.user in (None, ''):
    #         raise AuthenticationFailed('Please login first')
    #     else:
    #         print request.path, request.user, '-> valid'

    def initialize_request(self, request, *args, **kwargs):
        parser_context = self.get_parser_context(request)

        return MyRequest(
            request,
            parsers=self.get_parsers(),
            authenticators=self.get_authenticators(),
            negotiator=self.get_content_negotiator(),
            parser_context=parser_context
        )

    def permission_denied(self, request, message=None):
        raise exceptions.PermissionDenied(detail=message)

    def handle_exception(self, exc):
        try:
            return super(MyGenericViewSet, self).handle_exception(exc)
        except Exception, e:
            return Response(data={'detail': e.message})
        except:
            return Response(data={'detail': 'unknown error'})


class MyModelViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     MyGenericViewSet):
    pass


class MyCreateViewSet(mixins.CreateModelMixin,
                      MyGenericViewSet):
    pass


class MyListCreateViewSet(mixins.CreateModelMixin,
                                  mixins.ListModelMixin,
                                  MyGenericViewSet):
    pass


class UserViewSet(MyModelViewSet):
    queryset = User._default_manager.all()
    serializer_class = UserModelSerializer
    permission_classes = [IsSysUser]


class LoginViewSet(MyCreateViewSet):
    queryset = User._default_manager.all()
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        """
        参考D:\Program_Files\Python27\Lib\site-packages\django\contrib\auth\__init__.py\login
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user_name = data.get('name')
        password = data.get('password')

        try:
            user_object = self.queryset.get(name=user_name)
        except User.DoesNotExist:
            raise Exception('Name or password error')

        if not check_password_hash(user_object.password, password):
            raise Exception('Name or password error')

        # 创建新的session key
        request.session.cycle_key()
        user_token = request.session.session_key

        # 返回user token
        response = Response(user_token)
        response.set_cookie('user_token', user_token)

        # 保存session信息
        request.session['user_name'] = user_name
        request.session['user_id'] = user_object.id
        return response


class LogoutViewSet(MyCreateViewSet):
    queryset = User._default_manager.all()
    serializer_class = LogoutSerializer

    def create(self, request, *args, **kwargs):
        # remember language choice saved to session
        language = request.session.get(LANGUAGE_SESSION_KEY)

        request.session.flush()
        request.user = None
        if language is not None:
            request.session[LANGUAGE_SESSION_KEY] = language

        return Response('OK')


class BlogViewSet(MyModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogModelSerializer
    permission_classes = [IsLogin]
    # authentication_classes = ()

    def get_page_param(self, request):
        page = request.query_params.get(self.paginator.page_query_param, 1)
        page_size = request.query_params.get(self.paginator.page_size_query_param, self.paginator.page_size)
        return page, page_size

    def list(self, request, *args, **kwargs):
        page, page_size = self.get_page_param(request)

        # 从cache加载数据
        data = cache.get('blogs_{}_{}'.format(page, page_size))
        if data is not None:
            return Response(data)

        self.queryset = self.queryset.filter(author=request.user)

        # 调用基类方法
        response = super(BlogViewSet, self).list(request, *args, **kwargs)

        # 缓存
        cache.set('blogs_{}_{}'.format(page, page_size), response.data)
        return response


@cache_page(60*15)
def index(request):
    return HttpResponse('Hello Django!')
