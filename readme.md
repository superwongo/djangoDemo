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


class VerifyCode(models.Model):
    """
    验证码
    """
    code = models.CharField("验证码", max_length=10)
    mobile = models.CharField("电话", max_length=11)
    add_time = models.DateTimeField("添加时间", default=datetime.now)

    class Meta:
        verbose_name = "短信验证"
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
    menu_style = "accordion"


class VerifyCodeAdmin(object):
    list_display = ['code', 'mobile', "add_time"]


xadmin.site.register(VerifyCode, VerifyCodeAdmin)
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


> 相关资料

- [Django REST framework+Vue 打造生鲜超市](http://www.cnblogs.com/derek1184405959/p/8733194.html)
- [Django+xadmin打造在线教育平台](http://www.cnblogs.com/derek1184405959/p/8590360.html)
- [Django用户登录与注册系统](http://www.cnblogs.com/derek1184405959/p/8567522.html)