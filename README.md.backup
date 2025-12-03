# 家庭收纳App

![Django](https://img.shields.io/badge/Django-4.2-green)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![SQLite](https://img.shields.io/badge/SQLite-3.0%2B-blue)

一个功能完整的家庭收纳应用，支持物品管理、分类管理、存储位置管理和标签打印等功能，帮助家庭成员轻松管理家庭物品。

## 功能特性

- **物品管理**：添加、编辑、查询、删除和移动物品
- **分类系统**：多级分类结构，便于家庭物品组织和管理
- **存储位置**：精确定位物品的存储位置（如衣柜、抽屉、储物柜等）
- **标签管理**：自定义标签模板，支持条形码和二维码生成
- **用户系统**：多用户支持，适合家庭共享使用
- **数据统计**：物品数量、分类统计等数据分析功能
- **响应式设计**：适配桌面和移动设备，方便在不同场景下使用
- **简洁美观**：采用类似Apple风格的简洁界面设计，操作直观易用

## 技术栈

- **后端**：Django 4.2、Python 3.8+
- **数据库**：SQLite（默认），也支持MySQL 5.7+
- **前端**：Tailwind CSS、Font Awesome
- **其他工具**：
  - python-barcode/qrcode：条形码和二维码生成
  - Pillow：图像处理
  - whitenoise：静态文件部署

> **注意：这是一个家庭收纳应用，不是仓库管理系统。设计初衷是帮助普通家庭更好地管理和查找家庭物品，界面简洁直观，操作简单易用。**

## 快速开始

### 环境要求

- Python 3.8 或更高版本
- MySQL 5.7 或更高版本
- Redis（可选，用于缓存和任务队列）

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

5. **数据库配置**

   确保MySQL已安装并运行，创建数据库：

   ```sql
   CREATE DATABASE storage_db DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

6. **数据库迁移**

   项目使用了apps目录下的应用，数据库迁移命令保持不变：

   ```bash
   python manage.py migrate
   ```

7. **创建超级用户**

   ```bash
   python manage.py createsuperuser
   ```

8. **收集静态文件**

   ```bash
   python manage.py collectstatic
   ```

9. **运行开发服务器**

   ```bash
   python manage.py runserver
   ```

   访问 http://127.0.0.1:8000/ 查看网站
   访问 http://127.0.0.1:8000/admin/ 进入管理后台

   > 注意：项目使用统一的settings.py配置文件，无需指定DJANGO_SETTINGS_MODULE环境变量

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

5. **数据库配置**

   确保MySQL已安装并运行，创建数据库：

   ```sql
   CREATE DATABASE storage_db DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

6. **数据库迁移**

   ```bash
   python manage.py migrate
   ```

7. **创建超级用户**

   ```bash
   python manage.py createsuperuser
   ```

8. **收集静态文件**

   ```bash
   python manage.py collectstatic
   ```

9. **运行开发服务器**

   ```bash
   python manage.py runserver
   ```

   访问 http://127.0.0.1:8000/ 查看网站
   访问 http://127.0.0.1:8000/admin/ 进入管理后台

## 目录结构

```
storage/
├── apps/             # 应用集合目录
│   ├── categories/   # 分类管理应用
│   ├── items/        # 物品管理应用
│   ├── labels/       # 标签管理应用
│   ├── storages/     # 存储位置管理应用
│   └── users/        # 用户管理应用
├── config/           # Django配置
│   ├── settings.py   # 统一配置文件
│   ├── urls.py       # URL配置
│   └── wsgi.py       # WSGI配置
├── scripts/          # 管理脚本
├── static/           # 静态文件
│   ├── css/          # CSS样式
│   ├── js/           # JavaScript
│   ├── img/          # 图片
│   └── fonts/        # 字体
├── templates/        # HTML模板
├── .env              # 环境变量（本地开发）
├── .env.example      # 环境变量模板
├── manage.py         # Django管理命令
├── README.md         # 项目说明
└── requirements.txt  # 依赖列表
```

## 管理脚本

项目包含以下管理脚本：

- **init_db.py**: 初始化数据库，创建必要的表结构
- **load_sample_data.py**: 加载示例数据
- **backup_db.py**: 数据库备份脚本
- **restore_db.py**: 数据库恢复脚本

使用方法：

```bash
python scripts/init_db.py
python scripts/load_sample_data.py
```

## 部署说明

### 生产环境配置

1. 修改 `.env` 文件中的配置：
   - 设置 `DEBUG=False`
   - 设置 `SECRET_KEY` 为强随机值
   - 配置 `ALLOWED_HOSTS` 为实际域名
   - 设置安全相关配置为 `True`

2. 统一使用单一配置文件，通过环境变量控制：

   ```bash
   # 无需再指定具体环境配置文件，默认使用config.settings
   ```

3. 推荐使用 Gunicorn 或 uWSGI 作为WSGI服务器，配合 Nginx 进行部署。

### Docker部署（可选）

项目支持Docker部署，提供了Dockerfile和docker-compose.yml文件。

```bash
docker-compose up -d
```

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

### 应用结构说明

应用都位于`apps/`目录下，每个应用负责不同的功能模块：
- **users**: 用户认证和管理
- **items**: 物品管理核心功能
- **categories**: 分类系统
- **storages**: 存储位置管理
- **labels**: 标签生成和管理

### 编写测试

```bash
python manage.py test
```

### 代码规范

项目遵循PEP 8规范，请确保代码符合规范：

```bash
flake8
```

## 故障排除

### 常见问题

1. **数据库连接失败**
   - 检查 `.env` 文件中的数据库配置
   - 确保MySQL服务正在运行
   - 检查数据库用户权限

2. **静态文件未加载**
   - 运行 `python manage.py collectstatic`
   - 检查静态文件配置

3. **权限错误**
   - 确保用户有足够的权限访问文件和目录

## 许可证

[MIT License](LICENSE)

## 贡献

欢迎提交问题和Pull Request！

## 联系方式

如有问题，请联系项目维护者。