# -*- coding: utf-8 -*-
from rest_framework import serializers

from commodity.models import Commodity


class CommoditySerializer(serializers.ModelSerializer):
    class Meta:
        model = Commodity
        fields = ['id', 'title', 'img_url', 'des', 'link', 'relation']
