# from django.contrib import admin
from django.conf.urls import url, include

from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
import xadmin


from media_files.views import ImageViewSet ,\
    FileViewSet,HandleImagesApi,OpenFdfsImage

from users.views import EmailCodeViewset,UserViewset,CustomAuthToken

from rest_framework_swagger.views import get_swagger_view



router = DefaultRouter()

#images
router.register(r'api/(?P<version>[v1|v2]+)/image',ImageViewSet,base_name="image")
#file
router.register(r'api/(?P<version>[v1|v2]+)/file',FileViewSet,base_name="file")
#短信验证码生成
router.register(r'api/(?P<version>[v1|v2]+)/codes', EmailCodeViewset, base_name="codes")
#用户注册
router.register(r'api/(?P<version>[v1|v2]+)/users', UserViewset, base_name="users")



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