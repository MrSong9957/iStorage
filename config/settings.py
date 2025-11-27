# -*- coding: utf-8 -*-
"""Django项目主配置"""

import os
from pathlib import Path
from dotenv import load_dotenv

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent

# 加载环境变量
load_dotenv(BASE_DIR / '.env')

# 密钥配置
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-!@#$%^&*()_+')

# 调试模式
DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'

# 允许的主机
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

# 应用列表
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # 自定义应用
    'apps.users',
    'apps.items',
]

# 使用自定义用户模型
AUTH_USER_MODEL = 'users.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# 数据库配置 - 开发环境使用SQLite，生产环境可选Supabase PostgreSQL
# 注意：生产环境切换到Supabase PostgreSQL需要安装psycopg2-binary或其他PostgreSQL驱动

# 默认使用SQLite数据库
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 生产环境配置Supabase PostgreSQL（需要安装PostgreSQL驱动）
# 可以在部署时取消注释以下代码并配置相应环境变量
# if os.environ.get('SUPABASE_DB_URL') and not DEBUG:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.postgresql_psycopg2',
#             'NAME': os.environ.get('DB_NAME', 'postgres'),
#             'USER': os.environ.get('DB_USER', 'postgres'),
#             'PASSWORD': os.environ.get('DB_PASSWORD', ''),
#             'HOST': os.environ.get('DB_HOST', 'db.supabase.co'),
#             'PORT': os.environ.get('DB_PORT', '5432'),
#         }
#     }

# Supabase配置
SUPABASE_URL = os.environ.get('SUPABASE_URL', '')
SUPABASE_ANON_KEY = os.environ.get('SUPABASE_ANON_KEY', '')
SUPABASE_SERVICE_ROLE_KEY = os.environ.get('SUPABASE_SERVICE_ROLE_KEY', '')

# 密码验证器
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# 国际化
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_TZ = True

# 静态文件配置
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# 媒体文件配置
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# 默认主键字段类型
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 登录URL配置
LOGIN_URL = '/users/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/users/login/'

# 认证后端配置
AUTHENTICATION_BACKENDS = [
    # 默认后端
    'django.contrib.auth.backends.ModelBackend',
    # 自定义认证后端，用于支持手机号登录
    'apps.users.backends.PhoneAuthenticationBackend',
    # Supabase认证后端（暂时注释，因为导入错误）
    # 'apps.users.backends.supabase_auth.SupabaseAuthenticationBackend',
]

# 邮件配置 - 本地测试使用SMTP邮件后端
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # 使用SMTP邮件后端
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'your-email@example.com')
EMAIL_SUBJECT_PREFIX = '[存储管理系统] '

# SMTP服务器配置
# 以下是通用配置，根据您的邮箱服务提供商进行调整
# 示例1：QQ邮箱配置
# EMAIL_HOST = 'smtp.qq.com'
# EMAIL_PORT = 587  # 或465（SSL）
# EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'your-qq-email@qq.com')
# EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'your-qq-email-authorization-code')  # QQ邮箱使用授权码，不是登录密码
# EMAIL_USE_TLS = True  # QQ邮箱使用TLS
# EMAIL_USE_SSL = False  # QQ邮箱不使用SSL

# 示例2：163邮箱配置
# EMAIL_HOST = 'smtp.163.com'
# EMAIL_PORT = 25  # 或465（SSL）
# EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'your-163-email@163.com')
# EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'your-163-email-authorization-code')  # 163邮箱使用授权码
# EMAIL_USE_TLS = True  # 163邮箱使用TLS
# EMAIL_USE_SSL = False  # 163邮箱不使用SSL

# 示例3：Gmail配置
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'your-gmail-email@gmail.com')
# EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'your-gmail-app-password')  # Gmail使用应用密码
# EMAIL_USE_TLS = True
# EMAIL_USE_SSL = False

# 请根据您的邮箱服务提供商取消注释并修改相应的配置
# 建议将敏感信息（如密码）存储在环境变量中，而不是直接写在代码里
# 您可以在项目根目录创建.env文件，添加以下内容：
# DEFAULT_FROM_EMAIL=your-email@example.com
# EMAIL_HOST_USER=your-email@example.com
# EMAIL_HOST_PASSWORD=your-email-password-or-authorization-code

# 密码重置配置
PASSWORD_RESET_TIMEOUT = 86400  # 密码重置链接有效期24小时

# 本地测试推荐配置（使用QQ邮箱示例）
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '274504958@qq.com')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'paognzzmpcnibjdb')
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

# 第三方登录配置
# 微信登录配置
WECHAT_APP_ID = os.environ.get('WECHAT_APP_ID', '')
WECHAT_APP_SECRET = os.environ.get('WECHAT_APP_SECRET', '')
WECHAT_REDIRECT_URI = os.environ.get('WECHAT_REDIRECT_URI', 'http://localhost:8000/users/oauth/wechat/callback/')

# QQ登录配置
QQ_APP_ID = os.environ.get('QQ_APP_ID', '')
QQ_APP_KEY = os.environ.get('QQ_APP_KEY', '')
QQ_REDIRECT_URI = os.environ.get('QQ_REDIRECT_URI', 'http://localhost:8000/users/oauth/qq/callback/')

# 支付宝登录配置
ALIPAY_APP_ID = os.environ.get('ALIPAY_APP_ID', '')
ALIPAY_PRIVATE_KEY = os.environ.get('ALIPAY_PRIVATE_KEY', '')
ALIPAY_PUBLIC_KEY = os.environ.get('ALIPAY_PUBLIC_KEY', '')
ALIPAY_REDIRECT_URI = os.environ.get('ALIPAY_REDIRECT_URI', 'http://localhost:8000/users/oauth/alipay/callback/')
ALIPAY_SANDBOX = os.environ.get('ALIPAY_SANDBOX', 'True').lower() == 'true'  # 是否使用沙箱环境