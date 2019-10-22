from datetime import datetime
from decimal import Decimal

from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from account.permissions import IsAuthenticatedWechat
from base.exceptions import ValidateException
from commodity.models import Commodity, Specification
from common.decorator import common_api
from mine.models import ShippingAddr, MyCoupon
from mine.serializers import ShippingAddrSerializer


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
    coupon_id = data.get("couponId")
    user = request.auth['user_id']

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
            if commodity.total_stocks < order_item["prodCount"]:
                raise ValidateException().add_message('error:error', '抱歉，商品库存不足!')
            pic = commodity.pic
            specification_name = " "
            price = commodity.price
        prod = {
            "prodId": order_item['prodId'],
            "skuId": order_item['skuId'],
            "name": commodity.name,
            "pic": pic,
            "specification": specification_name,
            "price": price.quantize(Decimal("0.00")),
            "count": order_item["prodCount"],
        }
        prod_items.append(prod)
    elif baskets:
        for item in baskets:
            commodity = Commodity.objects.filter(delete_status=0, id=item['prodId']).first()
            if not commodity:
                raise ValidateException().add_message('error:error', '含有已下架商品!')
            if item['skuId']:
                specification = Specification.objects.filter(id=item['skuId'], commodity=commodity).first()
                if specification.stocks < item["prodCount"]:
                    raise ValidateException().add_message('error:error', '抱歉，商品【{}】库存不足!'.format(commodity.name))
                pic = specification.pic
                specification_name = specification.name
                price = specification.price
            else:
                if commodity.total_stocks < item["prodCount"]:
                    raise ValidateException().add_message('error:error', '抱歉，商品【{}】库存不足!'.format(commodity.name))
                pic = commodity.pic
                specification_name = " "
                price = commodity.price
            prod = {
                "prodId": item['prodId'],
                "skuId": item['skuId'],
                "name": commodity.name,
                "pic": pic,
                "specification": specification_name,
                "price": price.quantize(Decimal("0.00")),
                "count": item["prodCount"],
            }
            prod_items.append(prod)
    else:
        raise ValidateException().add_message('error:error', 'Incomplete Params!')

    # 地址
    if addr_id:
        shipping_addr = ShippingAddr.objects.get(id=addr_id)
    else:
        shipping_addr = ShippingAddr.objects.filter(delete_status=0, user_id=user, default=True).first()
    addr, province_id = (shipping_addr.province_id, ShippingAddrSerializer(shipping_addr).data) if shipping_addr else (None, None)

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
        elif freight_template.charge_type == 2:
            if item["count"] >= freight_template.piece or item["count"]*item["price"] >= freight_template.amount:
                continue
            else:
                freight += freight_template.freight
        elif freight_template.charge_type == 3:
            if province_id in eval(freight_template.area_list):
                continue
            else:
                freight += freight_template.freight

    # TODO 优惠券
    my_coupons = MyCoupon.objects.filter(user_id=user, used=False, delete_status=0)
    now_date = datetime.now()
    prod_id_list = [x['prodId'] for x in prod_items]
    available, unavailable = [], []
    for my_coupon in my_coupons:
        if my_coupon.coupon.min_data < now_date < my_coupon.coupon.max_data and my_coupon.coupon_id in prod_id_list:
            available.append({
                'type': my_coupon.coupon_type,
                'amount': my_coupon.coupon_amount,
                'condition': my_coupon.coupon_condition,
                'min_data': my_coupon.coupon_min_data,
                'max_data': my_coupon.coupon_max_data,
            })
        else:
            unavailable.append({
                'type': my_coupon.coupon_type,
                'amount': my_coupon.coupon_amount,
                'condition': my_coupon.coupon_condition,
                'min_data': my_coupon.coupon_min_data,
                'max_data': my_coupon.coupon_max_data,
            })

    coupon = {
            "available": available,
            "unavailable": unavailable
    }
    if coupon_id:
        # TODO
        pass

    # 最终计算
    count = sum([x["count"] for x in prod_items])
    prod_total = Decimal(sum([x["count"]*x["price"] for x in prod_items])).quantize(Decimal("0.00"))
    data = {
        "addr": addr,
        'prodItems': prod_items,
        "count": count,
        "prod_total": prod_total,
        "coupon": coupon,
        "freight": "%.2f" % freight,
        "discounted_price": "0.00",
        "total": "%.2f" % (prod_total + freight)
    }
    return Response(data)

