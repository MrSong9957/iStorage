# -*- coding: utf-8 -*-
"""物品应用模型"""

from django.db import models
from django.conf import settings
from django.utils import timezone


class Navigation(models.Model):
    """导航模型，用于管理侧边栏的大分类和子标签"""
    # 导航类型：大分类或子标签
    TYPE_CHOICES = [
        ('main', '大分类'),
        ('sub', '子标签'),
    ]
    
    # 导航名称
    name = models.CharField(max_length=50, verbose_name='导航名称')
    
    # 导航类型
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name='导航类型')
    
    # 父级导航（仅子标签有）
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='children', 
        verbose_name='父级导航'
    )
    
    # 导航链接
    url = models.CharField(max_length=200, verbose_name='导航链接')
    
    # 图标
    icon = models.CharField(max_length=20, verbose_name='导航图标')
    
    # 排序顺序
    order = models.PositiveIntegerField(default=0, verbose_name='排序顺序')
    
    # 关联到用户
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='navigations', verbose_name='所属用户')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = '导航'
        verbose_name_plural = '导航'
        ordering = ['order', 'id']
        unique_together = (('user', 'name', 'type', 'parent'),)


class Item(models.Model):
    """物品模型"""
    # 物品编号，从1开始递增的简单数字
    item_code = models.PositiveIntegerField(unique=True, null=False, blank=False, verbose_name='物品编号')
    
    # 物品名称
    name = models.CharField(max_length=200, verbose_name='物品名称')
    
    # 物品图片
    image = models.ImageField(upload_to='item_images/', blank=True, null=True, verbose_name='物品图片')
    
    # 存放位置（房间）
    location = models.CharField(max_length=200, blank=True, verbose_name='存放位置')
    
    # 分类
    category = models.ForeignKey(
        'Category', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='items', 
        verbose_name='分类'
    )
    
    # 存放时间
    storage_time = models.DateTimeField(auto_now_add=True, verbose_name='存放时间')
    
    # 关联到用户
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='items', verbose_name='所属用户')
    
    def save(self, *args, **kwargs):
        # 如果是新建物品且没有指定编号，则生成新的递增编号
        if not self.pk:
            # 获取当前最大编号
            max_code = Item.objects.aggregate(max_code=models.Max('item_code'))['max_code']
            # 如果没有记录，从1开始，否则+1
            self.item_code = 1 if max_code is None else max_code + 1
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = '物品'
        verbose_name_plural = '物品'
        ordering = ['-storage_time']  # 按存放时间倒序排列


class Category(models.Model):
    """最小化的分类模型：与现有的 Item.location 字符串保持兼容。

    设计原则：
    - 最小字段：name 和 user（每用户独立分类）
    - 创建/重命名分类时，会在视图中同步更新 Item.location（如果需要）
    """
    name = models.CharField(max_length=200, verbose_name='分类名称')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='categories', verbose_name='所属用户')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'
        unique_together = (('user', 'name'),)
