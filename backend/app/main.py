from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import create_tables
from app.api import auth, user, task, device

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

# 包含API路由
app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
app.include_router(user.router, prefix="/api", tags=["用户管理"])
app.include_router(task.router, prefix="/api", tags=["任务管理"])
app.include_router(device.router, prefix="/api", tags=["设备管理"])

@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    create_tables()
    print(f"🚀 {settings.PROJECT_NAME} 已启动")
    print(f"📖 API文档: http://localhost:8000/docs")

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