from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import asyncio
from datetime import datetime
from app.config import settings
from app.database import create_tables
from app.api import auth, user, task, device, desktop, system, chat
from app.api import knowledge
from app.middleware.user_activity import UserActivityMiddleware
import os

# 创建FastAPI应用实例
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="多智能体协作运维系统 - 后端API",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加用户活跃状态中间件
app.add_middleware(UserActivityMiddleware)

# 确保上传目录存在
os.makedirs("uploads/chat", exist_ok=True)
os.makedirs("uploads/progress_reports", exist_ok=True)

# 挂载静态文件目录
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# 包含API路由
app.include_router(auth.router, prefix="/api/auth", tags=["用户认证"])
app.include_router(user.router, prefix="/api", tags=["用户管理"])
app.include_router(task.router, prefix="/api", tags=["任务管理"])
app.include_router(device.router, prefix="/api", tags=["设备管理"])
app.include_router(desktop.router, tags=["桌面管理"])
app.include_router(system.router, prefix="/api/system", tags=["系统管理"])
app.include_router(chat.router, prefix="/api/chat", tags=["在线聊天"])
app.include_router(knowledge.router, tags=["知识库"])

# 后台定时任务
async def cleanup_expired_users_task():
    """定期清理过期用户的后台任务"""
    from app.utils.redis_client import redis_client
    
    while True:
        try:
            # 执行用户清理
            redis_client.cleanup_expired_users()
            
            # 每5分钟执行一次清理
            await asyncio.sleep(300)
            
        except Exception as e:
            print(f"定时清理任务出错: {e}")
            # 出错时等待更长时间再重试
            await asyncio.sleep(600)

@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    from app.utils.redis_client import redis_client
    
    create_tables()
    
    # 测试Redis连接
    if redis_client.ping():
        print("✅ Redis连接成功")
        
        # 创建默认全局聊天室
        try:
            redis_client.create_chat_room("global", "全局聊天室", "所有用户的公共聊天室", 0)
            print("✅ 创建默认聊天室成功")
        except Exception as e:
            print(f"⚠️ 创建默认聊天室失败: {e}")
        
        # 启动定时清理任务
        asyncio.create_task(cleanup_expired_users_task())
        print("✅ 启动用户过期清理定时任务")
        
    else:
        print("❌ Redis连接失败，用户在线状态功能可能不可用")
    
    print(f"🚀 {settings.PROJECT_NAME} 已启动")
    print(f"📖 API文档: http://localhost:8000/docs")
    print(f"💬 聊天API: http://localhost:8000/api/chat")
    print(f"⏰ 用户在线状态超时时间: 1小时")
    print(f"🔄 自动清理周期: 5分钟")

@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件"""
    print(f"🛑 {settings.PROJECT_NAME} 已关闭")

@app.get("/")
async def root():
    """根路径"""
    return {
        "message": f"欢迎使用{settings.PROJECT_NAME}",
        "version": settings.VERSION,
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "service": settings.PROJECT_NAME}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    ) 