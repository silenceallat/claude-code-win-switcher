# 🌟 Claude Code · AI模型配置切换工具

一个专为Windows用户设计的AI环境配置管理工具，专为Claude Code用户打造，支持快速切换不同AI服务的配置环境。

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)

## ✨ 主要特性

- 🎯 **Claude Code专用**: 专为Claude Code用户设计，支持11种主流AI服务无缝切换
- 🚀 **一键切换**: 快速在不同AI环境配置间切换
- 💻 **无需管理员权限**: 普通用户权限即可使用
- 🎨 **现代化界面**: Apple风格设计，Toast通知系统
- 🔧 **PowerShell方案**: 稳定可靠的环境变量修改方式
- 📱 **响应式布局**: 适配不同屏幕尺寸
- 🔄 **实时同步**: 配置变更立即生效

## 🚀 快速开始

### 系统要求

- Windows 10/11
- Python 3.6+
- PowerShell 5.0+

### 安装依赖

```bash
pip install -r requirements.txt
```

### 启动应用

#### 方式一：使用启动脚本（推荐）
```bash
start_simple.bat
```

#### 方式二：命令行启动
```bash
python app.py
```

启动成功后访问：**http://localhost:5000**

## 📖 使用指南

### 基础操作

1. **创建配置方案**
   - 点击"新建配置"按钮
   - 填写配置名称和API信息
   - 保存配置

2. **切换AI模型**
   - 在左侧配置列表中选择目标AI服务
   - 点击"应用配置"按钮
   - 确认后Claude Code将自动连接到新的AI服务

3. **导入/导出配置**
   - 支持JSON格式配置文件导入导出
   - 方便在不同设备间同步配置
   - 配置文件中已预置11种AI服务的示例模板

### 支持的AI服务

基于 `configs.json` 配置文件，目前支持以下AI服务：

| 服务提供商 | 配置标识 | 典型模型 | API基础URL |
|-----------|----------|----------|------------|
| **智谱GLM** | `GLM-4.6` | GLM-4.6 | `open.bigmodel.cn` |
| **OpenRouter** | `OpenRouter` | Claude Haiku 4.5 | `openrouter.ai` |
| **魔搭ModelScope** | `ModelScope` | Qwen3-Coder-480B | `api-inference.modelscope.cn` |
| **OpenAI** | `OpenAI GPT-4o` | GPT-4o-mini | `api.openai.com` |
| **Azure OpenAI** | `Azure OpenAI` | GPT-4o-mini | Azure定制端点 |
| **DeepSeek** | `DeepSeek` | DeepSeek-Coder | `api.deepseek.com` |
| **月之暗面** | `Moonshot` | Moonshot-v1-128k | `api.moonshot.cn` |
| **SiliconFlow** | `SiliconFlow` | Qwen2.5-Coder-32B | `api.siliconflow.cn` |
| **豆包Doubao** | `Doubao` | 定制模型 | `ark.cn-beijing.volces.com` |
| **通义千问** | `DashScope` | Qwen-Max | `dashscope.aliyuncs.com` |
| **Groq** | `Groq` | Llama-3.1-70B | `api.groq.com` |

> 💡 **提示**: 所有配置使用统一的环境变量 `ANTHROPIC_AUTH_TOKEN`、`ANTHROPIC_BASE_URL`、`AI_model` 等，便于Claude Code无缝切换不同AI服务。

## 🏗️ 技术架构

### 核心技术栈

- **后端**: Python Flask
- **前端**: 原生HTML/CSS/JavaScript
- **环境变量管理**: PowerShell脚本
- **数据存储**: JSON文件

### 架构设计

```
cc_switch_win10/
├── 🎯 app.py                     # 主应用入口
├── 📄 templates/index.html       # 单页面应用
├── 🔧 core/                      # 核心功能模块
│   ├── script_executor.py        # PowerShell脚本执行器
│   └── permissions.py            # 权限管理
├── 🛠️ services/                  # 业务服务层
│   ├── env_service.py           # 环境变量服务
│   └── config_service.py        # 配置管理服务
├── 📊 models/                    # 数据模型
│   └── config.py                # 配置数据模型
├── 🌐 api/                       # API路由层
│   └── routes.py                # Flask API路由
└── 📜 scripts/                   # PowerShell脚本
    └── Set-EnvironmentVariable.ps1
```

