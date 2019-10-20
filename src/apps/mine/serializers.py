# -*- coding: utf-8 -*-
from rest_framework import serializers

from mine.models import ShoppingCart


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
            return specification.price
        return obj.commodity.price

    class Meta:
        model = ShoppingCart
        fields = ['id', 'commodity', 'specification', 'pic', 'count', 'price']
