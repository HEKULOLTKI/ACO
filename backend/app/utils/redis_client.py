import redis
import json
import time
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from app.config import settings


class RedisClient:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=getattr(settings, 'REDIS_HOST', 'localhost'),
            port=getattr(settings, 'REDIS_PORT', 6379),
            db=getattr(settings, 'REDIS_DB', 0),
            password=getattr(settings, 'REDIS_PASSWORD', None),
            decode_responses=True
        )
    
    def ping(self) -> bool:
        """检查Redis连接状态"""
        try:
            self.redis_client.ping()
            return True
        except Exception:
            return False
    
    def set_user_online(self, user_id: int, username: str, ip: str, user_agent: str):
        """设置用户在线状态"""
        try:
            current_time = time.time()
            
            # 设置用户在线信息 - 使用兼容性更好的方式
            pipeline = self.redis_client.pipeline()
            pipeline.hset(f"user:online:{user_id}", "user_id", user_id)
            pipeline.hset(f"user:online:{user_id}", "username", username)
            pipeline.hset(f"user:online:{user_id}", "ip", ip)
            pipeline.hset(f"user:online:{user_id}", "user_agent", user_agent)
            pipeline.hset(f"user:online:{user_id}", "login_time", current_time)
            pipeline.hset(f"user:online:{user_id}", "last_activity", current_time)
            
            # 添加到在线用户集合
            pipeline.sadd("online_users", user_id)
            
            # 设置过期时间（30分钟无活动自动下线）
            pipeline.expire(f"user:online:{user_id}", 1800)
            
            pipeline.execute()
            
        except Exception as e:
            print(f"设置用户在线状态失败: {e}")
            # 回退到单个命令方式
            try:
                current_time = time.time()
                self.redis_client.hset(f"user:online:{user_id}", "user_id", str(user_id))
                self.redis_client.hset(f"user:online:{user_id}", "username", username)
                self.redis_client.hset(f"user:online:{user_id}", "ip", ip)
                self.redis_client.hset(f"user:online:{user_id}", "user_agent", user_agent)
                self.redis_client.hset(f"user:online:{user_id}", "login_time", str(current_time))
                self.redis_client.hset(f"user:online:{user_id}", "last_activity", str(current_time))
                self.redis_client.sadd("online_users", user_id)
                self.redis_client.expire(f"user:online:{user_id}", 1800)
                print(f"使用回退方式成功设置用户 {user_id} 在线状态")
            except Exception as fallback_e:
                print(f"回退方式也失败: {fallback_e}")
    
    def set_user_offline(self, user_id: int):
        """设置用户离线状态"""
        try:
            # 删除用户在线信息
            self.redis_client.delete(f"user:online:{user_id}")
            
            # 从在线用户集合中移除
            self.redis_client.srem("online_users", user_id)
            
        except Exception as e:
            print(f"设置用户离线状态失败: {e}")
    
    def is_user_online(self, user_id: int) -> bool:
        """检查用户是否在线"""
        try:
            return self.redis_client.exists(f"user:online:{user_id}") > 0
        except Exception:
            return False
    
    def get_user_online_info(self, user_id: int) -> Optional[Dict[str, Any]]:
        """获取用户在线信息"""
        try:
            user_info = self.redis_client.hgetall(f"user:online:{user_id}")
            if user_info:
                # 转换时间戳为可读格式
                user_info['login_time'] = float(user_info.get('login_time', 0))
                user_info['last_activity'] = float(user_info.get('last_activity', 0))
                user_info['user_id'] = int(user_info.get('user_id', 0))
                return user_info
            return None
        except Exception as e:
            print(f"获取用户在线信息失败: {e}")
            return None
    
    def get_user_ip(self, user_id: int) -> Optional[str]:
        """获取用户IP地址"""
        try:
            return self.redis_client.hget(f"user:online:{user_id}", "ip")
        except Exception:
            return None
    
    def update_user_activity(self, user_id: int):
        """更新用户活动时间"""
        try:
            if self.is_user_online(user_id):
                self.redis_client.hset(f"user:online:{user_id}", "last_activity", str(time.time()))
                # 重新设置过期时间
                self.redis_client.expire(f"user:online:{user_id}", 1800)
        except Exception as e:
            print(f"更新用户活动时间失败: {e}")
    
    def get_online_users(self) -> List[Dict[str, Any]]:
        """获取所有在线用户"""
        try:
            online_user_ids = self.redis_client.smembers("online_users")
            online_users = []
            
            for user_id in online_user_ids:
                user_info = self.get_user_online_info(int(user_id))
                if user_info:
                    online_users.append(user_info)
                else:
                    # 如果用户信息不存在，从集合中移除
                    self.redis_client.srem("online_users", user_id)
            
            return online_users
        except Exception as e:
            print(f"获取在线用户失败: {e}")
            return []
    
    def get_online_users_count(self) -> int:
        """获取在线用户数量"""
        try:
            return self.redis_client.scard("online_users")
        except Exception:
            return 0
    
    def add_login_record(self, user_id: int, ip: str, user_agent: str, status: str):
        """添加登录记录"""
        try:
            record = {
                "user_id": user_id,
                "ip": ip,
                "user_agent": user_agent,
                "status": status,
                "timestamp": time.time(),
                "datetime": datetime.now().isoformat()
            }
            
            # 添加到用户登录记录列表
            self.redis_client.lpush(f"login_records:{user_id}", json.dumps(record))
            
            # 只保留最近100条记录
            self.redis_client.ltrim(f"login_records:{user_id}", 0, 99)
            
            # 设置过期时间（30天）
            self.redis_client.expire(f"login_records:{user_id}", 2592000)
            
        except Exception as e:
            print(f"添加登录记录失败: {e}")
    
    def get_login_records(self, user_id: int, limit: int = 20) -> List[Dict[str, Any]]:
        """获取用户登录记录"""
        try:
            records = self.redis_client.lrange(f"login_records:{user_id}", 0, limit - 1)
            return [json.loads(record) for record in records]
        except Exception as e:
            print(f"获取登录记录失败: {e}")
            return []
    
    def cleanup_expired_users(self):
        """清理过期的在线用户"""
        try:
            online_user_ids = self.redis_client.smembers("online_users")
            for user_id in online_user_ids:
                if not self.redis_client.exists(f"user:online:{user_id}"):
                    self.redis_client.srem("online_users", user_id)
        except Exception as e:
            print(f"清理过期用户失败: {e}")


# 创建全局Redis客户端实例
redis_client = RedisClient() 