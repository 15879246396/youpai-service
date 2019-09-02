from rest_framework.decorators import api_view
from rest_framework.response import Response

from common.decorator import common_api
from index.models import IndexImg
from index.serializers import IndexImgSerializer


@common_api
@api_view(['GET'])
def index_img(request):
    index_imgs = IndexImg.objects.filter(delete_status=False).order_by("seq")
    data = IndexImgSerializer(index_imgs, many=True).data
    return Response(data)
