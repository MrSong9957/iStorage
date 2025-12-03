# -*- coding: utf-8 -*-
"""物品应用表单"""

from django import forms
from .models import Item


class ItemForm(forms.ModelForm):
    """物品录入表单"""
    
    class Meta:
        model = Item
        fields = ['name', 'image', 'location', 'category']
        labels = {
            'name': '物品名称',
            'image': '物品图片',
            'location': '存放位置',
            'category': '分类',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def clean(self):
        """验证表单数据"""
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        
        # 验证物品名称必填
        if not name:
            raise forms.ValidationError('请输入物品名称')
        
        return cleaned_data
