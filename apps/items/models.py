# -*- coding: utf-8 -*-
"""物品应用模型"""

from django.db import models
from django.conf import settings
from django.utils import timezone


class Room(models.Model):
    """房间模型"""
    # 房间名称，不能为空
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name='房间名称')
    
    # 房间字母标识，用于生成储物格编号
    letter = models.CharField(max_length=1, null=True, blank=True, verbose_name='房间字母标识')
    
    # 关联到用户
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rooms', verbose_name='所属用户')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = '房间'
        verbose_name_plural = '房间'
        unique_together = ['name', 'user']  # 确保每个用户的房间名称唯一
        ordering = ['name']


class Furniture(models.Model):
    """家具模型"""
    # 家具名称，不能为空
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name='家具名称')
    
    # 家具字母标识，用于生成储物格编号
    letter = models.CharField(max_length=1, null=True, blank=True, verbose_name='家具字母标识')
    
    # 关联到用户
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='furnitures', verbose_name='所属用户')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = '家具'
        verbose_name_plural = '家具'
        unique_together = ['name', 'user']  # 确保每个用户的家具名称唯一
        ordering = ['name']


class Storage(models.Model):
    """储物格模型"""
    # 房间信息，不能为空，外键关联到Room模型
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='storages', verbose_name='房间')
    
    # 家具信息，不能为空，外键关联到Furniture模型
    furniture = models.ForeignKey(Furniture, on_delete=models.CASCADE, related_name='storages', verbose_name='家具')
    
    # 储物格编号，不能为空，每个用户内部唯一
    storage_code = models.CharField(max_length=50, null=False, blank=False, verbose_name='储物格编号')
    
    # 二进制二维码，不能为空
    qr_code = models.BinaryField(null=False, blank=False, verbose_name='二维码')
    
    # 关联到用户
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='storages', verbose_name='所属用户')
    
    def save(self, *args, **kwargs):
        # 如果是新建储物格且没有指定编号，则自动生成A1001格式的编号
        if not self.pk and not self.storage_code:
            # 处理房间字母分配
            if not self.room.letter:
                # 获取当前用户的所有房间，按创建时间排序
                user_rooms = Room.objects.filter(user=self.user).order_by('id')
                
                # 收集已使用的字母
                used_letters = [room.letter for room in user_rooms if room.letter]
                
                # 查找下一个可用字母
                next_letter = None
                for i in range(26):
                    letter = chr(ord('A') + i)
                    if letter not in used_letters:
                        next_letter = letter
                        break
                
                # 保存房间字母
                self.room.letter = next_letter
                self.room.save()
            
            # 使用房间字母+家具ID作为前缀
            room_initial = self.room.letter
            furniture_id = self.furniture.id
            
            # 生成前缀，格式：A1
            prefix = f"{room_initial}{furniture_id}"
            
            # 查找该房间+家具组合下的最大编号
            max_storage = Storage.objects.filter(
                user=self.user,
                storage_code__startswith=prefix
            ).order_by('-storage_code').first()
            
            # 生成新编号
            if max_storage:
                # 提取现有编号的数字部分，加1后重新格式化
                current_num = int(max_storage.storage_code[-3:])
                new_number = current_num + 1
            else:
                # 没有现有编号，从001开始
                new_number = 1
            
            # 组合成A1001格式
            self.storage_code = f"{prefix}{new_number:03d}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        # 返回格式：房间 - 家具
        return f"{self.room.name} - {self.furniture.name}"
    
    class Meta:
        verbose_name = '储物格'
        verbose_name_plural = '储物格'
        ordering = ['room', 'furniture', 'storage_code']  # 按房间、家具、编号排序
        unique_together = ['storage_code', 'user']  # 确保每个用户的储物格编号唯一


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
    storages = models.ManyToManyField(Storage, related_name='items', blank=True, verbose_name='存放的储物格')
    
    # 二维码base64编码
    qr_code = models.TextField(blank=True, null=True, verbose_name='二维码')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = '物品'
        verbose_name_plural = '物品'
        ordering = ['-storage_time']  # 按存放时间倒序排列
