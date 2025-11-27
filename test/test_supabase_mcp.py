#!/usr/bin/env python
"""
测试Supabase MCP客户端功能
"""
import os
import sys

# 添加项目根目录到Python路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

try:
    from config.supabase_client import supabase_client
    from supabase import Client
    from dotenv import load_dotenv
    
    # 加载环境变量
    load_dotenv()
    
    print("Supabase MCP客户端功能测试")
    print("=" * 40)
    
    # 测试客户端获取
    print("1. 测试客户端获取...")
    client = supabase_client.client
    if isinstance(client, Client):
        print("✓ 成功获取Supabase客户端")
    else:
        print("✗ 获取Supabase客户端失败")
    
    # 测试服务角色客户端获取
    print("\n2. 测试服务角色客户端获取...")
    service_client = supabase_client.get_service_role_client()
    if isinstance(service_client, Client):
        print("✓ 成功获取Supabase服务角色客户端")
    else:
        print("✗ 获取Supabase服务角色客户端失败")
    
    # 测试简单查询
    print("\n3. 测试简单查询...")
    try:
        # 尝试查询用户表（可能不存在，但可以测试连接）
        response = client.table('auth.users').select('*').limit(1).execute()
        print("✓ 查询执行成功")
        if response.data:
            print(f"  返回数据: {len(response.data)} 条记录")
        else:
            print("  无数据返回（可能是权限问题或表不存在）")
    except Exception as e:
        print(f"✗ 查询失败: {str(e)}")
    
    # 测试认证状态
    print("\n4. 测试认证状态...")
    try:
        auth = client.auth
        print("✓ 认证模块可用")
        
        # 获取当前用户（可能未登录）
        user = auth.get_user()
        if user:
            print(f"✓ 当前用户: {user}")
        else:
            print("  未登录用户")
    except Exception as e:
        print(f"✗ 认证测试失败: {str(e)}")
    
    print("\n✓ Supabase MCP客户端功能测试完成")
    
except Exception as e:
    print(f"错误: {str(e)}")
    import traceback
    traceback.print_exc()