# -*- coding: utf-8 -*-
"""
Supabase客户端连接测试
"""

import unittest
from django.conf import settings
from config.supabase_client import SupabaseClient, supabase_client


class SupabaseClientTestCase(unittest.TestCase):
    """
    测试Supabase客户端连接和基本功能
    """
    
    def setUp(self):
        """测试前的设置"""
        self.supabase_url = getattr(settings, 'SUPABASE_URL', '')
        self.supabase_anon_key = getattr(settings, 'SUPABASE_ANON_KEY', '')
    
    def test_supabase_client_initialization(self):
        """测试Supabase客户端初始化"""
        # 检查配置是否存在
        self.assertTrue(self.supabase_url, "Supabase URL配置不存在")
        self.assertTrue(self.supabase_anon_key, "Supabase匿名密钥配置不存在")
        
        # 检查全局客户端实例
        self.assertIsNotNone(supabase_client, "全局Supabase客户端实例不存在")
        self.assertIsInstance(supabase_client, SupabaseClient, "全局客户端不是SupabaseClient类型")
    
    def test_singleton_pattern(self):
        """测试单例模式"""
        # 创建新的客户端实例
        client1 = SupabaseClient()
        client2 = SupabaseClient()
        
        # 验证单例模式
        self.assertIs(client1, client2, "SupabaseClient未实现单例模式")
        self.assertIs(client1, supabase_client, "新实例与全局实例不同")
    
    def test_get_client(self):
        """测试获取普通客户端"""
        client = supabase_client.get_client()
        self.assertIsNotNone(client, "无法获取Supabase客户端")
    
    def test_get_service_role_client(self):
        """测试获取服务角色客户端"""
        service_role_key = getattr(settings, 'SUPABASE_SERVICE_ROLE_KEY', '')
        if service_role_key:
            service_client = supabase_client.get_service_role_client()
            self.assertIsNotNone(service_client, "无法获取Supabase服务角色客户端")
    
    def test_connection_validity(self):
        """测试连接有效性（简单验证，不实际连接）"""
        # 这个测试只是验证配置和客户端结构，不进行实际连接
        # 实际连接测试可能需要在集成测试环境中进行
        self.assertTrue(len(self.supabase_url) > 0, "Supabase URL为空")
        self.assertTrue(len(self.supabase_anon_key) > 0, "Supabase匿名密钥为空")


if __name__ == '__main__':
    unittest.main()
