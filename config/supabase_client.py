from supabase import create_client, Client
import os
from django.conf import settings


class SupabaseClient:
    """
    Supabase客户端封装类，用于管理与Supabase的连接和操作
    """
    _instance = None
    _client = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SupabaseClient, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._client is None:
            self._initialize_client()

    def _initialize_client(self):
        """
        初始化Supabase客户端
        """
        url = os.environ.get('SUPABASE_URL') or getattr(settings, 'SUPABASE_URL', '')
        key = os.environ.get('SUPABASE_ANON_KEY') or getattr(settings, 'SUPABASE_ANON_KEY', '')
        
        if not url or not key:
            raise ValueError("Supabase配置未设置，请确保SUPABASE_URL和SUPABASE_ANON_KEY环境变量已配置")
        
        # 确保客户端被正确初始化
        self._client = create_client(url, key)

    def reset_client(self):
        """
        重置Supabase客户端，用于手动触发重连
        """
        self._client = None

    @property
    def client(self) -> Client:
        """
        获取Supabase客户端实例，添加连接状态检查和自动重连机制
        """
        if self._client is None:
            self._initialize_client()
        
        # 检查客户端连接状态，尝试执行一个简单操作来验证连接
        try:
            # 尝试获取会话信息来检查连接状态
            self._client.auth.get_session()
        except Exception as e:
            # 连接失败，重新初始化客户端
            self._client = None
            self._initialize_client()
        
        return self._client

    def get_service_role_client(self) -> Client:
        """
        获取具有服务角色权限的Supabase客户端（用于管理员操作）
        """
        url = os.environ.get('SUPABASE_URL') or getattr(settings, 'SUPABASE_URL', '')
        service_role_key = os.environ.get('SUPABASE_SERVICE_ROLE_KEY') or getattr(settings, 'SUPABASE_SERVICE_ROLE_KEY', '')
        
        if not url or not service_role_key:
            raise ValueError("Supabase服务角色配置未设置，请确保SUPABASE_URL和SUPABASE_SERVICE_ROLE_KEY环境变量已配置")
        
        return create_client(url, service_role_key)


# 创建全局Supabase客户端实例
supabase_client = SupabaseClient()
