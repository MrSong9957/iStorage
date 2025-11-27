# Django储物格数据模型重构计划

## 1. 分析当前模型与需求差异

### 当前模型
- **Room模型**：name（房间名称）、letter（房间字母标识）、user（关联用户）
- **Furniture模型**：name（家具名称）、letter（家具字母标识）、user（关联用户）
- **Storage模型**：room（关联Room）、furniture（关联Furniture）、storage_code（储物格编号）、qr_code（二维码）、user（关联用户）

### 需求模型
- **Room模型**：room_code（单个大写字母，以A开头，唯一）、room_name（房间名称）
- **Furniture模型**：furniture_code（正整数，从1开始递增，唯一）、furniture_name（家具名称）
- **StorageCell模型**：room（关联Room）、furniture（关联Furniture）、cell_number（储物格基础编号）、cell_id（唯一标识，格式：房间编码+家具编码+3位储物格基础编号）

## 2. 重构步骤

### 步骤1：修改Room模型
- 将`name`字段重命名为`room_name`
- 将`letter`字段重命名为`room_code`，并添加约束：单个大写字母，以A开头，唯一
- 调整唯一约束

### 步骤2：修改Furniture模型
- 将`name`字段重命名为`furniture_name`
- 将`letter`字段重命名为`furniture_code`，并添加约束：正整数，从1开始递增，唯一
- 调整唯一约束

### 步骤3：修改Storage模型为StorageCell
- 重命名模型为`StorageCell`
- 将`storage_code`字段重命名为`cell_id`
- 新增`cell_number`字段，正整数，非空
- 添加联合唯一索引：`(room, furniture, cell_number)`
- 修改`save`方法，重新实现`cell_id`的生成逻辑

### 步骤4：处理Item模型关联
- 将Item模型中与Storage的多对多关联改为与StorageCell关联

### 步骤5：生成并执行迁移
- 生成迁移文件
- 执行迁移命令
- 如果出现迁移问题，清空数据库并重新执行迁移

## 3. 预期结果

- 数据模型符合需求描述
- 储物格唯一标识自动生成，格式正确
- 同一房间+同一家具下的储物格编号从1开始递增
- 模型间关联正确
- 代码简洁、易理解，符合Django最佳实践

## 4. 注意事项

- 由于用户允许清空数据库，将直接执行迁移，不保留现有数据
- 所有修改将严格遵循Django最佳实践
- 保持代码简洁，只修改必要的部分
- 确保模型间关联正确，避免出现引用错误