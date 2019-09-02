import time
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from common.models import DeleteStatusMixin, GmtCreateModifiedTimeMixin
from common.utils import generate_bsc

# Create your models here.


def user_directory_path(instance, filename):
    file_format = filename.split(".")[-1]
    return "{}{}.{}".format(int(time.time()), generate_bsc(32), file_format)


class FileUpload(GmtCreateModifiedTimeMixin, DeleteStatusMixin):
    file = models.FileField(upload_to=user_directory_path, null=True, blank=True, verbose_name="上载文件")
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="上传人")
    file_url = models.URLField(max_length=128, null=True, blank=True, verbose_name='文件链接')
    file_name = models.CharField(max_length=128, null=True, blank=True, verbose_name='文件原始名称')

    objects = models.Manager()

#
# class FileSet(GmtCreateModifiedTimeMixin, DeleteStatusMixin):
#     object_id = models.PositiveIntegerField(null=False, verbose_name="对象id")
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name="表id")
#     content_object = GenericForeignKey('content_type', 'object_id')
#     file = models.ForeignKey(FileUpload, on_delete=models.PROTECT, verbose_name="文件")
#
#     # if any model more than one field need to upload file, use 'fields' field
#     # fields = models.CharField(max_length=30, null=True, blank=True, verbose_name='字段名')
#
#     objects = models.Manager()


