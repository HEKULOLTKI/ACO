from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class SystemSettingsBase(BaseModel):
    """系统设置基础模式"""
    max_users: Optional[int] = 100
    max_devices: Optional[int] = 50
    default_password: Optional[str] = '123456'
    log_retention_days: Optional[int] = 30
    refresh_rate: Optional[str] = '30秒'
    encryption_level: Optional[str] = '标准加密'

class SystemSettingsUpdate(SystemSettingsBase):
    """系统设置更新模式"""
    pass

class SystemSettingsResponse(SystemSettingsBase):
    """系统设置响应模式"""
    id: int
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True) 