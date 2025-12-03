# 家庭收纳App

![Django](https://img.shields.io/badge/Django-4.2.11-green)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![SQLite](https://img.shields.io/badge/SQLite-3.0%2B-blue)

一个功能完整的家庭收纳应用，支持物品管理、分类管理、存储位置管理等功能，帮助家庭成员轻松管理家庭物品。

## 功能特性

- **物品管理**：添加、编辑、查询、删除物品
- **分类系统**：可编辑分类，便于家庭物品组织和管理
- **存储位置**：精确定位物品的存储位置（如房间、家具等）
- **用户系统**：多用户支持，适合家庭共享使用
- **响应式设计**：适配桌面和移动设备，方便在不同场景下使用
- **简洁美观**：采用类似Apple风格的简洁界面设计，操作直观易用

## 技术栈

- **后端**：Django 4.2.11、Python 3.8+
- **数据库**：SQLite（默认）
- **前端**：HTML/CSS/JavaScript、Tailwind CSS
- **其他工具**：
  - Supabase：用于数据存储和管理
  - Pillow：图像处理
  - python-dotenv：环境变量管理

## 快速开始

### 环境要求

- Python 3.8 或更高版本

### 安装步骤

1. **克隆项目**

   ```bash
   git clone https://github.com/yourusername/storage-management.git
   cd storage-management
   ```

2. **创建虚拟环境**

   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Linux/Mac
   source .venv/bin/activate
   ```

3. **安装依赖**

   ```bash
   pip install -r requirements.txt
   ```

4. **配置环境变量**

   复制环境变量模板文件并根据实际情况修改：

   ```bash
   cp .env.example .env
   # 编辑.env文件，设置数据库连接信息等
   ```

5. **数据库迁移**

   ```bash
   python manage.py migrate
   ```

6. **创建超级用户**

   ```bash
   python manage.py createsuperuser
   ```

7. **运行开发服务器**

   ```bash
   python manage.py runserver
   ```

   访问 http://127.0.0.1:8000/ 查看网站
   访问 http://127.0.0.1:8000/admin/ 进入管理后台

## 目录结构

```
storage/
├── .git/                  # Git 版本控制目录
├── .venv/                 # Python 虚拟环境
├── apps/                  # Django 应用目录
│   ├── items/             # 物品管理应用
│   └── users/             # 用户管理应用
├── config/                # Django配置
│   ├── settings.py        # 统一配置文件
│   ├── urls.py            # URL配置
│   └── wsgi.py            # WSGI配置
├── docs/                  # 项目文档目录
├── media/                 # 媒体文件目录
├── scripts/               # 辅助脚本目录
│   └── get_supabase_service_key.py # 获取Supabase服务密钥脚本
├── static/                # 静态文件目录
├── templates/             # HTML模板目录
├── test/                  # 测试目录
├── .env                   # 环境变量文件
├── .env.example           # 环境变量示例文件
├── db.sqlite3             # SQLite数据库文件
├── manage.py              # Django管理脚本
├── README.md              # 项目说明文档
├── requirements.txt       # Python依赖文件
└── storage.log            # 日志文件
```

## 管理脚本

项目包含以下管理脚本：

- **get_supabase_service_key.py**: 获取Supabase服务密钥

使用方法：

```bash
python scripts/get_supabase_service_key.py
```

## 部署说明

### 生产环境配置

1. 修改 `.env` 文件中的配置：
   - 设置 `DEBUG=False`
   - 设置 `SECRET_KEY` 为强随机值
   - 配置 `ALLOWED_HOSTS` 为实际域名
   - 设置安全相关配置为 `True`

2. 收集静态文件：

   ```bash
   python manage.py collectstatic
   ```

3. 推荐使用 Gunicorn 或 uWSGI 作为WSGI服务器，配合 Nginx 进行部署。

## 安全注意事项

- 生产环境必须设置强随机的 `SECRET_KEY`
- 确保 `DEBUG=False` 在生产环境
- 配置适当的 `ALLOWED_HOSTS`
- 启用 HTTPS
- 定期备份数据库
- 限制管理后台的访问IP

## 开发指南

### 添加新功能

1. 在apps目录下的相应应用中创建新的模型、视图和模板
2. 添加URL路由到相应的 `urls.py`
3. 运行数据库迁移：`python manage.py migrate`
4. 测试功能

### 代码规范

项目遵循PEP 8规范，请确保代码符合规范：

```bash
flake8
```

## 许可证

[MIT License](LICENSE)

## 贡献

欢迎提交问题和Pull Request！

## 联系方式

如有问题，请联系项目维护者。