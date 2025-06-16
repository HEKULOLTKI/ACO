from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.deps import get_current_user
from app.utils.redis_client import redis_client
import psutil
import platform
from datetime import datetime
from typing import Dict, Any

router = APIRouter()

@router.get("/status")
async def get_system_status(current_user = Depends(get_current_user)):
    """获取系统状态"""
    try:
        # 获取系统基本信息
        system_info = {
            "platform": platform.system(),
            "platform_release": platform.release(),
            "platform_version": platform.version(),
            "architecture": platform.machine(),
            "hostname": platform.node(),
            "processor": platform.processor(),
        }
        
        # 获取CPU信息
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        cpu_count_logical = psutil.cpu_count(logical=True)
        
        # 获取内存信息
        memory = psutil.virtual_memory()
        memory_info = {
            "total": memory.total,
            "available": memory.available,
            "percent": memory.percent,
            "used": memory.used,
            "free": memory.free
        }
        
        # 获取磁盘信息
        disk = psutil.disk_usage('/')
        disk_info = {
            "total": disk.total,
            "used": disk.used,
            "free": disk.free,
            "percent": (disk.used / disk.total) * 100
        }
        
        # 获取网络信息
        network = psutil.net_io_counters()
        network_info = {
            "bytes_sent": network.bytes_sent,
            "bytes_recv": network.bytes_recv,
            "packets_sent": network.packets_sent,
            "packets_recv": network.packets_recv
        }
        
        # Redis状态
        redis_status = redis_client.ping()
        online_users_count = redis_client.get_online_users_count() if redis_status else 0
        
        return {
            "timestamp": datetime.now(),
            "system_info": system_info,
            "cpu": {
                "percent": cpu_percent,
                "count": cpu_count,
                "count_logical": cpu_count_logical
            },
            "memory": memory_info,
            "disk": disk_info,
            "network": network_info,
            "redis": {
                "connected": redis_status,
                "online_users_count": online_users_count
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取系统状态失败: {str(e)}")

@router.get("/stats")
async def get_system_stats(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    """获取系统统计信息"""
    try:
        # 获取数据库统计
        from app.models.user import User
        from app.models.task import Task
        from app.models.device import Device
        
        user_count = db.query(User).count()
        task_count = db.query(Task).count()
        device_count = db.query(Device).count()
        
        # 获取任务状态统计
        pending_tasks = db.query(Task).filter(Task.status == 'pending').count()
        running_tasks = db.query(Task).filter(Task.status == 'running').count()
        completed_tasks = db.query(Task).filter(Task.status == 'completed').count()
        failed_tasks = db.query(Task).filter(Task.status == 'failed').count()
        
        # 获取设备状态统计
        online_devices = db.query(Device).filter(Device.status == 'online').count()
        offline_devices = db.query(Device).filter(Device.status == 'offline').count()
        
        # Redis统计
        redis_connected = redis_client.ping()
        online_users_count = redis_client.get_online_users_count() if redis_connected else 0
        
        return {
            "database": {
                "total_users": user_count,
                "total_tasks": task_count,
                "total_devices": device_count
            },
            "tasks": {
                "pending": pending_tasks,
                "running": running_tasks,
                "completed": completed_tasks,
                "failed": failed_tasks
            },
            "devices": {
                "online": online_devices,
                "offline": offline_devices
            },
            "users": {
                "online": online_users_count
            },
            "redis": {
                "connected": redis_connected
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取系统统计失败: {str(e)}")

@router.get("/health")
async def health_check():
    """系统健康检查"""
    try:
        # 检查数据库连接
        db_status = True
        try:
            # 这里可以添加数据库连接检查
            pass
        except Exception:
            db_status = False
        
        # 检查Redis连接
        redis_status = redis_client.ping()
        
        # 检查系统资源
        cpu_percent = psutil.cpu_percent(interval=1)
        memory_percent = psutil.virtual_memory().percent
        disk_percent = psutil.disk_usage('/').percent if platform.system() != 'Windows' else psutil.disk_usage('C:\\').percent
        
        # 判断系统状态
        system_status = "healthy"
        warnings = []
        
        if cpu_percent > 80:
            system_status = "warning"
            warnings.append("CPU使用率过高")
        
        if memory_percent > 80:
            system_status = "warning"
            warnings.append("内存使用率过高")
        
        if disk_percent > 80:
            system_status = "warning"
            warnings.append("磁盘使用率过高")
        
        if not redis_status:
            system_status = "error"
            warnings.append("Redis连接失败")
        
        if not db_status:
            system_status = "error"
            warnings.append("数据库连接失败")
        
        return {
            "status": system_status,
            "timestamp": datetime.now(),
            "services": {
                "database": db_status,
                "redis": redis_status
            },
            "resources": {
                "cpu_percent": cpu_percent,
                "memory_percent": memory_percent,
                "disk_percent": disk_percent
            },
            "warnings": warnings
        }
    except Exception as e:
        return {
            "status": "error",
            "timestamp": datetime.now(),
            "error": str(e)
        }

@router.post("/cleanup/redis")
async def cleanup_redis(current_user = Depends(get_current_user)):
    """清理Redis过期数据"""
    try:
        redis_client.cleanup_expired_users()
        return {"message": "Redis清理完成", "timestamp": datetime.now()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Redis清理失败: {str(e)}")

@router.get("/logs/recent")
async def get_recent_logs(current_user = Depends(get_current_user), limit: int = 100):
    """获取最近的系统日志"""
    try:
        # 这里可以实现日志读取逻辑
        # 暂时返回示例数据
        return {
            "logs": [
                {
                    "timestamp": datetime.now(),
                    "level": "INFO",
                    "message": "系统运行正常",
                    "source": "system"
                }
            ],
            "total": 1
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取日志失败: {str(e)}")

@router.get("/performance")
async def get_performance_metrics(current_user = Depends(get_current_user)):
    """获取性能指标"""
    try:
        # 获取CPU历史数据（最近10次采样）
        cpu_history = []
        for _ in range(10):
            cpu_history.append(psutil.cpu_percent(interval=0.1))
        
        # 获取内存详细信息
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        # 获取进程信息
        process_count = len(psutil.pids())
        
        # 获取启动时间
        boot_time = psutil.boot_time()
        
        return {
            "cpu": {
                "current_percent": cpu_history[-1],
                "history": cpu_history,
                "count": psutil.cpu_count(),
                "count_logical": psutil.cpu_count(logical=True)
            },
            "memory": {
                "virtual": {
                    "total": memory.total,
                    "available": memory.available,
                    "percent": memory.percent,
                    "used": memory.used,
                    "free": memory.free,
                    "active": getattr(memory, 'active', 0),
                    "inactive": getattr(memory, 'inactive', 0),
                    "buffers": getattr(memory, 'buffers', 0),
                    "cached": getattr(memory, 'cached', 0)
                },
                "swap": {
                    "total": swap.total,
                    "used": swap.used,
                    "free": swap.free,
                    "percent": swap.percent
                }
            },
            "system": {
                "process_count": process_count,
                "boot_time": boot_time,
                "uptime": datetime.now().timestamp() - boot_time
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取性能指标失败: {str(e)}") 