import pymysql
from __future__ import absolute_import, unicode_literals
from .celery import CELERY as celery_app

pymysql.install_as_MySQLdb()

__all__ = ['celery_app']
