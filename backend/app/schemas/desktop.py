from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class DesktopItemBase(BaseModel):
    """桌面项目基础模式"""
    name: str
    type: Optional[str] = None
    path: Optional[str] = None
    icon: Optional[str] = None
    role: Optional[str] = None
    position_x: Optional[int] = 0
    position_y: Optional[int] = 0

class DesktopItemCreate(DesktopItemBase):
    """桌面项目创建模式"""
    user_id: Optional[int] = None

class DesktopItemUpdate(BaseModel):
    """桌面项目更新模式"""
    name: Optional[str] = None
    type: Optional[str] = None
    path: Optional[str] = None
    icon: Optional[str] = None
    role: Optional[str] = None
    position_x: Optional[int] = None
    position_y: Optional[int] = None

class DesktopItemResponse(DesktopItemBase):
    """桌面项目响应模式"""
    id: int
    user_id: Optional[int] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class ToolboxToolBase(BaseModel):
    """工具箱工具基础模式"""
    name: str
    command: Optional[str] = None
    icon: Optional[str] = None

class ToolboxToolCreate(ToolboxToolBase):
    """工具箱工具创建模式"""
    user_id: Optional[int] = None

class ToolboxToolUpdate(BaseModel):
    """工具箱工具更新模式"""
    name: Optional[str] = None
    command: Optional[str] = None
    icon: Optional[str] = None

class ToolboxToolResponse(ToolboxToolBase):
    """工具箱工具响应模式"""
    id: int
    user_id: Optional[int] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True) 