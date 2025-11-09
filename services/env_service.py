"""
环境变量服务
"""
from config.settings import ENV_VARS
from core.script_executor import script_executor


def get_env_var(var_name):
    """获取系统环境变量值（备用方法）"""
    try:
        import os
        return os.environ.get(var_name, '')
    except:
        return ''


def get_all_current_env_vars(env_vars):
    """获取所有当前系统环境变量（备用方法）"""
    result = {}
    for var_name in env_vars:
        result[var_name] = get_env_var(var_name)
    return result


class EnvService:
    """环境变量服务"""

    @staticmethod
    def get_current_env_vars():
        """获取当前系统环境变量"""
        # 优先使用脚本方式获取（更准确）
        vars_data = {}
        for var_name in ENV_VARS:
            result = script_executor.get_environment_variable(var_name, 'User')
            if result.get('success'):
                vars_data[var_name] = result.get('value', '')
            else:
                # 备用方法：使用原来的注册表方式
                vars_data[var_name] = get_env_var(var_name)

        return vars_data

    @staticmethod
    def apply_config(config):
        """应用配置到系统环境变量"""
        results = []
        success_count = 0
        errors = []

        for var_name in ENV_VARS:
            var_value = config.get(var_name, '')

            # 使用PowerShell脚本设置环境变量
            result = script_executor.set_environment_variable(var_name, var_value, 'User')

            success = result.get('success', False)
            message = result.get('message', 'Unknown error')

            results.append({
                'var_name': var_name,
                'success': success,
                'message': message,
                'var_value': var_value
            })

            if success:
                success_count += 1
            else:
                errors.append(f"{var_name}: {message}")

        return {
            'success': success_count == len(ENV_VARS),
            'success_count': success_count,
            'total_count': len(ENV_VARS),
            'results': results,
            'errors': errors,
            'method': 'PowerShell Script'
        }

    @staticmethod
    def test_environment_variable_access():
        """测试环境变量访问权限"""
        test_var = "__TEST_VAR__"
        test_value = "test_value_" + str(hash(test_var))

        # 尝试设置测试变量
        set_result = script_executor.set_environment_variable(test_var, test_value, 'User')

        if not set_result.get('success'):
            return {
                'can_modify': False,
                'method': 'PowerShell Script',
                'error': set_result.get('message', 'Unknown error'),
                'recommendation': 'Try running the application as administrator'
            }

        # 尝试获取测试变量
        get_result = script_executor.get_environment_variable(test_var, 'User')

        if not get_result.get('success'):
            return {
                'can_modify': False,
                'method': 'PowerShell Script',
                'error': 'Cannot read environment variable',
                'recommendation': 'Check PowerShell execution policy'
            }

        # 清理测试变量
        script_executor.delete_environment_variable(test_var, 'User')

        retrieved_value = get_result.get('value', '')
        if retrieved_value == test_value:
            return {
                'can_modify': True,
                'method': 'PowerShell Script',
                'test_result': 'Environment variable access test successful'
            }
        else:
            return {
                'can_modify': False,
                'method': 'PowerShell Script',
                'error': f'Value mismatch: expected {test_value}, got {retrieved_value}',
                'recommendation': 'Check PowerShell execution permissions'
            }