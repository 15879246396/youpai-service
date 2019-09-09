# -*- coding: utf-8 -*-
from rest_framework import serializers

from index.models import IndexImg, Notice


class IndexImgSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndexImg
        fields = ['id', 'title', 'img_url', 'des', 'link', 'relation']


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ['id', 'title', 'content', 'is_top', 'gmt_modified', ]
