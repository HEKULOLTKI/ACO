from fastapi import Request
from typing import Optional

def get_client_ip(request: Request) -> str:
    """获取客户端真实IP地址"""
    # 检查反向代理头部
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        # X-Forwarded-For 可能包含多个IP，取第一个
        return forwarded_for.split(",")[0].strip()
    
    # 检查其他常见的代理头部
    real_ip = request.headers.get("x-real-ip")
    if real_ip:
        return real_ip
    
    # 如果没有代理头部，使用客户端IP
    client_host = request.client.host if request.client else "unknown"
    return client_host

def get_user_agent(request: Request) -> str:
    """获取用户代理字符串"""
    return request.headers.get("user-agent", "unknown") 