from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Request
from fastapi.responses import JSONResponse
from typing import List, Optional
import uuid
import os
from datetime import datetime
import shutil

from app.schemas.chat import (
    ChatMessage, ChatMessageCreate, ChatRoom, OnlineUser, 
    ChatHistory, FileUploadResponse, ChatStats, MessageType
)
from app.utils.redis_client import redis_client
from app.api.deps import get_current_user
from app.schemas.user import UserResponse
from app.config import settings

router = APIRouter()

# 允许的文件类型
ALLOWED_FILE_TYPES = {
    'image/jpeg', 'image/png', 'image/gif', 'image/webp',
    'application/pdf', 'text/plain', 'application/msword', 
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
}

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

@router.post("/send", response_model=ChatMessage, summary="发送聊天消息")
async def send_message(
    message: ChatMessageCreate,
    current_user: UserResponse = Depends(get_current_user),
    room_id: str = "global"
):
    """发送聊天消息"""
    try:
        # 生成消息ID
        message_id = str(uuid.uuid4())
        
        # 创建消息数据 
        timestamp = datetime.now()
        message_data = {
            "id": message_id,
            "sender_id": current_user.id,
            "sender_name": current_user.username,
            "sender_role": current_user.role,
            "message_type": message.message_type.value,
            "content": message.content,
            "timestamp": timestamp.isoformat(),
            "reply_to": message.reply_to,
            "room_id": room_id
        }
        
        # 保存到Redis
        redis_client.save_chat_message(room_id, message_data)
        
        # 用户自动加入聊天室
        redis_client.join_chat_room(room_id, current_user.id)
        
        # 返回消息对象（使用datetime对象而不是ISO字符串）
        return ChatMessage(
            id=message_id,
            sender_id=current_user.id,
            sender_name=current_user.username,
            sender_role=current_user.role,
            message_type=message.message_type,
            content=message.content,
            timestamp=timestamp,
            reply_to=message.reply_to
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"发送消息失败: {str(e)}")

