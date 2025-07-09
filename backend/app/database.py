from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from app.config import settings
import logging

# 创建数据库引擎
engine = create_engine(
    settings.DATABASE_URL,
    # 对于MySQL，添加以下配置
    echo=False,  # 设置为True可以看到SQL语句
    pool_pre_ping=True,  # 连接池预检查
    pool_recycle=3600,   # 连接池回收时间
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基础模型类
Base = declarative_base()

def get_db() -> Session:
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """创建所有表"""
    try:
        # 导入所有模型以确保它们被注册到Base.metadata
        from app.models import user, device, system, task, desktop, knowledge, project
        
        # 创建所有表
        Base.metadata.create_all(bind=engine)
        logging.info("数据库表创建成功")
    except Exception as e:
        logging.error(f"创建数据库表失败: {e}")
        raise e

def check_database_connection():
    """检查数据库连接"""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            logging.info("数据库连接正常")
            return True
    except Exception as e:
        logging.error(f"数据库连接失败: {e}")
        return False 