
# from django.contrib import admin
from django.conf.urls import url, include

from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token
import xadmin


from media_files.views import ImageUploadViewSet,ImageListViewset
from users.views import SmsCodeViewset


router = DefaultRouter()

#配置images
router.register(r'images',ImageListViewset,base_name="images")

#短信验证码生成
router.register(r'codes', SmsCodeViewset, base_name="codes")

#上传图片

router.register(r'api/upload/image',ImageUploadViewSet,base_name="upload")


urlpatterns = [
    # path('admin/', admin.site.urls),
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    #上传图片
    # url(r'upload/$', ImageUploadViewSet.as_view(), name='file-upload'),

    #文档
    url(r'docs/',include_docs_urls(title="FDSops")),

    #jwt的认证接口
    url(r'^login/', obtain_jwt_token),

    #图片列表
    url(r'^',include(router.urls))
]