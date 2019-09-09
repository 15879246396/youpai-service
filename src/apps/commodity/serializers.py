# -*- coding: utf-8 -*-
from rest_framework import serializers

from commodity.models import Commodity


class CommoditySerializer(serializers.ModelSerializer):
    freight_template = serializers.SerializerMethodField()

    def get_freight_template(self, obj):
        if obj.freight_template:
            freight_template = {
                'freight': obj.freight_template.freight,
                'charge_type': obj.freight_template.charge_type,
                'amount': obj.freight_template.amount,
                'piece': obj.freight_template.piece,
            }
            return freight_template

    class Meta:
        model = Commodity
        fields = ['id', 'name', 'ori_price', 'price', 'is_free_fee', 'brief', 'content', 'pic', 'images', 'sold_num',
                  'total_stocks', 'freight_template']
