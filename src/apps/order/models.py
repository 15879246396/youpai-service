from django.db import models

from account.models import MyUser
from commodity.models import Commodity, Specification
from common.models import GmtCreateModifiedTimeMixin, DeleteStatusMixin
from mine.models import ShippingAddr
from order.utils import generate_ordering_no


class Delivery(GmtCreateModifiedTimeMixin):
    """物流公司"""
    name = models.CharField(max_length=32, verbose_name='名称')
    home_url = models.URLField(verbose_name="官网")
    query_url = models.URLField(verbose_name="查件地址")

    objects = models.Manager()


ORDER_STATUS = [
    (1, '待付款'),
    (2, '待发货'),
    (3, '待收货'),
    (4, '待评价'),
    (5, '成功'),
    (6, '失败'),
]

ORDER_CLOSE_TYPE = [
    (1, '超时未支付'),
    (2, '退款关闭'),
    (3, '买家取消'),
    (4, '买家取消'),
    (5, '已通过货到付款交易'),
]


class Order(GmtCreateModifiedTimeMixin, DeleteStatusMixin):
    """订单"""
    order_sn = models.CharField(max_length=128, verbose_name='订单号', default=generate_ordering_no)
    user = models.ForeignKey(MyUser, related_name='order', on_delete=models.PROTECT)
    user_addr = models.ForeignKey(ShippingAddr, verbose_name='用户订单地址', related_name='order', on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='订单价格')
    reduce_amount = models.DecimalField(verbose_name="优惠金额", max_digits=15, decimal_places=2, default=0.00)
    status = models.IntegerField(verbose_name="订单状态", choices=ORDER_STATUS, default=1)
    product_nums = models.IntegerField(verbose_name="订单商品总数")
    pay_status = models.BooleanField(default=False, verbose_name="支付状态")
    pay_type = models.IntegerField(verbose_name="支付方式", choices=[(1, '微信支付'), (2, '支付宝支付'), (3, '手动代付')], default=1)
    pay_time = models.DateTimeField(blank=True, null=True, verbose_name='订单支付(完成)时间')
    freight_amount = models.DecimalField(verbose_name="订单运费", max_digits=15, decimal_places=2, default=0.00)
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE)
    shipment_no = models.CharField(max_length=128, verbose_name='物流单号', null=True)
    dvy_time = models.DateTimeField(blank=True, null=True, verbose_name='发货时间')
    finally_time = models.DateTimeField(blank=True, null=True, verbose_name='订单完成时间')
    cancel_time = models.DateTimeField(blank=True, null=True, verbose_name='订单取消时间')
    close_type = models.IntegerField(verbose_name="订单关闭原因", choices=ORDER_CLOSE_TYPE, default=1)

    objects = models.Manager()


class OrderItem(GmtCreateModifiedTimeMixin, DeleteStatusMixin):
    """订单项"""
    order = models.ForeignKey(Order, related_name='order', on_delete=models.PROTECT)
    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE)
    specification = models.ForeignKey(Specification, on_delete=models.CASCADE)
    count = models.IntegerField(verbose_name="商品数量")
    comment_status = models.BooleanField(default=False, verbose_name="是否评价")

    objects = models.Manager()


class OrderRefund(DeleteStatusMixin):
    """退款"""
    refund_sn = models.CharField(max_length=128, verbose_name='退款编号', default=generate_ordering_no)
    user = models.ForeignKey(MyUser, related_name='refund', on_delete=models.PROTECT)
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    order_item = models.ForeignKey(OrderItem, related_name='refund', on_delete=models.CASCADE)
    apply_time = models.DateTimeField(verbose_name='申请时间', auto_now_add=True)
    buyer_msg = models.CharField(max_length=128, verbose_name='退款原因')
    photo_files = models.CharField(max_length=64, verbose_name='凭证文件id列表', default='[]')
    apply_type = models.IntegerField(verbose_name="申请类型", choices=[(1, '仅退款'), (2, '退款退货')], default=1)
    refund_status = models.IntegerField(verbose_name="处理状态", choices=[(1, '待审核'), (2, '同意'), (3, '不同意')], default=1)
    return_status = models.IntegerField(verbose_name="退款状态", choices=[(0, '退款处理中'), (1, '退款成功'), (-1, '退款失败')], default=0)
    pay_type = models.IntegerField(verbose_name="退款方式", choices=[(1, '微信支付'), (2, '支付宝'), (3, '其他')], null=True)
    out_refund_no = models.CharField(max_length=128, verbose_name='第三方退款单号(微信退款单号)')
    pay_type_name = models.CharField(max_length=64, verbose_name='订单支付名称')
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='退款金额')
    handel_time = models.DateTimeField(verbose_name='卖家处理时间', null=True)
    refund_time = models.DateTimeField(verbose_name='退款时间', null=True)
    seller_msg = models.CharField(max_length=128, verbose_name='卖家备注')
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE)
    delivery_no = models.CharField(max_length=128, verbose_name='物流单号', null=True)
    ship_time = models.DateTimeField(verbose_name='发货时间', null=True)

    objects = models.Manager()
