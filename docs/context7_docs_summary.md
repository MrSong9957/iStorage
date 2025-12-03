# Context7 文档摘要

本文件汇总了通过Context7获取的项目技术栈相关文档内容。

## Django 4.2.11

### URL配置
- 使用`include()`函数包含应用的URL配置
- `path()`函数用于定义URL模式
- `re_path()`函数用于正则表达式URL

### 中间件
- `CurrentSiteMiddleware`实现示例

### Admin功能
- 变更表单逻辑
- 模型保存方法

### Storage API
- 抽象方法定义

### Messages API
- 消息处理函数

### 项目结构
- 典型的Django项目结构示例

### 翻译功能
- 翻译函数使用

## Supabase Python客户端

### 客户端初始化
```python
from supabase import create_client
import os

url = os.getenv("SUPABASE_URL")
anon_key = os.getenv("SUPABASE_ANON_KEY")
supabase = create_client(url, anon_key)
```

### 用户认证
```python
# 登录
response = supabase.auth.sign_in_with_password({
    "email": "user@example.com",
    "password": "password123"
})

# 注册
response = supabase.auth.sign_up({
    "email": "user@example.com",
    "password": "password123"
})

# 登出
supabase.auth.sign_out()
```

### 存储功能
- `AsyncStorageClient`使用示例

### Realtime功能
- 实时数据监听示例

## Tailwind CSS

- 实用优先的CSS框架
- 通过扫描HTML和JavaScript文件生成样式
- 提供预定义的CSS类，可直接在HTML中组合使用

## python-dotenv

### 核心用法
```python
from dotenv import load_dotenv, dotenv_values
import os

# 加载.env文件中的环境变量
load_dotenv()

# 使用dotenv_values获取配置（不修改环境变量）
config = dotenv_values('.env')
```

### 命令行界面
```bash
# 安装CLI支持
pip install "python-dotenv[cli]"

# 设置环境变量
dotenv set API_KEY "secret_key_123"

# 列出所有环境变量
dotenv list

# 运行命令并加载环境变量
dotenv run -- python manage.py runserver
```

### 变量插值
- 支持在.env文件中使用变量插值
- 可配置是否覆盖现有环境变量