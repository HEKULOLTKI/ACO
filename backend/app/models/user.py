from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    """用户模型"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(255), comment="用户角色")
    type = Column(String(50), comment="用户类型")
    status = Column(String(50), default='inactive', comment="用户状态")
    photo_data = Column(Text, comment="头像数据")
    created_at = Column(TIMESTAMP, server_default=func.now(), comment="创建时间")
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 关联关系
    task_assignments = relationship("TaskAssignment", back_populates="user")
    desktop_items = relationship("DesktopItem", back_populates="user")
    toolbox_tools = relationship("ToolboxTool", back_populates="user")
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', role='{self.role}')>" 