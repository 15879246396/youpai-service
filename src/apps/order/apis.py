from decimal import Decimal

from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from account.permissions import IsAuthenticatedWechat
from base.exceptions import ValidateException
from commodity.models import Commodity, Specification
from common.decorator import common_api


@api_view(['POST'])
@permission_classes((IsAuthenticatedWechat, ))
@authentication_classes((JSONWebTokenAuthentication, SessionAuthentication))
@common_api
def confirm(request):
    """获取订单确认信息"""
    data = request.data
    addr_id = data.get("addrId")
    order_item = data.get("orderItem")
    baskets = data.get("basketIds")
    coupons = data.get("couponIds")

    prod_items = []
    if order_item:
        commodity = Commodity.objects.filter(delete_status=0, id=order_item['prodId']).first()
        if not commodity:
            raise ValidateException().add_message('error:error', '此商品已下架!')
        if order_item['skuId']:
            specification = Specification.objects.filter(id=order_item['skuId'], commodity=commodity).first()
            if specification.stocks < order_item["prodCount"]:
                raise ValidateException().add_message('error:error', '抱歉，商品库存不足!')
            pic = specification.pic
            specification_name = specification.name
            price = specification.price
        else:
            if commodity.stocks < order_item["prodCount"]:
                raise ValidateException().add_message('error:error', '抱歉，商品库存不足!')
            pic = commodity.pic
            specification_name = " "
            price = commodity.price
        prod = {
            "prodId": order_item['prodId'],
            "name": commodity.name,
            "pic": pic,
            "specification": specification_name,
            "price": price.quantize(Decimal("0.00")),
            "count": order_item["prodCount"],
        }
        prod_items.append(prod)
    else:
        raise ValidateException().add_message('error:error', 'Incomplete Params!')

    # TODO 运费计算
    freight = Decimal()
    for item in prod_items:
        commodity = Commodity.objects.filter(delete_status=0, id=item['prodId']).first()
        if commodity.is_free_fee:
            continue
        freight_template = commodity.freight_template
        if freight_template.charge_type == 0:
            if item["count"] >= freight_template.piece:
                continue
            else:
                freight += freight_template.freight
        elif freight_template.charge_type == 1:
            if item["count"]*item["price"] >= freight_template.amount:
                continue
            else:
                freight += freight_template.freight
        else:
            if item["count"] >= freight_template.piece or item["count"]*item["price"] >= freight_template.amount:
                continue
            else:
                freight += freight_template.freight

    # TODO 优惠券
    coupon = {
            "available": [],
            "unavailable": []
    }

    # 最终计算
    count = sum([x["count"] for x in prod_items])
    prod_total = Decimal(sum([x["count"]*x["price"] for x in prod_items])).quantize(Decimal("0.00"))
    data = {
        "addr": None,
        'prodItems': prod_items,
        "count": count,
        "prod_total": prod_total,
        "coupon": coupon,
        "freight": freight.quantize(Decimal("0.00")),
        "discounted_price": "0.00",
        "total": (prod_total + freight).quantize(Decimal("0.00"))
    }
    return Response(data)

