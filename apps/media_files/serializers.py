# -*- coding: utf-8 -*-
__author__ = 'young'
import time
from rest_framework import serializers


from media_files.models import  UploadMessage






#获取当前时间
def get_now_time(format='%Y-%m-%d %H:%M:%S'):
	tm = time.strftime(format,time.localtime(time.time()))
	return tm


#上传信息表
class UploadInfoSerializer(serializers.ModelSerializer):
    class Meta():
        model = UploadMessage
        fields = "__all__"
