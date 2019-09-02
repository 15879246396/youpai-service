from django.db import models

# Create your models here.
from account.models import MyUser
from common.models import GmtCreateModifiedTimeMixin, DeleteStatusMixin
from index.models import CommodityTag

ReviewedStatus = (
    (0, "未审核"),
    (1, "审核通过"),
    (2, "审核未通过"),
)

ChargeType = (
    (0, "满件数"),
    (1, "满金额"),
    (2, "满件数或者满金额"),
)


class Category(GmtCreateModifiedTimeMixin, DeleteStatusMixin):
    """商品类型"""
    name = models.CharField(verbose_name="产品类目名称", max_length=64, null=False)
    pic = models.URLField(verbose_name="类目的显示图片", null=True)
    seq = models.IntegerField(verbose_name="排序", null=False)

    objects = models.Manager()

    class Meta:
        ordering = ['-seq']


class FreightTemplate(GmtCreateModifiedTimeMixin, DeleteStatusMixin):
    """运费模板"""
    name = models.CharField(verbose_name="模板名称", max_length=64, null=False)
    freight = models.DecimalField(verbose_name="运费", max_digits=15, decimal_places=2, null=False)
    charge_type = models.IntegerField(verbose_name="收费方式", choices=ChargeType)
    amount = models.DecimalField(verbose_name="需满金额", max_digits=15, decimal_places=2, null=True, blank=True)
    piece = models.DecimalField(verbose_name="需满件数", max_digits=15, decimal_places=2, null=True, blank=True)

    objects = models.Manager()


class Commodity(GmtCreateModifiedTimeMixin, DeleteStatusMixin):
    """商品"""
    name = models.CharField(verbose_name="产品名称", max_length=64, null=False)
    ori_price = models.DecimalField(verbose_name="原价", max_digits=15, decimal_places=2, null=False)
    price = models.DecimalField(verbose_name="现价", max_digits=15, decimal_places=2, null=False)
    is_free_fee = models.BooleanField(verbose_name="是否包邮", default=True)
    freight_template = models.ForeignKey(verbose_name="运费模板", to=FreightTemplate, on_delete=models.CASCADE, null=True)
    brief = models.CharField(verbose_name="简要描述", max_length=512, null=True, blank=True)
    content = models.TextField(verbose_name="详细描述", null=True)
    pic = models.URLField(verbose_name="产品主图", null=True)
    images = models.CharField(verbose_name="产品图片", max_length=1024, null=True, blank=True)
    category = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE)
    commodity_tag = models.ForeignKey(CommodityTag, related_name='tag', on_delete=models.CASCADE, null=True)
    sold_num = models.IntegerField(verbose_name="销量", null=True, default=0)
    total_stocks = models.IntegerField(verbose_name="总库存", default=0)

    objects = models.Manager()


# class Evaluation(GmtCreateModifiedTimeMixin, DeleteStatusMixin):
#     """商品评价"""
#     prod = models.ForeignKey(verbose_name="产品名称", to=Commodity, on_delete=models.CASCADE)
#     order = models.ForeignKey(verbose_name="关联订单", to=Order, on_delete=models.CASCADE)
#     user = models.ForeignKey(verbose_name="评论人", to=MyUser, on_delete=models.CASCADE)
#     is_anonymous = models.BooleanField(verbose_name="是否匿名", default=False)
#     content = models.CharField(verbose_name="评论内容", max_length=512, null=False)
#     reply_sts = models.BooleanField(verbose_name="商家是否回复", default=False)
#     reply_content = models.CharField(verbose_name="商家回复", max_length=512, null=True, blank=True)
#     post_ip = models.CharField(verbose_name="IP来源", max_length=16, null=True, blank=True)
#     score = models.IntegerField(verbose_name="评分", null=False)
#     pics = models.CharField(verbose_name="晒图", max_length=1024, null=True)
#     reviewed_status = models.IntegerField(verbose_name="审核状态", choices=ReviewedStatus, default=0)

    # objects = models.Manager()




