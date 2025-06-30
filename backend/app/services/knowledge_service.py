from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from typing import List, Optional, Dict, Any
from fastapi import HTTPException, UploadFile
from app.models.knowledge import KnowledgeBase, KnowledgeDocument, AIModel
from app.schemas.knowledge import (
    KnowledgeBaseCreate, KnowledgeBaseUpdate, KnowledgeBaseResponse,
    KnowledgeDocumentCreate, KnowledgeDocumentUpdate, KnowledgeDocumentResponse,
    AIModelCreate, AIModelUpdate, AIModelResponse,
    KnowledgeSearchRequest, KnowledgeSearchResult, KnowledgeStatistics
)
import os
import uuid
import json
from datetime import datetime

class KnowledgeService:
    """知识库服务"""
    
    def __init__(self, db: Session):
        self.db = db
    
    # ===== 知识库管理 =====
    
    def create_knowledge_base(
        self, 
        knowledge_base: KnowledgeBaseCreate, 
        creator_id: int
    ) -> KnowledgeBaseResponse:
        """创建知识库"""
        # 检查名称是否重复
        existing = self.db.query(KnowledgeBase).filter(
            KnowledgeBase.name == knowledge_base.name
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="知识库名称已存在")
        
        db_knowledge_base = KnowledgeBase(
            **knowledge_base.dict(),
            creator_id=creator_id
        )
        self.db.add(db_knowledge_base)
        self.db.commit()
        self.db.refresh(db_knowledge_base)
        
        # 获取文档数量
        document_count = self.db.query(KnowledgeDocument).filter(
            KnowledgeDocument.knowledge_base_id == db_knowledge_base.id
        ).count()
        
        response = KnowledgeBaseResponse.from_orm(db_knowledge_base)
        response.document_count = document_count
        return response
    
    def get_knowledge_bases(
        self, 
        skip: int = 0, 
        limit: int = 20,
        category: Optional[str] = None,
        status: Optional[str] = None,
        creator_id: Optional[int] = None
    ) -> List[KnowledgeBaseResponse]:
        """获取知识库列表"""
        from app.models.user import User
        
        query = self.db.query(KnowledgeBase)
        
        if category:
            query = query.filter(KnowledgeBase.category == category)
        if status:
            query = query.filter(KnowledgeBase.status == status)
        if creator_id:
            query = query.filter(KnowledgeBase.creator_id == creator_id)
        
        knowledge_bases = query.offset(skip).limit(limit).all()
        
        results = []
        for kb in knowledge_bases:
            # 获取文档数量
            document_count = self.db.query(KnowledgeDocument).filter(
                KnowledgeDocument.knowledge_base_id == kb.id
            ).count()
            
            # 获取分配的工程师信息
            engineer_name = None
            engineer_photo = None
            if kb.assigned_engineer_id:
                engineer = self.db.query(User).filter(User.id == kb.assigned_engineer_id).first()
                if engineer:
                    engineer_name = engineer.username
                    engineer_photo = engineer.photo_data
            
            response = KnowledgeBaseResponse.from_orm(kb)
            response.document_count = document_count
            response.assigned_engineer_name = engineer_name
            response.assigned_engineer_photo = engineer_photo
            results.append(response)
        
        return results
    
    def get_knowledge_base_by_id(self, knowledge_base_id: int) -> KnowledgeBaseResponse:
        """根据ID获取知识库"""
        from app.models.user import User
        
        knowledge_base = self.db.query(KnowledgeBase).filter(
            KnowledgeBase.id == knowledge_base_id
        ).first()
        if not knowledge_base:
            raise HTTPException(status_code=404, detail="知识库不存在")
        
        # 获取文档数量
        document_count = self.db.query(KnowledgeDocument).filter(
            KnowledgeDocument.knowledge_base_id == knowledge_base_id
        ).count()
        
        # 获取分配的工程师信息
        engineer_name = None
        engineer_photo = None
        if knowledge_base.assigned_engineer_id:
            engineer = self.db.query(User).filter(User.id == knowledge_base.assigned_engineer_id).first()
            if engineer:
                engineer_name = engineer.username
                engineer_photo = engineer.photo_data
        
        response = KnowledgeBaseResponse.from_orm(knowledge_base)
        response.document_count = document_count
        response.assigned_engineer_name = engineer_name
        response.assigned_engineer_photo = engineer_photo
        return response
    
    def update_knowledge_base(
        self, 
        knowledge_base_id: int, 
        knowledge_base_update: KnowledgeBaseUpdate,
        user_id: int
    ) -> KnowledgeBaseResponse:
        """更新知识库"""
        db_knowledge_base = self.db.query(KnowledgeBase).filter(
            KnowledgeBase.id == knowledge_base_id
        ).first()
        if not db_knowledge_base:
            raise HTTPException(status_code=404, detail="知识库不存在")
        
        # 检查权限
        if db_knowledge_base.creator_id != user_id:
            raise HTTPException(status_code=403, detail="没有权限修改此知识库")
        
        # 更新字段
        update_data = knowledge_base_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_knowledge_base, field, value)
        
        self.db.commit()
        self.db.refresh(db_knowledge_base)
        
        # 获取文档数量
        document_count = self.db.query(KnowledgeDocument).filter(
            KnowledgeDocument.knowledge_base_id == knowledge_base_id
        ).count()
        
        response = KnowledgeBaseResponse.from_orm(db_knowledge_base)
        response.document_count = document_count
        return response
    
    def delete_knowledge_base(self, knowledge_base_id: int, user_id: int):
        """删除知识库"""
        db_knowledge_base = self.db.query(KnowledgeBase).filter(
            KnowledgeBase.id == knowledge_base_id
        ).first()
        if not db_knowledge_base:
            raise HTTPException(status_code=404, detail="知识库不存在")
        
        # 检查权限
        if db_knowledge_base.creator_id != user_id:
            raise HTTPException(status_code=403, detail="没有权限删除此知识库")
        
        # 删除相关文档文件
        documents = self.db.query(KnowledgeDocument).filter(
            KnowledgeDocument.knowledge_base_id == knowledge_base_id
        ).all()
        
        for doc in documents:
            if doc.file_path and os.path.exists(doc.file_path):
                try:
                    os.remove(doc.file_path)
                except Exception as e:
                    print(f"删除文件失败: {e}")
        
        # 删除知识库（会级联删除文档记录）
        self.db.delete(db_knowledge_base)
        self.db.commit()
    
    # ===== 文档管理 =====
    
    def create_document(
        self, 
        document: KnowledgeDocumentCreate, 
        creator_id: int,
        file: Optional[UploadFile] = None
    ) -> KnowledgeDocumentResponse:
        """创建知识库文档"""
        # 检查知识库是否存在
        knowledge_base = self.db.query(KnowledgeBase).filter(
            KnowledgeBase.id == document.knowledge_base_id
        ).first()
        if not knowledge_base:
            raise HTTPException(status_code=404, detail="知识库不存在")
        
        db_document = KnowledgeDocument(
            **document.dict(),
            creator_id=creator_id
        )
        
        # 处理文件上传
        if file:
            upload_dir = "uploads/knowledge"
            os.makedirs(upload_dir, exist_ok=True)
            
            file_extension = os.path.splitext(file.filename)[1]
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            file_path = os.path.join(upload_dir, unique_filename)
            
            # 保存文件
            with open(file_path, "wb") as buffer:
                content = file.file.read()
                buffer.write(content)
            
            db_document.file_path = file_path
            db_document.file_type = file.content_type
            db_document.file_size = len(content)
            
            # 文件上传成功后设置状态
            db_document.parse_status = 'success'
            db_document.is_processed = True
            
            # 如果是文本文件，尝试读取内容
            if file.content_type.startswith('text/'):
                try:
                    db_document.content = content.decode('utf-8')
                except:
                    pass
        else:
            # 如果没有文件但有内容，也设置为成功
            if db_document.content:
                db_document.parse_status = 'success'
                db_document.is_processed = True
        
        self.db.add(db_document)
        self.db.commit()
        self.db.refresh(db_document)
        
        return KnowledgeDocumentResponse.from_orm(db_document)
    
    def get_documents(
        self, 
        knowledge_base_id: Optional[int] = None,
        skip: int = 0, 
        limit: int = 20,
        source_type: Optional[str] = None
    ) -> List[KnowledgeDocumentResponse]:
        """获取文档列表"""
        query = self.db.query(KnowledgeDocument)
        
        if knowledge_base_id:
            query = query.filter(KnowledgeDocument.knowledge_base_id == knowledge_base_id)
        if source_type:
            query = query.filter(KnowledgeDocument.source_type == source_type)
        
        documents = query.offset(skip).limit(limit).all()
        return [KnowledgeDocumentResponse.from_orm(doc) for doc in documents]
    
    def get_document_by_id(self, document_id: int) -> KnowledgeDocumentResponse:
        """根据ID获取文档"""
        document = self.db.query(KnowledgeDocument).filter(
            KnowledgeDocument.id == document_id
        ).first()
        if not document:
            raise HTTPException(status_code=404, detail="文档不存在")
        
        return KnowledgeDocumentResponse.from_orm(document)
    
    def update_document(
        self, 
        document_id: int, 
        document_update: KnowledgeDocumentUpdate,
        user_id: int
    ) -> KnowledgeDocumentResponse:
        """更新文档"""
        db_document = self.db.query(KnowledgeDocument).filter(
            KnowledgeDocument.id == document_id
        ).first()
        if not db_document:
            raise HTTPException(status_code=404, detail="文档不存在")
        
        # 检查权限
        if db_document.creator_id != user_id:
            raise HTTPException(status_code=403, detail="没有权限修改此文档")
        
        # 更新字段
        update_data = document_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_document, field, value)
        
        self.db.commit()
        self.db.refresh(db_document)
        
        return KnowledgeDocumentResponse.from_orm(db_document)
    
    def delete_document(self, document_id: int, user_id: int):
        """删除文档"""
        db_document = self.db.query(KnowledgeDocument).filter(
            KnowledgeDocument.id == document_id
        ).first()
        if not db_document:
            raise HTTPException(status_code=404, detail="文档不存在")
        
        # 检查权限
        if db_document.creator_id != user_id:
            raise HTTPException(status_code=403, detail="没有权限删除此文档")
        
        # 删除文件
        if db_document.file_path and os.path.exists(db_document.file_path):
            try:
                os.remove(db_document.file_path)
            except Exception as e:
                print(f"删除文件失败: {e}")
        
        self.db.delete(db_document)
        self.db.commit()
    
    # ===== AI模型管理 =====
    
    def create_ai_model(self, ai_model: AIModelCreate) -> AIModelResponse:
        """创建AI模型配置"""
        # 如果设置为默认模型，先取消其他模型的默认状态
        if ai_model.is_default:
            self.db.query(AIModel).filter(
                AIModel.model_type == ai_model.model_type,
                AIModel.is_default == True
            ).update({AIModel.is_default: False})
        
        db_ai_model = AIModel(**ai_model.dict())
        self.db.add(db_ai_model)
        self.db.commit()
        self.db.refresh(db_ai_model)
        
        return AIModelResponse.from_orm(db_ai_model)
    
    def get_ai_models(
        self, 
        skip: int = 0, 
        limit: int = 20,
        model_type: Optional[str] = None,
        provider: Optional[str] = None
    ) -> List[AIModelResponse]:
        """获取AI模型列表"""
        query = self.db.query(AIModel)
        
        if model_type:
            query = query.filter(AIModel.model_type == model_type)
        if provider:
            query = query.filter(AIModel.provider == provider)
        
        ai_models = query.offset(skip).limit(limit).all()
        return [AIModelResponse.from_orm(model) for model in ai_models]
    
    def get_statistics(self) -> KnowledgeStatistics:
        """获取知识库统计信息"""
        total_knowledge_bases = self.db.query(KnowledgeBase).count()
        total_documents = self.db.query(KnowledgeDocument).count()
        
        # 按分类统计
        categories = self.db.query(
            KnowledgeBase.category,
            func.count(KnowledgeBase.id).label('count')
        ).group_by(KnowledgeBase.category).all()
        
        category_stats = [
            {"category": cat[0] or "未分类", "count": cat[1]}
            for cat in categories
        ]
        
        # 最近的文档
        recent_docs = self.db.query(KnowledgeDocument).order_by(
            KnowledgeDocument.created_at.desc()
        ).limit(5).all()
        
        recent_documents = [
            KnowledgeDocumentResponse.from_orm(doc) for doc in recent_docs
        ]
        
        return KnowledgeStatistics(
            total_knowledge_bases=total_knowledge_bases,
            total_documents=total_documents,
            categories=category_stats,
            recent_documents=recent_documents
        ) 