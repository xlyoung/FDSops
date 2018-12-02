
# from django.contrib import admin
from django.conf.urls import url, include
from media_files.views import FileUploadView,ImageListViewset
import xadmin
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

#配置images
router.register(r'images',ImageListViewset)



# router = DefaultRouter()

#

urlpatterns = [
    # path('admin/', admin.site.urls),
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    #上传图片
    url(r'upload/$', FileUploadView.as_view(), name='file-upload'),
    #图片列表
    url(r'^',include(router.urls))


]
