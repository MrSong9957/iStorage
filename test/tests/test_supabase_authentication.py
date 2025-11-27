# -*- coding: utf-8 -*-
"""
Supabase认证后端测试
"""

import unittest
from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch, MagicMock
from apps.users.backends.supabase_auth import SupabaseAuthenticationBackend


class SupabaseAuthenticationBackendTestCase(TestCase):
    """
    测试Supabase认证后端功能
    """
    
    def setUp(self):
        """测试前的设置"""
        self.backend = SupabaseAuthenticationBackend()
        self.User = get_user_model()
        
        # 创建测试用户
        self.test_user = self.User.objects.create(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
    
    def tearDown(self):
        """测试后的清理"""
        self.test_user.delete()
    
    @patch('apps.users.backends.supabase_auth.supabase_client')
    def test_authenticate_with_supabase_user_id_existing_user(self, mock_supabase_client):
        """测试使用已存在的Supabase用户ID进行认证"""
        # 设置用户的Supabase ID
        supabase_user_id = 'test_supabase_user_id'
        self.test_user.supabase_user_id = supabase_user_id
        self.test_user.save()
        
        # 模拟请求对象
        request = MagicMock()
        
        # 调用authenticate方法
        user = self.backend.authenticate(request, user_id=supabase_user_id)
        
        # 验证结果
        self.assertIsNotNone(user)
        self.assertEqual(user, self.test_user)
    
    @patch('apps.users.backends.supabase_auth.supabase_client')
    def test_authenticate_with_token(self, mock_supabase_client):
        """测试使用令牌进行认证"""
        # 设置模拟的Supabase用户数据
        supabase_user_id = 'test_supabase_user_id'
        mock_user_data = {
            'id': supabase_user_id,
            'email': 'test@example.com',
            'user_metadata': {
                'full_name': '测试用户'
            }
        }
        
        # 模拟Supabase客户端的auth.get_user方法
        mock_auth = MagicMock()
        mock_auth.get_user.return_value = {'data': {'user': mock_user_data}}
        mock_supabase_client.get_client.return_value.auth = mock_auth
        
        # 设置用户的Supabase ID
        self.test_user.supabase_user_id = supabase_user_id
        self.test_user.save()
        
        # 模拟请求对象
        request = MagicMock()
        
        # 调用authenticate方法
        user = self.backend.authenticate(request, token='test_token')
        
        # 验证结果
        self.assertIsNotNone(user)
        self.assertEqual(user, self.test_user)
        mock_supabase_client.get_client().auth.get_user.assert_called_once_with('test_token')
    
    @patch('apps.users.backends.supabase_auth.supabase_client')
    def test_authenticate_with_token_new_user(self, mock_supabase_client):
        """测试使用令牌为新用户进行认证"""
        # 设置模拟的Supabase用户数据
        supabase_user_id = 'new_supabase_user_id'
        mock_user_data = {
            'id': supabase_user_id,
            'email': 'newuser@example.com',
            'user_metadata': {
                'full_name': '新用户'
            }
        }
        
        # 模拟Supabase客户端的auth.get_user方法
        mock_auth = MagicMock()
        mock_auth.get_user.return_value = {'data': {'user': mock_user_data}}
        mock_supabase_client.get_client.return_value.auth = mock_auth
        
        # 确保没有该Supabase用户ID的本地用户
        self.assertEqual(self.User.objects.filter(supabase_user_id=supabase_user_id).count(), 0)
        
        # 模拟请求对象
        request = MagicMock()
        
        # 调用authenticate方法
        user = self.backend.authenticate(request, token='test_token')
        
        # 验证结果
        self.assertIsNotNone(user)
        self.assertEqual(user.supabase_user_id, supabase_user_id)
        self.assertEqual(user.email, 'newuser@example.com')
        
        # 验证创建了ThirdPartyAuth记录
        from apps.users.models import ThirdPartyAuth
        self.assertEqual(ThirdPartyAuth.objects.filter(
            user=user,
            provider='supabase',
            provider_user_id=supabase_user_id
        ).count(), 1)
    
    def test_get_user(self):
        """测试获取用户"""
        # 使用用户ID获取用户
        user = self.backend.get_user(self.test_user.id)
        
        # 验证结果
        self.assertIsNotNone(user)
        self.assertEqual(user, self.test_user)
    
    def test_get_user_nonexistent(self):
        """测试获取不存在的用户"""
        # 使用不存在的用户ID
        user = self.backend.get_user(999999)
        
        # 验证结果为None
        self.assertIsNone(user)


if __name__ == '__main__':
    unittest.main()
