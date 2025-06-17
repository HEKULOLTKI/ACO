# 在线聊天系统 API 文档

## 概述

在线聊天系统提供了完整的聊天功能，包括文本消息、文件上传、在线用户管理等。所有聊天数据存储在Redis中，用户IP信息也保存在Redis中。

## 功能特性

- ✅ 文本消息发送
- ✅ 文件上传和分享
- ✅ 多聊天室支持
- ✅ 在线用户管理
- ✅ 用户IP地址追踪
- ✅ 消息历史记录
- ✅ 消息删除功能
- ✅ 心跳检测保持在线状态

## API 端点

### 基础URL
```
http://localhost:8000/api/chat
```

### 1. 发送消息
```http
POST /api/chat/send
Content-Type: application/json
Authorization: Bearer <token>

{
  "message_type": "text",
  "content": "你好，这是一条测试消息",
  "reply_to": null
}
```

### 2. 文件上传
```http
POST /api/chat/upload
Content-Type: multipart/form-data
Authorization: Bearer <token>

file: <文件数据>
room_id: global
```

### 3. 获取消息历史
```http
GET /api/chat/messages?room_id=global&limit=50
Authorization: Bearer <token>
```

### 4. 获取在线用户
```http
GET /api/chat/online-users
Authorization: Bearer <token>
```

### 5. 获取聊天统计
```http
GET /api/chat/stats
Authorization: Bearer <token>
```

### 6. 创建聊天室
```http
POST /api/chat/rooms
Content-Type: multipart/form-data
Authorization: Bearer <token>

room_name: 技术讨论
description: 用于技术相关话题的讨论
```

### 7. 加入聊天室
```http
POST /api/chat/rooms/{room_id}/join
Authorization: Bearer <token>
```

### 8. 离开聊天室
```http
POST /api/chat/rooms/{room_id}/leave
Authorization: Bearer <token>
```

### 9. 获取聊天室列表
```http
GET /api/chat/rooms
Authorization: Bearer <token>
```

### 10. 删除消息
```http
DELETE /api/chat/messages/{message_id}?room_id=global
Authorization: Bearer <token>
```

### 11. 获取用户IP
```http
GET /api/chat/user-ip/{user_id}
Authorization: Bearer <token>
```

### 12. 心跳检测
```http
POST /api/chat/heartbeat
Authorization: Bearer <token>
```

## 数据模型

### 聊天消息 (ChatMessage)
```json
{
  "id": "uuid",
  "sender_id": 1,
  "sender_name": "用户名",
  "message_type": "text|file|image|system",
  "content": "消息内容",
  "file_url": "/uploads/chat/file.pdf",
  "file_name": "document.pdf",
  "file_size": 1024,
  "timestamp": "2024-01-01T12:00:00",
  "reply_to": "parent_message_id"
}
```

### 在线用户 (OnlineUser)
```json
{
  "user_id": 1,
  "username": "用户名",
  "ip": "192.168.1.100",
  "user_agent": "Mozilla/5.0...",
  "login_time": "2024-01-01T10:00:00",
  "last_activity": "2024-01-01T12:00:00"
}
```

### 聊天室 (ChatRoom)
```json
{
  "id": "room_12345678",
  "name": "聊天室名称",
  "description": "聊天室描述",
  "members": [1, 2, 3],
  "created_at": "2024-01-01T10:00:00",
  "last_message": {
    "id": "message_id",
    "content": "最后一条消息",
    "timestamp": "2024-01-01T12:00:00"
  }
}
```

## 支持的文件类型

- 图片: JPEG, PNG, GIF, WebP
- 文档: PDF, TXT, DOC, DOCX, XLS, XLSX
- 最大文件大小: 10MB

## Redis 数据结构

### 聊天消息
- Key: `chat:messages:{room_id}`
- Type: List
- 存储: JSON格式的消息数据

### 在线用户
- Key: `user:online:{user_id}`
- Type: Hash
- 字段: user_id, username, ip, user_agent, login_time, last_activity

### 聊天室信息
- Key: `chat:room:{room_id}`
- Type: Hash
- 字段: id, name, description, creator_id, created_at, last_activity

### 聊天室成员
- Key: `chat:room:{room_id}:members`
- Type: Set
- 存储: 用户ID列表

### 用户聊天室
- Key: `user:{user_id}:chat_rooms`
- Type: Set
- 存储: 用户加入的聊天室ID列表

## 使用示例

### 前端JavaScript示例
```javascript
// 发送消息
async function sendMessage(content) {
    const response = await fetch('/api/chat/send', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
        },
        body: JSON.stringify({
            message_type: 'text',
            content: content
        })
    });
    return await response.json();
}

// 获取消息历史
async function getMessages(roomId = 'global') {
    const response = await fetch(`/api/chat/messages?room_id=${roomId}`, {
        headers: {
            'Authorization': 'Bearer ' + token
        }
    });
    return await response.json();
}

// 上传文件
async function uploadFile(file, roomId = 'global') {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('room_id', roomId);
    
    const response = await fetch('/api/chat/upload', {
        method: 'POST',
        headers: {
            'Authorization': 'Bearer ' + token
        },
        body: formData
    });
    return await response.json();
}

// 获取在线用户
async function getOnlineUsers() {
    const response = await fetch('/api/chat/online-users', {
        headers: {
            'Authorization': 'Bearer ' + token
        }
    });
    return await response.json();
}

// 心跳检测（建议每30秒调用一次）
async function heartbeat() {
    const response = await fetch('/api/chat/heartbeat', {
        method: 'POST',
        headers: {
            'Authorization': 'Bearer ' + token
        }
    });
    return await response.json();
}
```

## 注意事项

1. 所有API都需要用户认证，需要在请求头中包含有效的JWT token
2. 聊天消息在Redis中保留7天，超过7天的消息会自动过期
3. 每个聊天室最多保留1000条消息
4. 用户在线状态会在30分钟无活动后自动过期
5. 建议前端定期调用心跳检测API来保持在线状态
6. 文件上传后会返回文件URL，前端可以通过这个URL访问文件

## 错误处理

API会返回标准的HTTP状态码和错误信息：

- 400: 请求参数错误
- 401: 未认证或token无效
- 403: 权限不足
- 404: 资源不存在
- 413: 文件大小超过限制
- 415: 不支持的文件类型
- 500: 服务器内部错误

错误响应格式：
```json
{
  "detail": "错误详细信息"
}
``` 