import os
import mimetypes
from typing import Optional, List
from fastapi import HTTPException, UploadFile

def get_file_extension(filename: str) -> str:
    """获取文件扩展名"""
    if not filename:
        return ""
    return os.path.splitext(filename)[1].lower()

def validate_file_type(file: UploadFile, allowed_types: List[str]) -> bool:
    """验证文件类型"""
    if not file.filename:
        return False
    
    file_ext = get_file_extension(file.filename)
    return file_ext in allowed_types

def validate_file_size(file: UploadFile, max_size: int = 10 * 1024 * 1024) -> bool:
    """验证文件大小（默认10MB）"""
    if not hasattr(file, 'size'):
        return True  # 如果无法获取文件大小，跳过验证
    
    return file.size <= max_size

def get_mime_type(filename: str) -> Optional[str]:
    """获取文件MIME类型"""
    mime_type, _ = mimetypes.guess_type(filename)
    return mime_type

def is_excel_file(filename: str) -> bool:
    """判断是否为Excel文件"""
    ext = get_file_extension(filename)
    return ext in ['.xlsx', '.xls']

def is_csv_file(filename: str) -> bool:
    """判断是否为CSV文件"""
    ext = get_file_extension(filename)
    return ext == '.csv'

def validate_upload_file(
    file: UploadFile, 
    allowed_types: List[str] = None, 
    max_size: int = 10 * 1024 * 1024
) -> None:
    """验证上传文件"""
    if not file or not file.filename:
        raise HTTPException(status_code=400, detail="请选择要上传的文件")
    
    # 验证文件类型
    if allowed_types and not validate_file_type(file, allowed_types):
        raise HTTPException(
            status_code=400, 
            detail=f"不支持的文件类型，允许的类型: {', '.join(allowed_types)}"
        )
    
    # 验证文件大小
    if not validate_file_size(file, max_size):
        raise HTTPException(
            status_code=400, 
            detail=f"文件大小超过限制，最大允许 {max_size // (1024 * 1024)}MB"
        ) 