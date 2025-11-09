"""
权限管理模块
"""
import os
import sys
import ctypes
import subprocess


def is_admin():
    """检查是否具有管理员权限"""
    try:
        # 使用更可靠的权限检测方法
        return ctypes.windll.shell.IsUserAnAdmin()
    except Exception:
        # 备用检测方法：尝试写入系统目录
        try:
            temp_file = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'temp_admin_test.txt')
            with open(temp_file, 'w') as f:
                f.write('test')
            os.remove(temp_file)
            return True
        except:
            return False


def can_modify_user_env():
    """检查是否能修改用户环境变量"""
    try:
        import winreg
        # 尝试打开用户环境变量的注册表项进行写入测试
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Environment', 0, winreg.KEY_WRITE)
        winreg.CloseKey(key)
        return True
    except:
        return False


def request_admin_privilege(script_path=None):
    """请求管理员权限（调用UAC）"""
    if not is_admin():
        try:
            if script_path is None:
                script_path = sys.argv[0] if sys.argv else os.path.abspath(__file__)

            # 获取脚本所在目录
            script_dir = os.path.dirname(os.path.abspath(script_path))

            # 使用ShellExecuteW进行UAC提升
            ctypes.windll.shell32.ShellExecuteW(
                None,
                'runas',  # 动词：以管理员身份运行
                sys.executable,
                f'"{script_path}"',
                script_dir,
                1  # SW_SHOWNORMAL
            )
            return True
        except Exception as e:
            print(f"Failed to request admin privileges: {e}")
            return False
    else:
        return True


def get_current_privilege_level():
    """获取当前权限级别的描述"""
    if is_admin():
        return "Administrator"
    elif can_modify_user_env():
        return "User (can modify environment variables)"
    else:
        return "Limited User"


def check_runtime_privilege():
    """运行时权限检查，返回权限信息和建议"""
    admin_status = is_admin()
    env_modify_status = can_modify_user_env()

    return {
        'is_admin': admin_status,
        'can_modify_env': env_modify_status,
        'level': get_current_privilege_level(),
        'recommendations': get_privilege_recommendations(admin_status, env_modify_status)
    }


def get_privilege_recommendations(is_admin, can_modify_env):
    """获取权限建议"""
    recommendations = []

    if not is_admin and not can_modify_env:
        recommendations.append({
            'type': 'error',
            'message': 'Cannot modify environment variables. Run as administrator.'
        })
    elif not is_admin and can_modify_env:
        recommendations.append({
            'type': 'warning',
            'message': 'Can modify user environment variables only. Some features may be limited.'
        })
    else:
        recommendations.append({
            'type': 'success',
            'message': 'Full administrator privileges available.'
        })

    return recommendations