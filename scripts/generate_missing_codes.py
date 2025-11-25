#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
为所有没有编号的物品生成唯一编号
"""

import os
import sys
import datetime
import random

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 设置Django环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# 导入Django模块
import django
django.setup()

# 导入模型
from apps.items.models import Item

def generate_item_code():
    """
    生成物品编号：前缀+时间戳+随机数
    格式：ITEM-20240520-10086
    """
    prefix = 'ITEM'
    timestamp = datetime.datetime.now().strftime('%Y%m%d')
    random_num = str(random.randint(10000, 99999))
    return f"{prefix}-{timestamp}-{random_num}"

# 为无编号的物品生成编号
def generate_missing_codes():
    print("=== 为无编号物品生成编号 ===")
    
    # 获取所有没有编号的物品
    items_without_code = Item.objects.filter(item_code__isnull=True) | Item.objects.filter(item_code='')
    
    if not items_without_code:
        print("没有需要生成编号的物品")
        return
    
    for item in items_without_code:
        # 生成唯一编号
        item_code = generate_item_code()
        
        # 确保编号唯一
        while Item.objects.filter(item_code=item_code).exists():
            item_code = generate_item_code()
        
        # 更新物品编号
        item.item_code = item_code
        item.save()
        
        print(f"为物品 {item.name} (ID: {item.id}) 生成编号：{item_code}")
    
    print("\n=== 生成完成 ===")

if __name__ == "__main__":
    generate_missing_codes()
