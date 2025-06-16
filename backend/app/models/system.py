from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class SystemSettings(Base):
    """系统设置模型"""
    __tablename__ = "system_settings"
    
    id = Column(Integer, primary_key=True, default=1, comment="设置ID")
    max_users = Column(Integer, default=100, comment="最大用户数")
    max_devices = Column(Integer, default=50, comment="最大设备数")
    default_password = Column(String(255), default='123456', comment="默认密码")
    log_retention_days = Column(Integer, default=30, comment="日志保留天数")
    refresh_rate = Column(String(50), default='30秒', comment="刷新频率")
    encryption_level = Column(String(50), default='标准加密', comment="加密级别")
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    def __repr__(self):
        return f"<SystemSettings(id={self.id}, max_users={self.max_users}, max_devices={self.max_devices})>" 