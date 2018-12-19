# -*- coding: utf-8 -*-
from django.db import models

from datetime import datetime

# Create your models here.

# 扫描后资产设备基础信息初表
class HostScanInifo(models.Model):

    SYSTEM_TYPE_CHIOCE = (
        ('0', 'linux'),
        ('1', 'windows'),
    )
    ip = models.CharField(max_length=64,null=False,verbose_name=u"主机IP信息")
    login_port = models.CharField(max_length=32,null=True,verbose_name=u"登录的端口")
    login_user = models.CharField(max_length=32,null=True,verbose_name=u"登录的用户")
    login_passwd = models.CharField(max_length=64,null=True,verbose_name=u"登录的密码",default="")
    login_status = models.IntegerField(verbose_name=u"0-登录失败,1-登录成功",default=0)
    host_type = models.CharField(max_length=256, verbose_name=u"主机系统类型", default="", null=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = u'初始化扫描信息表'
        verbose_name_plural = verbose_name
        db_table = "hosts_scan_inifo"