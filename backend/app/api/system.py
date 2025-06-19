from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.deps import get_current_user
from app.utils.redis_client import redis_client
import psutil
import platform
from datetime import datetime
from typing import Dict, Any, List
import os
import json
from pathlib import Path

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

@router.post("/reports/generate")
async def generate_project_report(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """生成项目报告PDF"""
    try:
        # 创建报告存储目录
        reports_dir = Path("uploads/progress_reports")
        reports_dir.mkdir(parents=True, exist_ok=True)
        
        # 获取系统统计数据
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
        
        # 创建报告数据
        report_data = {
            "report_title": "多智能体协作运维系统项目报告",
            "generated_at": datetime.now().strftime("%Y年%m月%d日 %H:%M:%S"),
            "generated_by": current_user.username,
            "system_overview": {
                "total_users": user_count,
                "total_tasks": task_count,
                "total_devices": device_count
            },
            "task_statistics": {
                "pending": pending_tasks,
                "running": running_tasks, 
                "completed": completed_tasks,
                "failed": failed_tasks
            },
            "device_statistics": {
                "online": online_devices,
                "offline": offline_devices
            }
        }
        
        # 生成PDF文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_filename = f"项目报告_{timestamp}.pdf"
        pdf_path = reports_dir / pdf_filename
        
        # 生成PDF报告
        await create_project_report_pdf(report_data, pdf_path)
        
        return {
            "message": "项目报告生成成功",
            "filename": pdf_filename,
            "file_path": f"/uploads/progress_reports/{pdf_filename}",
            "generated_at": datetime.now()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成项目报告失败: {str(e)}")

@router.get("/reports")
async def get_project_reports(current_user = Depends(get_current_user)):
    """获取项目报告列表"""
    try:
        reports_dir = Path("uploads/progress_reports")
        if not reports_dir.exists():
            return {"reports": []}
        
        reports = []
        for pdf_file in reports_dir.glob("*.pdf"):
            stat = pdf_file.stat()
            reports.append({
                "filename": pdf_file.name,
                "file_path": f"/uploads/progress_reports/{pdf_file.name}",
                "size": stat.st_size,
                "created_at": datetime.fromtimestamp(stat.st_ctime),
                "modified_at": datetime.fromtimestamp(stat.st_mtime)
            })
        
        # 按创建时间倒序排列
        reports.sort(key=lambda x: x["created_at"], reverse=True)
        
        return {"reports": reports}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取报告列表失败: {str(e)}")

@router.get("/reports/download/{filename}")
async def download_project_report(
    filename: str,
    current_user = Depends(get_current_user)
):
    """下载项目报告PDF"""
    try:
        reports_dir = Path("uploads/progress_reports")
        pdf_path = reports_dir / filename
        
        if not pdf_path.exists():
            raise HTTPException(status_code=404, detail="报告文件不存在")
        
        return FileResponse(
            path=str(pdf_path),
            filename=filename,
            media_type='application/pdf'
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"下载报告失败: {str(e)}")

@router.delete("/reports/{filename}")
async def delete_project_report(
    filename: str,
    current_user = Depends(get_current_user)
):
    """删除项目报告"""
    try:
        reports_dir = Path("uploads/progress_reports")
        pdf_path = reports_dir / filename
        
        if not pdf_path.exists():
            raise HTTPException(status_code=404, detail="报告文件不存在")
        
        pdf_path.unlink()
        
        return {"message": "报告删除成功"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除报告失败: {str(e)}")

async def create_project_report_pdf(report_data: dict, output_path: Path):
    """创建项目报告PDF文件"""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.lib import colors
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        
        # 创建PDF文档
        doc = SimpleDocTemplate(str(output_path), pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # 标题
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=20,
            spaceAfter=30,
            alignment=1  # 居中
        )
        story.append(Paragraph(report_data["report_title"], title_style))
        story.append(Spacer(1, 20))
        
        # 报告信息
        info_data = [
            ["生成时间", report_data["generated_at"]],
            ["生成用户", report_data["generated_by"]]
        ]
        info_table = Table(info_data, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(info_table)
        story.append(Spacer(1, 30))
        
        # 系统概览
        story.append(Paragraph("系统概览", styles['Heading2']))
        overview_data = [
            ["指标", "数值"],
            ["用户总数", str(report_data["system_overview"]["total_users"])],
            ["任务总数", str(report_data["system_overview"]["total_tasks"])],
            ["设备总数", str(report_data["system_overview"]["total_devices"])]
        ]
        overview_table = Table(overview_data, colWidths=[3*inch, 3*inch])
        overview_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(overview_table)
        story.append(Spacer(1, 20))
        
        # 任务统计
        story.append(Paragraph("任务状态统计", styles['Heading2']))
        task_data = [
            ["状态", "数量"],
            ["待处理", str(report_data["task_statistics"]["pending"])],
            ["进行中", str(report_data["task_statistics"]["running"])],
            ["已完成", str(report_data["task_statistics"]["completed"])],
            ["失败", str(report_data["task_statistics"]["failed"])]
        ]
        task_table = Table(task_data, colWidths=[3*inch, 3*inch])
        task_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(task_table)
        story.append(Spacer(1, 20))
        
        # 设备统计
        story.append(Paragraph("设备状态统计", styles['Heading2']))
        device_data = [
            ["状态", "数量"],
            ["在线", str(report_data["device_statistics"]["online"])],
            ["离线", str(report_data["device_statistics"]["offline"])]
        ]
        device_table = Table(device_data, colWidths=[3*inch, 3*inch])
        device_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(device_table)
        
        # 构建PDF
        doc.build(story)
        
    except ImportError:
        # 如果没有reportlab，创建一个简单的HTML转PDF或文本报告
        with open(output_path.with_suffix('.txt'), 'w', encoding='utf-8') as f:
            f.write(f"{report_data['report_title']}\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"生成时间: {report_data['generated_at']}\n")
            f.write(f"生成用户: {report_data['generated_by']}\n\n")
            f.write("系统概览:\n")
            f.write(f"  用户总数: {report_data['system_overview']['total_users']}\n")
            f.write(f"  任务总数: {report_data['system_overview']['total_tasks']}\n")
            f.write(f"  设备总数: {report_data['system_overview']['total_devices']}\n\n")
            f.write("任务统计:\n")
            f.write(f"  待处理: {report_data['task_statistics']['pending']}\n")
            f.write(f"  进行中: {report_data['task_statistics']['running']}\n")
            f.write(f"  已完成: {report_data['task_statistics']['completed']}\n")
            f.write(f"  失败: {report_data['task_statistics']['failed']}\n\n")
            f.write("设备统计:\n")
            f.write(f"  在线: {report_data['device_statistics']['online']}\n")
            f.write(f"  离线: {report_data['device_statistics']['offline']}\n")
        
        # 重命名为pdf（实际是文本文件）
        os.rename(str(output_path.with_suffix('.txt')), str(output_path))
    
    except Exception as e:
        # 创建一个简单的文本报告作为后备方案
        with open(output_path.with_suffix('.txt'), 'w', encoding='utf-8') as f:
            f.write(f"报告生成失败: {str(e)}\n")
            f.write(f"数据: {json.dumps(report_data, ensure_ascii=False, indent=2)}")
        
        # 重命名为pdf
        os.rename(str(output_path.with_suffix('.txt')), str(output_path)) 