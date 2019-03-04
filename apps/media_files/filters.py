# -*- coding: utf-8 -*-
__author__ = 'young'

import django_filters
from django.db.models import Q
from django.db import models as django_models

from .models import ImagesMessage,FileMessage


class ImagesFilter(django_filters.rest_framework.FilterSet):
    """
    图片的过滤类
    """
    # start_upload_time = django_filters.DateFilter('upload_time', label=('开始上传时间'))

    id = django_filters.NumberFilter(field_name='id')
    name = django_filters.CharFilter(field_name='name')
    file = django_filters.CharFilter(field_name='file')
    space = django_filters.CharFilter(field_name="space")
    user = django_filters.NumberFilter(field_name="user")


    class Meta:
        model = ImagesMessage
        fields = ['id',"name","file","space","user"]


class FilesFilter(django_filters.rest_framework.FilterSet):
    """
    文件的过滤类
    """
    # start_upload_time = django_filters.DateFilter('upload_time', label=('开始上传时间'))

    id = django_filters.NumberFilter(field_name='id')
    name = django_filters.CharFilter(field_name='name')
    file = django_filters.CharFilter(field_name='file')
    space = django_filters.CharFilter(field_name="space")
    user = django_filters.NumberFilter(field_name="user")


    class Meta:
        model = FileMessage
        fields = ['id',"name","file","space","user"]