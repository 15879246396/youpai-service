from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from account.permissions import IsAuthenticatedWechat
from commodity.models import CommodityCollect, Commodity
from commodity.serializers import CommodityListSerializer
from common.decorator import common_api


@api_view(['GET'])
@permission_classes((IsAuthenticatedWechat, ))
@authentication_classes((JSONWebTokenAuthentication, SessionAuthentication))
@common_api
def get_collect_list(request):
    """我的收藏"""
    user = request.auth.id
    collect_list = CommodityCollect.objects.filter(delete_status=0, user=user)\
        .order_by("-gmt_modified").values_list('id', flat=True)
    commodities = Commodity.objects.filter(category_id__in=collect_list)
    data = CommodityListSerializer(commodities).data
    return Response(data)
