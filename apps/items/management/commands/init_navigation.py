# -*- coding: utf-8 -*-
"""
初始化导航数据管理命令
用于向数据库中添加默认的导航菜单和子标签
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.items.models import Navigation

# 获取用户模型
User = get_user_model()


class Command(BaseCommand):
    """初始化导航数据命令"""
    help = '初始化导航数据，添加默认的导航菜单和子标签'
    
    def handle(self, *args, **options):
        """执行命令"""
        self.stdout.write(self.style.SUCCESS('正在初始化导航数据...'))
        
        # 获取所有用户
        users = User.objects.all()
        
        if not users:
            self.stdout.write(self.style.WARNING('没有找到任何用户，将创建一个测试用户并初始化导航数据'))
            
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
                self.stdout.write(self.style.SUCCESS(f'创建了测试用户: {test_user.username}'))
            
            # 初始化测试用户的导航数据
            self.init_navigation_data(test_user)
        else:
            # 为每个用户初始化导航数据
            for user in users:
                self.init_navigation_data(user)
        
        self.stdout.write(self.style.SUCCESS('导航数据初始化完成！'))
    
    def init_navigation_data(self, user):
        """初始化导航数据"""
        
        self.stdout.write(f"正在为用户 {user.username} 初始化导航数据...")
        
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
                self.stdout.write(self.style.SUCCESS(f"创建了主导航: {nav.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"主导航已存在: {nav.name}"))
            
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
                self.stdout.write(self.style.ERROR(f"父级导航 {parent_name} 不存在，无法创建子标签"))
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
                    self.stdout.write(self.style.SUCCESS(f"创建了子标签: {sub_nav.name} (父级: {parent_nav.name})"))
                else:
                    self.stdout.write(self.style.WARNING(f"子标签已存在: {sub_nav.name} (父级: {parent_nav.name})"))
        
        self.stdout.write(f"用户 {user.username} 的导航数据初始化完成！")