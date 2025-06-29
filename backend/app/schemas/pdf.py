from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class PDFInfoResponse(BaseModel):
    """PDF文件信息响应模型"""
    page_count: int
    title: str
    author: str
    subject: str
    creator: str
    producer: str
    creation_date: str
    modification_date: str
    file_size: int


class PDFPageResponse(BaseModel):
    """PDF页面响应模型"""
    page_number: int
    image: str  # base64编码的图像数据
    width: int
    height: int
    text: Optional[str] = None


class PDFPreviewResponse(BaseModel):
    """PDF预览响应模型"""
    file_name: str
    file_path: str
    info: PDFInfoResponse
    pages: List[PDFPageResponse]


class PDFPageRequest(BaseModel):
    """PDF页面请求模型"""
    page_number: int = 0
    zoom: float = 1.0
    max_width: int = 800
    max_height: int = 1200
    include_text: bool = False


class PDFThumbnailRequest(BaseModel):
    """PDF缩略图请求模型"""
    zoom: float = 0.5
    max_width: int = 400
    max_height: int = 600 