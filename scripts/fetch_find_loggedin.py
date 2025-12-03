import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.test import Client

User = get_user_model()
# 创建或更新临时查看用户（仅用于本地渲染，不用于生产）
u, created = User.objects.get_or_create(username='tempviewer', defaults={'email': 'temp@example.com'})
u.set_password('tempPass123')
u.save()

# 使用 Django test client 登录并获取页面
c = Client()
logged = c.login(username='tempviewer', password='tempPass123')
print('logged in:', logged)
resp = c.get('/items/find/')
open('temp_find_items_loggedin.html', 'wb').write(resp.content)
print('wrote temp_find_items_loggedin.html, status_code=', resp.status_code)
