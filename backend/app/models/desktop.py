from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class DesktopItem(Base):
    """桌面项目模型"""
    __tablename__ = "desktop_items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, comment="项目名称")
    type = Column(String(50), comment="项目类型")
    path = Column(Text, comment="项目路径")
    icon = Column(Text, comment="图标数据")
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), comment="用户ID")
    role = Column(String(255), comment="适用角色")
    position_x = Column(Integer, default=0, comment="X坐标")
    position_y = Column(Integer, default=0, comment="Y坐标")
    created_at = Column(TIMESTAMP, server_default=func.now(), comment="创建时间")
    
    # 关联关系
    user = relationship("User", back_populates="desktop_items")
    
    def __repr__(self):
        return f"<DesktopItem(id={self.id}, name='{self.name}', type='{self.type}')>"

class ToolboxTool(Base):
    """工具箱工具模型"""
    __tablename__ = "toolbox_tools"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, comment="工具名称")
    command = Column(Text, comment="执行命令")
    icon = Column(Text, comment="图标数据")
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), comment="用户ID")
    created_at = Column(TIMESTAMP, server_default=func.now(), comment="创建时间")
    
    # 关联关系
    user = relationship("User", back_populates="toolbox_tools")
    
    def __repr__(self):
        return f"<ToolboxTool(id={self.id}, name='{self.name}')>" 