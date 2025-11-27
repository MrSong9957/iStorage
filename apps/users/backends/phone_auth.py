# -*- coding: utf-8 -*-
"""手机号认证后端"""

from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from apps.users.models import User


class PhoneAuthenticationBackend(ModelBackend):
    """手机号认证后端，支持通过手机号和密码登录"""
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        """认证用户，支持手机号登录"""
        try:
            # 尝试通过手机号查找用户
            user = User.objects.get(Q(phone=username))
            # 验证密码
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            # 用户不存在，返回None
            return None
        
    def get_user(self, user_id):
        """根据用户ID获取用户"""
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
