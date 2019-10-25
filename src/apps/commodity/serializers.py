# -*- coding: utf-8 -*-
from datetime import datetime

from rest_framework import serializers

from commodity.models import Commodity, FreightTemplate, Category, CommodityCollect, Coupon
from mine.models import MyCoupon


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
            data = [{
                "id": x.id,
                "name": x.name,
                'pic': x.pic,
                'stocks': x.stocks,
                'price': x.price
            } for x in specification]
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


class CouponSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    valid_days = serializers.SerializerMethodField()

    def get_valid_days(self, obj):
        max_date = obj.max_date
        now_date = datetime.now().date()
        valid_days = (max_date - now_date).days
        return valid_days

    def get_status(self, obj):
        if not self.context:
            return '未领取'
        auth = self.context["request"].auth
        if auth:
            my_coupon = MyCoupon.objects.filter(user_id=auth['user_id'], coupon_id=obj.id).first()
            if my_coupon:
                status = '已使用' if my_coupon.used else '已领取'
                return status
        return '未领取'

    class Meta:
        model = Coupon
        fields = ['id', 'type', 'amount', 'condition', 'min_data', 'max_data', 'valid_days', 'status']
