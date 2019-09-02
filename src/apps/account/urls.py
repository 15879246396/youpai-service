# coding=utf8
# Create your views here.

from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token

from account import apis


urlpatterns = [
    path('login/', apis.WechatLoginView.as_view()),
    path('userInfo/', apis.WechatUserInfoAPI.as_view()),
]



