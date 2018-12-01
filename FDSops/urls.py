
# from django.contrib import admin
from django.conf.urls import url, include
from media_files.views import FileUploadView
import xadmin



urlpatterns = [
    # path('admin/', admin.site.urls),
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^upload/$', FileUploadView.as_view(), name='file-upload'),
]
