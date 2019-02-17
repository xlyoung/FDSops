from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser,FormParser,FileUploadParser
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import filters


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



class UploadPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100

class ImageUploadViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    create:
    上传图片
    """
    # permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = [TokenAuthtication]


    queryset = UploadImagesMessage.objects.all()
    parser_classes = (MultiPartParser, )
    serializer_class = UploadImageSerializer



class FileUploadViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    create:
    上传文件
    """
    # permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    # authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    authentication_classes = [TokenAuthtication]

    queryset = UploadFileMessage.objects.all()
    parser_classes = (MultiPartParser, )
    serializer_class = UploadFileSerializer




class ImageListViewset(mixins.ListModelMixin,viewsets.GenericViewSet):
    """
    图片列表页
    """
    authentication_classes = [TokenAuthtication]
    queryset = UploadImagesMessage.objects.all()
    serializer_class = ListImageSerializer
    pagination_class = UploadPagination


    #过滤
    filter_backends = (DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter)
    filter_class = ImagesFilter
    search_fields = ('name', 'space')
    ordering_fields = ('id', 'creat_time')


class FileListViewset(mixins.ListModelMixin,viewsets.GenericViewSet):
    """
    文件列表页
    """
    authentication_classes = [TokenAuthtication]
    queryset = UploadFileMessage.objects.all()
    serializer_class = ListFileSerializer
    pagination_class = UploadPagination


    #过滤
    filter_backends = (DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter)
    filter_class = FilesFilter
    search_fields = ('name', 'space')
    ordering_fields = ('id', 'creat_time')


class HandleImagesApi(APIView):
    """
    列出处理过的图片
    """
    authentication_classes = [TokenAuthtication]
    authentication_classes = []
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