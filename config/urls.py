# -*- coding: utf-8 -*-
"""Django项目URL配置"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    # 首页
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    # 首页的别名，用于视图重定向
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    # 支持/index路径访问首页
    path('index', TemplateView.as_view(template_name='index.html'), name='index_alias'),
    # 管理后台
    path('admin/', admin.site.urls),
    
    # 用户应用 - 只保留登录相关功能
    path('users/', include('apps.users.urls')),
    # 物品应用URLs
    path('items/', include('apps.items.urls')),
]

# 静态文件和媒体文件的URL配置
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
