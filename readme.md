**django安装**

---
1. 创建django项目

```
# 未创建项目目录
django-admin startproject djangoDemo
# 已创建项目目录
django-admin startproject djangoDemo .
```

2. 启动服务

```
python manage.py runserver
```

3. 创建app

```
python manage.py startapp users
```

4. 将创建的app统一拖放至apps目录进行管理

```
# 在settings.py中进行app配置

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import sys
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
```
- settings.py文件配置介绍
```
# DEBUG：True,开发模式；False,生产模式
DEBUG = True
# 生产模式配置主域名
ALLOWED_HOSTS = []
# APP配置
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.users',
]
# 数据库配置，支持Mysql、Postgresql、Oracle等
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
# 项目语言设置
# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'zh-hans'
# 时区设置
# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Shanghai'
# 模板设置
# 设置不根据APP根目录查找模板文件：'APP_DIRS': False,
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

5. 设置用户models

[相关资料网址](http://www.cnblogs.com/derek1184405959/p/8733194.html)

```
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    """
    用户信息
    """
    GENDER_CHOICES = (
        ("male", "男"),
        ("female", "女")
    )
    # 用户用手机注册，所以姓名，生日和邮箱可以为空
    name = models.CharField("姓名", max_length=30, null=True, blank=True)
    birthday = models.DateField("出生年月", null=True, blank=True)
    gender = models.CharField("性别", max_length=6, choices=GENDER_CHOICES, default="female")
    mobile = models.CharField("电话", max_length=11)
    email = models.EmailField("邮箱", max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class MobileVerifyRecord(models.Model):
    """
    手机验证
    """
    code = models.CharField("验证码", max_length=10)
    mobile = models.CharField("电话", max_length=11)
    add_time = models.DateTimeField("添加时间", default=datetime.now)

    class Meta:
        verbose_name = "短信验证"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code


class EmailVerifyRecord(models.Model):
    """
    邮箱验证
    """
    send_choices = (
        ("register", "注册"),
        ("forget", "找回密码")
    )

    code = models.CharField("验证码", max_length=20)
    email = models.EmailField("邮箱", max_length=50)
    send_type = models.CharField("发送类型", choices=send_choices, max_length=10)
    send_time = models.DateTimeField("发送时间", default=datetime.now)

    class Meta:
        verbose_name = '邮箱验证'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code

```

6. 配置settings.py，重载系统用户

```
#重载系统用户，让UserProfile生效
AUTH_USER_MODEL = 'users.UserProfile'
```


7. 安装配置xadmin

```
# 安装
pip install https://codeload.github.com/sshwsfc/xadmin/zip/django2
# 配置settings.py中的APP
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.users',
    'xadmin',
    'crispy_forms',
    # 'reversion',
]
# 配置urls.py文件
import xadmin
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
]
```

8. 新建users/adminx.py文件，配置xadmin

```
import xadmin
from xadmin import views

from .models import VerifyCode


class BaseSetting(object):
    # 添加主题功能
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    # 全局配置，后台管理标题和页脚
    site_title = "django demo"
    site_footer = "© Copyright 2018 by wangc"
    # 菜单收缩
    # menu_style = "accordion"


class MobileVerifyRecordAdmin(object):
    # 显示的列
    list_display = ['code', 'mobile', "add_time"]
    # 搜索的字段，不要添加时间搜索
    search_fields = ['code', 'mobile']
    # 过滤
    list_filter = ['code', 'mobile', 'add_time']


class EmailVerifyRecordAdmin(object):
    # 显示的列
    list_display = ['code', 'email', "send_type", "send_time"]
    # 搜索的字段，不要添加时间搜索
    search_fields = ['code', 'email', "send_type"]
    # 过滤
    list_filter = ['code', 'email', "send_type", "send_time"]


xadmin.site.register(MobileVerifyRecord, MobileVerifyRecordAdmin)
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
```

9. 修改users/apps.py文件

```
from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'apps.users'
    # app名字后台显示中文
    verbose_name = "用户管理"

