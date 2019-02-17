
# from django.contrib import admin
from django.conf.urls import url, include

from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
import xadmin


from media_files.views import ImageUploadViewSet,ImageListViewset,\
    FileUploadViewSet,FileListViewset,HandleImagesApi,OpenFdfsImage

from users.views import EmailCodeViewset,UserViewset,CustomAuthToken

from rest_framework_swagger.views import get_swagger_view



router = DefaultRouter()

#配置images
router.register(r'api/v1/list_images',ImageListViewset,base_name="list_image")
#配置files
router.register(r'api/v1/list_files',FileListViewset,base_name="list_file")
#短信验证码生成
router.register(r'api/v1/codes', EmailCodeViewset, base_name="codes")
#上传图片
router.register(r'api/v1/upload/image',ImageUploadViewSet,base_name="upload_image")
#上传文件
router.register(r'api/v1/upload/file',FileUploadViewSet,base_name="upload_file")
#用户注册
router.register(r'api/v1/users', UserViewset, base_name="users")



schema_view = get_swagger_view(title="FDSops")

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #文档
    url(r'docs/',include_docs_urls(title="FDSops")),
    #token的认证接口
    url(r'^api-token-auth/', CustomAuthToken.as_view()),
    #图片列表
    url(r'^',include(router.urls)),
    #图片切割
    url(r'^group(?P<gid>[0-9])/(?P<fileid>.+)!(?P<parameter>.+)',HandleImagesApi.as_view()),
    #打开图片
    url(r'^group(?P<gid>[0-9])/(?P<fileid>.+)',OpenFdfsImage.as_view()),

]