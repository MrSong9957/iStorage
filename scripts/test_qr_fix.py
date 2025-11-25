#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试二维码修复效果
"""

import requests

# 测试查找物品页面
url = 'http://127.0.0.1:8000/items/find/'

print(f"测试访问: {url}")

# 发送请求
response = requests.get(url)

if response.status_code == 200:
    print("✓ 页面访问成功")
    
    # 检查页面内容
    html = response.text
    
    # 检查物品卡片数量
    item_card_count = html.count('item-card')
    print(f"\n找到 {item_card_count} 个物品卡片")
    
    # 检查data-item-qr-code属性
    qr_code_attr_count = html.count('data-item-qr-code')
    print(f"\n找到 {qr_code_attr_count} 个带有二维码数据的物品卡片")
    
    # 检查二维码显示区域
    if 'modalItemQRCode' in html:
        print("✓ 二维码显示区域已存在")
    else:
        print("✗ 二维码显示区域不存在")
        
    # 检查base64二维码显示逻辑
    if 'data:image/png;base64,' in html:
        print("✓ 页面中包含base64二维码显示逻辑")
    else:
        print("✗ 页面中缺少base64二维码显示逻辑")
    
    # 检查是否移除了动态生成二维码的代码
    if 'generateQRCode' not in html:
        print("✓ 已移除动态生成二维码的代码")
    else:
        print("✗ 动态生成二维码的代码仍存在")
        
else:
    print(f"✗ 页面访问失败，状态码: {response.status_code}")

print("\n测试完成")
