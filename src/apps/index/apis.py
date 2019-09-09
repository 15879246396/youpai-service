from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from commodity.models import Commodity
from common.decorator import common_api
from index.models import IndexImg, Notice, CommodityTag
from index.serializers import IndexImgSerializer, NoticeSerializer


@api_view(['GET'])
@common_api
def index_img(request):
    index_imgs = IndexImg.objects.filter(delete_status=False).order_by("seq")
    data = IndexImgSerializer(index_imgs, many=True).data
    return Response(data)


class IndexNoticeView(APIView):

    @common_api
    def get(self, request):
        notices = Notice.objects.filter(delete_status=False, status=True)
        data = NoticeSerializer(notices, many=True).data
        return Response(data)


@api_view(['GET'])
@common_api
def index_commodity(request):
    tags = CommodityTag.objects.filter(delete_status=0).order_by("seq")
    data_list = []
    for tag in tags:
        prod_count = tag.prod_count
        commodutys = Commodity.objects.filter(delete_status=0, commodity_tag=tag).limit(prod_count)
        data = {
            "id": tag.id,
            "style": tag.id,
        }
        data_list.append(data)

    return Response(tags)
