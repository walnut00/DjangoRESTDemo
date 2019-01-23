# -*- coding: utf-8 -*-

from rest_framework.serializers import ModelSerializer
from models import *
import bcrypt
from werkzeug.security import generate_password_hash

class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'password')

    @property
    def validated_data(self):
        validated = super(UserModelSerializer, self).validated_data
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


class BlogModelSerializer(ModelSerializer):
    class Meta:
        model = Blog
        fields = ('id', 'title', 'author', 'content')