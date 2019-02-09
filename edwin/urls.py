# -*- coding: utf8 -*-
from django.conf.urls import url
from django.conf.urls import include
from rest_framework.routers import DefaultRouter
from . import views

# url路由
router = DefaultRouter()
# need to set base_name，otherwise will reporut：AttributeError: 'QuerySet' object has no attribute 'model'

router.register(r'blog', views.BlogViewSet, basename='blog')
router.register(r'users_blog', views.UsersBlogViewSet, basename='users_blog')
router.register(r'login', views.LoginViewSet, basename=u'登陆')
router.register(r'users', views.UserViewSet, basename=u'用户管理')
router.register(r'logout', views.LogoutViewSet, basename=u'登出')

urlpatterns = [
    url(r'', include(router.urls)),
    #url(r'', views.BlogDetail.as_view()),
    url(r'^index/$', views.index, name='index'),
    #url(r'^name/$', views.name, name='name'),
]