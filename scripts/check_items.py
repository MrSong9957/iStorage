#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
检查数据库中物品的情况，特别是小米钢化杯的编号
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 设置Django环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# 导入Django模块
import django
django.setup()

# 导入模型
from apps.items.models import Item, Storage

# 检查物品情况
print("=== 物品情况检查 ===")
items = Item.objects.all()
for item in items:
    print(f"ID: {item.id}")
    print(f"Name: {item.name}")
    print(f"Code: {item.item_code}")
    print(f"Category: {item.category} ({item.get_category_display()})")
    print(f"Location: {item.location}")
    print("---")

# 检查储物格情况
print("\n=== 储物格情况检查 ===")
storages = Storage.objects.all()
for storage in storages:
    print(f"ID: {storage.id}")
    print(f"Name: {storage.name}")
    print(f"Code: {storage.storage_code}")
    print(f"Room: {storage.room}")
    print(f"Furniture: {storage.furniture}")
    print(f"Unit: {storage.unit}")
    print("---")

# 检查是否有小米钢化杯没有编号
print("\n=== 小米钢化杯编号检查 ===")
xiaomi_cups = Item.objects.filter(name__icontains='小米钢化杯')
for cup in xiaomi_cups:
    if not cup.item_code:
        print(f"小米钢化杯 {cup.id} 没有编号！")
    else:
        print(f"小米钢化杯 {cup.id} 编号：{cup.item_code}")
