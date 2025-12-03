# -*- coding: utf-8 -*-
"""为现有物品分配分类关联"""

from django.core.management.base import BaseCommand
from apps.users.models import User
from apps.items.models import Item, Category


class Command(BaseCommand):
    """为现有物品分配分类关联"""
    help = '为现有物品分配分类关联'

    def handle(self, *args, **options):
        """执行命令"""
        # 获取所有用户
        users = User.objects.all()
        
        for user in users:
            self.stdout.write(f'处理用户: {user.username}')
            
            # 获取用户的分类
            categories = Category.objects.filter(user=user)
            if not categories.exists():
                self.stdout.write(f'  跳过: 用户没有分类')
                continue
            
            # 将分类名称映射到对象
            category_map = {cat.name: cat for cat in categories}
            
            # 获取用户的物品
            items = Item.objects.filter(user=user)
            updated_count = 0
            
            for item in items:
                # 如果物品已经有分类，跳过
                if item.category is not None:
                    continue
                
                # 根据物品名称或其他逻辑分配分类
                # 这里简单地随机分配一个分类
                import random
                category = random.choice(list(categories))
                
                # 使用update方法避免触发save逻辑，因为有些物品的item_code是字符串格式
                try:
                    Item.objects.filter(pk=item.pk).update(category=category)
                    updated_count += 1
                except Exception as e:
                    self.stdout.write(f'  跳过物品 {item.id}: {e}')
            
            if updated_count > 0:
                self.stdout.write(f'  为 {updated_count} 个物品分配了分类关联')
            else:
                self.stdout.write(f'  所有物品已分配分类关联')
        
        self.stdout.write(self.style.SUCCESS('完成'))
