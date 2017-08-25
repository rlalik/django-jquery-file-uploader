# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import index, UploadView, delete

app_name="jqfuploader"

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^upload/$', UploadView.as_view(), name='upload'),
    url(r'^delete/(?P<uid>[0-9a-fA-F]+)$', delete, name='delete'),
]
