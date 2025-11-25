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
    path('find/', views.find_items, name='find_items'),  # 查找物品页面
    path('save_description/<int:item_id>/', views.save_description, name='save_description'),  # 保存物品描述API
    path('delete/<int:item_id>/', views.delete_item, name='delete_item'),  # 删除物品API
    path('update_category/<int:item_id>/', views.update_item_category, name='update_item_category'),  # 更新物品分类API
    path('update_location/<int:item_id>/', views.update_item_location, name='update_item_location'),  # 更新物品位置API
]