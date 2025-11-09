"""
配置管理服务
"""
from models.config import ConfigModel


def validate_config(config):
    """验证配置参数，返回警告信息列表"""
    warnings = []

    token = config.get('ANTHROPIC_AUTH_TOKEN', '').strip()
    if not token:
        warnings.append('ANTHROPIC_AUTH_TOKEN 为空')
    elif len(token) < 10:
        warnings.append('ANTHROPIC_AUTH_TOKEN 看起来太短')

    url = config.get('ANTHROPIC_BASE_URL', '').strip()
    if not url:
        warnings.append('ANTHROPIC_BASE_URL 为空')
    elif not url.startswith('http'):
        warnings.append('ANTHROPIC_BASE_URL 不是有效的URL格式')

    traffic = config.get('CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC', '').strip().lower()
    if traffic and traffic not in ['true', 'false']:
        warnings.append('CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC 应该是 true 或 false')

    model = config.get('AI_model', '').strip()
    if not model:
        warnings.append('AI_model 为空')

    return warnings


class ConfigService:
    """配置管理服务"""

    @staticmethod
    def get_all_configs():
        """获取所有配置"""
        data = ConfigModel.load_configs()
        return {
            'success': True,
            'defaultConfigId': data.get('defaultConfigId'),
            'configs': data.get('configs', [])
        }

    @staticmethod
    def create_config(config_data):
        """创建新配置"""
        try:
            data = ConfigModel.load_configs()
            new_config = ConfigModel.create_config(
                config_data.get('name', '新配置'),
                config_data
            )
            data['configs'].append(new_config)
            ConfigModel.save_configs(data)
            return {'success': True, 'config': new_config}
        except Exception as e:
            return {'success': False, 'message': str(e)}

    @staticmethod
    def update_config(config_id, update_data):
        """更新配置"""
        try:
            data = ConfigModel.load_configs()
            for config in data['configs']:
                if config['id'] == config_id:
                    ConfigModel.update_config(config, update_data)
                    ConfigModel.save_configs(data)
                    return {'success': True, 'config': config}
            return {'success': False, 'message': '配置不存在'}
        except Exception as e:
            return {'success': False, 'message': str(e)}

    @staticmethod
    def delete_config(config_id):
        """删除配置"""
        try:
            data = ConfigModel.load_configs()
            if ConfigModel.delete_config(data, config_id):
                ConfigModel.save_configs(data)
                return {'success': True}
            return {'success': False, 'message': '配置不存在'}
        except Exception as e:
            return {'success': False, 'message': str(e)}

    @staticmethod
    def set_default_config(config_id):
        """设置默认配置"""
        try:
            data = ConfigModel.load_configs()
            if ConfigModel.set_default_config(data, config_id):
                ConfigModel.save_configs(data)
                return {'success': True}
            return {'success': False, 'message': '配置不存在'}
        except Exception as e:
            return {'success': False, 'message': str(e)}

    @staticmethod
    def validate_config_data(config):
        """验证配置数据"""
        warnings = validate_config(config)
        return {
            'valid': len(warnings) == 0,
            'warnings': warnings
        }

    @staticmethod
    def import_configs(import_data):
        """导入配置"""
        try:
            data = ConfigModel.load_configs()
            imported_configs = import_data.get('configs', [])
            data['configs'].extend(imported_configs)
            ConfigModel.save_configs(data)
            return {'success': True, 'imported_count': len(imported_configs)}
        except Exception as e:
            return {'success': False, 'message': str(e)}

    @staticmethod
    def export_configs():
        """导出配置"""
        try:
            data = ConfigModel.load_configs()
            return {'success': True, 'data': data}
        except Exception as e:
            return {'success': False, 'message': str(e)}