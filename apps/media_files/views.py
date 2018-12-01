from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.pagination import PageNumberPagination

from rest_framework.parsers import MultiPartParser,FormParser
from rest_framework import status

from .models import UploadMessage ,get_now_time
from .serializers import UploadInfoSerializer




from FDSops.settings import TYPE_LIST , MEDIA_ROOT
from media_files.lib.limit import pCalculateMd5 ,pIsAllowedFileSize ,pIsAllowedImageType ,pGetFileExtension







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

        # 计算文件md5
        md5 = pCalculateMd5(file)
        uploadImg = UploadMessage.getImageByMd5(md5)
        # 图片文件已存在， 直接返回
        if uploadImg:
            content = {'MSG': '请勿重复上传','URL':uploadImg.getImageUrl()}
            return Response(content,status=status.HTTP_302_FOUND)

        # 获取扩展类型 并 判断
        ext = pGetFileExtension(file)
        if not pIsAllowedImageType(ext):
            content = {'MSG': "文件类型错误，仅支持" + str(TYPE_LIST) }
            return Response(content, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

        serializer = UploadInfoSerializer(data={
            'name': file.name,
            'file_md5': md5,
            'file_path':request.data['file'] ,
            'file_size':file.size,
            'file_type':ext,
            'space':"test",
        })

        # serializer = UploadInfoSerializer(data=request.data)
        if serializer.is_valid():
            test = serializer.save()
            test.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)




