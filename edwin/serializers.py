# -*- coding: utf-8 -*-

from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import HyperlinkedRelatedField

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
    class Meta:
        model = Blog
        fields = ('title', 'content')


class UsersBlogSerializer(ModelSerializer):
    blogs = HyperlinkedRelatedField(many=True, read_only=True, view_name='blog-detail')
    #blogs = BlogSerializer(many=True)

    class Meta:
        model = User
        fields = ('id', 'name', 'blogs')