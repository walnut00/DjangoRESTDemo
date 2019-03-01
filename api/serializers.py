# -*- coding: utf-8 -*-

from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer
from rest_framework.serializers import HyperlinkedRelatedField, StringRelatedField
from rest_framework.fields import ChoiceField

from models import *
import bcrypt
from werkzeug.security import generate_password_hash


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'password')

    @property
    def validated_data(self):
        validated = super(UserSerializer, self).validated_data
        password = validated.get('password')

        # 密码加密存储
        assert password not in (None, '')
        validated['password'] = generate_password_hash(password)
        return validated


class LoginSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'password')


class LogoutSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ()


class BlogSerializer(ModelSerializer):
    user_name = StringRelatedField(source='user.name')

    class Meta:
        model = Blog
        fields = ('id', 'title', 'user_name', 'content')


class BlogHyperlinkedSerializer(HyperlinkedModelSerializer):
    # HyperlinkedModelSerializer有一个url属性
    user_name = StringRelatedField(source='user.name')

    class Meta:
        model = Blog
        fields = ('id', 'url', 'title', 'user_name', 'abstract')


class CommentSerializer(ModelSerializer):
    # 这个会查找blog的title属性
    blog_title = StringRelatedField(source='blog.title')
    # 同上
    user_name = StringRelatedField(source='user.name')

    class Meta:
        model = Comment
        # blog是一个外键，这里会查找其__unicode__属性
        fields = ('id', 'blog', 'blog_title', 'user_name', 'comment')


class UserBlogsSerializer(ModelSerializer):
    # 超链接，指向一个blog，该字段指向User的users_blog关联属性
    user_blogs = HyperlinkedRelatedField(many=True, read_only=True, view_name='blog-detail')

    class Meta:
        model = User
        fields = ('id', 'name', 'user_blogs')


class BlogCommentsSerializer(ModelSerializer):
    # 某个blog的所有comment
    blog_comments = StringRelatedField(many=True)

    class Meta:
        model = Blog
        fields = ('id', 'title', 'blog_comments')
