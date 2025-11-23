# -*- coding: utf-8 -*-
"""用户应用表单"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate
from .models import User


class LoginForm(AuthenticationForm):
    """登录表单，支持记住我功能"""
    # 记住我功能
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'id': 'id_remember_me'}))
    
    # 使用自定义的User模型
    class Meta:
        model = User
        fields = ('username', 'password', 'remember_me')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 为表单字段添加自定义样式类
        self.fields['username'].widget.attrs.update({'class': 'form-input', 'id': 'id_username', 'placeholder': '请输入用户名'})
        self.fields['password'].widget.attrs.update({'class': 'form-input', 'id': 'id_password', 'placeholder': '请输入密码'})
    
    def clean(self):
        """表单验证"""
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if username and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)
        
        return self.cleaned_data


class RegisterForm(UserCreationForm):
    """注册表单"""
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': '请输入邮箱'}))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 为表单字段添加自定义样式类
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-input'
            # 移除密码帮助文本
            field.help_text = ''
            if field_name == 'password1':
                field.widget.attrs['placeholder'] = '请设置密码'
            elif field_name == 'password2':
                field.widget.attrs['placeholder'] = '请确认密码'
            elif field_name == 'username':
                field.widget.attrs['placeholder'] = '请设置用户名'
