# -*- coding: utf-8 -*-
__author__ = 'young'
import time
from rest_framework import serializers


from media_files.models import  UploadImagesMessage
from FDSops.settings import FDFS_URL


#获取当前时间
def get_now_time(format='%Y-%m-%d %H:%M:%S'):
	tm = time.strftime(format,time.localtime(time.time()))
	return tm

#上传信息表
class UploadInfoSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    upload_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    image_url = serializers.SerializerMethodField()


    #获取图片fastdfs的地址id
    def get_image_url(self,image):
        image_url = image.fds_path
        return image_url

    #获取图片名称
    def validate(self, attrs):
        attrs["name"] = attrs['fds_path'].name
        return attrs

    # #验证图片大小
    # def validate_image(self,attrs):
    #     if attrs['fds_path'].size > 20000000:
    #         raise serializers.ValidationError('图片不能大于20M')
    #     return attrs

    class Meta():
        model = UploadImagesMessage
        fields = ('id','name','upload_time','image_url','fds_path','space','file_desc')
        # fields = '__all__'


class ListImageSerializer(serializers.ModelSerializer):
    class Meta():
        model = UploadImagesMessage
        fields = '__all__'