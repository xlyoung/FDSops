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
from .models import ImagesMessage
from .models import FileMessage


class UploadImageMessageAdmin(object):
    # 设置列表显示字段
    list_display = ["id","name", "file", "creat_time", "space", "file_desc","user"]
    # 设置列表查询字段
    search_fields = ['id','name','file',"space","user" ]
    #设置字段可以直接在列表页修改
    list_editable = ["space","file_desc","name" ]
    # 设置列表过滤字段
    list_filter = ["id","name", "file", "creat_time", "space","user"]

    style_fields = {"file_desc": "ueditor"}

    #刷新
    refresh_times = (3,5)
    #显示数据详情
    show_detail_fields = ['name']

    #数据导出
    list_export = ('xls','xml','json')
    list_export_fields = ('id','file','creat_time','space')

    #只读字段
    readonly_fields = ['creat_time','name']


class UploadFileMessageAdmin(object):
    # 设置列表显示字段
    list_display = ["id","name", "file", "creat_time", "space", "file_desc","user"]
    # 设置列表查询字段
    search_fields = ['id','name','file',"space","user" ]
    #设置字段可以直接在列表页修改
    list_editable = ["space","file_desc","name" ]
    # 设置列表过滤字段
    list_filter = ["id","name", "file", "creat_time", "space","user"]

    style_fields = {"file_desc": "ueditor"}

    #刷新
    refresh_times = (3,5)
    #显示数据详情
    show_detail_fields = ['name']

    #数据导出
    list_export = ('xls','xml','json')
    list_export_fields = ('id','file','creat_time','space')

    #只读字段
    readonly_fields = ['creat_time','name']










xadmin.site.register(ImagesMessage, UploadImageMessageAdmin)
xadmin.site.register(FileMessage, UploadFileMessageAdmin)



