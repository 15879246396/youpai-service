from django.db import models

# Create your models here.
from account.models import MyUser
from commodity.models import Commodity, Specification
from common.models import GmtCreateModifiedTimeMixin, DeleteStatusMixin


class ShoppingCart(GmtCreateModifiedTimeMixin, DeleteStatusMixin):
    """购物车"""
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE)
    specification = models.ForeignKey(Specification, on_delete=models.CASCADE)
    count = models.IntegerField(verbose_name="数量", default=1)

    objects = models.Manager()
