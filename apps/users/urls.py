# -*- coding: utf-8 -*-
"""用户应用URL配置"""

from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # 登录视图 - 仅保留这一个URL
    path('login/', views.user_login, name='user_login'),
    path('register/', views.user_register, name='user_register'),
]
