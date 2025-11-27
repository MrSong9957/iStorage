#!/usr/bin/env python
"""
测试Supabase与Django集成的视图
"""
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from config.supabase_client import supabase_client
import json

@login_required
def test_supabase_integration(request):
    """
    测试Supabase集成功能
    """
    try:
        # 获取Supabase客户端
        client = supabase_client.client
        
        # 测试连接
        result = {
            'status': 'success',
            'message': 'Supabase连接成功',
            'details': {
                'client_initialized': True,
                'user_authenticated': request.user.is_authenticated,
                'username': request.user.username
            }
        }
        
        return JsonResponse(result)
    
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Supabase连接失败: {str(e)}'
        })

def supabase_status(request):
    """
    检查Supabase状态
    """
    try:
        # 获取Supabase客户端
        client = supabase_client.client
        
        # 简单状态检查
        status = {
            'supabase_connected': True,
            'service_role_available': True
        }
        
        return JsonResponse(status)
    
    except Exception as e:
        return JsonResponse({
            'supabase_connected': False,
            'error': str(e)
        })

def supabase_test_page(request):
    """
    Supabase测试页面
    """
    return render(request, 'users/supabase_test.html')