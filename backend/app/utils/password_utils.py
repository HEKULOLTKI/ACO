"""
密码工具模块
提供明文密码获取和生成功能
"""
import hashlib
from typing import Optional, Dict
from app.utils.redis_client import redis_client

class PasswordUtils:
    """密码工具类"""
    
    # 已知用户的明文密码映射表（用于开发/测试环境）
    KNOWN_PASSWORDS = {
        "admin": "123456",
        "user3": "123456",
        "user2": "123456",
        "user1": "123456"
    }
    
    @staticmethod
    def get_plain_password(username: str, user_id: int, password_hash: str) -> str:
        """
        获取用户的明文密码
        
        Args:
            username: 用户名
            user_id: 用户ID
            password_hash: 加密后的密码哈希
            
        Returns:
            明文密码字符串
        """
        # 方法1: 从已知密码表中获取
        if username in PasswordUtils.KNOWN_PASSWORDS:
            return PasswordUtils.KNOWN_PASSWORDS[username]
        
        # 方法2: 尝试从Redis登录记录中获取最近的密码
        try:
            login_records = redis_client.get_login_records(user_id, limit=5)
            for record in login_records:
                if record.get('status') == 'success' and 'plain_password' in record:
                    return record['plain_password']
        except Exception:
            pass
        
        # 方法3: 根据用户名生成可预测的密码
        if username.startswith('admin'):
            return "admin123"
        elif username.startswith('user'):
            return f"{username}123"
        elif username.startswith('test'):
            return "test123"
        
        # 方法4: 使用系统默认密码
        return "123456"
    
    @staticmethod
    def generate_user_password(username: str, user_type: str = None) -> str:
        """
        根据用户信息生成合适的密码
        
        Args:
            username: 用户名
            user_type: 用户类型
            
        Returns:
            生成的密码
        """
        if user_type == "管理员":
            return f"{username}_admin123"
        elif user_type == "操作员":
            return f"{username}_op123"
        else:
            return f"{username}_123"
    
    @staticmethod
    def create_password_mapping(users_list: list) -> Dict[str, str]:
        """
        为用户列表创建密码映射
        
        Args:
            users_list: 用户列表
            
        Returns:
            用户名到密码的映射字典
        """
        password_mapping = {}
        
        for user in users_list:
            username = user.get('username') if isinstance(user, dict) else user.username
            user_id = user.get('id') if isinstance(user, dict) else user.id
            password_hash = user.get('password') if isinstance(user, dict) else user.password
            
            password_mapping[username] = PasswordUtils.get_plain_password(
                username, user_id, password_hash
            )
        
        return password_mapping
    
    @staticmethod
    def store_login_password(user_id: int, username: str, plain_password: str):
        """
        在用户登录时存储明文密码到Redis（仅用于开发环境）
        
        Args:
            user_id: 用户ID
            username: 用户名
            plain_password: 明文密码
        """
        try:
            # 先清除该用户之前的密码缓存
            PasswordUtils.clear_user_password_cache(user_id)
            
            # 创建包含明文密码的登录记录
            import time
            import json
            from datetime import datetime
            
            record = {
                "user_id": user_id,
                "username": username,
                "plain_password": plain_password,
                "timestamp": time.time(),
                "datetime": datetime.now().isoformat(),
                "type": "login_password_cache",
                "session_start": True
            }
            
            # 存储到专门的密码备份列表
            redis_client.redis_client.lpush(f"password_backup:{user_id}", json.dumps(record))
            redis_client.redis_client.ltrim(f"password_backup:{user_id}", 0, 0)  # 只保留最新1条
            redis_client.redis_client.expire(f"password_backup:{user_id}", 7200)  # 2小时过期
            
            # 同时更新已知密码表（用于开发环境）
            PasswordUtils.KNOWN_PASSWORDS[username] = plain_password
            
            print(f"✅ 已存储用户 {username} 的登录密码缓存")
            
        except Exception as e:
            print(f"❌ 存储密码备份失败: {e}")
    
    @staticmethod
    def clear_user_password_cache(user_id: int):
        """
        清除指定用户的密码缓存
        
        Args:
            user_id: 用户ID
        """
        try:
            # 删除密码备份
            backup_key = f"password_backup:{user_id}"
            reset_key = f"password_reset:{user_id}"
            
            deleted_count = 0
            if redis_client.redis_client.exists(backup_key):
                redis_client.redis_client.delete(backup_key)
                deleted_count += 1
                
            if redis_client.redis_client.exists(reset_key):
                redis_client.redis_client.delete(reset_key)
                deleted_count += 1
            
            print(f"✅ 清除用户 {user_id} 的 {deleted_count} 个密码缓存")
            return deleted_count
            
        except Exception as e:
            print(f"❌ 清除用户 {user_id} 的密码缓存失败: {e}")
            return 0
    
    @staticmethod
    def record_password_reset(user_id: int, username: str, new_password: str):
        """
        记录密码重置操作（用于管理和审计）
        
        Args:
            user_id: 用户ID
            username: 用户名  
            new_password: 新密码
        """
        try:
            import time
            import json
            from datetime import datetime
            
            # 更新已知密码表
            PasswordUtils.KNOWN_PASSWORDS[username] = new_password
            
            # 记录重置操作
            reset_record = {
                "user_id": user_id,
                "username": username,
                "new_password": new_password,
                "reset_time": time.time(),
                "reset_datetime": datetime.now().isoformat(),
                "type": "password_reset"
            }
            
            # 存储重置记录
            redis_client.redis_client.lpush(f"password_reset:{user_id}", json.dumps(reset_record))
            redis_client.redis_client.ltrim(f"password_reset:{user_id}", 0, 9)  # 保留最近10条
            redis_client.redis_client.expire(f"password_reset:{user_id}", 86400)  # 24小时过期
            
            print(f"✅ 已记录用户 {username} 的密码重置操作")
            
        except Exception as e:
            print(f"记录密码重置失败: {e}")
    
    @staticmethod
    def get_stored_password(user_id: int) -> Optional[str]:
        """
        从Redis中获取存储的明文密码
        
        Args:
            user_id: 用户ID
            
        Returns:
            明文密码或None
        """
        try:
            import json
            records = redis_client.redis_client.lrange(f"password_backup:{user_id}", 0, 0)
            if records:
                record = json.loads(records[0])
                return record.get('plain_password')
        except Exception:
            pass
        
        return None 