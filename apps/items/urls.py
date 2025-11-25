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
    path('print_selector/', views.print_selector, name='print_selector'),  # 打印选择器中间页面
    path('deposit_storage/', views.deposit_storage, name='deposit_storage'),  # 储物格录入页面
    path('associate/', views.associate_item_storage, name='associate_item_storage'),
    path('clear_association/', views.clear_association, name='clear_association'),
]