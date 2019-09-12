# -*- coding: utf-8 -*-

from django.urls import path, include
from rest_framework import routers

from . import apis


router = routers.SimpleRouter()
router.register('list', apis.CommodityListView, base_name="commodity_list")

urlpatterns = [
    path('', include(router.urls)),
]
