#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: young
@license: Apache Licence
@contact: 114729329
@software: PyCharm
@file: adminx.py
@time: 2018/11/25
"""
import xadmin
from .models import UploadMessage  ,FdsMessage


class FileInfoAdmin(object):
    list_display = ["md5_value", "filename", "filesize", "stype", "add_time", "local_storage_path",
                    "is_delete", "space"]
    search_fields = ['name','stype',"md5_value" ]
    list_editable = ["space", ]
    list_filter = ["md5_value", "filename", "filesize", "stype", "add_time", "local_storage_path",
                    "is_delete", "space"]
    style_fields = {"file_desc": "ueditor"}

    class UploadImagesInline(object):
        model = UploadMessage
        exclude = ["add_time"]
        extra = 1
        style = 'tab'

    inlines = [UploadImagesInline]




xadmin.site.register(UploadMessage, FileInfoAdmin)

#测试上传
from .models import Post

xadmin.site.register(Post)


