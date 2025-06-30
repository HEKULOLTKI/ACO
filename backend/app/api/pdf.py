from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse, FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import time
import uuid
from datetime import datetime, timedelta

from app.database import get_db
from app.api.deps import get_current_user
from app.schemas.user import UserResponse
from app.schemas.pdf import (
    PDFInfoResponse, PDFPageResponse, PDFPreviewResponse,
    PDFPageRequest, PDFThumbnailRequest
)
from app.services.pdf_service import PDFService
from app.config import settings

router = APIRouter(prefix="/api/pdf")

# 初始化PDF服务
pdf_service = PDFService()

# 存储临时下载token（生产环境应使用Redis）
temp_download_tokens = {}


def generate_temp_download_token(filename: str, user_id: int, expires_minutes: int = 30) -> str:
    """生成临时下载token"""
    token = str(uuid.uuid4())
    expires_at = datetime.now() + timedelta(minutes=expires_minutes)
    
    temp_download_tokens[token] = {
        "filename": filename,
        "user_id": user_id,
        "expires_at": expires_at,
        "created_at": datetime.now()
    }
    
    return token


def validate_temp_download_token(token: str, filename: str) -> bool:
    """验证临时下载token"""
    if token not in temp_download_tokens:
        return False
    
    token_data = temp_download_tokens[token]
    
    # 检查是否过期
    if datetime.now() > token_data["expires_at"]:
        del temp_download_tokens[token]
        return False
    
    # 检查文件名是否匹配
    if token_data["filename"] != filename:
        return False
    
    return True


@router.get("/files", summary="获取PDF文件列表")
async def get_pdf_files(
    directory: str = Query("uploads/progress_reports", description="目录路径"),
    current_user: UserResponse = Depends(get_current_user)
):
    """获取指定目录下的PDF文件列表"""
    try:
        if not os.path.exists(directory):
            raise HTTPException(status_code=404, detail="目录不存在")
        
        pdf_files = []
        for filename in os.listdir(directory):
            if filename.lower().endswith('.pdf'):
                file_path = os.path.join(directory, filename)
                file_size = os.path.getsize(file_path)
                modification_time = os.path.getmtime(file_path)
                
                pdf_files.append({
                    "filename": filename,
                    "file_path": file_path,
                    "file_size": file_size,
                    "modification_time": modification_time
                })
        
        # 按修改时间排序（最新的在前）
        pdf_files.sort(key=lambda x: x["modification_time"], reverse=True)
        
        return {"files": pdf_files}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取文件列表失败: {str(e)}")


@router.get("/info", response_model=PDFInfoResponse, summary="获取PDF文件信息")
async def get_pdf_info(
    file_path: str = Query(..., description="PDF文件路径"),
    current_user: UserResponse = Depends(get_current_user)
):
    """获取PDF文件的基本信息"""
    try:
        # 安全检查：确保文件路径在允许的目录内
        if not (file_path.startswith("uploads/") or file_path.startswith("./uploads/")):
            raise HTTPException(status_code=403, detail="不允许访问此路径")
        
        info = pdf_service.get_pdf_info(file_path)
        return PDFInfoResponse(**info)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取PDF信息失败: {str(e)}")


