# 修复FieldError问题计划

## 1. 问题分析

根据错误信息，在`/items/find/`页面出现了FieldError，提示无法解析关键字'unit'为字段。这是因为在`find_items`视图中，尝试按照`unit`字段对储物格进行排序，但是Storage模型中并没有`unit`字段，而是使用`storage_code`字段来存储储物格编号。

## 2. 解决方案

### 2.1 修改find_items视图
- **文件路径**：`apps/items/views.py`
- **修改内容**：将第541行的`order_by('room', 'furniture', 'unit')`改为`order_by('room', 'furniture', 'storage_code')`
- **修改原因**：Storage模型中使用`storage_code`字段存储储物格编号，而不是`unit`字段

### 2.2 检查其他可能的问题
- 检查项目中其他地方是否有类似的错误，特别是在查询Storage模型时
- 确保修改后代码符合极简主义设计原则，只做必要修改

## 3. 实施步骤

1. **修改find_items视图**：将排序字段从'unit'改为'storage_code'
2. **测试修复结果**：运行开发服务器，访问`/items/find/`页面，确认错误已解决
3. **验证其他功能**：确保修改不会影响其他功能的正常运行

## 4. 预期结果

- `/items/find/`页面能够正常访问，不再出现FieldError
- 储物格能够按照房间、家具和储物格编号正确排序
- 页面风格保持延续性，符合极简主义设计原则
- 只做了必要修改，其他内容保持不变

## 5. 技术要点

- 使用Django ORM的order_by方法对查询结果进行排序
- 确保排序字段与模型定义一致
- 遵循极简主义设计原则，只做必要修改
- 保持代码的可读性和可维护性