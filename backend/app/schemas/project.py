from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field
from app.schemas.user import UserProfile

class ProjectBase(BaseModel):
    """项目基础模型"""
    name: str = Field(..., title="项目名称", max_length=255)
    description: Optional[str] = Field(None, title="项目描述")
    status: Optional[str] = Field("开发中", title="项目状态")
    icon: Optional[str] = Field("Briefcase", title="项目图标")
    manager_id: Optional[int] = Field(None, title="负责人ID")
    planning: Optional[str] = Field(None, title="项目策划")

class ProjectCreate(ProjectBase):
    """创建项目模型"""
    pass

class ProjectUpdate(BaseModel):
    """更新项目模型"""
    name: Optional[str] = Field(None, title="项目名称", max_length=255)
    description: Optional[str] = Field(None, title="项目描述")
    status: Optional[str] = Field(None, title="项目状态")
    icon: Optional[str] = Field(None, title="项目图标")
    manager_id: Optional[int] = Field(None, title="负责人ID")
    planning: Optional[str] = Field(None, title="项目策划")

class Project(ProjectBase):
    """项目响应模型"""
    id: int
    created_at: datetime
    updated_at: datetime
    manager: Optional[UserProfile] = None
    
    class Config:
        orm_mode = True
        
class ProjectImportResult(BaseModel):
    """项目导入结果"""
    success_count: int = Field(..., title="成功数量")
    fail_count: int = Field(..., title="失败数量")
    failed_projects: List[dict] = Field([], title="失败项目列表")
    message: str = Field(..., title="结果消息") 