```

10. 修改users/__init__.py文件

```
default_app_config = 'users.apps.UsersConfig'
```

11. 创建超级用户

```
# 同步数据库模型
python manage.py makemigrations
python manage.py migrate
# 创建超级用户
python manage.py createsuperuser
```

12. 新建static目录用来存放静态文件

```
# 在settings.py中设置路径
STATICFILES_DIRS = (
    os.path.join(BASE_DIR,'static'),
)
```

13.注册用户models

```
# 修改users/admin.py
from django.contrib import admin

from .models import UserProfile

admin.site.register(UserProfile)
```

14.设置url.py，配置路由

```
# 修改url.py
# from django.contrib import admin
from django.urls import path
from users import views

import xadmin

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    path('index/', views.index),
    path('login/', views.login),
    path('register/', views.register),
    path('logout/', views.logout),
]

```

15.编写view.py伪代码，创建视图框架

```
# 修改users/view.py
from django.shortcuts import render, redirect


def index(request):
    return render(request, 'login/index.html')


def login(request):
    return render(request, 'login/login.html')


def register(request):
    return render(request, 'login/register.html')


def logout(request):
    return redirect('/index/')

```

16.创建HTML文件

> 在templates目录中新建login目录

> 在login目录中新建index.html、login.html、register

17.登录页面原生HTML编写

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>登录</title>
</head>
<body>
    <div style="margin: 15% 40%;">
        <h1>欢迎登录！</h1>
        <form action="/login/" method="post">
            <p>
                <label for="id_username">用户名：</label>
                <input type="text" id="id_username" name="username" placeholder="用户名" autofocus required />
            </p>
            <p>
                <label for="id_password">密码：</label>
                <input type="password" id="id_password" placeholder="密码" name="password" required >
            </p>
            <input type="submit" value="确定">
        </form>
    </div>
</body>
</html>
```

18.下载Bootstrap
- [下载Bootstrap](https://getbootstrap.com/docs/4.1/getting-started/download/)
- [下载JQuery](https://code.jquery.com/jquery-3.3.1.min.map)
- 在项目目录下创建static目录
- 在static目录下创建css、js目录，分别用于存放样式文件和js文件

19.通过Bootstrap美化HTML页面
- 在templates目录中新建base.html，拷贝Bootstrap基本模板
```
<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://cdn.bootcss.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

    <title>Hello, world!</title>
  </head>
  <body>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <a class="navbar-brand" href="#">Navbar</a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
    
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav mr-auto">
          <li class="nav-item active">
            <a class="nav-link" href="#">Home <span class="sr-only">(current)</span></a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#">Link</a>
          </li>
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
              Dropdown
            </a>
            <div class="dropdown-menu" aria-labelledby="navbarDropdown">
              <a class="dropdown-item" href="#">Action</a>
              <a class="dropdown-item" href="#">Another action</a>
              <div class="dropdown-divider"></div>
              <a class="dropdown-item" href="#">Something else here</a>
            </div>
          </li>
          <li class="nav-item">
            <a class="nav-link disabled" href="#">Disabled</a>
          </li>
        </ul>
        <form class="form-inline my-2 my-lg-0">
          <input class="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search">
          <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
        </form>
      </div>
    </nav>
    <h1>Hello, world!</h1>

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://cdn.bootcss.com/jquery/3.2.1/jquery.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://cdn.bootcss.com/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
    <script src="https://cdn.bootcss.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
  </body>
</html>
```




---


> 相关资料

- [Django REST framework+Vue 打造生鲜超市](http://www.cnblogs.com/derek1184405959/p/8733194.html)
- [Django+xadmin打造在线教育平台](http://www.cnblogs.com/derek1184405959/p/8590360.html)
- [Django用户登录与注册系统](http://www.cnblogs.com/derek1184405959/p/8567522.html)