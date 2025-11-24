# 项目目录结构

storage/
├── .env                     # 环境变量配置文件
├── .env.example             # 环境变量示例文件
├── .trae/                   # Trae AI相关配置
│   └── rules/
│       └── project_rules.md
├── .venv/                   # 虚拟环境
├── README.md                # 项目说明文档
├── apps/                    # 所有业务应用
│   ├── __init__.py
│   ├── __pycache__/
│   │   └── __init__.cpython-313.pyc
│   ├── items/               # 物品模块
│   │   ├── __init__.py
│   │   ├── __pycache__/
│   │   ├── apps.py          # 应用配置
│   │   ├── forms.py         # 表单定义
│   │   ├── migrations/      # 数据库迁移
│   │   ├── models.py        # 数据模型
│   │   ├── urls.py          # 模块路由
│   │   └── views.py         # 视图函数
│   └── users/               # 用户模块
│       ├── __init__.py
│       ├── __pycache__/
│       ├── apps.py          # 应用配置
│       ├── forms.py         # 表单定义
│       ├── migrations/      # 数据库迁移
│       ├── models.py        # 数据模型
│       ├── urls.py          # 模块路由
│       └── views.py         # 视图函数
├── config/                  # 项目核心配置
│   ├── __init__.py
│   ├── __pycache__/
│   │   ├── __init__.cpython-313.pyc
│   │   ├── settings.cpython-313.pyc
│   │   ├── urls.cpython-313.pyc
│   │   └── wsgi.cpython-313.pyc
│   ├── settings.py          # 项目主配置
│   ├── urls.py              # 项目主路由
│   └── wsgi.py              # WSGI部署配置
├── db.sqlite3               # SQLite数据库文件
├── docs/                    # 项目文档
│   ├── project_structure.md # 项目结构文档
│   └── storage_management_requirements.md # 存储管理需求文档
├── manage.py                # Django命令行工具
├── media/                   # 媒体文件目录
│   └── item_images/         # 物品图片
│       ├── bootstrap-logo.svg
│       └── bootstrap-logo_WcLjRF5.svg
├── requirements.txt         # 项目依赖清单
├── static/                  # 全局静态资源
│   ├── css/               # CSS 样式文件
│   │   ├── tailwind-cdn.min.js  # Tailwind CSS本地JS文件
│   │   └── tailwind.min.css     # Tailwind CSS本地文件
│   └── js/                  # JavaScript文件
│       └── deposit_module.js # 存储模块JavaScript
├── storage.log              # 项目日志文件
└── templates/               # 全局模板
    ├── index.html            # 首页/基础模板
    ├── base_template.html   # 扩展模板
    ├── items/               # 物品模块模板
    │   ├── deposit_item.html
    │   ├── deposit_item_modal.html
    │   ├── tag_view.html     # 物品标签展示和打印页面（新增）
    │   └── success.html      # 物品录入成功页面（带倒计时重定向）
    └── users/               # 用户模块模板
        ├── login.html       # 登录页面
        └── register.html    # 注册页面