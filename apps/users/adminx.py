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
from xadmin import views
from .models import EmailVerifyCode


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "FDSops"
    site_footer = "fdsops"
    # menu_style = "accordion"


class VerifyCodeAdmin(object):
    list_display = ['code', 'email', "add_time"]

    #设置字段可以直接在列表页修改
    list_editable = ["code","email","add_time" ]


xadmin.site.register(EmailVerifyCode, VerifyCodeAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)