# 项目目录结构

my_django_project/
├── config/                   # 项目核心配置
│   ├── __init__.py
│   ├── settings.py           # 项目主配置
│   ├── urls.py               # 项目主路由
│   ├── asgi.py               # ASGI 部署配置
│   └── wsgi.py               # WSGI 部署配置
├── apps/                     # 所有业务应用
│   ├── __init__.py
│   ├── users/                # 用户模块（示例应用1）
│   │   ├── __init__.py
│   │   ├── models.py         # 用户数据模型
│   │   ├── views.py          # 用户视图
│   │   ├── urls.py           # 用户模块路由
│   │   └── apps.py           # 应用配置
│   └── products/             # 商品模块（示例应用2）
│       ├── __init__.py
│       ├── models.py
│       ├── views.py
│       ├── urls.py
│       └── apps.py
├── static/                   # 全局静态资源
│   ├── css/
│   │   └── base.css
│   ├── js/
│   │   └── common.js
│   └── images/
│       └── logo.png
├── templates/                # 全局模板
│   ├── base.html             # 基础模板
│   ├── 404.html              # 404 错误页面
│   └── 500.html              # 500 错误页面
├── manage.py                 # Django 命令行工具
├── requirements.txt          # 项目依赖清单
└── .gitignore                # Git 忽略文件