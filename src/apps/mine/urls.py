# coding=utf8
# Create your views here.

from django.urls import path

from mine import apis


urlpatterns = [
    path('collect/', apis.get_collect_list, name="get_collect_list"),
    path('cart/', apis.ShoppingCartView.as_view(), name="cart"),
    path('count/', apis.shopping_cart_count, name="shopping_cart_count"),
]



