# -*- coding: utf-8 -*-
from rest_framework import serializers

from index.models import IndexImg


class IndexImgSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndexImg
        fields = ['id', 'title', 'img_url', 'des', 'link', 'relation']
