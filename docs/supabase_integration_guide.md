# Supabase集成指南

本指南详细介绍了将Supabase集成到储物管理系统中的步骤和实现细节。

## 1. Supabase项目设置

### 1.1 创建Supabase项目

1. 访问 [Supabase官网](https://supabase.com/) 并注册/登录账号
2. 创建新的项目，设置项目名称和密码
3. 等待项目初始化完成（通常需要几分钟）

### 1.2 获取项目配置

项目初始化完成后，从Supabase控制台获取以下配置信息：

- **Project URL**: 项目的API URL
- **Anon Key**: 用于匿名访问的API密钥
- **Service Role Key**: 用于服务器端操作的API密钥（谨慎保管）

## 2. 环境配置

### 2.1 更新.env文件

在项目根目录的`.env`文件中添加以下配置：

```env
# Supabase配置
SUPABASE_URL="https://your-project.supabase.co"
SUPABASE_ANON_KEY="your-anon-key"
SUPABASE_SERVICE_ROLE_KEY="your-service-role-key"
```

### 2.2 更新依赖

在`requirements.txt`文件中添加Supabase客户端依赖：

```
# Supabase依赖
python-dotenv==1.0.0
supabase==2.7.1
```

## 3. Supabase客户端实现

### 3.1 创建Supabase客户端模块

在`config`目录下创建`supabase_client.py`文件，实现单例模式的Supabase客户端：

```python
# -*- coding: utf-8 -*-
"""
Supabase客户端配置模块
"""

from supabase import create_client, Client
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class SupabaseClient:
    """
    Supabase客户端封装类（单例模式）
    """
    _instance = None
    
    def __new__(cls):
        """实现单例模式"""
        if cls._instance is None:
            cls._instance = super(SupabaseClient, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """初始化Supabase客户端"""
        self.supabase_url = getattr(settings, 'SUPABASE_URL', '')
        self.supabase_anon_key = getattr(settings, 'SUPABASE_ANON_KEY', '')
        self.supabase_service_role_key = getattr(settings, 'SUPABASE_SERVICE_ROLE_KEY', '')
        
        # 验证必要的配置
        if not self.supabase_url or not self.supabase_anon_key:
            logger.warning("Supabase配置不完整，某些功能可能不可用")
            self._client = None
            self._service_role_client = None
        else:
            # 创建普通客户端
            self._client = create_client(self.supabase_url, self.supabase_anon_key)
            
            # 创建服务角色客户端
            if self.supabase_service_role_key:
                self._service_role_client = create_client(
                    self.supabase_url, 
                    self.supabase_service_role_key
                )
            else:
                self._service_role_client = None
                logger.warning("未配置Supabase服务角色密钥，服务端高级功能不可用")
    
    def get_client(self):
        """
        获取普通Supabase客户端
        
        返回:
            Client: Supabase客户端实例，如果配置不完整则返回None
        """
        return self._client
    
    def get_service_role_client(self):
        """
        获取服务角色Supabase客户端（具有更高权限）
        
        返回:
            Client: 服务角色Supabase客户端实例，如果未配置则返回None
        """
        return self._service_role_client


# 创建全局Supabase客户端实例
supabase_client = SupabaseClient()
```

## 4. 数据库配置

### 4.1 修改settings.py

更新`config/settings.py`文件，配置数据库连接：

```python
# Supabase配置
SUPABASE_URL = os.environ.get('SUPABASE_URL', '')
SUPABASE_ANON_KEY = os.environ.get('SUPABASE_ANON_KEY', '')
SUPABASE_SERVICE_ROLE_KEY = os.environ.get('SUPABASE_SERVICE_ROLE_KEY', '')

# 数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 生产环境可使用Supabase PostgreSQL
# 注意：使用前需要安装PostgreSQL驱动
# pip install psycopg2-binary 或者 pip install psycopg2cffi
# SUPABASE_DB_URL = os.environ.get('SUPABASE_DB_URL', '')
# if SUPABASE_DB_URL and not DEBUG:
#     DATABASES['default'] = {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'URL': SUPABASE_DB_URL,
#     }
```

## 5. 用户认证集成

### 5.1 更新用户模型

在`apps/users/models.py`中为`User`模型添加`supabase_user_id`字段：

```python
class User(AbstractUser):
    # 现有字段...
    
    # Supabase认证相关
    supabase_user_id = models.CharField(
        verbose_name='Supabase用户ID',
        max_length=100,
        blank=True,
        null=True,
        unique=True
    )
    
    # ...

class ThirdPartyAuth(models.Model):
    # ...
    
    PROVIDER_CHOICES = (
        ('wechat', '微信'),
        ('qq', 'QQ'),
        ('alipay', '支付宝'),
        ('supabase', 'Supabase'),  # 添加Supabase选项
    )
    
    # ...
```

### 5.2 创建Supabase认证后端

在`apps/users/backends/`目录下创建`supabase_auth.py`文件：

```python
# -*- coding: utf-8 -*-
"""
Supabase认证后端
"""

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.db import IntegrityError
import logging

# 导入Supabase客户端
from config.supabase_client import supabase_client

logger = logging.getLogger(__name__)


class SupabaseAuthenticationBackend(BaseBackend):
    """
    Supabase认证后端类
    """
    
    def authenticate(self, request, token=None, user_id=None):
        """
        认证用户
        
        参数:
            request: 请求对象
            token: Supabase访问令牌
            user_id: Supabase用户ID
            
        返回:
            User: 认证成功的用户对象，失败返回None
        """
        User = get_user_model()
        
        # 如果提供了user_id，直接根据user_id查找用户
        if user_id:
            try:
                user = User.objects.get(supabase_user_id=user_id)
                return user
            except User.DoesNotExist:
                logger.info(f"未找到Supabase用户ID为{user_id}的本地用户")
                return None
        
        # 如果提供了token，验证token并获取用户信息
        if token:
            try:
                # 使用Supabase客户端验证token
                client = supabase_client.get_client()
                if not client:
                    logger.error("Supabase客户端未初始化")
                    return None
                
                # 获取用户信息
                user_data = client.auth.get_user(token)
                if not user_data or 'data' not in user_data or 'user' not in user_data['data']:
                    logger.error("无法从Supabase获取用户信息")
                    return None
                
                supabase_user = user_data['data']['user']
                user_id = supabase_user.get('id')
                email = supabase_user.get('email', '')
                
                # 尝试查找现有用户
                try:
                    user = User.objects.get(supabase_user_id=user_id)
                except User.DoesNotExist:
                    # 如果没有找到用户，尝试通过邮箱查找
                    if email:
                        try:
                            user = User.objects.get(email=email)
                            # 更新用户的Supabase ID
                            user.supabase_user_id = user_id
                            user.save()
                        except User.DoesNotExist:
                            # 创建新用户
                            username = email.split('@')[0] if email else f'supabase_user_{user_id[:8]}'
                            
                            # 确保用户名唯一
                            original_username = username
                            counter = 1
                            while User.objects.filter(username=username).exists():
                                username = f"{original_username}_{counter}"
                                counter += 1
                            
                            user = User.objects.create_user(
                                username=username,
                                email=email,
                                password=None,  # OAuth用户不需要密码
                                supabase_user_id=user_id
                            )
                    else:
                        # 没有邮箱信息，无法创建用户
                        logger.error("Supabase用户信息中没有邮箱")
                        return None
                
                # 记录第三方认证信息
                from apps.users.models import ThirdPartyAuth
                try:
                    ThirdPartyAuth.objects.update_or_create(
                        user=user,
                        provider='supabase',
                        defaults={
                            'provider_user_id': user_id,
                            'access_token': token  # 注意：实际项目中可能需要加密存储
                        }
                    )
                except IntegrityError as e:
                    logger.warning(f"无法更新第三方认证信息: {e}")
                
                return user
                
            except Exception as e:
                logger.error(f"Supabase认证失败: {e}")
                return None
        
        return None
    
    def get_user(self, user_id):
        """
        根据用户ID获取用户
        
        参数:
            user_id: 用户ID
            
        返回:
            User: 用户对象，不存在返回None
        """
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
```

### 5.3 更新认证后端配置

在`settings.py`中添加Supabase认证后端：

```python
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # 默认后端
    'apps.users.backends.phone_backend.PhoneAuthenticationBackend',  # 手机号登录后端
    'apps.users.backends.supabase_auth.SupabaseAuthenticationBackend',  # Supabase认证后端
]
```

### 5.4 添加登录和回调视图

在`apps/users/views.py`中添加Supabase登录和回调视图：

```python
def supabase_login(request):
    """
    Supabase OAuth登录视图
    
    重定向用户到Supabase的授权页面
    """
    # 保存下一个URL
    next_url = request.GET.get('next', '')
    if next_url:
        request.session['next_url'] = next_url
    
    # 获取Supabase配置
    supabase_url = getattr(settings, 'SUPABASE_URL', '')
    supabase_anon_key = getattr(settings, 'SUPABASE_ANON_KEY', '')
    
    if not supabase_url or not supabase_anon_key:
        logger.error("Supabase配置不完整")
        return render(request, 'users/third_party_login_callback.html', {
            'provider': 'Supabase',
            'error': 'Supabase配置不完整，请联系管理员'
        })
    
    # 构建回调URL
    redirect_uri = request.build_absolute_uri(reverse_lazy('users:supabase_callback'))
    
    # 构建Supabase认证URL
    auth_url = f"{supabase_url}/auth/v1/authorize?" + urlencode({
        'client_id': supabase_anon_key.split('.')[0],
        'redirect_uri': redirect_uri,
        'response_type': 'code',
        'state': f"supabase_{int(time.time())}"
    })
    
    return redirect(auth_url)

def supabase_callback(request):
    """
    Supabase OAuth回调处理视图
    
    处理来自Supabase的认证响应
    """
    code = request.GET.get('code')
    error = request.GET.get('error')
    
    if error:
        return render(request, 'users/third_party_login_callback.html', {
            'provider': 'Supabase',
            'error': f'授权失败: {error}'
        })
    
    if not code:
        return render(request, 'users/third_party_login_callback.html', {
            'provider': 'Supabase',
            'error': '未收到授权码，请重试'
        })
    
    try:
        # 获取Supabase配置
        supabase_url = getattr(settings, 'SUPABASE_URL', '')
        supabase_anon_key = getattr(settings, 'SUPABASE_ANON_KEY', '')
        
        # 构建回调URL
        redirect_uri = request.build_absolute_uri(reverse_lazy('users:supabase_callback'))
        
        # 使用授权码获取访问令牌
        token_url = f"{supabase_url}/auth/v1/token"
        response = requests.post(
            token_url,
            data={
                'grant_type': 'authorization_code',
                'client_id': supabase_anon_key.split('.')[0],
                'code': code,
                'redirect_uri': redirect_uri
            }
        )
        
        if response.status_code != 200:
            return render(request, 'users/third_party_login_callback.html', {
                'provider': 'Supabase',
                'error': '获取访问令牌失败'
            })
        
        token_data = response.json()
        access_token = token_data.get('access_token')
        user_id = token_data.get('user', {}).get('id')
        
        if not access_token:
            return render(request, 'users/third_party_login_callback.html', {
                'provider': 'Supabase',
                'error': '未获取到访问令牌'
            })
        
        # 使用Supabase认证后端进行认证
        user = authenticate(request, token=access_token, user_id=user_id)
        
        if user:
            # 登录用户
            login(request, user)
            
            # 设置会话信息
            request.session['supabase_access_token'] = access_token
            if token_data.get('refresh_token'):
                request.session['supabase_refresh_token'] = token_data.get('refresh_token')
            
            # 处理登录后的重定向
            next_url = request.session.pop('next_url', '')
            if next_url:
                return redirect(next_url)
            return redirect('items:deposit_item')
        else:
            return render(request, 'users/third_party_login_callback.html', {
                'provider': 'Supabase',
                'error': '用户认证失败'
            })
            
    except Exception as e:
        logger.error(f"Supabase回调处理异常: {str(e)}")
        return render(request, 'users/third_party_login_callback.html', {
            'provider': 'Supabase',
            'error': f'登录异常: {str(e)}'
        })
```

### 5.5 更新URL配置

在`apps/users/urls.py`中添加Supabase相关URL：

```python
# Supabase登录
path('supabase/login/', views.supabase_login, name='supabase_login'),
path('supabase/callback/', views.supabase_callback, name='supabase_callback'),
```

## 6. 测试用例

### 6.1 Supabase客户端测试

创建`apps/users/tests/test_supabase_client.py`文件：

```python
# 包含Supabase客户端初始化和连接测试
```

### 6.2 认证后端测试

创建`apps/users/tests/test_supabase_authentication.py`文件：

```python
# 包含Supabase认证后端测试
```

### 6.3 视图测试

创建`apps/users/tests/test_supabase_views.py`文件：

```python
# 包含Supabase登录和回调视图测试
```

## 7. 运行测试

运行测试以验证Supabase集成：

```bash
python manage.py test apps.users.tests
```

## 8. 注意事项

1. **安全考虑**：
   - 确保`SUPABASE_SERVICE_ROLE_KEY`只在服务器端使用，不要在前端代码中暴露
   - 令牌应该安全存储，避免明文保存

2. **错误处理**：
   - 生产环境中应完善错误处理和日志记录
   - 考虑添加令牌刷新机制以处理令牌过期问题

3. **数据同步**：
   - 如果使用Supabase数据库，需要考虑与Django模型的同步
   - 可能需要添加数据迁移脚本

4. **性能优化**：
   - 考虑缓存Supabase连接以提高性能
   - 实现连接池管理以避免频繁创建连接

5. **用户体验**：
   - 提供明确的错误提示和加载状态
   - 确保登录流程流畅，减少用户等待时间

---

本集成指南提供了将Supabase与Django储物管理系统集成的完整步骤，包括客户端配置、用户认证和测试方法。根据实际项目需求，可能需要进一步调整和优化。