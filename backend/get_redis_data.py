
#!/usr/bin/env python3
"""
Redis数据查看工具
获取并显示Redis中的所有数据
"""

import redis
import json
import time
from datetime import datetime
from typing import Dict, List, Any
from app.config import settings


def format_timestamp(timestamp):
    """格式化时间戳"""
    try:
        if isinstance(timestamp, str):
            timestamp = float(timestamp)
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    except:
        return str(timestamp)


def get_redis_data():
    """获取Redis中的所有数据"""
    try:
        # 连接Redis
        redis_client = redis.Redis(
            host=getattr(settings, 'REDIS_HOST', 'localhost'),
            port=getattr(settings, 'REDIS_PORT', 6379),
            db=getattr(settings, 'REDIS_DB', 0),
            password=getattr(settings, 'REDIS_PASSWORD', None),
            decode_responses=True
        )
        
        # 测试连接
        redis_client.ping()
        print("✅ Redis连接成功")
        print("=" * 60)
        
        # 获取所有键
        all_keys = redis_client.keys('*')
        print(f"📊 Redis中共有 {len(all_keys)} 个键")
        
        if not all_keys:
            print("❌ Redis中没有数据")
            return
        
        print("\n🔍 Redis数据详情:")
        print("=" * 60)
        
        # 按类型分组显示数据
        user_online_keys = []
        login_record_keys = []
        other_keys = []
        
        for key in all_keys:
            if key.startswith('user:online:'):
                user_online_keys.append(key)
            elif key.startswith('login_records:'):
                login_record_keys.append(key)
            else:
                other_keys.append(key)
        
        # 显示在线用户信息
        if user_online_keys:
            print("\n👥 在线用户信息:")
            print("-" * 40)
            for key in sorted(user_online_keys):
                user_data = redis_client.hgetall(key)
                if user_data:
                    user_id = user_data.get('user_id', 'N/A')
                    username = user_data.get('username', 'N/A')
                    ip = user_data.get('ip', 'N/A')
                    login_time = format_timestamp(user_data.get('login_time', 0))
                    last_activity = format_timestamp(user_data.get('last_activity', 0))
                    
                    print(f"🔑 键: {key}")
                    print(f"   用户ID: {user_id}")
                    print(f"   用户名: {username}")
                    print(f"   IP地址: {ip}")
                    print(f"   登录时间: {login_time}")
                    print(f"   最后活动: {last_activity}")
                    print(f"   用户代理: {user_data.get('user_agent', 'N/A')}")
                    
                    # 检查TTL
                    ttl = redis_client.ttl(key)
                    if ttl > 0:
                        print(f"   ⏰ 过期时间: {ttl}秒")
                    elif ttl == -1:
                        print(f"   ⏰ 永不过期")
                    else:
                        print(f"   ⏰ 已过期或不存在")
                    print()
        
        # 显示登录记录
        if login_record_keys:
            print("\n📝 登录记录:")
            print("-" * 40)
            for key in sorted(login_record_keys):
                records = redis_client.lrange(key, 0, -1)
                user_id = key.split(':')[1]
                print(f"🔑 键: {key} (用户ID: {user_id})")
                print(f"   记录数量: {len(records)}")
                
                if records:
                    print("   最近的记录:")
                    for i, record_str in enumerate(records[:3]):  # 只显示前3条
                        try:
                            record = json.loads(record_str)
                            timestamp = format_timestamp(record.get('timestamp', 0))
                            print(f"     {i+1}. {timestamp} - {record.get('status', 'N/A')} - IP: {record.get('ip', 'N/A')}")
                        except:
                            print(f"     {i+1}. {record_str}")
                    
                    if len(records) > 3:
                        print(f"     ... 还有 {len(records) - 3} 条记录")
                
                # 检查TTL
                ttl = redis_client.ttl(key)
                if ttl > 0:
                    print(f"   ⏰ 过期时间: {ttl}秒")
                elif ttl == -1:
                    print(f"   ⏰ 永不过期")
                print()
        
        # 显示其他数据
        if other_keys:
            print("\n🔧 其他数据:")
            print("-" * 40)
            for key in sorted(other_keys):
                key_type = redis_client.type(key)
                ttl = redis_client.ttl(key)
                
                print(f"🔑 键: {key}")
                print(f"   类型: {key_type}")
                
                if key_type == 'string':
                    value = redis_client.get(key)
                    print(f"   值: {value}")
                elif key_type == 'list':
                    length = redis_client.llen(key)
                    print(f"   长度: {length}")
                    if length > 0:
                        first_item = redis_client.lindex(key, 0)
                        print(f"   第一个元素: {first_item}")
                elif key_type == 'set':
                    members = redis_client.smembers(key)
                    print(f"   成员数量: {len(members)}")
                    print(f"   成员: {list(members)}")
                elif key_type == 'hash':
                    hash_data = redis_client.hgetall(key)
                    print(f"   字段数量: {len(hash_data)}")
                    print(f"   数据: {hash_data}")
                elif key_type == 'zset':
                    zset_data = redis_client.zrange(key, 0, -1, withscores=True)
                    print(f"   成员数量: {len(zset_data)}")
                    print(f"   数据: {zset_data}")
                
                if ttl > 0:
                    print(f"   ⏰ 过期时间: {ttl}秒")
                elif ttl == -1:
                    print(f"   ⏰ 永不过期")
                print()
        
        # 显示在线用户集合
        online_users_set = redis_client.smembers('online_users')
        if online_users_set:
            print(f"\n👥 在线用户集合 (online_users): {list(online_users_set)}")
        
        # 显示Redis信息
        print("\n📈 Redis服务器信息:")
        print("-" * 40)
        info = redis_client.info()
        print(f"Redis版本: {info.get('redis_version', 'N/A')}")
        print(f"已用内存: {info.get('used_memory_human', 'N/A')}")
        print(f"连接数: {info.get('connected_clients', 'N/A')}")
        print(f"键空间: {info.get('db0', 'N/A')}")
        
    except redis.ConnectionError:
        print("❌ 无法连接到Redis服务器")
        print("请检查Redis是否运行以及配置是否正确")
    except Exception as e:
        print(f"❌ 获取Redis数据时出错: {e}")


def clear_redis_data():
    """清理Redis中的所有数据"""
    try:
        # 连接Redis
        redis_client = redis.Redis(
            host=getattr(settings, 'REDIS_HOST', 'localhost'),
            port=getattr(settings, 'REDIS_PORT', 6379),
            db=getattr(settings, 'REDIS_DB', 0),
            password=getattr(settings, 'REDIS_PASSWORD', None),
            decode_responses=True
        )
        
        # 询问用户是否清理数据
        user_input = input("是否清理Redis缓存? (y/n): ").strip().lower()
        if user_input == 'y':
            # 清除所有数据
            redis_client.flushdb()
            print("✅ Redis缓存已清理")
        else:
            print("❌ Redis缓存未清理")
        
    except redis.ConnectionError:
        print("❌ 无法连接到Redis服务器")
        print("请检查Redis是否运行以及配置是否正确")
    except Exception as e:
        print(f"❌ 清理Redis数据时出错: {e}")


if __name__ == "__main__":
    print("🔍 Redis数据查看工具")
    print("=" * 60)
    get_redis_data()
    clear_redis_data()
    print("\n✅ 数据获取完成") 