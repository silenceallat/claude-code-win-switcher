"""
Flask API路由模块
"""
from flask import Flask, render_template, jsonify, request
from services.config_service import ConfigService
from services.env_service import EnvService
from core.permissions import is_admin, request_admin_privilege


def create_routes(app: Flask):
    """创建所有API路由"""

    @app.route('/')
    def index():
        """主页面"""
        return render_template('index.html')

    @app.route('/api/check-admin', methods=['GET'])
    def check_admin():
        """检查管理员权限"""
        from core.permissions import check_runtime_privilege
        privilege_info = check_runtime_privilege()
        return jsonify({
            'isAdmin': privilege_info['is_admin'],
            'canModifyEnv': privilege_info['can_modify_env'],
            'level': privilege_info['level'],
            'recommendations': privilege_info['recommendations']
        })

    @app.route('/api/test-env-access', methods=['GET'])
    def test_env_access():
        """测试环境变量访问权限"""
        from services.env_service import EnvService

        try:
            test_result = EnvService.test_environment_variable_access()
            return jsonify({
                'success': True,
                'test_result': test_result
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Environment variable access test failed: {str(e)}'
            })

    @app.route('/api/configs', methods=['GET'])
    def get_configs():
        """获取所有配置"""
        return jsonify(ConfigService.get_all_configs())

    @app.route('/api/configs', methods=['POST'])
    def create_config():
        """创建新配置"""
        data = request.json
        return jsonify(ConfigService.create_config(data))

    @app.route('/api/configs/<config_id>', methods=['PUT'])
    def update_config(config_id):
        """更新配置"""
        data = request.json
        return jsonify(ConfigService.update_config(config_id, data))

    @app.route('/api/configs/<config_id>', methods=['DELETE'])
    def delete_config(config_id):
        """删除配置"""
        return jsonify(ConfigService.delete_config(config_id))

    @app.route('/api/configs/<config_id>/set-default', methods=['POST'])
    def set_default_config(config_id):
        """设置默认配置"""
        return jsonify(ConfigService.set_default_config(config_id))

    @app.route('/api/configs/<config_id>/apply', methods=['POST'])
    def apply_config(config_id):
        """应用配置到系统环境变量"""
        from core.permissions import check_runtime_privilege

        # 检查权限
        privilege_info = check_runtime_privilege()
        if not privilege_info['can_modify_env']:
            recommendations = privilege_info['recommendations']
            error_message = recommendations[0]['message'] if recommendations else 'Insufficient privileges'

            return jsonify({
                'needsAdmin': not privilege_info['is_admin'],
                'success': False,
                'message': error_message,
                'canModifyUserEnv': privilege_info['can_modify_env']
            })

        # 获取配置数据
        configs_result = ConfigService.get_all_configs()
        if not configs_result['success']:
            return jsonify({'success': False, 'message': '获取配置失败'})

        config = None
        for c in configs_result['configs']:
            if c['id'] == config_id:
                config = c
                break

        if not config:
            return jsonify({'success': False, 'message': '配置不存在'})

        # 应用配置
        result = EnvService.apply_config(config)
        return jsonify(result)

    @app.route('/api/validate', methods=['POST'])
    def validate_config():
        """验证配置参数"""
        data = request.json
        return jsonify(ConfigService.validate_config_data(data))

    @app.route('/api/env-vars', methods=['GET'])
    def get_env_vars():
        """获取当前系统环境变量"""
        vars_data = EnvService.get_current_env_vars()
        return jsonify({
            'success': True,
            'vars': vars_data
        })

    @app.route('/api/export', methods=['GET'])
    def export_configs():
        """导出配置"""
        result = ConfigService.export_configs()
        if result['success']:
            return jsonify(result['data'])
        else:
            return jsonify({'success': False, 'message': result['message']})

    @app.route('/api/import', methods=['POST'])
    def import_configs():
        """导入配置"""
        data = request.json
        return jsonify(ConfigService.import_configs(data))

    return app