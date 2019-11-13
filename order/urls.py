"""
    作者：zyp
    日期：2019/9/23 15:03
"""
from django.urls import re_path,path
from django.conf.urls import url,include
from . import views
app_name='order'
urlpatterns = [
    url(r'^user_order/$', views.user_order, name='user_order'),
    url(r'^select/', views.select, name='select'),
    url(r'^insert/', views.insert, name='insert'),
    url(r'^sorder/', views.user_order, name='sorder'),
    url(r'^alipay/', views.alipay, name='alipay'),
]