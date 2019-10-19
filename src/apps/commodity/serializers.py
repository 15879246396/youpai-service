# -*- coding: utf-8 -*-
from rest_framework import serializers

from commodity.models import Commodity, FreightTemplate, Category, CommodityCollect


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
    is_collect = serializers.SerializerMethodField()

    def get_images(self, obj):
        if obj.images:
            return eval(obj.images)

    def get_specification(self, obj):
        specification = obj.commodity_specification.all()
        if specification:
            data = [{"id": x.id, "name": x.name} for x in specification]
            return data

    def get_is_collect(self, obj):
        if not self.context:
            return False
        auth = self.context["request"].auth
        if auth:
            is_collect = CommodityCollect.objects.filter(user_id=auth['user_id'], commodity=obj.id, delete_status=0).first()
            return bool(is_collect)
        else:
            return False

    class Meta:
        model = Commodity
        fields = CommodityListSerializer.Meta.fields + ['is_free_fee', 'content', 'images', 'total_stocks',
                                                        'freight_template', 'specification', 'is_collect']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name', 'pic', ]
