from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser



# Create your models here.

class UserProfile(AbstractUser):
    """
    用户注册
    """
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name="姓名")
    birthday = models.DateField(null=True, blank=True, verbose_name="出生年月")
    gender = models.CharField(max_length=6, choices=(("male", u"男"), ("female", "女")), default="female", verbose_name="性别")
    mobile = models.CharField(null=True, blank=True, max_length=11, verbose_name="电话")
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name="邮箱")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username



class UserToken(models.Model):
    """
    用户md5_token值
    """
    user = models.OneToOneField(to='UserProfile')
    token = models.CharField(max_length=64)
    add_time = models.DateTimeField(auto_now=datetime.now(), verbose_name="添加时间")

class EmailVerifyCode(models.Model):
    """
    邮件验证码
    """
    code = models.CharField(max_length=10, verbose_name="验证码")
    email = models.EmailField(verbose_name="邮箱地址")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "邮件验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code


class ModulePermission(models.Model):
    class Meta:
        # 定义权限，放在用户管理
        permissions = (
            ("image.upload", u"图片管理-上传信息"),
            ("image.list", u"图片管理-列表信息"),
        )