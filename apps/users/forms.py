# -*- coding: utf-8 -*-
"""用户应用表单"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator
from .models import User


class LoginForm(forms.Form):
    """登录表单，支持用户名/邮箱/手机号登录和记住我功能"""
    # 用户名/邮箱/手机号字段
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-input', 'id': 'id_username', 'placeholder': '请输入用户名、邮箱或手机号'})
    )
    
    # 密码字段
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'id': 'id_password', 'placeholder': '请输入密码'})
    )
    
    # 记住我功能
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'id': 'id_remember_me'}))
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
    
    def clean(self):
        """表单验证，支持用户名、邮箱或手机号登录"""
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        
        if username and password:
            # 尝试通过用户名登录
            user = authenticate(self.request, username=username, password=password)
            
            # 如果用户名登录失败，尝试通过邮箱登录
            if user is None:
                try:
                    # 查找邮箱对应的用户
                    user_obj = User.objects.get(email=username)
                    # 使用找到的用户名尝试登录
                    user = authenticate(self.request, username=user_obj.username, password=password)
                except User.DoesNotExist:
                    # 邮箱不存在，尝试通过手机号登录
                    try:
                        # 查找手机号对应的用户
                        user_obj = User.objects.get(phone=username)
                        # 使用找到的用户名尝试登录
                        user = authenticate(self.request, username=user_obj.username, password=password)
                    except User.DoesNotExist:
                        # 手机号不存在，登录失败
                        user = None
            
            if user is None:
                raise forms.ValidationError(
                    '用户名、邮箱或密码错误',
                    code='invalid_login'
                )
            else:
                # 验证用户是否允许登录
                if not user.is_active:
                    raise forms.ValidationError(
                        '该账户已被禁用',
                        code='inactive'
                    )
                
                # 保存用户缓存
                self.user_cache = user
        
        return cleaned_data
    
    def get_user(self):
        """获取登录用户"""
        return getattr(self, 'user_cache', None)


class RegisterForm(UserCreationForm):
    """注册表单"""
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': '请输入邮箱'}))
    phone = forms.CharField(
        required=False,
        max_length=11,
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '请输入有效的手机号')],
        widget=forms.TextInput(attrs={'placeholder': '请输入手机号（可选）'})
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'password1', 'password2')
    
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
            elif field_name == 'phone':
                field.widget.attrs['placeholder'] = '请输入手机号（可选）'


class CustomPasswordResetForm(PasswordResetForm):
    """自定义密码重置表单，支持通过手机号或邮箱重置密码"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 修改email字段的label和placeholder
        self.fields['email'].label = '邮箱或手机号'
        self.fields['email'].widget.attrs.update({
            'placeholder': '请输入邮箱或手机号',
            'class': 'form-input'
        })
    
    def clean_email(self):
        """验证邮箱或手机号"""
        email = self.cleaned_data.get('email')
        
        # 判断是邮箱还是手机号
        import re
        is_phone = re.match(r'^1[3-9]\d{9}$', email)
        
        if is_phone:
            # 手机号格式，查找对应的用户
            users = User.objects.filter(phone=email)
            if not users.exists():
                raise forms.ValidationError('未找到使用该手机号的用户')
            # 使用第一个用户的邮箱作为密码重置的邮箱
            return users.first().email
        else:
            # 邮箱格式，使用默认验证
            try:
                return super().clean_email()
            except forms.ValidationError:
                raise forms.ValidationError('未找到使用该邮箱的用户')
    
    def get_users(self, email_or_phone):
        """获取要重置密码的用户"""
        import re
        is_phone = re.match(r'^1[3-9]\d{9}$', email_or_phone)
        
        if is_phone:
            # 通过手机号查找用户
            return User.objects.filter(phone=email_or_phone, is_active=True)
        else:
            # 通过邮箱查找用户
            return super().get_users(email_or_phone)
