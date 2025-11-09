"""
脚本执行器模块
用于调用PowerShell或CMD脚本执行系统级操作
"""
import subprocess
import json
import os
import sys
from pathlib import Path


class ScriptExecutor:
    """脚本执行器，用于执行PowerShell和CMD脚本"""

    def __init__(self):
        self.scripts_dir = Path(__file__).parent.parent / 'scripts'
        self.scripts_dir.mkdir(exist_ok=True)

    def _normalize_output_keys(self, data):
        """递归地将返回结果的键名统一为小写，便于调用方处理"""
        if isinstance(data, dict):
            normalized = {}
            for key, value in data.items():
                new_key = key.lower() if isinstance(key, str) else key
                normalized[new_key] = self._normalize_output_keys(value)
            return normalized
        if isinstance(data, list):
            return [self._normalize_output_keys(item) for item in data]
        return data

    def execute_powershell_script(self, script_name, parameters=None, timeout=30):
        """
        执行PowerShell脚本

        Args:
            script_name (str): 脚本文件名
            parameters (dict): 传递给脚本的参数
            timeout (int): 超时时间（秒）

        Returns:
            dict: 执行结果
        """
        script_path = self.scripts_dir / script_name
        if not script_path.exists():
            return {
                'success': False,
                'message': f'Script not found: {script_path}',
                'error': 'File not found'
            }

        try:
            # 构建PowerShell命令
            ps_command = [
                'powershell',
                '-ExecutionPolicy', 'Bypass',
                '-File', str(script_path)
            ]

            # 添加参数
            if parameters:
                for key, value in parameters.items():
                    ps_command.extend(['-' + key, str(value)])

            # 执行脚本
            result = subprocess.run(
                ps_command,
                capture_output=True,
                text=True,
                timeout=timeout,
                encoding='gbk',
                errors='ignore'
            )

            if result.returncode == 0:
                try:
                    # 尝试解析JSON输出，并统一键名大小写
                    output_data = json.loads(result.stdout.strip())
                    return self._normalize_output_keys(output_data)
                except json.JSONDecodeError:
                    return {
                        'success': True,
                        'message': 'Script executed successfully',
                        'output': result.stdout.strip()
                    }
            else:
                return {
                    'success': False,
                    'message': 'Script execution failed',
                    'error': result.stderr.strip(),
                    'return_code': result.returncode
                }

        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'message': f'Script execution timed out after {timeout} seconds',
                'error': 'Timeout'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Failed to execute script: {str(e)}',
                'error': str(e)
            }

    def execute_cmd_script(self, script_name, parameters=None, timeout=30):
        """
        执行CMD脚本

        Args:
            script_name (str): 脚本文件名
            parameters (dict): 传递给脚本的参数
            timeout (int): 超时时间（秒）

        Returns:
            dict: 执行结果
        """
        script_path = self.scripts_dir / script_name
        if not script_path.exists():
            return {
                'success': False,
                'message': f'Script not found: {script_path}',
                'error': 'File not found'
            }

        try:
            # 构建CMD命令
            cmd_command = ['cmd', '/c', str(script_path)]

            # 添加参数（通过环境变量传递）
            env = os.environ.copy()
            if parameters:
                for key, value in parameters.items():
                    env[key.upper()] = str(value)

            # 执行脚本
            result = subprocess.run(
                cmd_command,
                capture_output=True,
                text=True,
                timeout=timeout,
                encoding='gbk',
                errors='ignore',
                env=env
            )

            if result.returncode == 0:
                try:
                    # 尝试解析JSON输出
                    output_data = json.loads(result.stdout.strip())
                    return output_data
                except json.JSONDecodeError:
                    return {
                        'success': True,
                        'message': 'Script executed successfully',
                        'output': result.stdout.strip()
                    }
            else:
                return {
                    'success': False,
                    'message': 'Script execution failed',
                    'error': result.stderr.strip(),
                    'return_code': result.returncode
                }

        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'message': f'Script execution timed out after {timeout} seconds',
                'error': 'Timeout'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Failed to execute script: {str(e)}',
                'error': str(e)
            }

    def set_environment_variable(self, var_name, var_value, scope='User'):
        """
        设置环境变量

        Args:
            var_name (str): 变量名
            var_value (str): 变量值
            scope (str): 作用域 ('User' 或 'Machine')

        Returns:
            dict: 执行结果
        """
        return self.execute_powershell_script(
            'Set-EnvironmentVariable.ps1',
            {
                'Name': var_name,
                'Value': var_value,
                'Scope': scope,
                'Action': 'Set'
            }
        )

    def get_environment_variable(self, var_name, scope='User'):
        """
        获取环境变量

        Args:
            var_name (str): 变量名
            scope (str): 作用域 ('User' 或 'Machine')

        Returns:
            dict: 执行结果
        """
        return self.execute_powershell_script(
            'Set-EnvironmentVariable.ps1',
            {
                'Name': var_name,
                'Scope': scope,
                'Action': 'Get'
            }
        )

    def delete_environment_variable(self, var_name, scope='User'):
        """
        删除环境变量

        Args:
            var_name (str): 变量名
            scope (str): 作用域 ('User' 或 'Machine')

        Returns:
            dict: 执行结果
        """
        return self.execute_powershell_script(
            'Set-EnvironmentVariable.ps1',
            {
                'Name': var_name,
                'Scope': scope,
                'Action': 'Delete'
            }
        )

    def list_environment_variables(self, scope='User'):
        """
        列出环境变量

        Args:
            scope (str): 作用域 ('User' 或 'Machine')

        Returns:
            dict: 执行结果
        """
        return self.execute_powershell_script(
            'Set-EnvironmentVariable.ps1',
            {
                'Scope': scope,
                'Action': 'List'
            }
        )


# 创建全局执行器实例
script_executor = ScriptExecutor()
