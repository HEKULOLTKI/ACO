from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from io import BytesIO
import logging

from app.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.device import (
    DeviceCreate, 
    DeviceUpdate, 
    DeviceResponse, 
    DeviceListResponse,
    DeviceImportResult
)
from app.services.device_service import DeviceService
from app.utils.file_utils import validate_upload_file

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/devices", response_model=DeviceListResponse)
async def get_devices(
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None,
    type: Optional[str] = None,
    status: Optional[str] = None,
    location: Optional[str] = None,
    ip: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取设备列表"""
    try:
        devices, total = DeviceService.get_devices(
            db=db, 
            skip=skip, 
            limit=limit,
            name=name,
            type=type,
            status=status,
            location=location,
            ip=ip
        )
        
        return DeviceListResponse(
            devices=devices,
            total=total,
            page=skip // limit + 1,
            page_size=limit
        )
    except Exception as e:
        logger.error(f"获取设备列表失败: {str(e)}")
        raise HTTPException(status_code=500, detail="获取设备列表失败")

@router.get("/devices/{device_id}", response_model=DeviceResponse)
async def get_device(
    device_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取单个设备详情"""
    device = DeviceService.get_device(db, device_id=device_id)
    if not device:
        raise HTTPException(status_code=404, detail="设备不存在")
    return device

@router.post("/devices", response_model=DeviceResponse)
async def create_device(
    device: DeviceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建设备"""
    try:
        return DeviceService.create_device(db=db, device=device)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"创建设备失败: {str(e)}")
        raise HTTPException(status_code=500, detail="创建设备失败")

@router.put("/devices/{device_id}", response_model=DeviceResponse)
async def update_device(
    device_id: int,
    device: DeviceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新设备"""
    try:
        db_device = DeviceService.update_device(db=db, device_id=device_id, device=device)
        if not db_device:
            raise HTTPException(status_code=404, detail="设备不存在")
        return db_device
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"更新设备失败: {str(e)}")
        raise HTTPException(status_code=500, detail="更新设备失败")

@router.delete("/devices/{device_id}")
async def delete_device(
    device_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除设备"""
    try:
        success = DeviceService.delete_device(db=db, device_id=device_id)
        if not success:
            raise HTTPException(status_code=404, detail="设备不存在")
        return {"message": "设备删除成功"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"删除设备失败: {str(e)}")
        raise HTTPException(status_code=500, detail="删除设备失败")

@router.delete("/devices/batch")
async def batch_delete_devices(
    device_ids: List[int],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """批量删除设备"""
    try:
        if not device_ids:
            raise HTTPException(status_code=400, detail="请选择要删除的设备")
        
        deleted_count = DeviceService.batch_delete_devices(db=db, device_ids=device_ids)
        return {
            "message": f"成功删除 {deleted_count} 个设备",
            "deleted_count": deleted_count
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"批量删除设备失败: {str(e)}")
        raise HTTPException(status_code=500, detail="批量删除设备失败")

@router.get("/devices/statistics")
async def get_device_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取设备统计信息"""
    try:
        return DeviceService.get_device_statistics(db=db)
    except Exception as e:
        logger.error(f"获取设备统计信息失败: {str(e)}")
        raise HTTPException(status_code=500, detail="获取设备统计信息失败")

@router.post("/devices/import", response_model=DeviceImportResult)
async def import_devices(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """批量导入设备"""
    try:
        # 验证文件
        validate_upload_file(
            file, 
            allowed_types=['.xlsx', '.xls', '.csv'],
            max_size=5 * 1024 * 1024  # 5MB
        )
        
        # 导入设备
        result = DeviceService.import_devices_from_file(db=db, file=file)
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"导入设备失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"导入设备失败: {str(e)}")

@router.get("/devices/template/download")
async def download_import_template(
    current_user: User = Depends(get_current_user)
):
    """下载设备导入模板"""
    try:
        template_data = DeviceService.export_devices_template()
        
        return StreamingResponse(
            BytesIO(template_data),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=设备导入模板.xlsx"}
        )
        
    except Exception as e:
        logger.error(f"下载导入模板失败: {str(e)}")
        raise HTTPException(status_code=500, detail="下载导入模板失败")

@router.get("/devices/export")
async def export_devices(
    name: Optional[str] = None,
    type: Optional[str] = None,
    status: Optional[str] = None,
    location: Optional[str] = None,
    ip: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """导出设备数据"""
    try:
        import pandas as pd
        from io import BytesIO
        
        # 获取所有符合条件的设备
        devices, _ = DeviceService.get_devices(
            db=db,
            skip=0,
            limit=10000,  # 导出时获取所有数据
            name=name,
            type=type,
            status=status,
            location=location,
            ip=ip
        )
        
        # 转换为DataFrame
        device_data = []
        for device in devices:
            device_data.append({
                'ID': device.id,
                '设备名称': device.name,
                '设备类型': device.type or '',
                '设备IP': device.ip or '',
                '状态': device.status,
                '位置': device.location or ''
            })
        
        df = pd.DataFrame(device_data)
        
        # 创建Excel文件
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='设备列表', index=False)
            
            # 设置列宽
            worksheet = writer.sheets['设备列表']
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width
        
        output.seek(0)
        
        return StreamingResponse(
            BytesIO(output.getvalue()),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=设备列表.xlsx"}
        )
        
    except Exception as e:
        logger.error(f"导出设备数据失败: {str(e)}")
        raise HTTPException(status_code=500, detail="导出设备数据失败")

# 设备状态管理接口
@router.put("/devices/{device_id}/status")
async def update_device_status(
    device_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新设备状态"""
    try:
        # 验证状态值
        valid_statuses = ['online', 'offline', 'maintenance', 'error']
        if status not in valid_statuses:
            raise HTTPException(
                status_code=400, 
                detail=f"无效的状态值，允许的状态: {', '.join(valid_statuses)}"
            )
        
        device_update = DeviceUpdate(status=status)
        db_device = DeviceService.update_device(db=db, device_id=device_id, device=device_update)
        
        if not db_device:
            raise HTTPException(status_code=404, detail="设备不存在")
        
        return {"message": f"设备状态已更新为 {status}"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"更新设备状态失败: {str(e)}")
        raise HTTPException(status_code=500, detail="更新设备状态失败")

@router.post("/devices/batch/status")
async def batch_update_device_status(
    device_ids: List[int],
    status: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """批量更新设备状态"""
    try:
        if not device_ids:
            raise HTTPException(status_code=400, detail="请选择要更新的设备")
        
        # 验证状态值
        valid_statuses = ['online', 'offline', 'maintenance', 'error']
        if status not in valid_statuses:
            raise HTTPException(
                status_code=400, 
                detail=f"无效的状态值，允许的状态: {', '.join(valid_statuses)}"
            )
        
        updated_count = 0
        device_update = DeviceUpdate(status=status)
        
        for device_id in device_ids:
            device = DeviceService.update_device(db=db, device_id=device_id, device=device_update)
            if device:
                updated_count += 1
        
        return {
            "message": f"成功更新 {updated_count} 个设备状态为 {status}",
            "updated_count": updated_count
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"批量更新设备状态失败: {str(e)}")
        raise HTTPException(status_code=500, detail="批量更新设备状态失败") 