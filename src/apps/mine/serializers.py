# -*- coding: utf-8 -*-
from rest_framework import serializers

from mine.models import ShoppingCart, ShippingAddr, Area


class ShoppingCartSerializer(serializers.ModelSerializer):
    commodity = serializers.SerializerMethodField()
    specification = serializers.SerializerMethodField()
    pic = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    def get_commodity(self, obj):
        commodity = obj.commodity
        if commodity:
            data = {
                "id": commodity.id,
                "name": commodity.name,
            }
            return data

    def get_specification(self, obj):
        specification = obj.specification
        if specification:
            data = {
                "id": specification.id,
                "name": specification.name,
            }
            return data

    def get_pic(self, obj):
        specification = obj.specification
        if specification:
            return specification.pic
        return obj.commodity.pic

    def get_price(self, obj):
        specification = obj.specification
        if specification:
            return "%.2f" % specification.price
        return "%.2f" % obj.commodity.price

    class Meta:
        model = ShoppingCart
        fields = ['id', 'commodity', 'specification', 'pic', 'count', 'price']


class AreaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Area
        fields = ['id', 'name', 'level']


class ShippingAddrSerializer(serializers.ModelSerializer):
    province = serializers.CharField(source='province.name', read_only=True)
    city = serializers.CharField(source='city.name', read_only=True)
    area = serializers.CharField(source='area.name', read_only=True)

    class Meta:
        model = ShippingAddr
        fields = ['id', 'default', 'receiver', 'addr', 'phone', 'province', 'city', 'area']
