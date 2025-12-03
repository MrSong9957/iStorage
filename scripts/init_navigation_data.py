#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
初始化导航数据脚本
用于向数据库中添加默认的导航菜单和子标签
"""

import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.items.models import Navigation

# 获取用户模型
User = get_user_model()


def init_navigation_data(user):
    """初始化导航数据"""
    
    print(f"正在为用户 {user.username} 初始化导航数据...")
    
    # 创建默认的主导航
    main_navs = [
        {'name': '按房间找', 'type': 'main', 'url': '/items/find/?filter=room', 'icon': '🔍', 'order': 1},
        {'name': '按分类找', 'type': 'main', 'url': '/items/find/?filter=category', 'icon': '📦', 'order': 2},
        {'name': '管理分类', 'type': 'main', 'url': '/items/manage/', 'icon': '⚙️', 'order': 3},
    ]
    
    # 存储创建的主导航对象，用于后续创建子标签
    main_nav_objects = {}
    
    # 创建主导航
    for nav_data in main_navs:
        nav, created = Navigation.objects.get_or_create(
            user=user,
            name=nav_data['name'],
            type=nav_data['type'],
            defaults={
                'url': nav_data['url'],
                'icon': nav_data['icon'],
                'order': nav_data['order'],
            }
        )
        
        if created:
            print(f"创建了主导航: {nav.name}")
        else:
            print(f"主导航已存在: {nav.name}")
        
        # 保存到字典中，用于后续创建子标签
        main_nav_objects[nav.name] = nav
    
    # 创建子标签数据
    sub_navs = [
        {
            'parent_name': '管理分类',
            'sub_navs': [
                {'name': '分类管理', 'url': '/items/manage/?sub_tag=分类管理', 'icon': '📋', 'order': 1},
                {'name': '房间管理', 'url': '/items/manage/?sub_tag=房间管理', 'icon': '🏠', 'order': 2},
            ]
        }
    ]
    
    # 创建子标签
    for sub_nav_data in sub_navs:
        parent_name = sub_nav_data['parent_name']
        parent_nav = main_nav_objects.get(parent_name)
        
        if not parent_nav:
            print(f"警告：父级导航 {parent_name} 不存在，无法创建子标签")
            continue
        
        for sub_nav_item in sub_nav_data['sub_navs']:
            sub_nav, created = Navigation.objects.get_or_create(
                user=user,
                name=sub_nav_item['name'],
                type='sub',
                parent=parent_nav,
                defaults={
                    'url': sub_nav_item['url'],
                    'icon': sub_nav_item['icon'],
                    'order': sub_nav_item['order'],
                }
            )
            
            if created:
                print(f"创建了子标签: {sub_nav.name} (父级: {parent_nav.name})")
            else:
                print(f"子标签已存在: {sub_nav.name} (父级: {parent_nav.name})")
    
    print(f"用户 {user.username} 的导航数据初始化完成！")


if __name__ == '__main__':
    # 获取所有用户
    users = User.objects.all()
    
    if not users:
        print("没有找到任何用户，将创建一个测试用户并初始化导航数据")
        
        # 创建测试用户
        test_user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'test@example.com',
            }
        )
        
        if created:
            test_user.set_password('testpassword')
            test_user.save()
            print(f"创建了测试用户: {test_user.username}")
        
        # 初始化测试用户的导航数据
        init_navigation_data(test_user)
    else:
        # 为每个用户初始化导航数据
        for user in users:
            init_navigation_data(user)
    
    print("\n导航数据初始化脚本执行完成！")