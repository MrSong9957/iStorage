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
    path('tag_view/', views.tag_view, name='tag_view'),
    path('find/', views.find_items, name='find_items'),  # 查找物品页面
    path('test-find/', views.test_find_items, name='test_find_items'),
    path('detail/<int:item_id>/', views.item_detail, name='item_detail'),  # 物品详情页
    path('delete/<int:item_id>/', views.delete_item, name='delete_item'),  # 删除物品API
    path('update_location/<int:item_id>/', views.update_item_location, name='update_item_location'),  # 更新物品位置API
    path('add_category/', views.add_category, name='add_category'),  # 添加新分类API
    path('add_room/', views.add_room, name='add_room'),  # 添加新房间API
    path('manage/', views.manage_categories, name='manage_categories'),  # 管理分类和房间
    path('manage_nav/', views.manage_navigation, name='manage_navigation'),  # 管理导航项API

]