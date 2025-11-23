# -*- coding: utf-8 -*-
"""用户应用模型"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model


class User(AbstractUser):
    """自定义用户模型"""
    # 扩展Django默认的用户模型
    phone = models.CharField('手机号', max_length=11, blank=True, null=True)
    department = models.CharField('部门', max_length=100, blank=True, null=True)
    position = models.CharField('职位', max_length=100, blank=True, null=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
