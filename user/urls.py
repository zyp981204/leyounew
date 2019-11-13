"""
    作者：zyp
    日期：2019/9/23 15:03
"""
from django.urls import re_path,path
from django.conf.urls import url,include
from . import views

urlpatterns = [
    url(r'^get_uorder/$', views.get_uorder, name='get_uorder'),
    url(r'^uinfo/(?P<id>\w*)$', views.get_uinfo, name='userinfo'),
    url(r'^update_uinfo/$', views.update_uinfo, name='update_uinfo'),
    url(r'^get_user/', views.get_user, name='get_user'),
    url(r'^update_upwd/', views.update_upwd, name='update_upwd'),
    # 手机密码登录
    url(r'^login/', views.login, name='login'),
    # 注册
    url(r'^add_user/', views.add_user, name='add_user'),
    # 手机动态码登录
    url(r'^login_code/', views.login_code, name='login_code'),
    # 获取验证码
    url(r'^get_code/', views.get_code, name='get_code'),
    # 忘记密码
    url(r'^forget_pwd/', views.forget_pwd, name='forget_pwd'),
    # 支付
    url(r'^alipay/', views.alipay, name='alipay'),
]
# python manage.py makemigrations
# 运行以为这些更改创建迁移
# python manage.py migrate
# 运行以将这些更改应用于数据库