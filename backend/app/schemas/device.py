from pydantic import BaseModel, ConfigDict, validator, Field
from typing import Optional, List
import re

class DeviceBase(BaseModel):
    """设备基础模式"""
    name: str = Field(..., min_length=1, max_length=255, description="设备名称")
    type: Optional[str] = Field(None, max_length=100, description="设备类型")
    ip: Optional[str] = Field(None, max_length=50, description="设备IP地址")
    status: Optional[str] = Field('offline', description="设备状态")
    location: Optional[str] = Field(None, max_length=255, description="设备位置")
    
    @validator('ip')
    def validate_ip(cls, v):
        """验证IP地址格式"""
        if v is None:
            return v
        ip_pattern = re.compile(
            r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
        )
        if not ip_pattern.match(v):
            raise ValueError('IP地址格式不正确')
        return v

class DeviceCreate(DeviceBase):
    """设备创建模式"""
    pass

class DeviceUpdate(BaseModel):
    """设备更新模式"""
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="设备名称")
    type: Optional[str] = Field(None, max_length=100, description="设备类型")
    ip: Optional[str] = Field(None, max_length=50, description="设备IP地址")
    status: Optional[str] = Field(None, description="设备状态")
    location: Optional[str] = Field(None, max_length=255, description="设备位置")
    
    @validator('ip')
    def validate_ip(cls, v):
        """验证IP地址格式"""
        if v is None:
            return v
        ip_pattern = re.compile(
            r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
        )
        if not ip_pattern.match(v):
            raise ValueError('IP地址格式不正确')
        return v

class DeviceResponse(DeviceBase):
    """设备响应模式"""
    id: int
    
    model_config = ConfigDict(from_attributes=True)

# 批量导入相关模式
class DeviceBatchCreate(BaseModel):
    """设备批量创建模式"""
    devices: List[DeviceCreate]

class DeviceImportResult(BaseModel):
    """设备导入结果"""
    success_count: int = Field(description="成功导入数量")
    failure_count: int = Field(description="失败数量")
    success_devices: List[DeviceResponse] = Field(description="成功导入的设备")
    failure_details: List[dict] = Field(description="失败详情")

class DeviceListResponse(BaseModel):
    """设备列表响应"""
    devices: List[DeviceResponse]
    total: int
    page: int
    page_size: int 