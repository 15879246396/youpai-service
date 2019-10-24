from django.db import transaction
from django.db.models import F
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from account.permissions import IsAuthenticatedWechat
from base.exceptions import ValidateException
from commodity.models import CommodityCollect, Commodity
from commodity.serializers import CommodityListSerializer
from common.decorator import common_api
from mine.models import ShoppingCart, ShippingAddr, Area
from mine.serializers import ShoppingCartSerializer, ShippingAddrSerializer, AreaSerializer


@api_view(['GET'])
@permission_classes((IsAuthenticatedWechat, ))
@authentication_classes((JSONWebTokenAuthentication, SessionAuthentication))
@common_api
def get_collect_list(request):
    """我的收藏"""
    user = request.auth['user_id']
    collect_list = CommodityCollect.objects.filter(delete_status=0, user=user)\
        .order_by("-gmt_modified").values_list('id', flat=True)
    commodities = Commodity.objects.filter(category_id__in=collect_list)
    data = CommodityListSerializer(commodities).data
    return Response(data)


@api_view(['GET'])
@permission_classes((IsAuthenticatedWechat, ))
@authentication_classes((JSONWebTokenAuthentication, SessionAuthentication))
@common_api
def shopping_cart_count(request):
    """购物车数量"""
    user = request.auth['user_id']
    my_cart = ShoppingCart.objects.filter(user_id=user, delete_status=0, count__gt=0)
    count = sum(my_cart.values_list("count", flat=True))
    return Response(count)


class ShoppingCartView(APIView):
    """购物车"""
    permission_classes = (IsAuthenticatedWechat,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    @common_api
    def get(self, request):
        """查看购物车"""
        user = request.auth['user_id']
        my_cart = ShoppingCart.objects.filter(user_id=user, delete_status=0, count__gt=0)
        data = ShoppingCartSerializer(my_cart, many=True).data
        return Response(data)

    @common_api
    def put(self, request):
        """加入购物车"""
        commodity_id = request.data.get("prodId")
        specification_id = request.data.get("skuId")
        count = request.data.get("count")
        if not all((commodity_id, count)):
            raise ValidateException().add_message('error:error', 'Incomplete Params!')
        user = request.auth['user_id']
        shopping = ShoppingCart.objects.filter(
            user_id=user, commodity_id=commodity_id, specification_id=specification_id)
        if shopping:
            shopping.update(count=F("count")+count, delete_status=0)
        else:
            ShoppingCart.objects.create(
                user_id=user, commodity_id=commodity_id, specification_id=specification_id, count=count)
        return Response('success')

    @common_api
    def delete(self, request):
        """购物车删除"""
        items = request.data.get("items")
        if not items:
            raise ValidateException().add_message('error:error', 'Incomplete Params!')
        user = request.auth['user_id']
        with transaction.atomic():
            for item in items:
                shopping = ShoppingCart.objects.filter(
                    user_id=user, commodity_id=item["prodId"], specification_id=item["skuId"])
                shopping.update(delete_status=1, count=0)
            return Response('success')

    @common_api
    def post(self, request):
        """购物车改数量"""
        commodity_id = request.data.get("prodId")
        specification_id = request.data.get("skuId")
        count = request.data.get("count")
        if not all((commodity_id, count)):
            raise ValidateException().add_message('error:error', 'Incomplete Params!')
        user = request.auth['user_id']
        shopping = ShoppingCart.objects.filter(
            user_id=user, commodity_id=commodity_id, specification_id=specification_id)
        with transaction.atomic():
            shopping.update(count=count)
            return Response('success')


class ShoppingAddrView(APIView):
    """收货地址"""
    permission_classes = (IsAuthenticatedWechat,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    @common_api
    def get(self, request):
        addr_id = request.query_params.get('id')
        user = request.auth['user_id']
        if addr_id:
            addr = ShippingAddr.objects.filter(delete_status=0, user_id=user, id=addr_id)
            data = ShippingAddrSerializer(addr).data
        else:
            addr = ShippingAddr.objects.filter(delete_status=0, user_id=user)
            data = ShippingAddrSerializer(addr, many=True).data
        return Response(data)

    @common_api
    def put(self, request):
        update_data = request.data
        addr_id = update_data.pop('id')
        if not all((addr_id, update_data)):
            raise ValidateException().add_message('error:error', 'Incomplete Params!')
        user = request.auth['user_id']
        addr = ShippingAddr.objects.filter(delete_status=0, user_id=user, id=addr_id)
        with transaction.atomic():
            addr.update(**update_data)
            data = ShippingAddrSerializer(addr.first()).data
            return Response(data)

    @common_api
    def post(self, request):
        post_data = request.data
        user = request.auth['user_id']
        addr = ShippingAddr.objects.filter(delete_status=0, user_id=user)
        if not addr:
            post_data['default'] = True
        post_data['user_id'] = user
        with transaction.atomic():
            addr = ShippingAddr.objects.create(**post_data)
            data = ShippingAddrSerializer(addr).data
            return Response(data)

    @common_api
    def delete(self, request):
        addr_id = request.data.get('id')
        if not addr_id:
            raise ValidateException().add_message('error:error', 'Incomplete Params!')
        user = request.auth['user_id']
        addr = ShippingAddr.objects.filter(delete_status=0, user_id=user, id=addr_id)
        addr.update(delete_status=1)
        addr = ShippingAddr.objects.filter(delete_status=0, user_id=user).first()
        if addr:
            addr.default = True
            addr.save()
        return Response('success')


@api_view(['POST'])
@permission_classes((IsAuthenticatedWechat, ))
@authentication_classes((JSONWebTokenAuthentication, SessionAuthentication))
@common_api
def set_default_addr(request):
    """设为默认收货地址"""
    addr_id = request.data.get('id')
    if not addr_id:
        raise ValidateException().add_message('error:error', 'Incomplete Params!')
    user = request.auth['user_id']
    addr = ShippingAddr.objects.filter(delete_status=0, user_id=user, id=addr_id)
    if not addr:
        raise ValidateException().add_message('error:error', 'Addr Id Error!')
    with transaction.atomic():
        ShippingAddr.objects.filter(delete_status=0, user_id=user, default=True).update(default=False)
        addr.update(default=True)
        return Response("success")


@api_view(['GET'])
@permission_classes((IsAuthenticatedWechat, ))
@authentication_classes((JSONWebTokenAuthentication, SessionAuthentication))
@common_api
def get_area(request):
    """地址区域"""
    area_id = request.query_params.get('areaId')
    areas = Area.objects.filter(parent_id=area_id)
    data = AreaSerializer(areas, many=True).data
    return Response(data)
