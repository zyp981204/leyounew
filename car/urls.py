"""
    作者：zyp
    日期：2019/9/23 15:04
"""
from django.urls import re_path,path
from django.conf.urls import url,include
from . import views

urlpatterns = [
    url(r'^get_typecarinfo/$', views.get_typecarinfo, name='get_typecarinfo'),
    url(r'^index/$', views.index, name='index'),
    url(r'^get_index_carinfo/$', views.get_index_carinfo, name='get_index_carinfo'),
    url(r'^info/', views.info_body_left, name='info'),
    url(r'^orderrent/', views.order_rent, name='orderrent'),
    url(r'^orderinfo/', views.order_info, name='orderinfo'),
    url(r'^search_carinfo/', views.search_carinfo, name='search_carinfo'),

]