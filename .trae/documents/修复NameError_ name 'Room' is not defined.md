## 修复NameError: name 'Room' is not defined

### 问题分析

1. 在`views.py`文件中，第16行的导入语句只导入了`Item`和`Storage`模型
2. 但在`tag_view`函数中，使用了`Room`和`Furniture`模型
3. 因此，当执行到`Room.objects.get_or_create()`时，会出现`NameError: name 'Room' is not defined`

### 修改内容

1. **修改`views.py`文件的导入语句**
   - 在导入语句中添加`Room`和`Furniture`模型
   - 确保导入语句正确，没有拼写错误

### 预期效果

* 修复`NameError: name 'Room' is not defined`错误
* 标签生成功能正常工作
* 保持页面风格的延续性，符合极简主义设计原则

### 实施步骤

1. 修改`views.py`文件的导入语句，添加`Room`和`Furniture`模型
2. 测试修复后的功能，确保标签生成功能正常工作

