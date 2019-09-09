# -*- coding: utf-8 -*-
from rest_framework import serializers

from commodity.models import Commodity, FreightTemplate


class FreightTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = FreightTemplate
        fields = ['id', 'name', 'freight', 'charge_type', 'amount', 'piece']


class CommodityListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Commodity
        fields = ['id', 'name', 'ori_price', 'price', 'brief', 'pic', ]


class CommoditySerializer(CommodityListSerializer):
    images = serializers.SerializerMethodField()
    freight_template = FreightTemplateSerializer(allow_null=True, required=False)

    def get_images(self, obj):
        if obj.images:
            return eval(obj.images)

    class Meta:
        model = Commodity
        fields = CommodityListSerializer.Meta.fields + ['is_free_fee', 'content', 'images', 'sold_num', 'total_stocks',
                                                        'freight_template']
