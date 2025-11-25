# -*- coding: utf-8 -*-
"""物品应用模型"""

from django.db import models
from django.conf import settings
from django.utils import timezone


class Storage(models.Model):
    """储物格模型"""
    # 储物格编号（前缀+时间戳+随机数）
    storage_code = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name='储物格编号')
    
    # 储物格名称（格式：房间-家具-储物格）
    name = models.CharField(max_length=200, verbose_name='储物格名称')
    
    # 房间信息
    room = models.CharField(max_length=100, verbose_name='房间')
    
    # 家具信息
    furniture = models.CharField(max_length=100, verbose_name='家具')
    
    # 储物格单元信息
    unit = models.CharField(max_length=100, verbose_name='储物格')
    
    # 创建时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    # 关联到用户
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='storages', verbose_name='所属用户')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = '储物格'
        verbose_name_plural = '储物格'
        ordering = ['-created_at']  # 按创建时间倒序排列


class Item(models.Model):
    """物品模型"""
    # 物品编号（前缀+时间戳+随机数）
    item_code = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name='物品编号')
    
    # 物品名称
    name = models.CharField(max_length=200, verbose_name='物品名称')
    
    # 物品描述（文字）
    description = models.TextField(blank=True, null=True, verbose_name='文字描述')
    
    # 物品图片
    image = models.ImageField(upload_to='item_images/', blank=True, null=True, verbose_name='物品图片')
    
    # 物品种类/标签
    CATEGORY_CHOICES = [
        ('electronics', '电子产品'),
        ('clothing', '服装'),
        ('documents', '文件'),
        ('jewelry', '首饰'),
        ('others', '其他'),
    ]
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='others', verbose_name='物品种类')
    
    # 物品价值
    value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='物品价值')
    
    # 存放位置
    location = models.CharField(max_length=200, verbose_name='存放位置')
    
    # 存放时间
    storage_time = models.DateTimeField(auto_now_add=True, verbose_name='存放时间')
    
    # 备注
    notes = models.TextField(blank=True, null=True, verbose_name='备注')
    
    # 关联到用户
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='items', verbose_name='所属用户')
    
    # 多对多关联到储物格（一个物品可以放在多个储物格，一个储物格可以放多个物品）
    storages = models.ManyToManyField(Storage, related_name='items', blank=True, verbose_name='存放的储物格')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = '物品'
        verbose_name_plural = '物品'
        ordering = ['-storage_time']  # 按存放时间倒序排列
