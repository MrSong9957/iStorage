# -*- coding: utf-8 -*-
"""物品应用URL配置"""

from django.urls import path
from . import views

app_name = 'items'
urlpatterns = [
    path('deposit/', views.deposit_item, name='deposit_item'),
    path('generate_tag/', views.generate_tag, name='generate_tag'),
]