from django.db import models

# Create your models here.
from account.models import MyUser
from commodity.models import Commodity, Specification
from common.models import GmtCreateModifiedTimeMixin, DeleteStatusMixin


class ShoppingCart(GmtCreateModifiedTimeMixin, DeleteStatusMixin):
    """购物车"""
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE)
    specification = models.ForeignKey(Specification, on_delete=models.CASCADE, null=True)
    count = models.IntegerField(verbose_name="数量", default=1)

    objects = models.Manager()


class Area(models.Model):
    """地址"""
    name = models.CharField(verbose_name="地区名称（省市区县）", max_length=32, null=False)
    parent = models.ForeignKey('self', verbose_name="上级地区", related_name="subarea", on_delete=models.CASCADE, null=True)
    level = models.IntegerField(verbose_name="级别", choices=[(1, '省'), (2, '市'), (3, '区/县')], default=1)
    objects = models.Manager()


class ShippingAddr(GmtCreateModifiedTimeMixin, DeleteStatusMixin):
    """收货地址"""
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    default = models.BooleanField(verbose_name="是否默认地址", null=False, default=False)
    receiver = models.CharField(verbose_name="收货人", max_length=32, null=False)
    addr = models.CharField(verbose_name="详细地址", max_length=64, null=False)
    phone = models.CharField(verbose_name="手机号", max_length=16, null=False)
    province = models.ForeignKey(Area, verbose_name="省份", related_name="province", on_delete=models.CASCADE)
    city = models.ForeignKey(Area, verbose_name="城市", related_name="city", on_delete=models.CASCADE)
    area = models.ForeignKey(Area, verbose_name="区/县", related_name="area", on_delete=models.CASCADE)

    objects = models.Manager()
