from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    """用户基础模式"""
    username: str
    role: Optional[str] = None
    type: Optional[str] = None
    status: Optional[str] = 'inactive'

class UserCreate(UserBase):
    """用户创建模式"""
    password: str

class UserUpdate(BaseModel):
    """用户更新模式"""
    role: Optional[str] = None
    type: Optional[str] = None
    status: Optional[str] = None
    photo_data: Optional[str] = None

class UserResponse(UserBase):
    """用户响应模式"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    """用户登录模式"""
    username: str
    password: str

class UserProfile(BaseModel):
    """用户档案模式"""
    id: int
    username: str
    role: Optional[str] = None
    type: Optional[str] = None
    status: str
    photo_data: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    """访问令牌模式"""
    access_token: str
    token_type: str
    user: UserResponse

class UserBulkCreate(BaseModel):
    """批量创建用户模式"""
    users: List[UserCreate]

class BulkImportResult(BaseModel):
    """批量导入结果"""
    success_count: int
    fail_count: int
    failed_users: List[dict]
    message: str 