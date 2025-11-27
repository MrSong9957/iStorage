#!/usr/bin/env python
"""
测试Supabase连接的脚本
"""

import os
import sys
import django
from pathlib import Path

# 设置Django环境
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# 导入Supabase客户端
from config.supabase_client import supabase_client

def test_supabase_connection():
    """测试Supabase连接"""
    try:
        print("测试Supabase连接...")
        
        # 获取客户端
        client = supabase_client.client
        print(f"✓ Supabase客户端初始化成功")
        
        # 测试连接 - 尝试获取项目信息
        try:
            # 这里使用一个简单的健康检查
            # 由于Supabase没有直接的ping方法，我们尝试访问auth模块
            auth_status = client.auth.get_session()
            print(f"✓ Supabase连接测试成功")
            return True
        except Exception as e:
            print(f"✗ Supabase连接测试失败: {str(e)}")
            return False
            
    except Exception as e:
        print(f"✗ Supabase客户端初始化失败: {str(e)}")
        return False

def test_supabase_config():
    """测试Supabase配置"""
    print("\n检查Supabase配置...")
    
    url = os.environ.get('SUPABASE_URL')
    anon_key = os.environ.get('SUPABASE_ANON_KEY')
    service_role_key = os.environ.get('SUPABASE_SERVICE_ROLE_KEY')
    
    if not url:
        print("✗ SUPABASE_URL未配置")
    else:
        print(f"✓ SUPABASE_URL已配置: {url[:30]}...")
    
    if not anon_key:
        print("✗ SUPABASE_ANON_KEY未配置")
    else:
        print(f"✓ SUPABASE_ANON_KEY已配置: {anon_key[:20]}...")
    
    if not service_role_key or service_role_key == "your-service-role-key-here":
        print("✗ SUPABASE_SERVICE_ROLE_KEY未正确配置")
    else:
        print(f"✓ SUPABASE_SERVICE_ROLE_KEY已配置: {service_role_key[:20]}...")
    
    return url and anon_key

if __name__ == "__main__":
    print("Supabase连接测试脚本")
    print("=" * 50)
    
    # 检查配置
    config_ok = test_supabase_config()
    
    if not config_ok:
        print("\n请检查.env文件中的Supabase配置")
        sys.exit(1)
    
    # 测试连接
    connection_ok = test_supabase_connection()
    
    if connection_ok:
        print("\n✓ Supabase连接测试通过")
        sys.exit(0)
    else:
        print("\n✗ Supabase连接测试失败")
        sys.exit(1)