# -*- coding: utf-8 -*-
__author__ = 'young'
import time
from rest_framework import serializers


from media_files.models import  UploadImagesMessage



#获取当前时间
def get_now_time(format='%Y-%m-%d %H:%M:%S'):
	tm = time.strftime(format,time.localtime(time.time()))
	return tm


#上传信息表
class UploadInfoSerializer(serializers.ModelSerializer):
    upload_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    name = serializers.CharField(read_only=True)

    class Meta():
        model = UploadImagesMessage
        fields = '__all__'


    def create(self, validated_data):
        name = validated_data['fds_path']
        # fds_path = validated_data.get('file')
        image = UploadImagesMessage.objects.create(name=name)
        return image
