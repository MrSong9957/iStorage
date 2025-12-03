# 收纳APP简化改造计划

## 需求分析

* 只保留录入物品功能，删除储物格功能

* 存放位置靠文字记录，不使用储物格关联

* 最多只保存名称、编号和照片（可选）到数据库

* 标签只有编号且从1开始，以便区分

* 使用示例："我把1号放在了主卧床头柜。"

## 实现步骤

### 1. 模型层修改

* **修改Item模型**：

  * 保留核心字段：name, item\_code, image, location, user

  * 删除与储物格相关的字段：storage\_cells（多对多关联）

  * 删除其他不必要字段：description, category, value, notes, qr\_code

  * 修改item\_code生成逻辑，使用从1开始的简单数字编号

* **删除不需要的模型**：

  * 删除Room模型

  * 删除Furniture模型

  * 删除StorageCell模型

### 2. 视图层修改

* **修改物品录入视图**：

  * 简化deposit\_item视图，只处理name、image字段

  * 修改generate\_item\_code函数，使用从1开始的递增编号

  * 删除与储物格相关的视图：deposit\_storage, associate\_item\_storage, clear\_association, print\_selector

  * 修改tag\_view视图，只处理物品标签生成

  * 修改find\_items视图，删除储物格相关逻辑

### 3. URL层修改

* 删除与储物格相关的URL路由：

  * deposit\_storage

  * associate\_item\_storage

  * clear\_association

  * print\_selector

  * 其他与储物格相关的路由

### 4. 模板层修改

* **修改物品录入模板**：

  * 简化deposit\_item.html，只保留名称和图片上传字段

  * 删除与储物格相关的模板：deposit\_storage.html, associate\_item\_storage.html, print\_selector.html

  * 修改tag\_view\.html，只显示物品编号和名称

  * 修改find\_items.html，删除储物格相关内容

### 5. 数据兼容性处理

* 确保现有数据的兼容性，只修改字段，不删除现有数据

* 对于删除的字段，使用Django的迁移功能进行处理

## 预期效果

* 简化后的收纳APP只保留物品录入功能

* 物品编号从1开始递增，方便用户记忆和使用

* 存放位置通过文字记录，灵活方便

* 页面风格保持极简主义设计原则

* 代码结构清晰，易于维护

## 技术要点

* 遵循Django最佳实践

* 使用最简单、最容易理解的代码

* 兼顾性能最优

* 保持页面风格的延续性

* 确保现有数据的兼容性

