#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
为现有物品生成二维码并保存到数据库
"""

import os
import sys
import json
import base64
import io
import qrcode

# 设置Django环境
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from apps.items.models import Item

def generate_qr_code(item):
    """
    为物品生成二维码
    :param item: Item对象
    :return: 二维码的base64编码
    """
    # 生成二维码数据
    qr_data = json.dumps({
        'code': item.item_code,
        'name': item.name,
        'category': 'item'
    })
    
    # 创建二维码
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    # 生成二维码图片
    qr_image = qr.make_image(fill_color="black", back_color="white")
    
    # 将图片转换为base64编码
    buffer = io.BytesIO()
    qr_image.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    return qr_base64

def main():
    """
    主函数：为所有物品生成二维码
    """
    print("开始为物品生成二维码...")
    
    # 获取所有物品
    items = Item.objects.all()
    
    for item in items:
        print(f"为物品 '{item.name}' (编号: {item.item_code}) 生成二维码...")
        
        # 生成二维码
        qr_base64 = generate_qr_code(item)
        
        # 保存到数据库
        item.qr_code = qr_base64
        item.save()
        
        print(f"物品 '{item.name}' 的二维码已保存")
    
    print("所有物品的二维码生成完成！")

if __name__ == "__main__":
    main()
