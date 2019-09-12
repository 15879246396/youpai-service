from rest_framework import filters
from rest_framework.authentication import SessionAuthentication
from rest_framework.mixins import ListModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from account.permissions import IsAuthenticatedWechat
from commodity.models import Commodity
from commodity.serializers import CommodityListSerializer
from common.decorator import common_api


class CommodityListPagination(PageNumberPagination):
    """商品列表分页"""
    # 默认每页显示的数据条数
    page_size = 10
    # 获取URL参数中设置的每页显示数据条数
    page_size_query_param = 'page_size'

    # 获取URL参数中传入的页码key
    page_query_param = 'page'

    # 最大支持的每页显示的数据条数
    max_page_size = 20


class CommodityListView(GenericViewSet, ListModelMixin):
    """商品列表"""
    serializer_class = CommodityListSerializer
    # permission_classes = (IsAuthenticatedWechat,)
    # authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    pagination_class = CommodityListPagination
    filter_backends = (filters.OrderingFilter, filters.SearchFilter,)
    ordering_fields = ('sold_num', 'price')
    search_fields = ('name', 'brief',)

    def get_queryset(self):
        tag_id = self.request.query_params.get('tag', None)
        category_id = self.request.query_params.get('category', None)
        if tag_id:
            query_set = Commodity.objects.filter(delete_status=0, commodity_tag=tag_id)
        elif category_id:
            query_set = Commodity.objects.filter(delete_status=0, category=category_id)
        else:
            query_set = Commodity.objects.filter(delete_status=0)
        return query_set

    @common_api
    def list(self, request, *args, **kwargs):
        return super(CommodityListView, self).list(request, *args, **kwargs)
