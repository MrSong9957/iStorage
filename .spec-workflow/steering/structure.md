# 结构指导文档

## 1. 项目结构概览

```
storage/                  # 项目根目录
├── .env                  # 环境变量配置
├── .env.example          # 环境变量示例
├── .venv/                # Python虚拟环境
├── README.md             # 项目说明文档
├── apps/                 # Django应用目录
│   ├── __init__.py
│   ├── items/            # 物品管理应用
│   └── users/            # 用户管理应用
├── config/               # 项目配置目录
│   ├── __init__.py
│   ├── settings.py       # 项目设置
│   ├── urls.py           # 主URL配置
│   └── wsgi.py           # WSGI配置
├── db.sqlite3            # SQLite数据库文件
├── docs/                 # 项目文档
├── media/                # 媒体文件存储
│   └── item_images/      # 物品图片
├── requirements.txt      # 项目依赖
├── scripts/              # 辅助脚本
├── static/               # 静态资源
│   ├── css/              # CSS文件
│   └── js/               # JavaScript文件
└── templates/            # HTML模板
    ├── base_template.html # 基础模板
    ├── index.html        # 首页模板
    ├── items/            # 物品应用模板
    └── users/            # 用户应用模板
```

## 2. 目录规范

### 2.1 应用目录（apps/）
- 每个Django应用独立成一个子目录
- 应用名称使用小写字母
- 每个应用包含必要的文件：models.py, views.py, urls.py, forms.py, apps.py
- 使用Django的应用注册机制进行配置

### 2.2 模板目录（templates/）
- 根目录存放共享模板（如base_template.html）
- 按应用创建子目录，存放特定应用的模板
- 模板命名使用小写字母和下划线
- 继承关系清晰，避免循环依赖

### 2.3 静态资源目录（static/）
- 按资源类型（css, js, images）组织子目录
- 第三方库放在独立子目录中（如js/vendor/）
- 资源文件命名使用小写字母、数字和连字符
- 版本化静态资源以支持缓存刷新

### 2.4 文档目录（docs/）
- 存放项目文档、API参考、使用指南等
- 文档使用Markdown格式
- 为不同类型的文档创建分类目录

## 3. 命名约定

### 3.1 文件命名
- Python文件：使用小写字母和下划线
- HTML模板：使用小写字母和下划线
- CSS/JS文件：使用小写字母、数字和连字符
- 媒体文件：使用描述性名称，避免特殊字符

### 3.2 类命名
- 模型类：使用PascalCase（大驼峰命名法），如`Item`, `Storage`
- 视图类：使用PascalCase，如`ItemListView`
- 表单类：使用PascalCase，如`ItemForm`

### 3.3 函数/变量命名
- 函数名：使用snake_case（小驼峰命名法），如`get_item_details`
- 变量名：使用snake_case，如`item_count`, `storage_location`
- 常量名：使用全大写和下划线，如`MAX_IMAGE_SIZE`

### 3.4 数据库表/字段命名
- 表名：使用应用名前缀和snake_case，如`items_item`, `users_user`
- 字段名：使用snake_case，如`item_name`, `storage_code`
- 外键字段：使用相关模型名加`_id`后缀，如`user_id`

## 4. 代码规范

### 4.1 Python编码规范
- 遵循PEP 8规范
- 每行不超过79个字符
- 使用4个空格缩进，不使用Tab
- 导入语句分组（标准库、第三方库、本地库）
- 文档字符串使用Google风格或reStructuredText

### 4.2 HTML/CSS编码规范
- 使用语义化HTML标签
- 使用Tailwind CSS进行样式管理
- 遵循苹果设计风格：简洁、现代、有层次感
- 保持一致的间距和对齐
- 使用响应式设计确保在不同设备上的兼容性

### 4.3 JavaScript编码规范
- 使用ES6+语法
- 避免全局变量污染
- 使用const/let而不是var
- 函数使用箭头函数（适当时）
- 遵循JavaScript标准格式

## 5. 设计模式

### 5.1 Django模式
- **模型层**：业务逻辑和数据访问
- **视图层**：请求处理和响应生成
- **模板层**：界面渲染和用户交互

### 5.2 常用设计模式
- **表单验证模式**：使用Django表单进行输入验证
- **模板继承模式**：基于base_template.html的继承体系
- **上下文处理器模式**：全局数据传递到模板

## 6. 文档标准

### 6.1 代码注释
- 类和函数必须有文档字符串
- 复杂逻辑必须有行注释
- 避免冗余或过时的注释

### 6.2 项目文档
- 保持文档与代码同步更新
- 使用Markdown格式编写文档
- 为重要功能提供使用示例
- 记录API接口规范

### 6.3 版本记录
- 在README中记录主要版本更新
- 为重大更改提供迁移指南

## 7. 最佳实践

### 7.1 代码组织
- 一个函数只做一件事
- 保持视图函数简洁，复杂逻辑移至服务层
- 使用装饰器管理视图权限

### 7.2 模板开发
- 合理使用模板继承和包含
- 使用模板标签和过滤器增强功能
- 避免在模板中编写复杂逻辑

### 7.3 数据库使用
- 优先使用Django ORM而非原生SQL
- 使用事务确保数据一致性
- 避免在循环中执行数据库查询

### 7.4 错误处理
- 使用try-except捕获预期异常
- 提供友好的错误页面
- 记录错误日志以便调试

## 8. 工具与辅助脚本

### 8.1 脚本目录规范
- 脚本名称使用描述性命名
- 为脚本添加使用说明
- 确保脚本可重用和可维护

### 8.2 开发工具
- 使用Django shell进行快速测试
- 使用Django管理命令进行数据库维护
- 配置代码格式化工具确保一致性