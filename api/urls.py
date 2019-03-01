# -*- coding: utf8 -*-
from django.conf.urls import url
from django.conf.urls import include
from rest_framework.routers import DefaultRouter
from . import views

# url路由
router = DefaultRouter()
# need to set base_name，otherwise will reporut：AttributeError: 'QuerySet' object has no attribute 'model'

router.register(r'blog', views.BlogViewSet, basename='blog')
router.register(r'blog_abstract', views.BlogHyperlinkedViewSet, basename='blog_abstract')
router.register(r'comment', views.CommentViewSet, base_name='comment')
router.register(r'user_blogs', views.UserBlogsViewSet, basename='user_blogs')
router.register(r'blog_comments', views.BlogCommentsViewSet, base_name='blog_comments')
router.register(r'login', views.LoginViewSet, basename=u'登陆')
router.register(r'users', views.UserViewSet, basename=u'用户管理')
router.register(r'logout', views.LogoutViewSet, basename=u'登出')

urlpatterns = [
    url(r'', include(router.urls)),
    # url(r'', views.BlogDetail.as_view()),
]