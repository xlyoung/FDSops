
# from django.contrib import admin
from django.conf.urls import url, include

from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token
import xadmin


from media_files.views import ImageUploadViewSet,ImageListViewset,FileUploadViewSet,FileListViewset,test_upload
from users.views import EmailCodeViewset,UserViewset

from rest_framework_swagger.views import get_swagger_view



router = DefaultRouter()

#配置images
router.register(r'list/images',ImageListViewset,base_name="list_image")
#配置files
router.register(r'list/files',FileListViewset,base_name="list_file")
#短信验证码生成
router.register(r'codes', EmailCodeViewset, base_name="codes")
#上传图片
router.register(r'api/upload/image',ImageUploadViewSet,base_name="upload_image")
#上传文件
router.register(r'api/upload/file',FileUploadViewSet,base_name="upload_file")
#用户注册
router.register(r'users', UserViewset, base_name="users")


schema_view = get_swagger_view(title="FDSops")

urlpatterns = [
    # path('admin/', admin.site.urls),
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    #文档
    url(r'docs/',include_docs_urls(title="FDSops")),

    #swagger
    # url(r"^docs/$", schema_view),
    # url(r'test/',test_upload),


    #jwt的认证接口
    url(r'^login/', obtain_jwt_token),

    #图片列表
    url(r'^',include(router.urls))
]