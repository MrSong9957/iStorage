# -*- coding: utf-8 -*-
"""
Supabase登录视图测试
"""

from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model
from unittest.mock import patch, MagicMock
from apps.users import views


class SupabaseViewsTestCase(TestCase):
    """
    测试Supabase登录相关视图功能
    """
    
    def setUp(self):
        """测试前的设置"""
        self.factory = RequestFactory()
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
    
    @patch('apps.users.views.settings')
    def test_supabase_login_without_config(self, mock_settings):
        """测试Supabase登录（缺少配置）"""
        # 设置模拟配置为空
        mock_settings.SUPABASE_URL = ''
        mock_settings.SUPABASE_ANON_KEY = ''
        
        # 创建GET请求
        request = self.factory.get(reverse('users:supabase_login'))
        
        # 调用视图函数
        response = views.supabase_login(request)
        
        # 验证响应
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/third_party_login_callback.html')
    
    @patch('apps.users.views.settings')
    def test_supabase_login_with_config(self, mock_settings):
        """测试Supabase登录（有配置）"""
        # 设置模拟配置
        mock_settings.SUPABASE_URL = 'https://test.supabase.co'
        mock_settings.SUPABASE_ANON_KEY = 'test_anon_key'
        
        # 创建GET请求
        request = self.factory.get(reverse('users:supabase_login'))
        request.build_absolute_uri = MagicMock(return_value='http://testserver/users/supabase/callback/')
        
        # 调用视图函数
        response = views.supabase_login(request)
        
        # 验证响应是重定向
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('https://test.supabase.co/auth/v1/authorize?'))
    
    @patch('apps.users.views.settings')
    @patch('apps.users.views.requests.post')
    @patch('apps.users.views.authenticate')
    @patch('apps.users.views.login')
    def test_supabase_callback_success(self, mock_login, mock_authenticate, mock_post, mock_settings):
        """测试Supabase回调（成功情况）"""
        # 设置模拟配置
        mock_settings.SUPABASE_URL = 'https://test.supabase.co'
        mock_settings.SUPABASE_ANON_KEY = 'test_anon_key'
        
        # 模拟认证函数返回用户
        mock_authenticate.return_value = self.test_user
        
        # 模拟HTTP POST响应
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'access_token': 'test_access_token',
            'refresh_token': 'test_refresh_token',
            'user': {
                'id': 'test_user_id'
            }
        }
        mock_post.return_value = mock_response
        
        # 创建带code参数的GET请求
        request = self.factory.get(reverse('users:supabase_callback'), {'code': 'test_code'})
        request.build_absolute_uri = MagicMock(return_value='http://testserver/users/supabase/callback/')
        request.session = {}
        
        # 调用视图函数
        response = views.supabase_callback(request)
        
        # 验证认证和登录被调用
        mock_authenticate.assert_called_once()
        mock_login.assert_called_once()
        
        # 验证响应是重定向
        self.assertEqual(response.status_code, 302)
    
    @patch('apps.users.views.settings')
    @patch('apps.users.views.requests.post')
    def test_supabase_callback_error_response(self, mock_post, mock_settings):
        """测试Supabase回调（错误响应）"""
        # 设置模拟配置
        mock_settings.SUPABASE_URL = 'https://test.supabase.co'
        mock_settings.SUPABASE_ANON_KEY = 'test_anon_key'
        
        # 模拟HTTP POST响应失败
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_post.return_value = mock_response
        
        # 创建带code参数的GET请求
        request = self.factory.get(reverse('users:supabase_callback'), {'code': 'test_code'})
        request.build_absolute_uri = MagicMock(return_value='http://testserver/users/supabase/callback/')
        request.session = {}
        
        # 调用视图函数
        response = views.supabase_callback(request)
        
        # 验证响应
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/third_party_login_callback.html')
    
    @patch('apps.users.views.settings')
    def test_supabase_callback_with_error(self, mock_settings):
        """测试Supabase回调（带错误参数）"""
        # 创建带error参数的GET请求
        request = self.factory.get(reverse('users:supabase_callback'), {'error': 'access_denied'})
        
        # 调用视图函数
        response = views.supabase_callback(request)
        
        # 验证响应
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/third_party_login_callback.html')
    
    @patch('apps.users.views.settings')
    def test_supabase_callback_without_code(self, mock_settings):
        """测试Supabase回调（缺少code参数）"""
        # 创建不带code参数的GET请求
        request = self.factory.get(reverse('users:supabase_callback'))
        
        # 调用视图函数
        response = views.supabase_callback(request)
        
        # 验证响应
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/third_party_login_callback.html')
    
    @patch('apps.users.views.settings')
    @patch('apps.users.views.requests.post')
    def test_supabase_callback_exception(self, mock_post, mock_settings):
        """测试Supabase回调（异常情况）"""
        # 设置模拟配置
        mock_settings.SUPABASE_URL = 'https://test.supabase.co'
        mock_settings.SUPABASE_ANON_KEY = 'test_anon_key'
        
        # 模拟HTTP POST抛出异常
        mock_post.side_effect = Exception('Test exception')
        
        # 创建带code参数的GET请求
        request = self.factory.get(reverse('users:supabase_callback'), {'code': 'test_code'})
        request.build_absolute_uri = MagicMock(return_value='http://testserver/users/supabase/callback/')
        request.session = {}
        
        # 调用视图函数
        response = views.supabase_callback(request)
        
        # 验证响应
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/third_party_login_callback.html')


if __name__ == '__main__':
    unittest.main()
