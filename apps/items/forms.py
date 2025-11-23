# -*- coding: utf-8 -*-
"""物品应用表单"""

from django import forms
from .models import Item


class ItemForm(forms.ModelForm):
    """物品录入表单"""
    
    class Meta:
        model = Item
        fields = ['name', 'description', 'image', 'category', 'value', 'location', 'notes']
        labels = {
            'name': '物品名称',
            'description': '文字描述',
            'image': '物品图片',
            'category': '物品种类',
            'value': '物品价值',
            'location': '存放位置',
            'notes': '备注',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'value': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
    
    def clean(self):
        """验证表单数据，确保至少提供图片或文字描述之一"""
        cleaned_data = super().clean()
        description = cleaned_data.get('description')
        image = cleaned_data.get('image')
        
        # 验证描述或图片至少提供一个
        if not description and not image:
            raise forms.ValidationError('请至少提供文字描述或物品图片之一')
        
        return cleaned_data