@router.get("/page", response_model=PDFPageResponse, summary="获取PDF页面图像")
async def get_pdf_page(
    file_path: str = Query(..., description="PDF文件路径"),
    page_number: int = Query(0, ge=0, description="页码（从0开始）"),
    zoom: float = Query(1.0, gt=0, le=3.0, description="缩放倍数"),
    max_width: int = Query(800, gt=0, le=2000, description="最大宽度"),
    max_height: int = Query(1200, gt=0, le=3000, description="最大高度"),
    include_text: bool = Query(False, description="是否包含文本内容"),
    current_user: UserResponse = Depends(get_current_user)
):
    """获取PDF指定页面的图像"""
    try:
        # 安全检查：确保文件路径在允许的目录内
        if not (file_path.startswith("uploads/") or file_path.startswith("./uploads/")):
            raise HTTPException(status_code=403, detail="不允许访问此路径")
        
        # 渲染页面为图像
        image_data = pdf_service.render_page_to_image(
            file_path, page_number, zoom, max_width, max_height
        )
        
        # 获取图像尺寸信息
        import fitz
        doc = fitz.open(file_path)
        page = doc[page_number]
        page_rect = page.rect
        
        # 计算实际渲染尺寸
        scale_x = max_width / page_rect.width if page_rect.width > max_width else zoom
        scale_y = max_height / page_rect.height if page_rect.height > max_height else zoom
        final_zoom = min(scale_x, scale_y, zoom)
        
        actual_width = int(page_rect.width * final_zoom)
        actual_height = int(page_rect.height * final_zoom)
        
        # 提取文本（如果需要）
        text = None
        if include_text:
            text = pdf_service.extract_text_from_page(file_path, page_number)
        
        doc.close()
        
        return PDFPageResponse(
            page_number=page_number,
            image=image_data,
            width=actual_width,
            height=actual_height,
            text=text
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取PDF页面失败: {str(e)}")


@router.get("/thumbnails", response_model=List[PDFPageResponse], summary="获取PDF所有页面缩略图")
async def get_pdf_thumbnails(
    file_path: str = Query(..., description="PDF文件路径"),
    zoom: float = Query(0.5, gt=0, le=1.0, description="缩放倍数"),
    max_width: int = Query(400, gt=0, le=800, description="最大宽度"),
    max_height: int = Query(600, gt=0, le=1200, description="最大高度"),
    current_user: UserResponse = Depends(get_current_user)
):
    """获取PDF所有页面的缩略图"""
    try:
        # 安全检查：确保文件路径在允许的目录内
        if not (file_path.startswith("uploads/") or file_path.startswith("./uploads/")):
            raise HTTPException(status_code=403, detail="不允许访问此路径")
        
        pages = pdf_service.render_all_pages_to_images(
            file_path, zoom, max_width, max_height
        )
        
        return [PDFPageResponse(**page) for page in pages]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取PDF缩略图失败: {str(e)}")


@router.get("/preview", response_model=PDFPreviewResponse, summary="获取PDF完整预览")
async def get_pdf_preview(
    file_path: str = Query(..., description="PDF文件路径"),
    thumbnail_only: bool = Query(True, description="仅获取缩略图"),
    current_user: UserResponse = Depends(get_current_user)
):
    """获取PDF文件的完整预览，包括文件信息和页面图像"""
    try:
        # 安全检查：确保文件路径在允许的目录内
        if not (file_path.startswith("uploads/") or file_path.startswith("./uploads/")):
            raise HTTPException(status_code=403, detail="不允许访问此路径")
        
        # 获取文件信息
        info = pdf_service.get_pdf_info(file_path)
        
        # 获取页面图像
        if thumbnail_only:
            pages = pdf_service.render_all_pages_to_images(file_path)
        else:
            # 如果不是缩略图模式，渲染高质量图像（但限制页数）
            max_pages = min(info["page_count"], 10)  # 限制最多10页
            pages = []
            for page_num in range(max_pages):
                image_data = pdf_service.render_page_to_image(file_path, page_num)
                pages.append({
                    "page_number": page_num,
                    "image": image_data,
                    "width": 800,  # 默认宽度
                    "height": 1200  # 默认高度
                })
        
        return PDFPreviewResponse(
            file_name=os.path.basename(file_path),
            file_path=file_path,
            info=PDFInfoResponse(**info),
            pages=[PDFPageResponse(**page) for page in pages]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取PDF预览失败: {str(e)}")


@router.get("/text/{page_number}", summary="提取PDF页面文本")
async def extract_pdf_text(
    page_number: int,
    file_path: str = Query(..., description="PDF文件路径"),
    current_user: UserResponse = Depends(get_current_user)
):
    """提取PDF指定页面的文本内容"""
    try:
        # 安全检查：确保文件路径在允许的目录内
        if not (file_path.startswith("uploads/") or file_path.startswith("./uploads/")):
            raise HTTPException(status_code=403, detail="不允许访问此路径")
        
        text = pdf_service.extract_text_from_page(file_path, page_number)
        
        return {
            "page_number": page_number,
            "text": text,
            "character_count": len(text),
            "word_count": len(text.split()) if text else 0
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"提取文本失败: {str(e)}")


@router.post("/send-to-client", summary="发送PDF预览请求到客户端")
async def send_pdf_to_client(
    filename: str = Query(..., description="PDF文件名"),
    current_user: UserResponse = Depends(get_current_user)
):
    """发送PDF预览请求到客户端"""
    try:
        from app.utils.redis_client import redis_client
        import requests
        import json
        import os
        from urllib.parse import unquote
        
        # URL解码文件名（处理中文字符）
        decoded_filename = unquote(filename)
        print(f"原始文件名: {filename}")
        print(f"解码后文件名: {decoded_filename}")
        
        # 获取用户IP地址
        user_ip = redis_client.get_user_ip(current_user.id)
        if not user_ip:
            raise HTTPException(status_code=404, detail="用户不在线或无法获取IP地址")
        
        print(f"用户IP地址: {user_ip}")
        
        # 构建PDF文件路径（使用解码后的文件名）
        reports_dir = "uploads/progress_reports"
        pdf_path = os.path.join(reports_dir, decoded_filename)
        
        if not os.path.exists(pdf_path):
            raise HTTPException(status_code=404, detail=f"PDF文件不存在: {decoded_filename}")
        
        # 获取PDF基本信息
        file_size = os.path.getsize(pdf_path)
        modification_time = os.path.getmtime(pdf_path)
        
        # 获取当前服务器信息 - 使用实际的服务器地址
        # 从请求中获取服务器地址，或使用配置的地址
        server_host = getattr(settings, 'SERVER_HOST', 'localhost')
        server_port = getattr(settings, 'SERVER_PORT', 8000)
        
        # 使用URL编码的文件名作为下载链接（无需认证）
        from urllib.parse import quote
        safe_filename = quote(decoded_filename, safe='')
        download_url = f"http://{server_host}:{server_port}/api/pdf/download/{safe_filename}"
        
        # 构建发送给客户端的JSON数据
        pdf_data = {
            "action": "pdf_download_and_preview",
            "data": {
                "filename": decoded_filename,  # 使用解码后的文件名
                "download_url": download_url,
                "file_size": file_size,
                "modification_time": modification_time,
                "preview_type": "pdf_document",
                "request_time": time.time(),
                "server_info": {
                    "host": server_host,
                    "port": server_port,
                    "protocol": "http"
                },
                "requester": {
                    "user_id": current_user.id,
                    "username": current_user.username,
                    "role": current_user.role,
                    "type": getattr(current_user, 'type', None)  # 安全获取type属性
                }
            },
            "instructions": {
                "action_required": "download_and_open_pdf",
                "download_url": download_url,
                "display_mode": "default_viewer",
                "cache_policy": "download_fresh"
            }
        }
        
        # 发送JSON数据到客户端
        client_url = f"http://{user_ip}:8800/pdf-preview"
        
        print(f"准备发送JSON数据到客户端: {client_url}")
        print(f"JSON数据内容: {json.dumps(pdf_data, ensure_ascii=False, indent=2)}")
        
        try:
            response = requests.post(
                client_url,
                json=pdf_data,
                timeout=10,
                headers={
                    'Content-Type': 'application/json',
                    'User-Agent': 'ACO-Backend-Service/1.0'
                }
            )
            
            print(f"客户端响应状态码: {response.status_code}")
            
            if response.status_code == 200:
                return {
                    "status": "success",
                    "message": f"PDF预览请求已成功发送到客户端 {user_ip}",
                    "filename": decoded_filename,
                    "target_ip": user_ip,
                    "download_url": download_url,
                    "client_response": response.json() if response.content else None
                }
            else:
                return {
                    "status": "warning",
                    "message": f"客户端响应异常 (状态码: {response.status_code})",
                    "filename": decoded_filename,
                    "target_ip": user_ip,
                    "download_url": download_url,
                    "error_detail": response.text
                }
                
        except requests.exceptions.ConnectionError:
            raise HTTPException(
                status_code=503,
                detail=f"无法连接到客户端 {user_ip}:8800，请确保客户端服务正在运行"
            )
        except requests.exceptions.Timeout:
            raise HTTPException(
                status_code=504,
                detail=f"连接客户端 {user_ip}:8800 超时"
            )
        except Exception as req_error:
            print(f"发送请求异常: {str(req_error)}")
            raise HTTPException(
                status_code=500,
                detail=f"发送请求到客户端失败: {str(req_error)}"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"发送PDF预览请求异常: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"发送PDF预览请求失败: {str(e)}")


@router.get("/reports/list", summary="获取可用的项目报告列表")
async def get_available_reports(
    current_user: UserResponse = Depends(get_current_user)
):
    """获取可用的项目报告列表"""
    try:
        reports_dir = "uploads/progress_reports"
        reports = []
        
        if os.path.exists(reports_dir):
            for filename in os.listdir(reports_dir):
                if filename.lower().endswith('.pdf'):
                    file_path = os.path.join(reports_dir, filename)
                    if os.path.isfile(file_path):
                        # 获取文件信息
                        stat = os.stat(file_path)
                        reports.append({
                            'filename': filename,
                            'path': file_path,
                            'size': stat.st_size,
                            'modified': stat.st_mtime
                        })
        
        # 按修改时间排序（最新的在前）
        reports.sort(key=lambda x: x['modified'], reverse=True)
        
        return {"reports": reports}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取报告列表失败: {str(e)}")


@router.get("/get-preview-data", summary="获取PDF预览JSON数据")
async def get_pdf_preview_data(
    filename: str = Query(..., description="PDF文件名"),
    current_user: UserResponse = Depends(get_current_user)
):
    """获取PDF预览的JSON数据，由客户端主动请求"""
    try:
        from urllib.parse import unquote, quote
        import os
        
        # URL解码文件名（处理中文字符）
        decoded_filename = unquote(filename)
        print(f"获取预览数据 - 原始文件名: {filename}")
        print(f"获取预览数据 - 解码后文件名: {decoded_filename}")
        
        # 构建PDF文件路径
        reports_dir = "uploads/progress_reports"
        pdf_path = os.path.join(reports_dir, decoded_filename)
        
        if not os.path.exists(pdf_path):
            raise HTTPException(status_code=404, detail=f"PDF文件不存在: {decoded_filename}")
        
        # 获取PDF基本信息
        file_size = os.path.getsize(pdf_path)
        modification_time = os.path.getmtime(pdf_path)
        
        # 获取当前服务器信息
        server_host = "localhost"  # 可以根据实际需要修改
        server_port = 8000  # 后端默认端口
        
        # 使用URL编码的文件名作为下载链接
        safe_filename = quote(decoded_filename, safe='')
        download_url = f"http://{server_host}:{server_port}/api/pdf/download/{safe_filename}"
        
        # 获取用户IP地址（可选，用于客户端参考）
        from app.utils.redis_client import redis_client
        user_ip = redis_client.get_user_ip(current_user.id)
        
        # 构建返回的JSON数据
        pdf_data = {
            "action": "pdf_download_and_preview",
            "data": {
                "filename": decoded_filename,
                "download_url": download_url,
                "file_size": file_size,
                "modification_time": modification_time,
                "preview_type": "pdf_document",
                "request_time": modification_time,
                "server_info": {
                    "host": server_host,
                    "port": server_port,
                    "protocol": "http"
                },
                "requester": {
                    "user_id": current_user.id,
                    "username": current_user.username,
                    "role": current_user.role,
                    "type": getattr(current_user, 'type', None)
                }
            },
            "instructions": {
                "action_required": "download_and_open_pdf",
                "download_url": download_url,
                "display_mode": "default_viewer",
                "cache_policy": "download_fresh"
            },
            "client_info": {
                "user_ip": user_ip,
                "target_port": 8800,
                "endpoint": "/pdf-preview"
            }
        }
        
        print(f"✅ 准备PDF预览数据成功")
        print(f"   文件名: {decoded_filename}")
        print(f"   文件大小: {file_size} bytes")
        print(f"   用户IP: {user_ip}")
        
        return pdf_data
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"获取PDF预览数据异常: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"获取PDF预览数据失败: {str(e)}")


@router.get("/download/{filename}", summary="下载PDF文件（无需认证）")
async def download_pdf_file(
    filename: str
):
    """提供PDF文件下载服务，供客户端下载并预览（无需认证）"""
    try:
        from urllib.parse import unquote
        
        # URL解码文件名（处理中文字符）
        decoded_filename = unquote(filename)
        print(f"下载请求 - 原始文件名: {filename}")
        print(f"下载请求 - 解码后文件名: {decoded_filename}")
        
        # 安全检查：验证文件名
        if not decoded_filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="仅支持PDF文件下载")
        
        # 防止路径遍历攻击
        if '..' in decoded_filename or '/' in decoded_filename or '\\' in decoded_filename:
            raise HTTPException(status_code=400, detail="无效的文件名")
        
        # 构建文件路径
        reports_dir = "uploads/progress_reports"
        file_path = os.path.join(reports_dir, decoded_filename)
        
        # 检查文件是否存在
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail=f"文件不存在: {decoded_filename}")
        
        # 检查文件是否在允许的目录内
        abs_file_path = os.path.abspath(file_path)
        abs_reports_dir = os.path.abspath(reports_dir)
        
        if not abs_file_path.startswith(abs_reports_dir):
            raise HTTPException(status_code=403, detail="文件路径不允许")
        
        # 记录下载日志
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"下载PDF文件: {decoded_filename}")
        
        # 处理中文文件名编码问题
        from urllib.parse import quote
        
        # 创建ASCII安全的文件名作为备用
        safe_filename = "document.pdf"
        try:
            # 尝试使用原文件名（去掉扩展名）作为基础
            base_name = os.path.splitext(decoded_filename)[0]
            # 为ASCII兼容性，如果文件名包含非ASCII字符，使用简化名称
            if any(ord(char) > 127 for char in base_name):
                safe_filename = "document.pdf"
            else:
                safe_filename = decoded_filename
        except:
            safe_filename = "document.pdf"
        
        # 为HTTP头部准备编码的文件名
        encoded_filename = quote(decoded_filename.encode('utf-8'))
        
        # 返回文件响应，使用更兼容的Content-Disposition格式
        return FileResponse(
            path=file_path,
            filename=safe_filename,  # FastAPI内部使用的安全文件名
            media_type='application/pdf',
            headers={
                "Content-Disposition": f"attachment; filename=\"{safe_filename}\"; filename*=UTF-8''{encoded_filename}",
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"下载PDF文件异常: {str(e)}")
        raise HTTPException(status_code=500, detail=f"下载文件失败: {str(e)}")


@router.get("/download-with-token/{filename}", summary="使用临时token下载PDF文件（无需认证）")
async def download_pdf_with_token(
    filename: str,
    token: str = Query(..., description="临时下载token")
):
    """使用临时token下载PDF文件，无需用户认证"""
    try:
        from urllib.parse import unquote
        
        # URL解码文件名
        decoded_filename = unquote(filename)
        
        # 验证临时token
        if not validate_temp_download_token(token, decoded_filename):
            raise HTTPException(status_code=401, detail="无效或已过期的下载token")
        
        # 安全检查：验证文件名
        if not decoded_filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="仅支持PDF文件下载")
        
        # 防止路径遍历攻击
        if '..' in decoded_filename or '/' in decoded_filename or '\\' in decoded_filename:
            raise HTTPException(status_code=400, detail="无效的文件名")
        
        # 构建文件路径
        reports_dir = "uploads/progress_reports"
        file_path = os.path.join(reports_dir, decoded_filename)
        
        # 检查文件是否存在
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail=f"文件不存在: {decoded_filename}")
        
        # 检查文件是否在允许的目录内
        abs_file_path = os.path.abspath(file_path)
        abs_reports_dir = os.path.abspath(reports_dir)
        
        if not abs_file_path.startswith(abs_reports_dir):
            raise HTTPException(status_code=403, detail="文件路径不允许")
        
        # 使用后删除token（一次性使用）
        del temp_download_tokens[token]
        
        print(f"✅ 临时token下载PDF文件: {decoded_filename}")
        
        # 处理中文文件名编码问题
        from urllib.parse import quote
        
        # 创建ASCII安全的文件名作为备用
        safe_filename = "document.pdf"
        try:
            # 尝试使用原文件名（去掉扩展名）作为基础
            base_name = os.path.splitext(decoded_filename)[0]
            # 为ASCII兼容性，如果文件名包含非ASCII字符，使用简化名称
            if any(ord(char) > 127 for char in base_name):
                safe_filename = "document.pdf"
            else:
                safe_filename = decoded_filename
        except:
            safe_filename = "document.pdf"
        
        # 为HTTP头部准备编码的文件名
        encoded_filename = quote(decoded_filename.encode('utf-8'))
        
        # 返回文件响应，使用更兼容的Content-Disposition格式
        return FileResponse(
            path=file_path,
            filename=safe_filename,  # FastAPI内部使用的安全文件名
            media_type='application/pdf',
            headers={
                "Content-Disposition": f"attachment; filename=\"{safe_filename}\"; filename*=UTF-8''{encoded_filename}",
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"临时token下载PDF文件异常: {str(e)}")
        raise HTTPException(status_code=500, detail=f"下载文件失败: {str(e)}") 