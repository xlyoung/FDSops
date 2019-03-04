# -*- coding: utf-8 -*-
__author__ = 'young'
import time
from rest_framework import serializers


from media_files.models import  ImagesMessage,FileMessage


#获取当前时间
def get_now_time(format='%Y-%m-%d %H:%M:%S'):
	tm = time.strftime(format,time.localtime(time.time()))
	return tm

#上传信息表
class UploadImageSerializer(serializers.ModelSerializer):
    """
    图片的serializer
    """
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    name = serializers.CharField(read_only=True)
    creat_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M',help_text="上传时间")
    path = serializers.SerializerMethodField()



    # #获取图片fastdfs的地址id
    def get_path(self,image):
        path = image.file
        return path

    #获取图片名称
    def validate(self, attrs):
        attrs["name"] = attrs['file'].name
        return attrs


    class Meta():
        model = ImagesMessage
        fields = ('id','name','creat_time','file','path','space','file_desc','user')
        depth = 1

class UploadFileSerializer(serializers.ModelSerializer):
    """
    文件的serializer
    # """
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    name = serializers.CharField(read_only=True)
    creat_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M',help_text="上传时间")
    path = serializers.SerializerMethodField()

    # #获取文件fastdfs的地址id
    def get_path(self,file):
        path = file.file
        return path

    #获取文件名称
    def validate(self, attrs):
        attrs["name"] = attrs['file'].name
        return attrs

    class Meta():
        model = FileMessage
        fields = ('id','name','creat_time','path','file','space','file_desc','user')



class ListFileSerializer(serializers.ModelSerializer):
    """
    文件列表
    """
    class Meta():
        model = FileMessage
        fields = '__all__'

class ListImageSerializer(serializers.ModelSerializer):
    """
    图片列表
    """
    class Meta():
        model = ImagesMessage
        fields = '__all__'
        # depth = 0