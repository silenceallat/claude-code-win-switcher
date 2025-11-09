"""
配置管理模块
"""
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent

# 配置文件路径（修改为项目目录内）
CONFIG_FILE = PROJECT_ROOT / 'configs.json'

# 环境变量名称列表
ENV_VARS = ['ANTHROPIC_AUTH_TOKEN', 'ANTHROPIC_BASE_URL', 'CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC', 'AI_model']

# Flask配置
FLASK_HOST = '0.0.0.0'
FLASK_PORT = 5000
FLASK_DEBUG = True