from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional, Union
from fastapi import UploadFile, HTTPException
import pandas as pd
import openpyxl
from io import BytesIO
import logging

from app.models.device import Device
from app.schemas.device import DeviceCreate, DeviceUpdate, DeviceImportResult
from app.utils.file_utils import validate_file_type, get_file_extension

logger = logging.getLogger(__name__)

class DeviceService:
    """设备服务类"""
    
    @staticmethod
    def get_device(db: Session, device_id: int) -> Optional[Device]:
        """获取单个设备"""
        return db.query(Device).filter(Device.id == device_id).first()
    
    @staticmethod
    def get_device_by_name(db: Session, name: str) -> Optional[Device]:
        """根据名称获取设备"""
        return db.query(Device).filter(Device.name == name).first()
    
    @staticmethod
    def get_device_by_ip(db: Session, ip: str) -> Optional[Device]:
        """根据IP获取设备"""
        return db.query(Device).filter(Device.ip == ip).first()
    
    @staticmethod
    def get_devices(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        name: Optional[str] = None,
        type: Optional[str] = None,
        status: Optional[str] = None,
        location: Optional[str] = None,
        ip: Optional[str] = None
    ) -> tuple[List[Device], int]:
        """获取设备列表"""
        query = db.query(Device)
        
        # 添加筛选条件
        if name:
            query = query.filter(Device.name.like(f'%{name}%'))
        if type:
            query = query.filter(Device.type == type)
        if status:
            query = query.filter(Device.status == status)
        if location:
            query = query.filter(Device.location.like(f'%{location}%'))
        if ip:
            query = query.filter(Device.ip.like(f'%{ip}%'))
        
        total = query.count()
        devices = query.offset(skip).limit(limit).all()
        
        return devices, total
    
    @staticmethod
    def create_device(db: Session, device: DeviceCreate) -> Device:
        """创建设备"""
        # 检查设备名称是否重复
        if DeviceService.get_device_by_name(db, device.name):
            raise HTTPException(status_code=400, detail="设备名称已存在")
        
        # 检查IP是否重复（如果提供了IP）
        if device.ip and DeviceService.get_device_by_ip(db, device.ip):
            raise HTTPException(status_code=400, detail="设备IP已存在")
        
        db_device = Device(**device.dict())
        db.add(db_device)
        db.commit()
        db.refresh(db_device)
        return db_device
    
    @staticmethod
    def update_device(db: Session, device_id: int, device: DeviceUpdate) -> Optional[Device]:
        """更新设备"""
        db_device = DeviceService.get_device(db, device_id)
        if not db_device:
            return None
        
        # 检查名称唯一性（如果更新名称）
        if device.name and device.name != db_device.name:
            existing_device = DeviceService.get_device_by_name(db, device.name)
            if existing_device:
                raise HTTPException(status_code=400, detail="设备名称已存在")
        
        # 检查IP唯一性（如果更新IP）
        if device.ip and device.ip != db_device.ip:
            existing_device = DeviceService.get_device_by_ip(db, device.ip)
            if existing_device:
                raise HTTPException(status_code=400, detail="设备IP已存在")
        
        # 更新字段
        update_data = device.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_device, field, value)
        
        db.commit()
        db.refresh(db_device)
        return db_device
    
    @staticmethod
    def delete_device(db: Session, device_id: int) -> bool:
        """删除设备"""
        db_device = DeviceService.get_device(db, device_id)
        if not db_device:
            return False
        
        db.delete(db_device)
        db.commit()
        return True
    
    @staticmethod
    def batch_delete_devices(db: Session, device_ids: List[int]) -> int:
        """批量删除设备"""
        deleted_count = db.query(Device).filter(Device.id.in_(device_ids)).count()
        db.query(Device).filter(Device.id.in_(device_ids)).delete(synchronize_session=False)
        db.commit()
        return deleted_count
    
    @staticmethod
    def get_device_statistics(db: Session) -> dict:
        """获取设备统计信息"""
        total_devices = db.query(Device).count()
        online_devices = db.query(Device).filter(Device.status == 'online').count()
        offline_devices = db.query(Device).filter(Device.status == 'offline').count()
        
        # 按类型统计
        type_stats = db.query(Device.type, db.func.count(Device.id)).group_by(Device.type).all()
        type_statistics = {type_name: count for type_name, count in type_stats if type_name}
        
        return {
            'total_devices': total_devices,
            'online_devices': online_devices,
            'offline_devices': offline_devices,
            'type_statistics': type_statistics
        }
    
    @staticmethod
    def import_devices_from_file(db: Session, file: UploadFile) -> DeviceImportResult:
        """从文件导入设备"""
        try:
            # 验证文件类型
            file_ext = get_file_extension(file.filename)
            if file_ext not in ['.xlsx', '.xls', '.csv']:
                raise HTTPException(status_code=400, detail="不支持的文件格式，请使用 Excel 或 CSV 文件")
            
            # 读取文件内容
            content = file.file.read()
            
            # 根据文件类型解析数据
            if file_ext in ['.xlsx', '.xls']:
                df = pd.read_excel(BytesIO(content))
            else:  # csv
                df = pd.read_csv(BytesIO(content), encoding='utf-8-sig')
            
            # 验证必要列是否存在
            required_columns = ['设备名称']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise HTTPException(
                    status_code=400, 
                    detail=f"缺少必要列: {', '.join(missing_columns)}"
                )
            
            # 处理数据
            success_devices = []
            failure_details = []
            
            for index, row in df.iterrows():
                try:
                    # 构建设备数据
                    device_data = {
                        'name': str(row['设备名称']).strip() if pd.notna(row['设备名称']) else None,
                        'type': str(row['设备类型']).strip() if pd.notna(row.get('设备类型')) else None,
                        'ip': str(row['设备IP']).strip() if pd.notna(row.get('设备IP')) else None,
                        'status': str(row['状态']).strip() if pd.notna(row.get('状态')) else 'offline',
                        'location': str(row['位置']).strip() if pd.notna(row.get('位置')) else None,
                    }
                    
                    # 验证必要字段
                    if not device_data['name']:
                        failure_details.append({
                            'row': index + 2,  # Excel行号从2开始（考虑标题行）
                            'error': '设备名称不能为空'
                        })
                        continue
                    
                    # 验证IP格式（如果提供）
                    if device_data['ip']:
                        import re
                        ip_pattern = re.compile(
                            r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
                        )
                        if not ip_pattern.match(device_data['ip']):
                            failure_details.append({
                                'row': index + 2,
                                'error': f'IP地址格式不正确: {device_data["ip"]}'
                            })
                            continue
                    
                    # 检查设备名称重复
                    if DeviceService.get_device_by_name(db, device_data['name']):
                        failure_details.append({
                            'row': index + 2,
                            'error': f'设备名称已存在: {device_data["name"]}'
                        })
                        continue
                    
                    # 检查IP重复（如果提供）
                    if device_data['ip'] and DeviceService.get_device_by_ip(db, device_data['ip']):
                        failure_details.append({
                            'row': index + 2,
                            'error': f'设备IP已存在: {device_data["ip"]}'
                        })
                        continue
                    
                    # 创建设备
                    device_create = DeviceCreate(**device_data)
                    db_device = Device(**device_create.dict())
                    db.add(db_device)
                    db.flush()  # 获取ID但不提交
                    success_devices.append(db_device)
                    
                except Exception as e:
                    failure_details.append({
                        'row': index + 2,
                        'error': str(e)
                    })
                    continue
            
            # 提交所有成功的设备
            if success_devices:
                db.commit()
                # 刷新对象以获取最新数据
                for device in success_devices:
                    db.refresh(device)
            else:
                db.rollback()
            
            return DeviceImportResult(
                success_count=len(success_devices),
                failure_count=len(failure_details),
                success_devices=success_devices,
                failure_details=failure_details
            )
            
        except Exception as e:
            db.rollback()
            logger.error(f"设备导入失败: {str(e)}")
            raise HTTPException(status_code=500, detail=f"文件处理失败: {str(e)}")
    
    @staticmethod
    def export_devices_template() -> bytes:
        """导出设备导入模板"""
        try:
            # 创建示例数据
            template_data = {
                '设备名称': ['服务器001', '交换机001', '路由器001'],
                '设备类型': ['服务器', '交换机', '路由器'],
                '设备IP': ['192.168.1.100', '192.168.1.101', '192.168.1.1'],
                '状态': ['online', 'offline', 'online'],
                '位置': ['机房A', '机房B', '机房A']
            }
            
            df = pd.DataFrame(template_data)
            
            # 创建Excel文件
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='设备导入模板', index=False)
                
                # 设置列宽
                worksheet = writer.sheets['设备导入模板']
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
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"导出模板失败: {str(e)}")
            raise HTTPException(status_code=500, detail="导出模板失败") 