from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.pagination import PageNumberPagination

from rest_framework.parsers import MultiPartParser,FormParser
from rest_framework import status

from .models import UploadMessage
from .serializers import UploadInfoSerializer




from FDSops.settings import TYPE_LIST , MEDIA_ROOT
from media_files.lib.limit import pCalculateMd5 ,pIsAllowedFileSize ,pIsAllowedImageType ,pGetFileExtension
import os

class UploadPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100

class FileUploadView(APIView):
    """
    上传文件
    """
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):

        file = request.data['file']
        # 文件对象不存在， 返回400请求错误
        if not file:
            content = {'MSG':'请选择文件'}
            return Response(content,status=status.HTTP_404_NOT_FOUND)

        # 图片大小限制
        if not pIsAllowedFileSize(file.size):
            content = {'MSG': '请上传小于20M图片'}
            return Response(content,status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)

        #定义空间命名
        try:
            space_value = request.data['space']
        except Exception:
            space_value = ""


        serializer = UploadInfoSerializer(data={
                                           'name' : file.name,
                                           'fds_path'  : file,
                                           'file_size'  : file.size,
                                            'space' : space_value,
                                            }
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors)