
# from django.contrib import admin
from django.conf.urls import url, include

from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token
import xadmin


from media_files.views import FileUploadView,ImageListViewset
from users.views import SmsCodeViewset
from scanhosts.views import ScanHostsViewset


router = DefaultRouter()

#配置images
router.register(r'images',ImageListViewset)

#短信验证码生成
router.register(r'codes', SmsCodeViewset, base_name="codes")


#扫描host主机
router.register(r'scanhosts', ScanHostsViewset, base_name="orders")





# router = DefaultRouter()

#

urlpatterns = [
    # path('admin/', admin.site.urls),
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    #上传图片
    url(r'upload/$', FileUploadView.as_view(), name='file-upload'),

    #文档
    url(r'docs/',include_docs_urls(title="FDSops")),

    #jwt的认证接口
    url(r'^login/', obtain_jwt_token),

    #图片列表
    url(r'^',include(router.urls))

    #
]
