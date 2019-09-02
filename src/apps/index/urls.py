# -*- coding: utf-8 -*-

from django.urls import path, include
from rest_framework import routers
from . import apis


urlpatterns = [
    path('indexImg/', apis.index_img, name='indexImg'),
]
