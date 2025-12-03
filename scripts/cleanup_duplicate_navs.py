#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
清理重复的导航项脚本
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from apps.items.models import Navigation
from django.contrib.auth import get_user_model


def cleanup_duplicate_navigations():
    """清理重复的导航项"""
    User = get_user_model()
    users = User.objects.all()
    
    for user in users:
        # 获取用户的所有导航项
        navs = Navigation.objects.filter(user=user)
        seen = set()
        duplicates = []
        
        for nav in navs:
            # 创建一个唯一键，用于检测重复项
            key = (
                nav.name,
                nav.type,
                nav.parent_id,
                nav.url,
                nav.icon
            )
            
            if key in seen:
                duplicates.append(nav.id)
            else:
                seen.add(key)
        
        if duplicates:
            # 删除重复的导航项
            Navigation.objects.filter(id__in=duplicates).delete()
            print(f'清理了用户 {user.username} 的 {len(duplicates)} 个重复导航项')
        else:
            print(f'用户 {user.username} 没有重复的导航项')


if __name__ == '__main__':
    cleanup_duplicate_navigations()
