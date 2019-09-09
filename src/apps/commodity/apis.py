from rest_framework import filters
from rest_framework.authentication import SessionAuthentication
from rest_framework.mixins import ListModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from account.permissions import IsAuthenticatedWechat
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
    permission_classes = (IsAuthenticatedWechat,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    pagination_class = CommodityListPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'brief',)

    @common_api
    def get_queryset(self):
        user_id = self.request.query_params.get('user_id', None)
        return Response()

    @common_api
    def list(self, request, *args, **kwargs):
        return super(CommodityListView, self).list(request, *args, **kwargs)
