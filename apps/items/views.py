# -*- coding: utf-8 -*-
"""物品应用视图"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import qrcode
from PIL import Image
import datetime
import random
import base64
import io
import json
from .models import Item

def generate_item_code():
    """
    生成物品编号：前缀+时间戳+随机数
    格式：ITEM-20240520-10086
    """
    prefix = 'ITEM'
    timestamp = datetime.datetime.now().strftime('%Y%m%d')
    random_num = str(random.randint(10000, 99999))
    return f"{prefix}-{timestamp}-{random_num}"

@login_required
def deposit_item(request):
    """
    物品录入视图 - 极简化版本，仅处理物品名称和图片字段的录入（二选一）
    """
    if request.method == 'POST':
        # 简化处理：直接从请求中获取必要字段
        name = request.POST.get('name')
        image = request.FILES.get('image')
        
        # 二选一验证：名称或图片至少有一个不为空
        if not name and not image:
            return redirect('items:deposit')
        
        try:
            # 生成唯一的物品编号
            item_code = generate_item_code()
            
            # 直接创建物品实例
            item = Item(
                item_code=item_code,
                name=name or '未命名物品',
                description='',  # 简化版本，不使用描述
                category='others',  # 默认为其他类别
                value=0.0,  # 简化版本，不使用价值
                location='',  # 简化版本，不使用位置
                notes='',  # 简化版本，不使用备注
                image=image,
                user=request.user
            )
            item.save()
            return redirect('items:deposit')
        except Exception as e:
            return redirect('items:deposit')
    else:
        # GET请求通常不会直接访问这个视图，因为表单在模态窗口中
        # 但如果直接访问，返回items:deposit
        return redirect('items:deposit')

@login_required
def generate_tag(request):
    """
    生成标签数据的API接口
    返回物品信息和二维码的base64编码
    """
    if request.method == 'POST':
        try:
            # 生成新的物品编号
            item_code = generate_item_code()
            name = request.POST.get('name', '未命名物品')
            
            # 生成二维码数据（包含物品编号和名称信息）
            qr_data = json.dumps({
                'item_code': item_code,
                'name': name
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
            
            # 返回JSON响应
            return JsonResponse({
                'success': True,
                'item_code': item_code,
                'name': name,
                'qr_code': qr_base64
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    # 非POST请求返回错误
    return JsonResponse({
        'success': False,
        'error': '只支持POST请求'
    })
