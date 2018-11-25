from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework import views
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser ,FileUploadParser ,FormParser
from rest_framework import status
from rest_framework.exceptions import ParseError


from .models import UploadMessage ,FileInfo,FdsMessage
from .serializers import UploadInfoSerializer,FdsMessageSerializer,FileInfoSerializer

import datetime
from FDSops.settings import MEDIA_ROOT


class UploadPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100


class FileUploadView(views.APIView):
    '''
    上传文件接口
    '''

    def post(self, request, *args, **kwargs):
        file_serializer = UploadInfoSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
