import fitz  # PyMuPDF
import io
import base64
from typing import List, Optional, Tuple
from fastapi import HTTPException
import os
from PIL import Image


class PDFService:
    """PDF处理服务，用于渲染PDF页面为图像"""
    
    def __init__(self):
        self.supported_formats = ['pdf']
    
    def validate_pdf_file(self, file_path: str) -> bool:
        """验证PDF文件是否存在且有效"""
        if not os.path.exists(file_path):
            return False
        
        if not file_path.lower().endswith('.pdf'):
            return False
        
        try:
            doc = fitz.open(file_path)
            doc.close()
            return True
        except Exception:
            return False
    
    def get_pdf_info(self, file_path: str) -> dict:
        """获取PDF文件基本信息"""
        if not self.validate_pdf_file(file_path):
            raise HTTPException(status_code=400, detail="无效的PDF文件")
        
        try:
            doc = fitz.open(file_path)
            info = {
                "page_count": doc.page_count,
                "title": doc.metadata.get("title", ""),
                "author": doc.metadata.get("author", ""),
                "subject": doc.metadata.get("subject", ""),
                "creator": doc.metadata.get("creator", ""),
                "producer": doc.metadata.get("producer", ""),
                "creation_date": doc.metadata.get("creationDate", ""),
                "modification_date": doc.metadata.get("modDate", ""),
                "file_size": os.path.getsize(file_path)
            }
            doc.close()
            return info
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"获取PDF信息失败: {str(e)}")
    
    def render_page_to_image(
        self, 
        file_path: str, 
        page_number: int = 0, 
        zoom: float = 1.0,
        max_width: int = 800,
        max_height: int = 1200
    ) -> str:
        """
        将PDF页面渲染为图像并返回base64编码
        
        Args:
            file_path: PDF文件路径
            page_number: 页码（从0开始）
            zoom: 缩放倍数
            max_width: 最大宽度
            max_height: 最大高度
            
        Returns:
            base64编码的图像数据
        """
        if not self.validate_pdf_file(file_path):
            raise HTTPException(status_code=400, detail="无效的PDF文件")
        
        try:
            doc = fitz.open(file_path)
            
            if page_number < 0 or page_number >= doc.page_count:
                doc.close()
                raise HTTPException(status_code=400, detail=f"页码超出范围，PDF共有{doc.page_count}页")
            
            page = doc[page_number]
            
            # 计算合适的缩放比例
            page_rect = page.rect
            scale_x = max_width / page_rect.width if page_rect.width > max_width else zoom
            scale_y = max_height / page_rect.height if page_rect.height > max_height else zoom
            final_zoom = min(scale_x, scale_y, zoom)
            
            # 创建变换矩阵
            mat = fitz.Matrix(final_zoom, final_zoom)
            
            # 渲染页面为图像
            pix = page.get_pixmap(matrix=mat)
            
            # 转换为PIL图像
            img_data = pix.tobytes("png")
            doc.close()
            
            # 转换为base64
            img_base64 = base64.b64encode(img_data).decode('utf-8')
            return f"data:image/png;base64,{img_base64}"
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"渲染PDF页面失败: {str(e)}")
    
    def render_all_pages_to_images(
        self, 
        file_path: str, 
        zoom: float = 0.5,
        max_width: int = 400,
        max_height: int = 600
    ) -> List[dict]:
        """
        将PDF所有页面渲染为缩略图
        
        Args:
            file_path: PDF文件路径
            zoom: 缩放倍数（缩略图通常较小）
            max_width: 最大宽度
            max_height: 最大高度
            
        Returns:
            包含所有页面图像的列表
        """
        if not self.validate_pdf_file(file_path):
            raise HTTPException(status_code=400, detail="无效的PDF文件")
        
        try:
            doc = fitz.open(file_path)
            pages = []
            
            for page_num in range(doc.page_count):
                page = doc[page_num]
                
                # 计算合适的缩放比例
                page_rect = page.rect
                scale_x = max_width / page_rect.width if page_rect.width > max_width else zoom
                scale_y = max_height / page_rect.height if page_rect.height > max_height else zoom
                final_zoom = min(scale_x, scale_y, zoom)
                
                # 创建变换矩阵
                mat = fitz.Matrix(final_zoom, final_zoom)
                
                # 渲染页面为图像
                pix = page.get_pixmap(matrix=mat)
                img_data = pix.tobytes("png")
                
                # 转换为base64
                img_base64 = base64.b64encode(img_data).decode('utf-8')
                
                pages.append({
                    "page_number": page_num,
                    "image": f"data:image/png;base64,{img_base64}",
                    "width": pix.width,
                    "height": pix.height
                })
            
            doc.close()
            return pages
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"渲染PDF页面失败: {str(e)}")
    
    def extract_text_from_page(self, file_path: str, page_number: int = 0) -> str:
        """从PDF页面提取文本"""
        if not self.validate_pdf_file(file_path):
            raise HTTPException(status_code=400, detail="无效的PDF文件")
        
        try:
            doc = fitz.open(file_path)
            
            if page_number < 0 or page_number >= doc.page_count:
                doc.close()
                raise HTTPException(status_code=400, detail=f"页码超出范围，PDF共有{doc.page_count}页")
            
            page = doc[page_number]
            text = page.get_text()
            doc.close()
            
            return text
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"提取文本失败: {str(e)}") 