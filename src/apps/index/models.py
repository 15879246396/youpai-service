from django.db import models

# Create your models here.
from common.models import GmtCreateModifiedTimeMixin, DeleteStatusMixin

IndexImgType = (
    (0, "商品"),
)

CommodityTagStyle = (
    (1, "一列一个"),
    (2, "一列两个"),
    (3, "一列三个"),
)


class IndexImg(GmtCreateModifiedTimeMixin, DeleteStatusMixin):
    """首页轮播图"""
    title = models.CharField(verbose_name="标题", max_length=64, null=False)
    img_url = models.URLField(verbose_name="图片", null=False)
    des = models.CharField(verbose_name="说明文字", max_length=256, null=True, blank=True)
    link = models.URLField(verbose_name="链接", null=True)
    seq = models.IntegerField(verbose_name="排序", default=0)
    type = models.IntegerField(verbose_name="关联类型", choices=IndexImgType, default=0)
    relation = models.IntegerField(verbose_name="关联")

    objects = models.Manager()

    class Meta:
        ordering = ['-seq']


class Notice(GmtCreateModifiedTimeMixin, DeleteStatusMixin):
    """公告"""
    title = models.CharField(verbose_name="公告标题", max_length=64, null=False)
    content = models.TextField(verbose_name="公告内容", null=False)
    is_top = models.BooleanField(verbose_name="是否置顶", default=False)
    status = models.BooleanField(verbose_name="是否公布", default=True)

    objects = models.Manager()


class CommodityTag(GmtCreateModifiedTimeMixin, DeleteStatusMixin):
    """首页分组标签"""
    title = models.CharField(verbose_name="分组标题", max_length=64, null=False)
    prod_count = models.IntegerField(verbose_name="展示数量", null=True)
    style = models.IntegerField(verbose_name="列表样式", choices=CommodityTagStyle, default=1)
    seq = models.IntegerField(verbose_name="排序", default=0)

    objects = models.Manager()