## 🔧 环境变量修改方案

本项目采用 **PowerShell脚本执行** 方案，完美解决了Python直接修改Windows环境变量的权限问题：

### 技术优势

- ✅ **无需管理员权限**: 普通用户即可修改用户环境变量
- ✅ **系统原生支持**: PowerShell是Windows原生组件
- ✅ **稳定可靠**: 避免了注册表操作的兼容性问题
- ✅ **错误处理完善**: 详细的错误信息和诊断建议

### 实现原理

```python
# Python层：业务逻辑
result = script_executor.set_environment_variable(
    'ANTHROPIC_AUTH_TOKEN', 'your_claude_code_token', 'User'
)

# PowerShell层：系统操作（Claude Code环境变量）
[System.Environment]::SetEnvironmentVariable($VarName, $VarValue, "User")
Set-ItemProperty -Path "HKCU:\Environment" -Name $VarName -Value $VarValue
```

## 🎨 用户界面特色

### 现代化设计

- **Apple风格界面**: 简洁优雅的设计语言
- **Toast通知系统**: 替代传统alert弹窗
- **响应式布局**: 自适应不同屏幕尺寸
- **优雅动画**: 流畅的交互体验

### 关键UI改进

- 📏 **字体优化**: 基础字体16px，提升可读性
- 🖱️ **交互优化**: 更大的点击区域和更清晰的视觉反馈
- 📱 **布局优化**: 侧边栏350px，状态面板420px
- 🎯 **信息展示**: 环境变量分层显示，信息更清晰

## 🛠️ 开发指南

### 本地开发

1. 克隆项目
```bash
git clone https://github.com/silenceallat/claude-code-win-switcher.git
cd claude-code-win-switcher
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 启动开发服务器
```bash
python app.py
```

### 项目结构说明

- **config/**: 应用配置和常量定义
- **core/**: 核心功能模块（权限、脚本执行）
- **services/**: 业务服务层（配置、环境变量）
- **models/**: 数据模型和CRUD操作
- **api/**: RESTful API路由定义
- **templates/**: HTML模板和前端资源
- **scripts/**: PowerShell脚本文件

### 添加新的AI服务支持

1. 在 `config/settings.py` 中添加环境变量名
2. 在 `services/config_service.py` 中添加验证规则
3. 更新前端界面的配置表单

## 🤝 贡献指南

我们欢迎所有形式的贡献！

### 贡献方式

1. **报告问题**: 在Issues中提交bug报告或功能请求
2. **代码贡献**: Fork项目，创建功能分支，提交Pull Request
3. **文档改进**: 完善文档和说明
4. **测试反馈**: 测试不同Windows版本下的兼容性

### 开发规范

- 遵循PEP 8 Python代码规范
- 保持模块化设计原则
- 添加必要的注释和文档
- 确保向后兼容性

## 📝 更新日志

### v1.0.0 (2024-11-09)

✨ **新功能**
- 多AI环境配置管理
- PowerShell环境变量修改方案
- 现代化Web界面
- Toast通知系统
- 配置导入/导出功能

🐛 **问题修复**
- 修复Windows环境变量权限问题
- 修复字符编码问题
- 修复UI显示问题

🎨 **界面优化**
- 增大字体和交互区域
- 优化布局和间距
- 改善响应式设计

## 📄 许可证

本项目采用 [MIT License](LICENSE) 开源协议。

## 🙏 致谢

- 感谢所有贡献者和用户的支持
- 灵感来源于多AI开发环境管理的实际需求
- 特别感谢PowerShell社区的技术支持

## 📞 联系方式

- 📧 Email: silenceallat@gmail.com
- 🐛 Issues: [GitHub Issues](https://github.com/silenceallat/claude-code-win-switcher/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/silenceallat/claude-code-win-switcher/discussions)

---

⭐ 如果这个项目对你有帮助，请给我们一个Star！
