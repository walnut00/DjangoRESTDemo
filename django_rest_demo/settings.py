# -*- coding: utf-8 -*-
"""
Django settings for django_rest_demo project.

Generated by 'django-admin startproject' using Django 1.11.18.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%ed@8d8e2-qzwq*n9)4g^+i&e$_2mj@lf2+()j!w^pq3#fb#!='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    #'django.contrib.admin',
    # 'django.contrib.auth',
    'django.contrib.contenttypes',
    #'django.contrib.sessions', # 将session存入数据库，必须配置此app
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'edwin',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    #'django.contrib.auth.middleware.AuthenticationMiddleware',
    'edwin.middleware.MyAuthenticationMiddleware',# 用户权限处理中间件
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'edwin.middleware.PrintMessageMiddleware', # 自定义中间件
]


# 缓存配置
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': BASE_DIR + '/django.cache',
        #'TIMEOUT': 60,
        'OPTIONS': {
            'MAX_ENTRIES': 1000,
        }
    }
}

# SESSION引擎配置
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
# 配置session cookie名称
SESSION_COOKIE_NAME = 'user_token'

# REST框架配置
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'edwin.pagination.MyPagination',# 配置全局分页, 也可以在viewset中局部指定pagination_class

    # 配置全局访问权限，也可以在每个viewset里面设置
    # 'DEFAULT_PERMISSION_CLASSES': ['edwin.authentication.MyPermission',],

    # 配置全局权限验证（否则默认是'rest_framework.authentication.SessionAuthentication'和
    # 'rest_framework.authentication.BasicAuthentication'）
    # 也可以为某个ViewSet单独配置authentication_classes = ()
    # 'DEFAULT_AUTHENTICATION_CLASSES': ('edwin.authentication.MyAuthentication',),
    'DEFAULT_AUTHENTICATION_CLASSES': (),

    # Exception handling
    #'EXCEPTION_HANDLER': 'edwin.views.exception_handler',

    # 为了不使用django自带的'django.contrib.auth'， 否则会异常
    'UNAUTHENTICATED_USER': None,
}


# 配置用户凭证验证backend
# AUTHENTICATION_BACKENDS = (
#     #'django.contrib.auth.backends.ModelBackend',
#     'edwin.authentication.MyAuthBackend',
# )

# 配置用户认证model
#AUTH_USER_MODEL = 'edwin.User'

ROOT_URLCONF = 'django_rest_demo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_rest_demo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'