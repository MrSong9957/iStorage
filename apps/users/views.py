# -*- coding: utf-8 -*-
"""用户应用视图"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django import forms
from django.contrib.auth.decorators import login_required

# 导入forms.py中定义的登录表单
from .forms import LoginForm

# 在forms.py中添加记住我功能到LoginForm


# 注册视图函数
def user_register(request):
    """用户注册视图"""
    from .forms import RegisterForm
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # 创建用户
            user = form.save()
            username = form.cleaned_data.get('username')
            
            # 注册成功后跳转到登录页面
            return redirect('users:user_login')
    else:
        form = RegisterForm()
    
    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    """用户登录视图，支持记住我功能"""
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me')
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # 设置会话过期时间，支持记住我功能
                if remember_me:
                    request.session.set_expiry(1209600)  # 2周
                else:
                    request.session.set_expiry(0)  # 浏览器关闭后过期
                return redirect('items:deposit_item')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})
