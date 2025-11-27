# -*- coding: utf-8 -*-
"""物品应用模型"""

from django.db import models
from django.conf import settings
from django.utils import timezone


class Room(models.Model):
    """房间模型"""
    # 房间编码，单个大写字母，以A开头，唯一
    room_code = models.CharField(max_length=1, unique=True, null=False, blank=False, verbose_name='房间编码')
    
    # 房间名称，不能为空
    room_name = models.CharField(max_length=50, null=False, blank=False, verbose_name='房间名称')
    
    # 关联到用户
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rooms', verbose_name='所属用户')
    
    def __str__(self):
        return self.room_name
    
    class Meta:
        verbose_name = '房间'
        verbose_name_plural = '房间'
        ordering = ['room_name']


class Furniture(models.Model):
    """家具模型"""
    # 家具编码，正整数，从1开始递增，唯一
    furniture_code = models.PositiveIntegerField(unique=True, null=False, blank=False, verbose_name='家具编码')
    
    # 家具名称，不能为空
    furniture_name = models.CharField(max_length=50, null=False, blank=False, verbose_name='家具名称')
    
    # 关联到用户
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='furnitures', verbose_name='所属用户')
    
    def __str__(self):
        return self.furniture_name
    
    class Meta:
        verbose_name = '家具'
        verbose_name_plural = '家具'
        ordering = ['furniture_name']


class StorageCell(models.Model):
    """储物格模型"""
    # 房间信息，不能为空，外键关联到Room模型
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='storage_cells', verbose_name='房间')
    
    # 家具信息，不能为空，外键关联到Furniture模型
    furniture = models.ForeignKey(Furniture, on_delete=models.CASCADE, related_name='storage_cells', verbose_name='家具')
    
    # 储物格基础编号，正整数，非空，同一房间+同一家具下从1开始递增
    cell_number = models.PositiveIntegerField(null=False, blank=False, verbose_name='储物格基础编号')
    
    # 储物格唯一标识，格式：房间编码+家具编码+3位储物格基础编号
    cell_id = models.CharField(max_length=7, unique=True, null=False, blank=False, verbose_name='储物格唯一标识')
    
    # 二进制二维码，不能为空
    qr_code = models.BinaryField(null=False, blank=False, verbose_name='二维码')
    
    # 关联到用户
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='storage_cells', verbose_name='所属用户')
    
    def save(self, *args, **kwargs):
        # 生成储物格唯一标识：房间编码+家具编码+3位储物格基础编号
        self.cell_id = f"{self.room.room_code}{self.furniture.furniture_code}{self.cell_number:03d}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        # 返回格式：房间 - 家具 - 储物格编号
        return f"{self.room.room_name} - {self.furniture.furniture_name} - {self.cell_id}"
    
    class Meta:
        verbose_name = '储物格'
        verbose_name_plural = '储物格'
        ordering = ['room', 'furniture', 'cell_number']  # 按房间、家具、编号排序
        unique_together = ['room', 'furniture', 'cell_number']  # 确保同一房间+同一家具下的储物格基础编号不重复


class Item(models.Model):
    """物品模型"""
    # 物品编号（前缀+时间戳+随机数）
    item_code = models.CharField(max_length=50, unique=True, null=False, blank=False, verbose_name='物品编号')
    
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
    storage_cells = models.ManyToManyField(StorageCell, related_name='items', blank=True, verbose_name='存放的储物格')
    
    # 二维码base64编码
    qr_code = models.TextField(blank=True, null=True, verbose_name='二维码')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = '物品'
        verbose_name_plural = '物品'
        ordering = ['-storage_time']  # 按存放时间倒序排列
