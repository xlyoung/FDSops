# -*- coding: utf-8 -*-
__author__ = 'young'

import django_filters
from django.db.models import Q
from django.db import models as django_models

from .models import UploadImagesMessage


class ImagesFilter(django_filters.rest_framework.FilterSet):
    """
    图片的过滤类
    """
    # start_upload_time = django_filters.DateFilter('upload_time', label=('开始上传时间'))

    id = django_filters.NumberFilter(field_name='id')
    name = django_filters.CharFilter(field_name='name')
    fds_path = django_filters.CharFilter(field_name='fds_path')
    space = django_filters.CharFilter(field_name="space")
    user = django_filters.NumberFilter(field_name="user")


    class Meta:
        model = UploadImagesMessage
        fields = ['id',"name","fds_path","space","user"]