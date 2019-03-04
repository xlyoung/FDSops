from django.db import models
from DjangoUeditor.models import UEditorField

from django.contrib.auth import get_user_model

from datetime import datetime

User = get_user_model()



class ImagesMessage(models.Model):
    """
    图片信息
    """
    name = models.CharField(max_length=100,verbose_name="文件名")
    file = models.ImageField( blank=True, verbose_name='图片地址')
    user = models.ForeignKey(User, verbose_name="用户")
    creat_time = models.DateTimeField(default=datetime.now, verbose_name="上传时间")
    space = models.CharField(max_length=100, null=True,blank=True,verbose_name="空间名")
    file_desc = UEditorField(verbose_name=u"内容", imagePath="images/", width=1000, height=300,
                               filePath="files/", null=True,blank=True,default='')

    class Meta:
        verbose_name = '图片信息'
        verbose_name_plural = verbose_name
        db_table = "images_message"

    def __str__(self):
        return self.name

class FileMessage(models.Model):
    """
    文件信息
    """
    name = models.CharField(max_length=100,verbose_name="文件名")
    file = models.FileField( blank=True, verbose_name='文件地址')
    creat_time = models.DateTimeField(default=datetime.now, verbose_name="上传时间")
    user = models.ForeignKey(User, verbose_name="用户")
    space = models.CharField(max_length=100, null=True,blank=True,verbose_name="空间名")
    file_desc = UEditorField(verbose_name=u"内容", imagePath="images/", width=1000, height=300,
                               filePath="files/", null=True,blank=True,default='')

    class Meta:
        verbose_name = '文件信息'
        verbose_name_plural = verbose_name
        db_table = "file_message"

    def __str__(self):
        return self.name