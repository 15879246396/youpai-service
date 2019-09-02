from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings

from rest_framework import routers

from upload import apis

router = routers.SimpleRouter()
router.register(r'file_view', apis.FileAPIViewSet, base_name='file_view')
router.register(r'cms_file_view', apis.CMSFileAPIViewSet, base_name='cms_file_view')


urlpatterns = [
    path('', include(router.urls)),
    re_path('media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path('^file_download/$', apis.file_download),
]