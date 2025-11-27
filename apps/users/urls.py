# -*- coding: utf-8 -*-
"""用户应用URL配置"""

from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from . import views

app_name = 'users'

urlpatterns = [
    # 登录视图 - 仅保留这一个URL
    path('login/', views.user_login, name='user_login'),
    path('register/', views.user_register, name='user_register'),
    
    # 密码重置相关URL
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset_form.html', email_template_name='users/password_reset_email.html', success_url='/users/password_reset/done/'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html', success_url='/users/reset/done/'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
    
    # 第三方登录相关URL
    # 微信登录
    path('wechat/login/', views.wechat_login, name='wechat_login'),
    path('wechat/callback/', views.wechat_callback, name='wechat_callback'),
    
    # QQ登录
    path('qq/login/', views.qq_login, name='qq_login'),
    path('qq/callback/', views.qq_callback, name='qq_callback'),
    
    # 支付宝登录
    path('alipay/login/', views.alipay_login, name='alipay_login'),
    path('alipay/callback/', views.alipay_callback, name='alipay_callback'),
    
    # Supabase登录
    path('supabase/login/', views.supabase_login, name='supabase_login'),
    path('supabase/callback/', views.supabase_callback, name='supabase_callback'),
    
    # 第三方登录重定向页面
    path('third_party/redirect/', views.third_party_redirect, name='third_party_redirect'),
    
    # 第三方登录回调处理页面
    path('third_party/callback/<str:provider>/', views.third_party_callback, name='third_party_callback'),
    
    # 登出视图
    path('logout/', views.user_logout, name='user_logout'),
    

]
