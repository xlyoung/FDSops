# -*- coding: utf-8 -*-
__author__ = 'young'
import time
from rest_framework import serializers


from media_files.models import  UploadImagesMessage,UploadFileMessage


#获取当前时间
def get_now_time(format='%Y-%m-%d %H:%M:%S'):
	tm = time.strftime(format,time.localtime(time.time()))
	return tm

#上传信息表
class UploadImageSerializer(serializers.ModelSerializer):
    """
    图片的serializer
    """
    # user = serializers.HiddenField(
    #     default=serializers.CurrentUserDefault()
    # )
    user = serializers.CharField(read_only=True,default=1)
    name = serializers.CharField(read_only=True)
    upload_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M',help_text="上传时间")
    image_url = serializers.SerializerMethodField()

    #获取图片fastdfs的地址id
    def get_image_url(self,image):
        image_url = image.fds_path
        return image_url

    #获取图片名称
    def validate(self, attrs):
        attrs["name"] = attrs['fds_path'].name
        return attrs

    class Meta():
        model = UploadImagesMessage
        fields = ('id','name','upload_time','image_url','fds_path','space','file_desc',"user")



class UploadFileSerializer(serializers.ModelSerializer):
    """
    文件的serializer
    """
    # user = serializers.HiddenField(
    #     default=serializers.CurrentUserDefault()
    # )
    user = serializers.CharField(read_only=True,default=1)
    name = serializers.CharField(read_only=True)
    upload_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M',help_text="上传时间")
    file_url = serializers.SerializerMethodField()

    #获取文件fastdfs的地址id
    def get_file_url(self,file):
        file_url = file.fds_path
        return file_url

    #获取文件名称
    def validate(self, attrs):
        attrs["name"] = attrs['fds_path'].name
        return attrs

    class Meta():
        model = UploadFileMessage
        fields = ('id','name','upload_time','file_url','fds_path','space','file_desc',"user")



class ListFileSerializer(serializers.ModelSerializer):
    """
    文件列表
    """
    class Meta():
        model = UploadFileMessage
        fields = '__all__'





class ListImageSerializer(serializers.ModelSerializer):
    """
    图片列表
    """
    class Meta():
        model = UploadImagesMessage
        fields = '__all__'