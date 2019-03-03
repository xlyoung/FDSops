from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser,FormParser,FileUploadParser
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions

from django_filters.rest_framework import DjangoFilterBackend
from .models import UploadImagesMessage,UploadFileMessage
from django.http import HttpResponse
from io import BytesIO
import requests
import time


from .serializers import UploadImageSerializer,ListImageSerializer,UploadFileSerializer,ListFileSerializer
from .filters import ImagesFilter,FilesFilter
from utils.auth import TokenAuthtication
from FDSops.settings import FDFS_URL
from media_files.lib.pil_image import HandleImage
from rest_framework.versioning import URLPathVersioning


class MediaPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100

class ImageViewSet(mixins.CreateModelMixin,mixins.ListModelMixin,viewsets.GenericViewSet):
    """
    create:
    上传图片
    list:
    列出图片
    """
    authentication_classes = [TokenAuthtication]
    #版本控制
    versioning_class = URLPathVersioning
    queryset = UploadImagesMessage.objects.all()
    parser_classes = (MultiPartParser, )
    serializer_class = UploadImageSerializer
    pagination_class = MediaPagination

    #过滤
    filter_backends = (DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter)
    filter_class = ImagesFilter
    search_fields = ('name', 'space')
    ordering_fields = ('id', 'creat_time')


    def get_serializer_class(self):
        if self.action == "create":
            return UploadImageSerializer
        elif self.action == "list":
            return ListImageSerializer

class FileViewSet(mixins.CreateModelMixin,mixins.ListModelMixin,viewsets.GenericViewSet):
    """
    create:
    上传文件
    list:
    列出文件
    """
    # TOKEN认证
    authentication_classes = [TokenAuthtication]
    #版本控制
    versioning_class = URLPathVersioning

    queryset = UploadFileMessage.objects.all()
    parser_classes = (MultiPartParser, )
    serializer_class = UploadFileSerializer
    pagination_class = MediaPagination


    #过滤
    filter_backends = (DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter)
    filter_class = FilesFilter
    search_fields = ('name', 'space')
    ordering_fields = ('id', 'creat_time')

    #获取Serializer
    def get_serializer_class(self):
        if self.action == "create":
            return UploadFileSerializer
        elif self.action == "list":
            return ListFileSerializer


class HandleImagesApi(APIView):
    """
    列出处理过的图片
    """

    # TOKEN认证
    # authentication_classes = [TokenAuthtication]
    def get(self,request,gid,fileid,parameter):
        """
        :param
        gid: fastdfs组Id
        fileid:图片id
        :parameter:处理参数 sz,lg,md
        :return:image
        """
        url = FDFS_URL + "group" + gid + "/" + fileid

        I = HandleImage(url=url)
        image = I.himage(parameter=parameter)
        # 写入内存
        buf = BytesIO()
        # 保存图片在内存中
        image.save(buf, 'png')
        return HttpResponse(buf.getvalue(), content_type='image/jpeg')


class OpenFdfsImage(APIView):
    """
        :param
        gid: fastdfs组Id
        fileid:图片id
        :return:image
    """

    def get(self,request,gid,fileid,):
        url =  FDFS_URL + "group" + gid + "/" + fileid
        # 读取fds配置文件
        print (time.time())
        r = requests.get(url)
        print (time.time())
        return HttpResponse(r.content, content_type="image/*")


