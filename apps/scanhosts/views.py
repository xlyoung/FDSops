from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import status
from rest_framework.response import Response



from .serializers import HostScanInfoSerializers
from .models import HostScanInifo
from scanhosts.lib.nmap_all_server import NmapScan



class ScanHostsViewset(mixins.CreateModelMixin,mixins.ListModelMixin,mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,viewsets.GenericViewSet):
    """
    list:
        获取主机信息
    create:
        添加主机信息
    update：
        更新主机信息
    delete：
        删除主机信息
    """
    queryset = HostScanInifo.objects.all()
    serializer_class = HostScanInfoSerializers







