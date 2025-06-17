from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class MessageType(str, Enum):
    """消息类型枚举"""
    TEXT = "text"
    FILE = "file"
    IMAGE = "image"
    SYSTEM = "system"

class ChatMessage(BaseModel):
    """聊天消息基础模型"""
    id: str = Field(..., description="消息ID")
    sender_id: int = Field(..., description="发送者ID")
    sender_name: str = Field(..., description="发送者用户名")
    message_type: MessageType = Field(default=MessageType.TEXT, description="消息类型")
    content: str = Field(..., description="消息内容")
    file_url: Optional[str] = Field(None, description="文件URL")
    file_name: Optional[str] = Field(None, description="文件名")
    file_size: Optional[int] = Field(None, description="文件大小")
    timestamp: datetime = Field(..., description="发送时间")
    reply_to: Optional[str] = Field(None, description="回复的消息ID")

class ChatMessageCreate(BaseModel):
    """创建聊天消息请求模型"""
    message_type: MessageType = Field(default=MessageType.TEXT, description="消息类型")
    content: str = Field(..., min_length=1, max_length=5000, description="消息内容")
    reply_to: Optional[str] = Field(None, description="回复的消息ID")

class ChatRoom(BaseModel):
    """聊天室模型"""
    id: str = Field(..., description="聊天室ID")
    name: str = Field(..., description="聊天室名称")
    description: Optional[str] = Field(None, description="聊天室描述")
    members: List[int] = Field(default=[], description="成员ID列表")
    created_at: datetime = Field(..., description="创建时间")
    last_message: Optional[ChatMessage] = Field(None, description="最后一条消息")

class OnlineUser(BaseModel):
    """在线用户模型"""
    user_id: int = Field(..., description="用户ID")
    username: str = Field(..., description="用户名")
    ip: str = Field(..., description="IP地址")
    user_agent: str = Field(..., description="用户代理")
    login_time: datetime = Field(..., description="登录时间")
    last_activity: datetime = Field(..., description="最后活动时间")

class ChatHistory(BaseModel):
    """聊天历史请求参数"""
    room_id: str = Field(default="global", description="聊天室ID")
    limit: int = Field(default=50, min=1, max=100, description="获取消息数量")
    before: Optional[str] = Field(None, description="获取此消息ID之前的消息")

class FileUploadResponse(BaseModel):
    """文件上传响应"""
    file_url: str = Field(..., description="文件URL")
    file_name: str = Field(..., description="文件名")
    file_size: int = Field(..., description="文件大小")
    upload_time: datetime = Field(..., description="上传时间")

class ChatStats(BaseModel):
    """聊天统计信息"""
    online_users_count: int = Field(..., description="在线用户数")
    total_messages_today: int = Field(..., description="今日消息总数")
    active_rooms: int = Field(..., description="活跃聊天室数") 