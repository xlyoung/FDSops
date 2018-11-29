

from django.db import models
from DjangoUeditor.models import UEditorField



from FDSops.settings import WEB_HOST_NAME,MEDIA_ROOT
# Create your models here.



from datetime import datetime
import time,os
#时间格式
#获取当前时间
def get_now_time(format='%Y-%m-%d %H:%M:%S'):
    tm = time.strftime(format,time.localtime(time.time()))
    if not os.path.exists(MEDIA_ROOT+tm):
        os.makedirs(MEDIA_ROOT+tm)
    return tm





class FdsMessage(models.Model):
    """
    文件信息
    """
    file_md5 = models.CharField(max_length=100, verbose_name="md5值")
    upload_ip = models.GenericIPAddressField(verbose_name="客户端上传ip")
    fds_storage_path = models.FilePathField(path="/group1/M00", max_length=200, verbose_name="fds存储位置")
    group_name = models.CharField(max_length=100, verbose_name="上传群主")
    fds_add_time = models.DateTimeField(default=datetime.now, verbose_name="fds添加时间")
    upload_status = models.CharField(max_length=100, verbose_name="上传fds状态")
    fds_size = models.FloatField(default=0, verbose_name="fds文件大小")

    class Meta:
        verbose_name = '文件信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.file_md5







class UploadMessage(models.Model):
    """
    上传信息
    """
    name = models.CharField(max_length=100, verbose_name="文件名")
    file_md5 = models.CharField(max_length=100, verbose_name="md5值")
    # file_path = models.ImageField(upload_to=get_now_time('%Y%m/'), null=False, blank=False, verbose_name='文件位置')
    file_path = models.ImageField(upload_to="", null=False, blank=False, verbose_name='文件位置')
    file_size = models.IntegerField(default=0, verbose_name="文件大小")
    file_type = models.CharField(max_length=100, verbose_name="文件类型")
    create_time = models.DateTimeField(default=datetime.now, verbose_name="文件创建时间")
    upload_time = models.DateTimeField(default=datetime.now, verbose_name="上传时间")
    space = models.CharField(max_length=100, default=None,verbose_name="空间名")
    file_fds_message = models.ForeignKey(FdsMessage , related_name='md5', null=True, blank=True, verbose_name="md5值")
    file_desc = UEditorField(verbose_name=u"内容", imagePath="images/", width=1000, height=300,
                              filePath="files/", default='')



    # 我们还定义了通过文件md5值获取模型对象的类方法
    @classmethod
    def getImageByMd5(cls, md5):
        try:
            return UploadMessage.objects.filter(file_md5=md5).first()
        except Exception as e:
            return None


    #获取图片地址
    def getImageUrl(self):
        filename = self.file_md5 + "." + self.file_type
        url = WEB_HOST_NAME + MEDIA_ROOT + get_now_time('/%Y%m/') + filename
        return url

    def getImagePath(self):
        filename = self.file_md5 + "." + self.file_type
        path = MEDIA_ROOT + get_now_time('/%Y%m/') + filename
        return path




    class Meta:
        verbose_name = '上传信息'
        verbose_name_plural = verbose_name
        db_table = "upload_message"




    def __str__(self):
        return self.name






