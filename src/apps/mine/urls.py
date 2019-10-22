# coding=utf8
# Create your views here.

from django.urls import path

from mine import apis


urlpatterns = [
    path('collect/', apis.get_collect_list, name="get_collect_list"),
    path('cart/', apis.ShoppingCartView.as_view(), name="cart"),
    path('cartCount/', apis.shopping_cart_count, name="shopping_cart_count"),
    path('addr/', apis.ShoppingAddrView.as_view(), name="addr"),
    path('defaultAddr/', apis.set_default_addr, name="set_default_addr"),
    path('area/', apis.get_area, name="get_area"),
]



