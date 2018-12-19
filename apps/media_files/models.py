from django.db import models
from DjangoUeditor.models import UEditorField



from datetime import datetime



class UploadImagesMessage(models.Model):
    """
    上传信息
    """
    name = models.CharField(max_length=100,verbose_name="文件名")
    fds_path = models.ImageField(null=False, blank=False, verbose_name='上传图片地址')
    upload_time = models.DateTimeField(default=datetime.now, verbose_name="上传时间")
    space = models.CharField(max_length=100, null=True,blank=True,verbose_name="空间名")
    file_desc = UEditorField(verbose_name=u"内容", imagePath="images/", width=1000, height=300,
                               filePath="files/", null=True,blank=True,default='')

    class Meta:
        verbose_name = '上传信息'
        verbose_name_plural = verbose_name
        db_table = "upload_images_message"

    def __str__(self):
        return self.name