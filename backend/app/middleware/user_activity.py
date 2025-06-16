from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from app.utils.redis_client import redis_client
from app.api.deps import get_current_user_from_token
from app.database import get_db

class UserActivityMiddleware(BaseHTTPMiddleware):
    """用户活跃状态中间件"""
    
    async def dispatch(self, request: Request, call_next):
        # 处理请求
        response = await call_next(request)
        
        # 只处理成功的API请求
        if (response.status_code == 200 and 
            request.url.path.startswith("/api/") and 
            request.method in ["GET", "POST", "PUT", "DELETE"]):
            
            try:
                # 从Authorization头获取token
                authorization = request.headers.get("Authorization")
                if authorization and authorization.startswith("Bearer "):
                    token = authorization[7:]  # 移除 "Bearer " 前缀
                    
                    # 获取数据库会话
                    db = next(get_db())
                    try:
                        # 验证token并获取用户
                        user = get_current_user_from_token(token, db)
                        if user:
                            # 更新用户活跃时间
                            redis_client.update_user_activity(user.id)
                    finally:
                        db.close()
                        
            except Exception as e:
                # 静默处理错误，不影响正常请求
                print(f"更新用户活跃状态时出错: {e}")
        
        return response 