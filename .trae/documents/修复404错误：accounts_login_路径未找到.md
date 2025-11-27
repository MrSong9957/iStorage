## 修复404错误：accounts/login/路径未找到

### 问题分析
1. **错误信息**：访问`http://127.0.0.1:8000/accounts/login/?next=/items/print_selector/`时出现404错误
2. **原因**：Django默认的登录URL是`accounts/login/`，但我们的项目中配置的是`users/login/`
3. **URL配置**：
   - 主URL配置中没有`accounts/`路径
   - 用户应用的URL配置在`users/`路径下，登录URL是`users/login/`
4. **触发条件**：当`@login_required`装饰器检测到用户未登录时，会重定向到默认的`accounts/login/`路径

### 解决方案
在`settings.py`中添加`LOGIN_URL`配置，告诉Django使用我们自定义的登录URL。

### 具体实现步骤
1. **修改settings.py**：添加`LOGIN_URL = '/users/login/'`配置
2. **保持其他配置不变**：不修改URL配置，只添加一行设置
3. **测试验证**：确保未登录用户访问受保护页面时能正确重定向到`users/login/`

### 预期效果
- 当用户未登录访问受保护页面时，会重定向到`users/login/`而不是`accounts/login/`
- 不再出现404错误
- 登录后能正确跳转到原来请求的页面

### 代码修改点
- `config/settings.py`：添加`LOGIN_URL`配置

### 注意事项
- 保持代码简洁，符合极简主义原则
- 只修改必要的代码，不影响其他功能
- 遵循Django最佳实践

### 优势
- 解决方案简单，只需要添加一行配置
- 不需要修改URL配置，减少潜在风险
- 符合Django的配置优先原则
- 便于维护和理解