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
            
            # 设置过期时间（1小时无活动自动下线）
            pipeline.expire(f"user:online:{user_id}", 3600)
            
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
                self.redis_client.expire(f"user:online:{user_id}", 3600)
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
                # 重新设置过期时间（1小时）
                self.redis_client.expire(f"user:online:{user_id}", 3600)
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
            expired_users = []
            
            for user_id in online_user_ids:
                user_key = f"user:online:{user_id}"
                
                # 检查用户在线记录是否仍然存在
                if not self.redis_client.exists(user_key):
                    # 用户记录已过期，从在线用户集合中移除
                    self.redis_client.srem("online_users", user_id)
                    expired_users.append(user_id)
                    continue
                
                # 检查用户最后活动时间
                user_info = self.redis_client.hgetall(user_key)
                if user_info and 'last_activity' in user_info:
                    try:
                        last_activity = float(user_info['last_activity'])
                        current_time = time.time()
                        
                        # 如果超过1小时无活动，手动设置用户离线
                        if current_time - last_activity > 3600:
                            self.set_user_offline(int(user_id))
                            expired_users.append(user_id)
                            print(f"用户 {user_id} 因超时无活动被自动下线")
                    except (ValueError, TypeError):
                        # 数据格式错误，清理该用户
                        self.set_user_offline(int(user_id))
                        expired_users.append(user_id)
            
            if expired_users:
                print(f"清理了 {len(expired_users)} 个过期用户: {expired_users}")
                
        except Exception as e:
            print(f"清理过期用户失败: {e}")
    
    def check_user_activity_timeout(self, user_id: int) -> bool:
        """检查用户是否因无活动超时"""
        try:
            user_info = self.get_user_online_info(user_id)
            if not user_info:
                return True  # 用户不在线，视为超时
            
            current_time = time.time()
            last_activity = user_info.get('last_activity', 0)
            
            # 超过1小时无活动
            return current_time - last_activity > 3600
            
        except Exception as e:
            print(f"检查用户活动超时失败: {e}")
            return False
    
    def get_user_online_duration(self, user_id: int) -> dict:
        """获取用户在线时长信息"""
        try:
            user_info = self.get_user_online_info(user_id)
            if not user_info:
                return {"online": False, "duration": 0, "remaining_time": 0}
            
            current_time = time.time()
            login_time = user_info.get('login_time', current_time)
            last_activity = user_info.get('last_activity', current_time)
            
            # 计算在线时长（秒）
            online_duration = current_time - login_time
            
            # 计算剩余在线时间（1小时减去无活动时间）
            inactive_duration = current_time - last_activity
            remaining_time = max(0, 3600 - inactive_duration)
            
            return {
                "online": True,
                "online_duration": int(online_duration),
                "inactive_duration": int(inactive_duration),
                "remaining_time": int(remaining_time),
                "will_expire_at": last_activity + 3600
            }
            
        except Exception as e:
            print(f"获取用户在线时长失败: {e}")
            return {"online": False, "duration": 0, "remaining_time": 0}
    
    # ===== 聊天相关功能 =====
    
    def save_chat_message(self, room_id: str, message_data: Dict[str, Any]):
        """保存聊天消息到Redis"""
        try:
            # 将消息添加到聊天室消息列表
            self.redis_client.lpush(f"chat:messages:{room_id}", json.dumps(message_data))
            
            # 只保留最近1000条消息
            self.redis_client.ltrim(f"chat:messages:{room_id}", 0, 999)
            
            # 设置过期时间（7天）
            self.redis_client.expire(f"chat:messages:{room_id}", 604800)
            
            # 更新聊天室最后活动时间
            self.redis_client.hset(f"chat:room:{room_id}", "last_activity", time.time())
            
            # 增加今日消息计数
            today = datetime.now().strftime("%Y-%m-%d")
            self.redis_client.incr(f"chat:stats:messages:{today}")
            self.redis_client.expire(f"chat:stats:messages:{today}", 86400 * 30)  # 30天过期
            
        except Exception as e:
            print(f"保存聊天消息失败: {e}")
    
    def get_chat_messages(self, room_id: str, limit: int = 50, before: Optional[str] = None) -> List[Dict[str, Any]]:
        """获取聊天消息"""
        try:
            if before:
                # 如果指定了before参数，需要找到该消息的位置然后获取之前的消息
                messages = self.redis_client.lrange(f"chat:messages:{room_id}", 0, -1)
                all_messages = [json.loads(msg) for msg in messages]
                
                # 找到before消息的索引
                before_index = -1
                for i, msg in enumerate(all_messages):
                    if msg.get('id') == before:
                        before_index = i
                        break
                
                if before_index >= 0:
                    # 返回before索引之后的消息（更早的消息）
                    start_index = before_index + 1
                    end_index = min(start_index + limit, len(all_messages))
                    return all_messages[start_index:end_index]
                else:
                    return []
            else:
                # 获取最新的消息
                messages = self.redis_client.lrange(f"chat:messages:{room_id}", 0, limit - 1)
                return [json.loads(msg) for msg in messages]
        except Exception as e:
            print(f"获取聊天消息失败: {e}")
            return []
    
    def get_chat_rooms(self) -> List[str]:
        """获取所有聊天室ID"""
        try:
            # 通过模式匹配获取所有聊天室
            room_keys = self.redis_client.keys("chat:room:*")
            return [key.replace("chat:room:", "") for key in room_keys]
        except Exception as e:
            print(f"获取聊天室列表失败: {e}")
            return []
    
    def create_chat_room(self, room_id: str, room_name: str, description: str = "", creator_id: int = 0):
        """创建聊天室"""
        try:
            room_data = {
                "id": room_id,
                "name": room_name,
                "description": description,
                "creator_id": creator_id,
                "created_at": time.time(),
                "last_activity": time.time(),
                "member_count": 0
            }
            
            # 保存聊天室信息
            for key, value in room_data.items():
                self.redis_client.hset(f"chat:room:{room_id}", key, str(value))
            
            # 添加到聊天室列表
            self.redis_client.sadd("chat:rooms", room_id)
            
        except Exception as e:
            print(f"创建聊天室失败: {e}")
    
    def join_chat_room(self, room_id: str, user_id: int):
        """用户加入聊天室"""
        try:
            # 添加用户到聊天室成员
            self.redis_client.sadd(f"chat:room:{room_id}:members", user_id)
            
            # 更新成员数量
            member_count = self.redis_client.scard(f"chat:room:{room_id}:members")
            self.redis_client.hset(f"chat:room:{room_id}", "member_count", member_count)
            
            # 添加用户的聊天室列表
            self.redis_client.sadd(f"user:{user_id}:chat_rooms", room_id)
            
        except Exception as e:
            print(f"加入聊天室失败: {e}")
    
    def leave_chat_room(self, room_id: str, user_id: int):
        """用户离开聊天室"""
        try:
            # 从聊天室成员中移除用户
            self.redis_client.srem(f"chat:room:{room_id}:members", user_id)
            
            # 更新成员数量
            member_count = self.redis_client.scard(f"chat:room:{room_id}:members")
            self.redis_client.hset(f"chat:room:{room_id}", "member_count", member_count)
            
            # 从用户的聊天室列表中移除
            self.redis_client.srem(f"user:{user_id}:chat_rooms", room_id)
            
        except Exception as e:
            print(f"离开聊天室失败: {e}")
    
    def get_room_members(self, room_id: str) -> List[int]:
        """获取聊天室成员"""
        try:
            members = self.redis_client.smembers(f"chat:room:{room_id}:members")
            return [int(member) for member in members]
        except Exception as e:
            print(f"获取聊天室成员失败: {e}")
            return []
    
    def get_user_chat_rooms(self, user_id: int) -> List[str]:
        """获取用户加入的聊天室"""
        try:
            return list(self.redis_client.smembers(f"user:{user_id}:chat_rooms"))
        except Exception as e:
            print(f"获取用户聊天室失败: {e}")
            return []
    
    def get_chat_stats(self) -> Dict[str, Any]:
        """获取聊天统计信息"""
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            
            stats = {
                "online_users_count": self.get_online_users_count(),
                "total_messages_today": int(self.redis_client.get(f"chat:stats:messages:{today}") or 0),
                "active_rooms": self.redis_client.scard("chat:rooms")
            }
            
            return stats
        except Exception as e:
            print(f"获取聊天统计失败: {e}")
            return {"online_users_count": 0, "total_messages_today": 0, "active_rooms": 0}
    
    def delete_chat_message(self, room_id: str, message_id: str, user_id: int):
        """删除聊天消息（软删除）"""
        try:
            # 获取所有消息
            messages = self.redis_client.lrange(f"chat:messages:{room_id}", 0, -1)
            
            # 找到要删除的消息并标记为已删除
            for i, msg_str in enumerate(messages):
                msg = json.loads(msg_str)
                if msg.get('id') == message_id and msg.get('sender_id') == user_id:
                    msg['deleted'] = True
                    msg['deleted_at'] = time.time()
                    # 更新消息
                    self.redis_client.lset(f"chat:messages:{room_id}", i, json.dumps(msg))
                    break
                    
        except Exception as e:
            print(f"删除聊天消息失败: {e}")


# 创建全局Redis客户端实例
redis_client = RedisClient() 