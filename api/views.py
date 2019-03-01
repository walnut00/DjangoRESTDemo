# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from collections import OrderedDict
from uuid import uuid4
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

from serializers import *
from models import User, Blog
from request import MyRequest

from authentication import IsAdminUser, IsSysUser, IsLogin
# Create your views here.


class MyGenericViewSet(viewsets.GenericViewSet):
    """
    自定义gemericViewSet
    """
    # def perform_authentication(self, request):
    #     if request.path in ('/Blog/', '/Blog/login/'):
    #         pass
    #     elif request.user in (None, ''):
    #         raise AuthenticationFailed('Please login first')
    #     else:
    #         print request.path, request.user, '-> valid'

    def initialize_request(self, request, *args, **kwargs):
        # 重载基类的初始化请求函数，这里返回自定义的request对象
        parser_context = self.get_parser_context(request)

        return MyRequest(
            request,
            parsers=self.get_parsers(),
            authenticators=self.get_authenticators(),
            negotiator=self.get_content_negotiator(),
            parser_context=parser_context
        )

    def permission_denied(self, request, message=None):
        # 重载权限拒绝函数
        raise exceptions.PermissionDenied(detail=message)

    def handle_exception(self, exc):
        # 重载异常处理函数
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
    """
    自定义ModelViewSet
    """
    pass


class MyCachedModelViewSet(MyModelViewSet):
    """
    支持缓存的ModelViewSet
    """
    def get_page_param(self, request):
        page = request.query_params.get(self.paginator.page_query_param, 1)
        page_size = request.query_params.get(self.paginator.page_size_query_param, self.paginator.page_size)
        return page, page_size

    def list(self, request, *args, **kwargs):
        page, page_size = self.get_page_param(request)
        cached_key = '{}_{}_{}_{}'.format(request.user.name, self.basename, page, page_size)

        # 从cache加载数据
        data = cache.get(cached_key)
        if data is not None:
            return Response(data)

        #self.queryset = self.queryset.filter()

        # 调用基类方法
        response = super(MyCachedModelViewSet, self).list(request, *args, **kwargs)

        # 缓存
        cache.set(cached_key, response.data)
        return response


class MyListViewSet(mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    MyGenericViewSet):
    """
    仅支持get的ViewSet
    """
    pass


class MyCreateViewSet(mixins.CreateModelMixin,
                      MyGenericViewSet):
    """
    仅支持post的ViewSet
    """
    pass


class MyListCreateViewSet(mixins.CreateModelMixin,
                                  mixins.ListModelMixin,
                                  MyGenericViewSet):
    """
    支持get，post的ViewSet
    """
    pass


class UserViewSet(MyCachedModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    #permission_classes = [IsSysUser]


class LoginViewSet(MyCreateViewSet):
    queryset = User.objects.all()
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

        user_token = request.session.get('user_token') or uuid4().hex

        # 设置session信息，在session中间件中进行存储
        request.session['user_token'] = user_token
        request.session['user_name'] = user_name
        request.session['user_id'] = user_object.id

        # cookie中，返回usertoken
        response = Response({'user_token': user_token})
        response.set_cookie('user_token', value=user_token)
        return response


class LogoutViewSet(MyCreateViewSet):
    queryset = User._default_manager.all()
    serializer_class = LogoutSerializer

    def create(self, request, *args, **kwargs):
        # # remember language choice saved to session
        # language = request.session.get(LANGUAGE_SESSION_KEY)

        user_token = request.COOKIES.get('user_token')
        request.session.flush(user_token)
        request.user = None
        # if language is not None:
        #     request.session[LANGUAGE_SESSION_KEY] = language

        return Response('OK')


class BlogViewSet(MyModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    #permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 设置user_id
        data = serializer.validated_data
        data['user_id'] = request.user.id

        self.queryset.create(**data)
        return Response('OK')


class BlogHyperlinkedViewSet(MyListViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogHyperlinkedSerializer
    #permission_classes = [IsAdminUser]


class CommentViewSet(MyModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsLogin]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        data['user_id'] = request.user.id

        self.queryset.create(**data)
        return Response('OK')


class UserBlogsViewSet(MyListViewSet):
    queryset = User.objects.all()#Blog.objects.all()
    serializer_class = UserBlogsSerializer
    #permission_classes = [IsLogin]


class BlogCommentsViewSet(MyModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogCommentsSerializer
    #permission_classes = [IsLogin]
