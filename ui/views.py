# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.shortcuts import render
from django.views.decorators.cache import cache_page
import requests

# Create your views here.


# @cache_page(60*15)
def index(request):
    r = requests.get('http://127.0.0.1:8000/api/blog_abstract/')
    r = r.json()
    item_list = r.get('results') or []
    return render(request, 'index.html', {'item_list': item_list})

def share(request):
    return render(request, 'share.html')