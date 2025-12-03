# -*- coding: utf-8 -*-
"""创建常用分类并为物品分配分类"""

from django.core.management.base import BaseCommand
from apps.users.models import User
from apps.items.models import Item, Category


class Command(BaseCommand):
    """创建常用分类并为物品分配分类"""
    help = '创建常用分类并为物品分配分类'

    def handle(self, *args, **options):
        """执行命令"""
        # 获取所有用户
        users = User.objects.all()
        
        # 常用分类列表
        common_categories = [
            '电子产品', 
            '家居用品', 
            '办公用品', 
            '服装配饰', 
            '书籍资料', 
            '厨房用品', 
            '运动器材', 
            '其他'
        ]
        
        for user in users:
            self.stdout.write(f'处理用户: {user.username}')
            
            # 创建常用分类
            categories_created = []
            for cat_name in common_categories:
                category, created = Category.objects.get_or_create(
                    user=user, 
                    name=cat_name
                )
                if created:
                    categories_created.append(cat_name)
            
            if categories_created:
                self.stdout.write(f'  创建了分类: {", ".join(categories_created)}')
            else:
                self.stdout.write(f'  所有常用分类已存在')
            
            # 获取用户的分类
            user_categories = list(Category.objects.filter(user=user))
            if not user_categories:
                self.stdout.write(f'  警告: 用户 {user.username} 没有分类')
                continue
            
            # 为没有分类的物品分配分类
            items = Item.objects.filter(user=user, location__isnull=True) | \
                   Item.objects.filter(user=user, location='')
            
            if items.exists():
                for item in items:
                    # 随机分配一个分类
                    import random
                    category = random.choice(user_categories)
                    item.location = category.name
                    item.save()
                self.stdout.write(f'  为 {items.count()} 个物品分配了分类')
            else:
                self.stdout.write(f'  所有物品已分配分类')
        
        self.stdout.write(self.style.SUCCESS('完成'))
