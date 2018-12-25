from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser,FormParser,FileUploadParser
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from .models import UploadImagesMessage
from .serializers import UploadInfoSerializer,ListImageSerializer
from utils.permissions import IsOwnerOrReadOnly



from .filters import ImagesFilter



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
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)


    queryset = UploadImagesMessage.objects.all()
    parser_classes = (MultiPartParser, )
    serializer_class = UploadInfoSerializer




class ImageListViewset(mixins.ListModelMixin,viewsets.GenericViewSet):
    """
    图片列表页
    """
    queryset = UploadImagesMessage.objects.all()
    serializer_class = ListImageSerializer
    pagination_class = UploadPagination


    #过滤
    filter_backends = (DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter)
    filter_class = ImagesFilter
    search_fields = ('name', 'space')
    ordering_fields = ('id', 'upload_time')
