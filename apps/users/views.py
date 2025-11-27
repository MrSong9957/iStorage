# -*- coding: utf-8 -*-
"""用户应用视图"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView
from django.urls import reverse_lazy
from django.conf import settings
from django.http import HttpResponse, JsonResponse
import requests
import json
import time
import uuid
from urllib.parse import urlencode, parse_qs
from datetime import datetime, timedelta
import logging

# 导入Supabase客户端
from config.supabase_client import supabase_client

logger = logging.getLogger(__name__)

# 导入forms.py中定义的表单
from .forms import LoginForm, CustomPasswordResetForm
from .models import User, ThirdPartyAuth


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
    """用户登录视图，支持用户名/邮箱/手机号登录和记住我功能"""
    if request.user.is_authenticated:
        # 已登录用户直接跳转，使用settings.py中的配置
        return redirect(settings.LOGIN_REDIRECT_URL)
    
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            # 获取登录用户
            user = form.get_user()
            remember_me = form.cleaned_data.get('remember_me')
            
            if user is not None:
                login(request, user)
                # 设置会话过期时间，支持记住我功能
                if remember_me:
                    request.session.set_expiry(1209600)  # 2周
                else:
                    request.session.set_expiry(0)  # 浏览器关闭后过期
                
                # 处理登录后的重定向
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                # 使用settings.py中的配置
                return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = LoginForm()
    
    return render(request, 'users/login.html', {'form': form})


class CustomPasswordResetView(PasswordResetView):
    """自定义密码重置视图，使用自定义的表单"""
    form_class = CustomPasswordResetForm
    template_name = 'users/password_reset_form.html'
    email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')


def _handle_third_party_login(request, provider, user_info):
    """处理第三方登录的通用函数
    
    Args:
        request: HTTP请求对象
        provider: 第三方登录提供商
        user_info: 第三方返回的用户信息
    
    Returns:
        User: 登录的用户对象
    """
    openid = user_info.get('openid') or user_info.get('userid')
    
    # 查找是否已有对应的第三方认证记录
    try:
        third_party_auth = ThirdPartyAuth.objects.get(provider=provider, openid=openid)
        user = third_party_auth.user
        # 更新用户信息
        third_party_auth.user_info = user_info
        third_party_auth.save()
    except ThirdPartyAuth.DoesNotExist:
        # 创建新用户
        username = f"{provider}_{openid[:8]}_{uuid.uuid4().hex[:8]}"
        nickname = user_info.get('nickname', '') or user_info.get('name', '') or username
        
        # 创建新用户
        user = User.objects.create_user(
            username=username,
            email=f"{username}@thirdparty.com",
            password=User.objects.make_random_password(length=16),
            is_third_party_user=True
        )
        
        # 设置第三方ID
        if provider == 'wechat':
            user.wechat_openid = openid
        elif provider == 'qq':
            user.qq_openid = openid
        elif provider == 'alipay':
            user.alipay_userid = openid
        
        # 设置昵称和头像
        if nickname:
            user.first_name = nickname[:30]  # Django用户名限制30字符
        if user_info.get('avatar', ''):
            # 这里简化处理，实际项目中可能需要下载并保存头像
            pass
        
        user.save()
        
        # 创建第三方认证记录
        ThirdPartyAuth.objects.create(
            user=user,
            provider=provider,
            openid=openid,
            user_info=user_info
        )
    
    return user

def wechat_login(request):
    """微信OAuth2登录授权视图"""
    # 保存下一个URL
    next_url = request.GET.get('next', '')
    if next_url:
        request.session['next_url'] = next_url
    
    # 微信授权URL
    wechat_appid = getattr(settings, 'WECHAT_APPID', '')
    wechat_redirect_uri = request.build_absolute_uri(reverse_lazy('users:wechat_callback'))
    
    auth_url = 'https://open.weixin.qq.com/connect/qrconnect?' + urlencode({
        'appid': wechat_appid,
        'redirect_uri': wechat_redirect_uri,
        'response_type': 'code',
        'scope': 'snsapi_login',
        'state': f"wechat_{int(time.time())}"
    }) + '#wechat_redirect'
    
    return redirect(auth_url)

def wechat_callback(request):
    """微信登录回调处理视图"""
    code = request.GET.get('code')
    state = request.GET.get('state')
    
    if not code:
        return render(request, 'users/third_party_login_callback.html', {
            'provider': '微信',
            'error': '授权失败，请重试'
        })
    
    try:
        # 获取access_token
        wechat_appid = getattr(settings, 'WECHAT_APPID', '')
        wechat_secret = getattr(settings, 'WECHAT_SECRET', '')
        
        token_url = 'https://api.weixin.qq.com/sns/oauth2/access_token'
        token_params = {
            'appid': wechat_appid,
            'secret': wechat_secret,
            'code': code,
            'grant_type': 'authorization_code'
        }
        
        response = requests.get(token_url, params=token_params)
        token_data = response.json()
        
        if 'errcode' in token_data:
            return render(request, 'users/third_party_login_callback.html', {
                'provider': '微信',
                'error': f'获取token失败: {token_data.get("errmsg")}'
            })
        
        # 获取用户信息
        user_info_url = 'https://api.weixin.qq.com/sns/userinfo'
        user_info_params = {
            'access_token': token_data.get('access_token'),
            'openid': token_data.get('openid'),
            'lang': 'zh_CN'
        }
        
        user_info_response = requests.get(user_info_url, params=user_info_params)
        user_info = user_info_response.json()
        
        if 'errcode' in user_info:
            return render(request, 'users/third_party_login_callback.html', {
                'provider': '微信',
                'error': f'获取用户信息失败: {user_info.get("errmsg")}'
            })
        
        # 处理登录
        user = _handle_third_party_login(request, 'wechat', user_info)
        
        # 登录用户
        login(request, user)
        
        # 跳转
        next_url = request.session.pop('next_url', '')
        if next_url:
            return redirect(next_url)
        return redirect('items:deposit_item')
        
    except Exception as e:
        return render(request, 'users/third_party_login_callback.html', {
            'provider': '微信',
            'error': f'登录异常: {str(e)}'
        })

def qq_login(request):
    """QQ OAuth2登录授权视图"""
    # 保存下一个URL
    next_url = request.GET.get('next', '')
    if next_url:
        request.session['next_url'] = next_url
    
    # QQ授权URL
    qq_appid = getattr(settings, 'QQ_APPID', '')
    qq_redirect_uri = request.build_absolute_uri(reverse_lazy('users:qq_callback'))
    
    auth_url = 'https://graph.qq.com/oauth2.0/authorize?' + urlencode({
        'response_type': 'code',
        'client_id': qq_appid,
        'redirect_uri': qq_redirect_uri,
        'state': f"qq_{int(time.time())}"
    })
    
    return redirect(auth_url)

def qq_callback(request):
    """QQ登录回调处理视图"""
    code = request.GET.get('code')
    state = request.GET.get('state')
    
    if not code:
        return render(request, 'users/third_party_login_callback.html', {
            'provider': 'QQ',
            'error': '授权失败，请重试'
        })
    
    try:
        # 获取access_token
        qq_appid = getattr(settings, 'QQ_APPID', '')
        qq_appkey = getattr(settings, 'QQ_APPKEY', '')
        qq_redirect_uri = request.build_absolute_uri(reverse_lazy('users:qq_callback'))
        
        token_url = 'https://graph.qq.com/oauth2.0/token'
        token_params = {
            'grant_type': 'authorization_code',
            'client_id': qq_appid,
            'client_secret': qq_appkey,
            'code': code,
            'redirect_uri': qq_redirect_uri
        }
        
        response = requests.get(token_url, params=token_params)
        token_data = parse_qs(response.text)
        access_token = token_data.get('access_token', [None])[0]
        
        if not access_token:
            return render(request, 'users/third_party_login_callback.html', {
                'provider': 'QQ',
                'error': '获取token失败'
            })
        
        # 获取openid
        openid_url = 'https://graph.qq.com/oauth2.0/me'
        openid_params = {'access_token': access_token}
        
        openid_response = requests.get(openid_url, params=openid_params)
        # 解析回调函数形式的响应
        callback_data = openid_response.text
        if callback_data.startswith('callback('):
            callback_data = callback_data[9:-3]  # 去除 callback( 和 )
        
        openid_data = json.loads(callback_data)
        openid = openid_data.get('openid')
        
        # 获取用户信息
        user_info_url = 'https://graph.qq.com/user/get_user_info'
        user_info_params = {
            'access_token': access_token,
            'oauth_consumer_key': qq_appid,
            'openid': openid
        }
        
        user_info_response = requests.get(user_info_url, params=user_info_params)
        user_info = user_info_response.json()
        user_info['openid'] = openid
        
        if user_info.get('ret') != 0:
            return render(request, 'users/third_party_login_callback.html', {
                'provider': 'QQ',
                'error': f'获取用户信息失败: {user_info.get("msg")}'
            })
        
        # 处理登录
        user = _handle_third_party_login(request, 'qq', user_info)
        
        # 登录用户
        login(request, user)
        
        # 跳转
        next_url = request.session.pop('next_url', '')
        if next_url:
            return redirect(next_url)
        return redirect('items:deposit_item')
        
    except Exception as e:
        return render(request, 'users/third_party_login_callback.html', {
            'provider': 'QQ',
            'error': f'登录异常: {str(e)}'
        })

def alipay_login(request):
    """支付宝OAuth2登录授权视图"""
    # 保存下一个URL
    next_url = request.GET.get('next', '')
    if next_url:
        request.session['next_url'] = next_url
    
    # 支付宝授权URL
    alipay_appid = getattr(settings, 'ALIPAY_APPID', '')
    alipay_redirect_uri = request.build_absolute_uri(reverse_lazy('users:alipay_callback'))
    
    auth_url = 'https://openauth.alipay.com/oauth2/publicAppAuthorize.htm?' + urlencode({
        'app_id': alipay_appid,
        'scope': 'auth_user',
        'redirect_uri': alipay_redirect_uri,
        'state': f"alipay_{int(time.time())}"
    })
    
    return redirect(auth_url)

def alipay_callback(request):
    """支付宝登录回调处理视图"""
    code = request.GET.get('auth_code')
    state = request.GET.get('state')
    
    if not code:
        return render(request, 'users/third_party_login_callback.html', {
            'provider': '支付宝',
            'error': '授权失败，请重试'
        })
    
    try:
        # 获取access_token和用户信息
        alipay_appid = getattr(settings, 'ALIPAY_APPID', '')
        alipay_private_key = getattr(settings, 'ALIPAY_PRIVATE_KEY', '')
        
        # 构建请求参数
        biz_content = json.dumps({
            'grant_type': 'authorization_code',
            'code': code
        })
        
        # 简化处理，实际项目中需要按照支付宝SDK要求进行签名
        # 这里模拟成功获取用户信息
        user_info = {
            'userid': f'alipay_user_{int(time.time())}',
            'nickname': '支付宝用户',
            'code': code
        }
        
        # 处理登录
        user = _handle_third_party_login(request, 'alipay', user_info)
        
        # 登录用户
        login(request, user)
        
        # 跳转
        next_url = request.session.pop('next_url', '')
        if next_url:
            return redirect(next_url)
        return redirect('items:deposit_item')
        
    except Exception as e:
        return render(request, 'users/third_party_login_callback.html', {
            'provider': '支付宝',
            'error': f'登录异常: {str(e)}'
        })

def third_party_redirect(request):
    """第三方登录重定向页面"""
    provider = request.GET.get('provider', '')
    return render(request, 'users/third_party_login_redirect.html', {'provider': provider})

def third_party_callback(request, provider):
    """第三方登录回调处理页面"""
    error = request.GET.get('error', '')
    return render(request, 'users/third_party_login_callback.html', {
        'provider': provider,
        'error': error
    })


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
    # 注意：实际项目中可能需要根据Supabase的OAuth流程调整URL格式
    auth_url = f"{supabase_url}/auth/v1/authorize?" + urlencode({
        'client_id': supabase_anon_key.split('.')[0],  # 使用anon key的第一部分作为client_id
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
        # 注意：这里使用Supabase Auth API直接交换令牌
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


def user_logout(request):
    """用户登出视图"""
    from django.contrib.auth import logout
    logout(request)
    return redirect('users:user_login')
