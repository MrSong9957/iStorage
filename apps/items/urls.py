# -*- coding: utf-8 -*-
"""物品应用URL配置"""

from django.urls import path
from . import views
from .views import ItemCreateView

app_name = 'items'
urlpatterns = [
    path('deposit/', views.deposit_item, name='deposit_item'),  # 保留原有的模态框路由
    path('create/', ItemCreateView.as_view(), name='item_create'),  # 新增独立页面路由
    path('success/', views.success, name='success'),  # 成功页面路由
    path('generate_tag/', views.generate_tag, name='generate_tag'),
    path('tag_view/', views.tag_view, name='tag_view'),
]