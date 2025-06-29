from pydantic_settings import BaseSettings
from typing import Optional, List

class Settings(BaseSettings):
    # 数据库配置
    DATABASE_URL: str = "mysql+pymysql://user:ChinaSkills!@localhost:3306/conlse_sql?charset=utf8mb4"
    
    # JWT配置
    SECRET_KEY: str = "your-secret-key-here-multi-agent-ops-system-2024"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS配置
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080", "http://127.0.0.1:3000"]
    
    # OpenAI配置
    OPENAI_API_KEY: Optional[str] = None
    CHAT_ID: Optional[str] = None
    
    # 文件上传配置
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    UPLOAD_PATH: str = "./uploads"
    
    # Redis配置
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    
    # 应用配置
    PROJECT_NAME: str = "多智能体协作运维系统"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # 服务器配置
    SERVER_HOST: str = "localhost"
    SERVER_PORT: int = 8000
    
    class Config:
        env_file = ".env"

settings = Settings() 