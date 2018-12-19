# -*- coding: utf-8 -*-
__author__ = 'young'

import django_filters
from django.db.models import Q

from .models import UploadImagesMessage


class ImagesFilter(django_filters.rest_framework.FilterSet):
    """
    图片的过滤类
    """
    start = django_filters.DateFilter('upload_time', label=('With start date'))

    class Meta:
        model = UploadImagesMessage
        fields = ['start']