@router.post("/upload", response_model=ChatMessage, summary="上传文件并发送")
async def upload_file_and_send(
    file: UploadFile = File(...),
    room_id: str = Form("global"),
    current_user: UserResponse = Depends(get_current_user)
):
    """上传文件并发送聊天消息"""
    try:
        # 检查文件大小
        if file.size > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="文件大小超过限制(10MB)")
        
        # 检查文件类型
        if file.content_type not in ALLOWED_FILE_TYPES:
            raise HTTPException(status_code=415, detail="不支持的文件类型")
        
        # 生成唯一文件名
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        
        # 确保上传目录存在
        upload_dir = os.path.join(settings.UPLOAD_PATH, "chat")
        os.makedirs(upload_dir, exist_ok=True)
        
        # 保存文件
        file_path = os.path.join(upload_dir, unique_filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 生成文件URL
        file_url = f"/uploads/chat/{unique_filename}"
        
        # 确定消息类型
        message_type = MessageType.IMAGE if file.content_type.startswith("image/") else MessageType.FILE
        
        # 生成消息ID
        message_id = str(uuid.uuid4())
        timestamp = datetime.now()
        
        # 创建消息数据
        message_data = {
            "id": message_id,
            "sender_id": current_user.id,
            "sender_name": current_user.username,
            "sender_role": current_user.role,
            "message_type": message_type.value,
            "content": f"发送了文件: {file.filename}",
            "file_url": file_url,
            "file_name": file.filename,
            "file_size": file.size,
            "timestamp": timestamp.isoformat(),
            "room_id": room_id
        }
        
        # 保存到Redis
        redis_client.save_chat_message(room_id, message_data)
        
        # 用户自动加入聊天室
        redis_client.join_chat_room(room_id, current_user.id)
        
        # 返回消息对象（使用datetime对象而不是ISO字符串）
        return ChatMessage(
            id=message_id,
            sender_id=current_user.id,
            sender_name=current_user.username,
            sender_role=current_user.role,
            message_type=message_type,
            content=f"发送了文件: {file.filename}",
            file_url=file_url,
            file_name=file.filename,
            file_size=file.size,
            timestamp=timestamp
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件上传失败: {str(e)}")

@router.get("/messages", response_model=List[ChatMessage], summary="获取聊天消息")
async def get_messages(
    room_id: str = "global",
    limit: int = 50,
    before: Optional[str] = None,
    current_user: UserResponse = Depends(get_current_user)
):
    """获取聊天消息历史"""
    try:
        # 确保用户在聊天室中
        redis_client.join_chat_room(room_id, current_user.id)
        
        # 获取消息
        messages_data = redis_client.get_chat_messages(room_id, limit, before)
        
        # 转换为消息对象
        messages = []
        for msg_data in messages_data:
            # 跳过已删除的消息
            if msg_data.get('deleted'):
                continue
                
            try:
                # 解析时间戳
                timestamp = datetime.fromisoformat(msg_data['timestamp'])
                
                message = ChatMessage(
                    id=msg_data['id'],
                    sender_id=msg_data['sender_id'],
                    sender_name=msg_data['sender_name'],
                    sender_role=msg_data.get('sender_role'),
                    message_type=MessageType(msg_data['message_type']),
                    content=msg_data['content'],
                    file_url=msg_data.get('file_url'),
                    file_name=msg_data.get('file_name'),
                    file_size=msg_data.get('file_size'),
                    timestamp=timestamp,
                    reply_to=msg_data.get('reply_to')
                )
                messages.append(message)
            except Exception as e:
                print(f"解析消息失败: {e}")
                continue
        
        return messages
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取消息失败: {str(e)}")

@router.get("/online-users", response_model=List[OnlineUser], summary="获取在线用户")
async def get_online_users(current_user: UserResponse = Depends(get_current_user)):
    """获取在线用户列表"""
    try:
        online_users_data = redis_client.get_online_users()
        
        online_users = []
        for user_data in online_users_data:
            try:
                online_user = OnlineUser(
                    user_id=user_data['user_id'],
                    username=user_data['username'],
                    ip=user_data['ip'],
                    user_agent=user_data['user_agent'],
                    login_time=datetime.fromtimestamp(user_data['login_time']),
                    last_activity=datetime.fromtimestamp(user_data['last_activity'])
                )
                online_users.append(online_user)
            except Exception as e:
                print(f"解析在线用户数据失败: {e}")
                continue
        
        return online_users
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取在线用户失败: {str(e)}")

@router.get("/stats", response_model=ChatStats, summary="获取聊天统计")
async def get_chat_stats(current_user: UserResponse = Depends(get_current_user)):
    """获取聊天统计信息"""
    try:
        stats_data = redis_client.get_chat_stats()
        return ChatStats(**stats_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取统计信息失败: {str(e)}")

@router.post("/rooms", summary="创建聊天室")
async def create_room(
    room_name: str = Form(...),
    description: str = Form(""),
    current_user: UserResponse = Depends(get_current_user)
):
    """创建新的聊天室"""
    try:
        # 生成聊天室ID
        room_id = f"room_{uuid.uuid4().hex[:8]}"
        
        # 创建聊天室
        redis_client.create_chat_room(room_id, room_name, description, current_user.id)
        
        # 创建者自动加入聊天室
        redis_client.join_chat_room(room_id, current_user.id)
        
        # 发送系统消息
        system_message = {
            "id": str(uuid.uuid4()),
            "sender_id": 0,
            "sender_name": "系统",
            "sender_role": "system",
            "message_type": MessageType.SYSTEM.value,
            "content": f"聊天室 '{room_name}' 已创建，{current_user.username}({current_user.role}) 加入了聊天室",
            "timestamp": datetime.now().isoformat(),
            "room_id": room_id
        }
        redis_client.save_chat_message(room_id, system_message)
        
        return {"room_id": room_id, "message": "聊天室创建成功"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建聊天室失败: {str(e)}")

@router.post("/rooms/{room_id}/join", summary="加入聊天室")
async def join_room(
    room_id: str,
    current_user: UserResponse = Depends(get_current_user)
):
    """加入聊天室"""
    try:
        # 加入聊天室
        redis_client.join_chat_room(room_id, current_user.id)
        
        # 发送系统消息
        system_message = {
            "id": str(uuid.uuid4()),
            "sender_id": 0,
            "sender_name": "系统",
            "sender_role": "system",
            "message_type": MessageType.SYSTEM.value,
            "content": f"{current_user.username}({current_user.role}) 加入了聊天室",
            "timestamp": datetime.now().isoformat(),
            "room_id": room_id
        }
        redis_client.save_chat_message(room_id, system_message)
        
        return {"message": "成功加入聊天室"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"加入聊天室失败: {str(e)}")

@router.post("/rooms/{room_id}/leave", summary="离开聊天室")
async def leave_room(
    room_id: str,
    current_user: UserResponse = Depends(get_current_user)
):
    """离开聊天室"""
    try:
        # 离开聊天室
        redis_client.leave_chat_room(room_id, current_user.id)
        
        # 发送系统消息
        system_message = {
            "id": str(uuid.uuid4()),
            "sender_id": 0,
            "sender_name": "系统",
            "sender_role": "system",
            "message_type": MessageType.SYSTEM.value,
            "content": f"{current_user.username}({current_user.role}) 离开了聊天室",
            "timestamp": datetime.now().isoformat(),
            "room_id": room_id
        }
        redis_client.save_chat_message(room_id, system_message)
        
        return {"message": "成功离开聊天室"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"离开聊天室失败: {str(e)}")

@router.get("/rooms", summary="获取聊天室列表")
async def get_rooms(current_user: UserResponse = Depends(get_current_user)):
    """获取所有聊天室"""
    try:
        room_ids = redis_client.get_chat_rooms()
        
        rooms = []
        for room_id in room_ids:
            try:
                # 获取聊天室信息
                room_info = redis_client.redis_client.hgetall(f"chat:room:{room_id}")
                if room_info:
                    # 获取最后一条消息
                    last_messages = redis_client.get_chat_messages(room_id, 1)
                    last_message = None
                    if last_messages:
                        msg_data = last_messages[0]
                        last_message = ChatMessage(
                            id=msg_data['id'],
                            sender_id=msg_data['sender_id'],
                            sender_name=msg_data['sender_name'],
                            sender_role=msg_data.get('sender_role'),
                            message_type=MessageType(msg_data['message_type']),
                            content=msg_data['content'],
                            timestamp=datetime.fromisoformat(msg_data['timestamp'])
                        )
                    
                    room = ChatRoom(
                        id=room_id,
                        name=room_info.get('name', '未命名聊天室'),
                        description=room_info.get('description', ''),
                        members=redis_client.get_room_members(room_id),
                        created_at=datetime.fromtimestamp(float(room_info.get('created_at', 0))),
                        last_message=last_message
                    )
                    rooms.append(room)
            except Exception as e:
                print(f"解析聊天室信息失败: {e}")
                continue
        
        return rooms
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取聊天室列表失败: {str(e)}")

@router.delete("/messages/{message_id}", summary="删除消息")
async def delete_message(
    message_id: str,
    room_id: str = "global",
    current_user: UserResponse = Depends(get_current_user)
):
    """删除聊天消息"""
    try:
        redis_client.delete_chat_message(room_id, message_id, current_user.id)
        return {"message": "消息删除成功"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除消息失败: {str(e)}")

@router.get("/user-ip/{user_id}", summary="获取用户IP")
async def get_user_ip(
    user_id: int,
    current_user: UserResponse = Depends(get_current_user)
):
    """获取指定用户的IP地址"""
    try:
        user_ip = redis_client.get_user_ip(user_id)
        if user_ip:
            return {"user_id": user_id, "ip": user_ip}
        else:
            raise HTTPException(status_code=404, detail="用户不在线或IP信息不存在")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取用户IP失败: {str(e)}")

@router.post("/heartbeat", summary="心跳检测")
async def heartbeat(
    request: Request,
    current_user: UserResponse = Depends(get_current_user)
):
    """用户心跳检测，保持在线状态"""
    try:
        # 更新用户活动时间
        redis_client.update_user_activity(current_user.id)
        
        # 获取用户IP
        client_ip = request.client.host
        if request.headers.get("X-Forwarded-For"):
            client_ip = request.headers.get("X-Forwarded-For").split(",")[0].strip()
        elif request.headers.get("X-Real-IP"):
            client_ip = request.headers.get("X-Real-IP")
        
        # 更新IP信息
        user_agent = request.headers.get("User-Agent", "")
        redis_client.set_user_online(current_user.id, current_user.username, client_ip, user_agent)
        
        return {"status": "ok", "timestamp": datetime.now().isoformat()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"心跳检测失败: {str(e)}") 