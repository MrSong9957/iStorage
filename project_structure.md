# 项目目录结构

## 项目概述
这是一个基于 Django 的物品存储管理系统，用于管理物品、储物格、房间和家具等信息。

## 目录结构

```
storage/
├── .git/                  # Git 版本控制目录
├── .spec-workflow/        # 规范工作流目录
├── .trae/                 # Trae AI 相关目录
├── .venv/                 # Python 虚拟环境
├── apps/                  # Django 应用目录
│   ├── items/             # 物品管理应用
│   └── users/             # 用户管理应用
├── config/                # Django 配置目录
├── docs/                  # 项目文档目录
├── media/                 # 媒体文件目录
├── scripts/               # 辅助脚本目录
│   └── get_supabase_service_key.py # 获取 Supabase 服务密钥脚本
├── static/                # 静态文件目录
├── templates/             # 模板文件目录
├── test/                  # 测试目录
├── .env                   # 环境变量文件
├── .env.example           # 环境变量示例文件
├── db.sqlite3             # SQLite 数据库文件
├── manage.py              # Django 管理脚本
├── README.md              # 项目说明文档
├── requirements.txt       # Python 依赖文件
└── storage.log            # 日志文件
```

## 文件说明

### 根目录文件
- `.env`：包含项目的环境变量配置，如数据库连接信息、密钥等
- `.env.example`：环境变量配置示例文件
- `db.sqlite3`：SQLite 数据库文件，用于存储项目数据
- `manage.py`：Django 管理脚本，用于执行各种管理命令
- `README.md`：项目说明文档，包含项目概述、安装和使用说明
- `requirements.txt`：Python 依赖文件，列出项目所需的所有 Python 包
- `storage.log`：项目日志文件

### apps 目录
- `items/`：物品管理应用，包含物品、储物格、房间和家具等模型
- `users/`：用户管理应用，包含用户模型和认证相关功能

### config 目录
包含 Django 项目的配置文件，如 settings.py、urls.py 等

### media 目录
用于存储上传的媒体文件，如图片、文档等

### scripts 目录
包含各种辅助脚本，用于执行一次性任务或调试操作

- `fetch_find_loggedin.py`：本地开发辅助脚本 — 使用 Django test client 创建临时用户并抓取 `/items/find/` 渲染后的 HTML（仅用于本地开发/调试，非生产）。

### static 目录
用于存储静态文件，如 CSS、JavaScript、图片等

### templates 目录
用于存储 Django 模板文件，用于渲染 HTML 页面

### test 目录
包含项目的测试文件，用于测试各种功能

## 项目优化
已完成项目文件清理，删除了不必要的临时脚本和调试文件，优化了项目结构，提高了可维护性。

## 新增文件说明
- `templates/items/item_detail.html`：物品详情与编辑页面（用于在卡片点击后查看和修改物品名称、房间/位置、图片）。

## 本次变更新增文件
- `apps/items/migrations/0003_add_category.py`：新增迁移，用于创建 `Category` 模型（每用户独立的分类表），以支持可编辑分类功能。
- `templates/items/_item_modal.html`：物品编辑模态窗片段（在 `find_items` 页面点击卡片时通过 AJAX 加载并展示）。

- `static/css/custom.css`：极简现代化样式文件，实现了苹果设计风格和响应式布局，用于物品查找页面的整体样式设计。

## 本次变更新改文件
## Context7文档汇总
- `docs/context7_docs_summary.md`：汇总了通过Context7获取的项目技术栈相关文档内容，包括Django、Supabase、Tailwind CSS和python-dotenv等技术的核心用法。

说明：为了兼容现有数据，`Category` 模型与原有 `Item.location` 字段共存。重命名分类时，后台会同步更新 `Item.location` 中匹配的值以保证兼容性。