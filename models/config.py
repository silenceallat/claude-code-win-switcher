"""
配置数据模型
"""
import json
import uuid
from datetime import datetime
from config.settings import CONFIG_FILE


class ConfigModel:
    """配置数据模型"""

    @staticmethod
    def load_configs():
        """加载配置文件"""
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {'defaultConfigId': None, 'configs': []}
        return {'defaultConfigId': None, 'configs': []}

    @staticmethod
    def save_configs(config_data):
        """保存配置文件"""
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, ensure_ascii=False, indent=2)
            return True
        except:
            return False

    @staticmethod
    def create_config(name, env_vars):
        """创建新配置"""
        return {
            'id': str(uuid.uuid4())[:8],
            'name': name,
            'isDefault': False,
            'ANTHROPIC_AUTH_TOKEN': env_vars.get('ANTHROPIC_AUTH_TOKEN', ''),
            'ANTHROPIC_BASE_URL': env_vars.get('ANTHROPIC_BASE_URL', ''),
            'CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC': env_vars.get('CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC', ''),
            'AI_model': env_vars.get('AI_model', ''),
            'createdAt': datetime.now().isoformat()
        }

    @staticmethod
    def update_config(config, update_data):
        """更新配置"""
        config['name'] = update_data.get('name', config['name'])
        config['ANTHROPIC_AUTH_TOKEN'] = update_data.get('ANTHROPIC_AUTH_TOKEN', '')
        config['ANTHROPIC_BASE_URL'] = update_data.get('ANTHROPIC_BASE_URL', '')
        config['CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC'] = update_data.get('CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC', '')
        config['AI_model'] = update_data.get('AI_model', '')

    @staticmethod
    def set_default_config(config_data, config_id):
        """设置默认配置"""
        # 先取消所有默认配置
        for config in config_data['configs']:
            config['isDefault'] = False

        # 设置新的默认配置
        for config in config_data['configs']:
            if config['id'] == config_id:
                config['isDefault'] = True
                config_data['defaultConfigId'] = config_id
                return True
        return False

    @staticmethod
    def delete_config(config_data, config_id):
        """删除配置"""
        for i, config in enumerate(config_data['configs']):
            if config['id'] == config_id:
                # 如果删除的是默认配置，清除默认配置ID
                if config_data.get('defaultConfigId') == config_id:
                    config_data['defaultConfigId'] = None
                del config_data['configs'][i]
                return True
        return False