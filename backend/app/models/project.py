from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Project(Base):
    """项目模型"""
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, comment="项目名称")  # 删除了unique和index参数
    description = Column(Text, nullable=True, comment="项目描述")
    status = Column(String(50), default='开发中', comment="项目状态")
    icon = Column(String(50), default='Briefcase', comment="项目图标")
    manager_id = Column(Integer, ForeignKey("users.id"), nullable=True, comment="负责人ID")
    planning = Column(Text, nullable=True, comment="项目策划")
    created_at = Column(TIMESTAMP, server_default=func.now(), comment="创建时间")
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 关联关系
    manager = relationship("User", foreign_keys=[manager_id])
    
    # 在类定义结束后，使用__table_args__添加自定义索引
    __table_args__ = (
        # 手动定义name列的唯一索引，设置mysql_length=250来限制索引长度
        Index('ix_projects_name', name, unique=True, mysql_length=250),
    )
    
    def __repr__(self):
        return f"<Project(id={self.id}, name='{self.name}', status='{self.status}')>" 