#!/usr/bin/env python
# encoding: utf-8
"""
@project = djangoDemo
@file = adminx.py
@author = wangc
@create_time =  2018/9/25 22:31
"""

import xadmin
from xadmin import views

from .models import VerifyCode


# 创建xadmin的最基本管理器配置，并与view绑定
class BaseSetting(object):
    # 开启主题功能
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    # 全局配置，后台管理标题和页脚
    site_title = "django demo"
    site_footer = "Copyright 2018 by wangc"
    # 菜单收缩
    # menu_style = "accordion"


class VerifyCodeAdmin(object):
    # 显示的列
    list_display = ['code', 'mobile', "add_time"]
    # 搜索的字段，不要添加时间搜索
    search_fields = ['code', 'mobile']
    # 过滤
    list_filter = ['code', 'mobile', 'add_time']


xadmin.site.register(VerifyCode, VerifyCodeAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
