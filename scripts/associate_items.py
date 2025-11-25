#!/usr/bin/env python
"""
关联物品到储物格的脚本
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 初始化Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from apps.items.models import Storage, Item

def main():
    """主函数"""
    # 获取储物格
    storage = Storage.objects.first()
    print(f"使用储物格: {storage.name}")
    
    # 获取所有物品
    items = Item.objects.all()
    print(f"找到 {items.count()} 个物品")
    
    # 关联每个物品到储物格
    for item in items:
        item.storages.add(storage)
        item.location = storage.name
        item.save()
        print(f"✓ 物品 {item.name} 已关联到储物格 {storage.name}")
    
    print("\n✅ 所有操作完成！")

if __name__ == "__main__":
    main()