# -*- coding: utf-8 -*-
"""Supabase认证后端"""

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.db import IntegrityError
import logging
from config.supabase_client import supabase_client

logger = logging.getLogger(__name__)
User = get_user_model()


class SupabaseAuthenticationBackend(BaseBackend):
    """
    Supabase认证后端，用于处理与Supabase的认证交互
    """
    
    def authenticate(self, request, token=None, user_id=None):
        """
        使用Supabase令牌认证用户
        
        Args:
            request: HTTP请求对象
            token: Supabase认证令牌
            user_id: Supabase用户ID
            
        Returns:
            认证成功返回User对象，失败返回None
        """
        if not token and not user_id:
            return None
            
        try:
            # 如果提供了user_id，尝试查找现有的用户
            if user_id:
                try:
                    user = User.objects.get(supabase_user_id=user_id)
                    return user
                except User.DoesNotExist:
                    # 用户不存在，我们需要从Supabase获取用户信息
                    pass
                    
            # 如果有token，可以使用Supabase客户端验证token并获取用户信息
            if token and supabase_client:
                try:
                    # 验证token并获取用户信息
                    # 注意：这里使用Supabase客户端的auth.get_user方法
                    user_data = supabase_client.auth.get_user(token)
                    
                    if user_data:
                        # 提取用户ID
                        supabase_id = user_data.user.id
                        
                        # 尝试查找现有用户
                        try:
                            user = User.objects.get(supabase_user_id=supabase_id)
                            return user
                        except User.DoesNotExist:
                            # 创建新用户
                            email = user_data.user.email or f"{supabase_id}@supabase.io"
                            username = user_data.user.email.split('@')[0] if user_data.user.email else f"supabase_{supabase_id[:8]}"
                            
                            # 确保用户名唯一
                            base_username = username
                            counter = 1
                            while User.objects.filter(username=username).exists():
                                username = f"{base_username}_{counter}"
                                counter += 1
                                
                            # 创建用户
                            user = User.objects.create(
                                username=username,
                                email=email,
                                supabase_user_id=supabase_id,
                                is_third_party_user=True,
                                is_active=True  # Supabase认证的用户默认为活跃
                            )
                            
                            # 保存第三方认证记录
                            from apps.users.models import ThirdPartyAuth
                            ThirdPartyAuth.objects.create(
                                user=user,
                                provider='supabase',
                                provider_user_id=supabase_id
                            )
                            
                            return user
                except Exception as e:
                    logger.error(f"Supabase认证失败: {str(e)}")
                    return None
                    
        except Exception as e:
            logger.error(f"Supabase认证过程异常: {str(e)}")
            return None
            
        return None
    
    def get_user(self, user_id):
        """
        根据用户ID获取用户
        
        Args:
            user_id: 用户ID
            
        Returns:
            用户存在返回User对象，不存在返回None
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
