from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'top_banana_service.settings')  # 设置django环境

CELERY = Celery('top_banana_service')

# 使用CELERY_ 作为前缀，在settings中写配置
CELERY.config_from_object('django.conf:settings', namespace='CELERY')

CELERY.autodiscover_tasks(lambda: settings.INSTALLED_APPS)  # 发现任务文件每个app下的task.py
