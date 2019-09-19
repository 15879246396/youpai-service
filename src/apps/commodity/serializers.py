# -*- coding: utf-8 -*-
from rest_framework import serializers

from commodity.models import Commodity, FreightTemplate, Category


class FreightTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = FreightTemplate
        fields = ['id', 'name', 'freight', 'charge_type', 'amount', 'piece']


class CommodityListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Commodity
        fields = ['id', 'name', 'ori_price', 'price', 'brief', 'pic', 'sold_num']


class CommoditySerializer(CommodityListSerializer):
    images = serializers.SerializerMethodField()
    freight_template = FreightTemplateSerializer(allow_null=True, required=False)
    specification = serializers.SerializerMethodField()

    def get_images(self, obj):
        if obj.images:
            return eval(obj.images)

    def get_specification(self, obj):
        specification = obj.commodity_specification.all()
        if specification:
            data = [{"id": x.id, "name": x.name} for x in specification]
            return data

    class Meta:
        model = Commodity
        fields = CommodityListSerializer.Meta.fields + ['is_free_fee', 'content', 'images', 'total_stocks',
                                                        'freight_template', 'specification']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name', 'pic', ]
