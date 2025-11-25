#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
检查数据库中物品的二维码数据
"""

import os
import sys

# 设置Django环境
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from apps.items.models import Item

def main():
    """主函数"""
    print("检查数据库中的物品二维码数据...")
    
    # 获取所有物品
    items = Item.objects.all()
    
    print(f"\n物品总数: {items.count()}")
    print("\n物品详情:")
    print("-" * 60)
    
    # 统计有二维码和无二维码的物品数量
    has_qr_count = 0
    no_qr_count = 0
    
    for item in items:
        has_qr = bool(item.qr_code)
        if has_qr:
            has_qr_count += 1
        else:
            no_qr_count += 1
        
        print(f"名称: {item.name}")
        print(f"编号: {item.item_code}")
        print(f"二维码: {'有' if has_qr else '无'}")
        if has_qr:
            print(f"二维码长度: {len(item.qr_code)} 字符")
        print("-" * 60)
    
    print(f"\n统计结果:")
    print(f"有二维码的物品: {has_qr_count} 个")
    print(f"无二维码的物品: {no_qr_count} 个")
    
    return has_qr_count, no_qr_count

if __name__ == "__main__":
    main()
