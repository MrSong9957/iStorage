# -*- coding: utf-8 -*-
"""用户应用模型"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model


class User(AbstractUser):
    """自定义用户模型"""
    # 扩展Django默认的用户模型
    phone = models.CharField('手机号', max_length=11, blank=True, null=True, unique=True)
    department = models.CharField('部门', max_length=100, blank=True, null=True)
    position = models.CharField('职位', max_length=100, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='头像')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    # 第三方登录相关字段
    wechat_openid = models.CharField(max_length=100, blank=True, null=True, verbose_name='微信OpenID', unique=True)
    qq_openid = models.CharField(max_length=100, blank=True, null=True, verbose_name='QQ OpenID', unique=True)
    alipay_userid = models.CharField(max_length=100, blank=True, null=True, verbose_name='支付宝用户ID', unique=True)
    supabase_user_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='Supabase用户ID', unique=True)
    
    # 用于标记是否是第三方登录用户
    is_third_party_user = models.BooleanField(default=False, verbose_name='是否第三方登录用户')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['phone']),
            models.Index(fields=['wechat_openid']),
            models.Index(fields=['qq_openid']),
            models.Index(fields=['alipay_userid']),
        ]

    def __str__(self):
        return self.username


class ThirdPartyAuth(models.Model):
    """第三方认证信息表，用于存储用户的第三方登录详细信息"""
    # 认证提供商类型
    PROVIDER_CHOICES = [
        ('wechat', '微信'),
        ('qq', 'QQ'),
        ('alipay', '支付宝'),
        ('supabase', 'Supabase'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='third_party_auths', verbose_name='关联用户')
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES, verbose_name='认证提供商')
    openid = models.CharField(max_length=100, verbose_name='第三方唯一标识')
    unionid = models.CharField(max_length=100, blank=True, null=True, verbose_name='统一标识（微信）')
    access_token = models.CharField(max_length=255, blank=True, null=True, verbose_name='访问令牌')
    refresh_token = models.CharField(max_length=255, blank=True, null=True, verbose_name='刷新令牌')
    expires_at = models.DateTimeField(blank=True, null=True, verbose_name='令牌过期时间')
    user_info = models.JSONField(default=dict, verbose_name='用户信息')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '第三方认证信息'
        verbose_name_plural = verbose_name
        # 确保每个用户在每个提供商下只有一条记录
        unique_together = ('user', 'provider')
        indexes = [
            models.Index(fields=['provider', 'openid']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.get_provider_display()}"
