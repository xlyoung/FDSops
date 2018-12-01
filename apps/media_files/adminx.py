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
from .models import UploadMessage


class UploadMessageAdmin(object):
    list_display = ["name", "fds_path", "file_size", "upload_time", "space", "file_desc"]
    search_fields = ['name','fds_path',"space" ]
    list_editable = ["space","file_desc","name" ]
    list_filter = ["name", "fds_path", "file_size", "upload_time", "space"]
    style_fields = {"file_desc": "ueditor"}

    readonly_fields = ["file_size","upload_time","name"]

    #刷新
    refresh_times = (3,5)
    #显示数据详情
    show_detail_fields = ['name']

    #数据导出
    list_export = ('xls','xml','json')
    list_export_fields = ('id','fds_path','upload_time','space','file_size')





xadmin.site.register(UploadMessage, UploadMessageAdmin)




