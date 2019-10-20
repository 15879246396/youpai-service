# coding=utf8
# Create your views here.

from django.urls import path

from . import apis


urlpatterns = [
    path('confirm/', apis.confirm, name="confirm"),
]



