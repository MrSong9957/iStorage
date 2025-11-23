# -*- coding: utf-8 -*-
"""Django项目WSGI配置"""

import os
from django.core.wsgi import get_wsgi_application

# 设置Django配置模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.config.settings.dev')

# 获取WSGI应用
application = get_wsgi_application()
