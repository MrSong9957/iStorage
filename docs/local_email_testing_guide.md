# 本地测试忘记密码功能的邮箱验证指南

## 1. 配置邮箱服务

### 1.1 选择邮箱服务提供商

您可以选择以下常用邮箱服务提供商之一：
- QQ邮箱
- 163邮箱
- Gmail
- 其他支持SMTP服务的邮箱

### 1.2 获取授权码/应用密码

大多数邮箱服务提供商要求使用授权码或应用密码，而不是登录密码，来进行SMTP认证。以下是获取授权码的方法：

#### QQ邮箱
1. 登录QQ邮箱
2. 点击右上角的"设置" → "账户"
3. 向下滚动找到"POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务"
4. 开启"POP3/SMTP服务"
5. 按照提示发送短信验证
6. 复制生成的授权码

#### 163邮箱
1. 登录163邮箱
2. 点击右上角的"设置" → "POP3/SMTP/IMAP"
3. 开启"SMTP服务"
4. 按照提示获取授权码

#### Gmail
1. 登录Gmail
2. 点击右上角的头像 → "管理您的Google账户"
3. 点击左侧的"安全性"
4. 向下滚动找到"应用密码"
5. 选择"邮件"作为应用，"其他"作为设备
6. 复制生成的应用密码

## 2. 配置项目

### 2.1 创建.env文件

在项目根目录创建一个`.env`文件，用于存储敏感信息：

```
# 邮件配置
DEFAULT_FROM_EMAIL=your-email@example.com
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-authorization-code
```

### 2.2 更新settings.py

根据您选择的邮箱服务提供商，更新`config/settings.py`中的邮件配置：

#### QQ邮箱示例
```python
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'your-qq-email@qq.com')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'your-qq-email-authorization-code')
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
```

#### 163邮箱示例
```python
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'your-163-email@163.com')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'your-163-email-authorization-code')
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
```

#### Gmail示例
```python
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'your-gmail-email@gmail.com')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'your-gmail-app-password')
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
```

## 3. 本地测试流程

### 3.1 启动开发服务器

```bash
python manage.py runserver
```

### 3.2 测试忘记密码功能

1. 访问登录页面：`http://127.0.0.1:8000/users/login/`
2. 点击"忘记密码？"链接
3. 进入密码重置请求页面：`http://127.0.0.1:8000/users/password_reset/`
4. 输入您的邮箱地址，点击"发送重置链接"
5. 检查您的邮箱，确认收到密码重置邮件
6. 点击邮件中的链接，进入密码重置确认页面
7. 输入新密码并确认，点击"重置密码"
8. 看到密码重置成功页面
9. 使用新密码登录，确认密码重置成功

## 4. 常见问题和解决方案

### 4.1 邮件发送失败

**问题**：点击"发送重置链接"后，页面显示错误或没有收到邮件。

**解决方案**：
1. 检查`.env`文件中的邮箱配置是否正确
2. 检查`settings.py`中的邮件配置是否正确
3. 确保邮箱服务提供商已开启SMTP服务
4. 确保使用的是授权码/应用密码，而不是登录密码
5. 查看Django开发服务器的日志，获取具体错误信息

### 4.2 密码重置链接无效

**问题**：点击邮件中的链接后，显示"密码重置链接无效或已过期"。

**解决方案**：
1. 确保点击的是最新收到的密码重置链接
2. 确保链接没有被截断（如果邮件客户端显示链接不完整，尝试复制完整链接到浏览器）
3. 检查Django的`SECRET_KEY`是否已更改（如果更改了，之前生成的链接将无效）

### 4.3 页面显示500错误

**问题**：访问密码重置相关页面时，显示500错误。

**解决方案**：
1. 查看Django开发服务器的日志，获取具体错误信息
2. 确保所有必要的模板文件都已创建
3. 确保URL配置正确

## 5. 测试完成后的清理

测试完成后，您可以选择：

1. 保留SMTP配置，继续使用实际邮箱进行测试
2. 将`settings.py`中的`EMAIL_BACKEND`改回控制台后端，用于开发调试：
   ```python
   EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
   ```

## 6. 注意事项

1. 不要将授权码/应用密码直接写在代码中，始终使用环境变量
2. 定期更新授权码/应用密码，确保账户安全
3. 在生产环境中，使用更安全的邮箱配置和加密方式
4. 测试完成后，建议删除`.env`文件中的敏感信息，或确保该文件不会被提交到版本控制系统

## 7. 参考文档

- [Django官方文档 - 发送邮件](https://docs.djangoproject.com/en/4.2/topics/email/)
- [QQ邮箱SMTP配置](https://service.mail.qq.com/cgi-bin/help?subtype=1&&id=28&&no=371)
- [163邮箱SMTP配置](https://help.mail.163.com/faqDetail.do?code=d7a5dc8471cd0c0e8b4b8f4f8e49998b374173cfe9171305fa1ce630d7f67ac2)
- [Gmail SMTP配置](https://support.google.com/mail/answer/7126229?hl=zh-Hans)
