from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Form, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import Token, UserResponse
from app.services.user_service import UserService
from app.utils.security import create_access_token
from app.utils.redis_client import redis_client
from app.utils.request_utils import get_client_ip, get_user_agent
from app.config import settings
from app.api.deps import get_current_user

router = APIRouter()

def clear_user_redis_cache(user_id: int):
    """清除指定用户的所有Redis缓存"""
    try:
        # 需要清除的键模式
        keys_to_clear = [
            f"password_backup:{user_id}",
            f"password_reset:{user_id}",
            f"login_records:{user_id}",
            f"online_user:{user_id}",
            f"user_session:{user_id}",
            f"user_activity:{user_id}"
        ]
        
        # 删除存在的键
        deleted_count = 0
        for key in keys_to_clear:
            if redis_client.redis_client.exists(key):
                redis_client.redis_client.delete(key)
                deleted_count += 1
        
        # 从在线用户集合中移除
        redis_client.redis_client.srem("online_users", user_id)
        
        print(f"✅ 清除用户 {user_id} 的 {deleted_count} 个Redis缓存")
        return deleted_count
        
    except Exception as e:
        print(f"❌ 清除用户 {user_id} 的Redis缓存失败: {e}")
        return 0

@router.post("/login", response_model=Token)
async def login_for_access_token(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    login_type: str = Form(...),
    db: Session = Depends(get_db)
) -> Token:
    """用户登录"""
    # 获取客户端IP和User-Agent
    client_ip = get_client_ip(request)
    user_agent = get_user_agent(request)
    
    user = UserService.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        # 记录失败的登录尝试
        redis_client.add_login_record(
            user_id=0,  # 未知用户ID
            ip=client_ip,
            user_agent=user_agent,
            status="failed_auth"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if user.status == 'inactive':
        # 记录被禁用账户的登录尝试
        redis_client.add_login_record(
            user_id=user.id,
            ip=client_ip,
            user_agent=user_agent,
            status="inactive_account"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="账户已被禁用",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 验证用户类型是否匹配
    if user.type != login_type:
        # 记录类型不匹配的登录尝试
        redis_client.add_login_record(
            user_id=user.id,
            ip=client_ip,
            user_agent=user_agent,
            status="type_mismatch"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"您的账户类型是\"{user.type}\"，请选择正确的登录类型",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 创建访问令牌
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    # 设置用户在线状态到Redis
    redis_client.set_user_online(
        user_id=user.id,
        username=user.username,
        ip=client_ip,
        user_agent=user_agent
    )
    
    # 记录成功的登录
    redis_client.add_login_record(
        user_id=user.id,
        ip=client_ip,
        user_agent=user_agent,
        status="success"
    )
    
    # 记录明文密码到Redis（仅在登录成功时）
    from app.utils.password_utils import PasswordUtils
    PasswordUtils.store_login_password(
        user_id=user.id,
        username=user.username,
        plain_password=form_data.password  # 记录用户输入的明文密码
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(user)
    )

@router.post("/logout")
async def logout(current_user = Depends(get_current_user)):
    """用户登出"""
    # 设置用户离线状态
    redis_client.set_user_offline(current_user.id)
    
    # 清除用户的所有Redis缓存
    clear_user_redis_cache(current_user.id)
    
    # 清除用户的密码缓存
    from app.utils.password_utils import PasswordUtils
    PasswordUtils.clear_user_password_cache(current_user.id)
    
    # 在实际应用中，这里可以将token加入黑名单
    return {"message": "登出成功，用户缓存已清除"}

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user = Depends(get_current_user)) -> UserResponse:
    """获取当前用户信息"""
    return UserResponse.model_validate(current_user)

@router.post("/refresh")
async def refresh_token(current_user = Depends(get_current_user)) -> Token:
    """刷新访问令牌"""
    # 更新用户活跃时间
    redis_client.update_user_activity(current_user.id)
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": current_user.username}, expires_delta=access_token_expires
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(current_user)
    )

@router.get("/online-users")
async def get_online_users(current_user = Depends(get_current_user)):
    """获取在线用户列表（需要登录）"""
    online_users = redis_client.get_online_users()
    return {
        "online_users": online_users,
        "count": len(online_users)
    }

@router.get("/online-status/{user_id}")
async def get_user_online_status(user_id: int, current_user = Depends(get_current_user)):
    """获取指定用户的在线状态"""
    user_info = redis_client.get_user_online_info(user_id)
    is_online = redis_client.is_user_online(user_id)
    user_ip = redis_client.get_user_ip(user_id)
    
    return {
        "user_id": user_id,
        "is_online": is_online,
        "user_info": user_info,
        "ip": user_ip
    }

@router.get("/login-records")
async def get_my_login_records(current_user = Depends(get_current_user)):
    """获取当前用户的登录记录"""
    records = redis_client.get_login_records(current_user.id, limit=20)
    return {
        "user_id": current_user.id,
        "records": records
    }

@router.get("/system-stats")
async def get_system_stats(current_user = Depends(get_current_user)):
    """获取系统统计信息"""
    online_count = redis_client.get_online_users_count()
    redis_connected = redis_client.ping()
    
    return {
        "online_users_count": online_count,
        "redis_connected": redis_connected,
        "current_user": {
            "id": current_user.id,
            "username": current_user.username,
            "is_online": redis_client.is_user_online(current_user.id)
        }
    }

@router.get("/user-session-info")
async def get_user_session_info(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    """获取当前用户的会话信息，包括IP地址和分配给用户的任务"""
    from app.services.task_service import TaskAssignmentService
    
    # 获取用户IP地址
    user_ip = redis_client.get_user_ip(current_user.id)
    user_info = redis_client.get_user_online_info(current_user.id)
    
    # 获取分配给当前用户的任务（从task_assignments表中）
    user_assignments = []
    try:
        # 使用TaskAssignmentService获取分配给当前用户的任务
        assignments = TaskAssignmentService.get_assignments_by_user(
            db=db, 
            user_id=current_user.id
        )
        
        user_assignments = [
            {
                "assignment_id": assignment.id,
                "task_id": assignment.task_id,
                "task_name": assignment.task_name,
                "task_type": assignment.task_type,
                "task_phase": assignment.task_phase,
                "username": assignment.username,
                "status": assignment.status,
                "progress": assignment.progress,
                "performance_score": assignment.performance_score,
                "comments": assignment.comments,
                "assigned_at": assignment.assigned_at.isoformat() if assignment.assigned_at else None,
                "last_update": assignment.last_update.isoformat() if assignment.last_update else None,
                # 添加任务详细信息
                "task_description": "",  # 稍后从task表中获取
                "priority": "normal",     # 默认优先级
                "estimated_duration": "unknown",
                "requirements": [],
                "deliverables": []
            }
            for assignment in assignments
        ]
        
        # 补充任务详细信息
        for assignment_data in user_assignments:
            if assignment_data["task_id"]:
                from app.services.task_service import TaskService
                task = TaskService.get_task(db=db, task_id=assignment_data["task_id"])
                if task:
                    assignment_data["task_description"] = task.description or ""
                    assignment_data["role_binding"] = task.role_binding or ""
        
        print(f"找到用户 {current_user.username} 的 {len(user_assignments)} 个分配任务")  # 调试信息
        
    except Exception as e:
        print(f"获取用户任务分配时发生错误: {e}")
        user_assignments = []
    
    # 添加实时时间戳和数据刷新标记
    import datetime
    current_timestamp = datetime.datetime.now().isoformat()
    
    return {
        "user_id": current_user.id,
        "username": current_user.username,
        "role": current_user.role,
        "type": current_user.type,
        "ip_address": user_ip,
        "session_info": user_info,
        "assigned_tasks": user_assignments,  # 改名为更明确的assigned_tasks
        "is_online": redis_client.is_user_online(current_user.id),
        "query_timestamp": current_timestamp,
        "tasks_count": len(user_assignments),
        "data_source": "task_assignments_table"
    }

@router.get("/user-complete-info")
async def get_user_complete_info(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    """获取当前用户的完整信息（包含明文密码），用于数据同步"""
    from app.models.user import User
    from app.services.user_service import UserService
    import datetime
    import time
    
    # 获取用户完整数据库信息
    db_user = db.query(User).filter(User.id == current_user.id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 获取Redis中的会话信息
    user_ip = redis_client.get_user_ip(current_user.id)
    user_info = redis_client.get_user_online_info(current_user.id)
    
    # 获取明文密码
    from app.utils.password_utils import PasswordUtils
    plain_password = PasswordUtils.get_plain_password(
        username=db_user.username,
        user_id=db_user.id,
        password_hash=db_user.password
    )
    
    # 构建完整的用户信息JSON
    user_data = {
        "action": "user_data_sync",
        "sync_info": {
            "sync_type": "current_user_export",
            "sync_time": datetime.datetime.now().isoformat() + "Z",
            "operator": {
                "user_id": current_user.id,
                "username": current_user.username,
                "operator_role": current_user.role or "未知角色",
                "operator_type": current_user.type or "未知类型"
            },
            "session": {
                "ip_address": user_ip,
                "user_agent": user_info.get('user_agent') if user_info else "unknown",
                "login_time": user_info.get('login_time') if user_info else time.time()
            },
            "data_source": {
                "database": "user_management",
                "table": "users",
                "version": "1.0",
                "environment": "production"
            }
        },
        "users": [
            {
                # 基本信息
                "id": db_user.id,
                "username": db_user.username,
                "password": plain_password,  # 明文密码
                "password_hash": db_user.password,  # 加密密码哈希
                
                # 角色与权限信息
                "role": db_user.role,
                "type": db_user.type,
                "status": db_user.status,
                
                # 个人信息
                "photo_data": db_user.photo_data,
                
                # 时间信息
                "created_at": db_user.created_at.isoformat() if db_user.created_at else None,
                "updated_at": db_user.updated_at.isoformat() if db_user.updated_at else None,
                
                # 扩展信息
                "last_login": user_info.get('login_time') if user_info else None,
                "login_count": len(redis_client.get_login_records(current_user.id)),
                "is_locked": db_user.status == "locked",
                "lock_reason": None if db_user.status != "locked" else "账户已锁定",
                "email": f"{db_user.username}@company.com",  # 生成默认邮箱
                "phone": None,  # 可以根据需要扩展
                "department": "信息技术部" if db_user.type == "管理员" else "运维部",
                "position": db_user.role or "未知职位"
            }
        ],
        "sync_summary": {
            "total_users": 1,
            "active_users": 1 if db_user.status == "active" else 0,
            "inactive_users": 0 if db_user.status == "active" else 1,
            "roles": [db_user.role] if db_user.role else [],
            "types": [db_user.type] if db_user.type else [],
            "sync_id": f"sync_{int(time.time() * 1000)}",
            "checksum": None,  # 可以根据需要添加
            "data_size": None,  # 可以根据需要计算
            "compression": "none"
        }
    }
    
    return user_data