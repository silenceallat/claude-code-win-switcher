# 🚀 部署指南

本文档提供了 Multi-AI Environment Config Manager 的详细部署指南。

## 📋 部署前准备

### 系统要求

- **操作系统**: Windows 10/11 (推荐)
- **Python**: 3.6 或更高版本
- **PowerShell**: 5.0 或更高版本
- **内存**: 至少 512MB 可用内存
- **磁盘空间**: 至少 100MB 可用空间
- **权限**: 普通用户权限（无需管理员权限）

### 权限检查

在部署前，请确保：

1. ✅ 可以运行PowerShell脚本
   ```powershell
   # 检查执行策略
   Get-ExecutionPolicy

   # 如果需要，设置为RemoteSigned
   Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

2. ✅ 可以修改用户环境变量
   ```powershell
   # 测试环境变量修改权限
   [System.Environment]::SetEnvironmentVariable("TEST_VAR", "test_value", "User")
   ```

3. ✅ Python环境正常
   ```bash
   python --version
   pip --version
   ```

## 📦 安装部署

### 方式一：源码部署（推荐）

#### 1. 下载源码

```bash
# 克隆Git仓库
git clone https://github.com/yourusername/cc_switch_win10.git
cd cc_switch_win10

# 或下载ZIP文件并解压
```

#### 2. 安装依赖

```bash
# 安装Python依赖
pip install -r requirements.txt

# 如果pip较旧，建议升级
pip install --upgrade pip
```

#### 3. 验证安装

```bash
# 测试应用启动
python app.py

# 如果看到服务器启动信息，说明安装成功
```

### 方式二：可执行文件部署（将来支持）

我们计划提供独立的可执行文件，无需Python环境即可运行。

```bash
# 下载对应版本的可执行文件
# Windows: cc-switch-win10-x64.exe
# 直接双击运行即可
```

## ⚙️ 配置说明

### 基础配置

应用配置文件位于 `config/settings.py`，主要配置项：

```python
# 环境变量列表
ENV_VARS = [
    'ANTHROPIC_AUTH_TOKEN',
    'ANTHROPIC_BASE_URL',
    'CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC',
    'AI_model',
    # 添加更多环境变量...
]

# 服务器配置
HOST = '127.0.0.1'
PORT = 5000
DEBUG = True
```

### 高级配置

#### 1. 修改服务器端口

```python
# 在 app.py 中修改
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
```

#### 2. 启用HTTPS（可选）

```python
# 需要SSL证书
app.run(host='0.0.0.0', port=443,
        ssl_context=('cert.pem', 'key.pem'))
```

#### 3. 自定义配置存储位置

```python
# 在 config/settings.py 中修改
CONFIG_FILE = 'custom_configs.json'
```

## 🚀 启动应用

### 方式一：使用启动脚本（推荐）

```bash
# Windows
start_simple.bat

# 或命令行启动
python app.py
```

### 方式二：作为服务运行（Windows服务）

#### 1. 创建服务脚本

创建 `install_service.py`:

```python
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import subprocess
import sys
import os

class AppService(win32serviceutil.ServiceFramework):
    _svc_name_ = "CCSwitchWin10"
    _svc_display_name_ = "Multi-AI Environment Config Manager"
    _svc_description_ = "Multi-AI environment configuration management service"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.process = None

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        if self.process:
            self.process.terminate()

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))

        # 启动应用
        app_dir = os.path.dirname(os.path.abspath(__file__))
        app_script = os.path.join(app_dir, 'app.py')

        self.process = subprocess.Popen([sys.executable, app_script])

        # 等待停止信号
        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(AppService)
```

#### 2. 安装和启动服务

```bash
# 安装服务
python install_service.py install

# 启动服务
python install_service.py start

# 停止服务
python install_service.py stop

# 删除服务
python install_service.py remove
```

## 🔧 生产环境部署

### 安全配置

#### 1. 限制访问范围

```python
# 只允许本地访问
app.run(host='127.0.0.1', port=5000)

# 或允许局域网访问
app.run(host='0.0.0.0', port=5000)
```

#### 2. 关闭调试模式

```python
# 生产环境设置
DEBUG = False
```

#### 3. 配置防火墙

```powershell
# Windows防火墙配置
New-NetFirewallRule -DisplayName "CC Switch" -Direction Inbound -Port 5000 -Protocol TCP -Action Allow
```

### 性能优化

#### 1. 使用WSGI服务器

```bash
# 安装Waitress
pip install waitress

# 启动生产服务器
waitress-serve --host=127.0.0.1 --port=5000 app:app
```

#### 2. 配置反向代理（可选）

使用Nginx或IIS作为反向代理：

```nginx
# Nginx配置示例
server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 📊 监控和日志

### 日志配置

```python
import logging
from logging.handlers import RotatingFileHandler

# 配置日志
if not app.debug:
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
```

### 健康检查

```python
@app.route('/health')
def health_check():
    return {'status': 'healthy', 'timestamp': time.time()}
```

## 🔒 安全最佳实践

### 1. 定期更新

```bash
# 更新Python依赖
pip install --upgrade -r requirements.txt

# 检查安全漏洞
pip install safety
safety check
```

### 2. 备份配置

```bash
# 定期备份配置文件
copy configs.json configs_backup_%date%.json
```

### 3. 监控访问

```python
# 添加访问日志
@app.before_request
def before_request():
    app.logger.info(f"Access from {request.remote_addr} to {request.path}")
```

## 🐛 故障排除

### 常见问题

#### 1. 端口被占用

```bash
# 查找占用端口的进程
netstat -ano | findstr :5000

# 结束进程
taskkill /PID <进程ID> /F
```

#### 2. PowerShell执行策略问题

```powershell
# 检查当前执行策略
Get-ExecutionPolicy

# 临时允许脚本执行
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### 3. 权限不足

```bash
# 以管理员身份运行命令提示符
# 或检查用户账户控制设置
```

#### 4. 依赖缺失

```bash
# 重新安装依赖
pip install -r requirements.txt --force-reinstall
```

### 日志分析

查看应用日志进行故障诊断：

```bash
# 查看最新日志
tail -f logs/app.log

# 搜索错误
findstr "ERROR" logs/app.log
```

## 📞 技术支持

如果在部署过程中遇到问题，请：

1. 📖 查看本文档的故障排除部分
2. 🔍 检查 [GitHub Issues](https://github.com/yourusername/cc_switch_win10/issues)
3. 📧 联系技术支持: support@yourdomain.com
4. 💬 参与 [GitHub Discussions](https://github.com/yourusername/cc_switch_win10/discussions)

---

## 更新记录

- v1.0.0 (2024-11-09): 初始部署文档
- 持续更新中...