from datetime import datetime

from django.db import models
from DjangoUeditor.models import UEditorField
# Create your models here.



class UploadMessage(models.Model):
    """
    上传信息
    """

    UPLOAD_STATUS = (
        (0, "上传成功"),
        (1, "上传失败"),

    )

    name = models.CharField(max_length=100, verbose_name="md5值")

    upload_time = models.DateTimeField(default=datetime.now, verbose_name="上传时间")

    assess_ip = models.GenericIPAddressField(verbose_name="上传ip")
    fds_ip = models.GenericIPAddressField(verbose_name="fds_ip")
    upload_code = models.CharField(default="", max_length=30, verbose_name="上传状态码", help_text="上传状态码")
    upload_status = models.IntegerField(choices=UPLOAD_STATUS, verbose_name="上传状态", help_text="上传状态")


    class Meta:
        verbose_name = '上传信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name



class FileInfo(models.Model):
    """
    文件信息
    """
    md5_value = models.ForeignKey(UploadMessage, verbose_name="md5值")

    filename = models.CharField(max_length=100, verbose_name="文件名")
    filesize = models.IntegerField(default=0, verbose_name="文件大小")
    stype = models.CharField(max_length=100, verbose_name="文件类型")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="文件创建时间")
    local_storage_path = models.FilePathField(path="/media/file", max_length=200, verbose_name="本地存储位置")
    is_delete = models.BooleanField(default=True, verbose_name="是否已删除")
    space = models.CharField(max_length=100, verbose_name="空间名")
    file_desc = UEditorField(verbose_name=u"内容", imagePath="images/", width=1000, height=300,
                              filePath="files/", default='')
    class Meta:
        verbose_name = '文件信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.md5_value.name



class FdsMessage(models.Model):
    """
    文件信息
    """
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
        return self.group_name


class UploadImage(models.Model):
    """
    商品轮播图
    """
    upload_file = models.ForeignKey(FileInfo, verbose_name="文件信息", related_name="images")
    image = models.ImageField(upload_to="", verbose_name="图片", null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '上传图片'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.upload_file.name