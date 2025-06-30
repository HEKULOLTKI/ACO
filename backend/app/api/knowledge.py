from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.api.deps import get_current_user, get_admin_user
from app.schemas.user import UserResponse
from app.schemas.knowledge import (
    KnowledgeBaseCreate, KnowledgeBaseUpdate, KnowledgeBaseResponse,
    KnowledgeDocumentCreate, KnowledgeDocumentUpdate, KnowledgeDocumentResponse,
    AIModelCreate, AIModelUpdate, AIModelResponse,
    KnowledgeSearchRequest, KnowledgeSearchResult, KnowledgeStatistics
)
from app.services.knowledge_service import KnowledgeService

router = APIRouter(prefix="/api/knowledge")

# ===== 知识库管理 =====

@router.post("/bases", response_model=KnowledgeBaseResponse, summary="创建知识库")
async def create_knowledge_base(
    knowledge_base: KnowledgeBaseCreate,
    current_user: UserResponse = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """创建新的知识库"""
    service = KnowledgeService(db)
    return service.create_knowledge_base(knowledge_base, current_user.id)

@router.get("/bases", response_model=List[KnowledgeBaseResponse], summary="获取知识库列表")
async def get_knowledge_bases(
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(20, ge=1, le=100, description="返回记录数"),
    category: Optional[str] = Query(None, description="分类筛选"),
    status: Optional[str] = Query(None, description="状态筛选"),
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取知识库列表"""
    service = KnowledgeService(db)
    # 管理员可以查看所有知识库，普通用户只能查看自己创建的
    creator_id = None if current_user.type == '管理员' else current_user.id
    return service.get_knowledge_bases(skip, limit, category, status, creator_id)

@router.get("/bases/{knowledge_base_id}", response_model=KnowledgeBaseResponse, summary="获取知识库详情")
async def get_knowledge_base(
    knowledge_base_id: str,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取指定知识库的详细信息"""
    try:
        kb_id = int(knowledge_base_id)
    except (ValueError, TypeError):
        raise HTTPException(status_code=422, detail="Invalid knowledge_base_id: must be a valid integer")
    
    service = KnowledgeService(db)
    return service.get_knowledge_base_by_id(kb_id)

@router.put("/bases/{knowledge_base_id}", response_model=KnowledgeBaseResponse, summary="更新知识库")
async def update_knowledge_base(
    knowledge_base_id: str,
    knowledge_base_update: KnowledgeBaseUpdate,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新知识库信息"""
    try:
        kb_id = int(knowledge_base_id)
    except (ValueError, TypeError):
        raise HTTPException(status_code=422, detail="Invalid knowledge_base_id: must be a valid integer")
    
    service = KnowledgeService(db)
    return service.update_knowledge_base(kb_id, knowledge_base_update, current_user.id)

@router.delete("/bases/{knowledge_base_id}", summary="删除知识库")
async def delete_knowledge_base(
    knowledge_base_id: str,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除知识库及其所有文档"""
    try:
        kb_id = int(knowledge_base_id)
    except (ValueError, TypeError):
        raise HTTPException(status_code=422, detail="Invalid knowledge_base_id: must be a valid integer")
    
    service = KnowledgeService(db)
    service.delete_knowledge_base(kb_id, current_user.id)
    return {"message": "知识库删除成功"}

# ===== 文档管理 =====

@router.post("/documents", response_model=KnowledgeDocumentResponse, summary="创建文档")
async def create_document(
    title: str = Form(...),
    content: Optional[str] = Form(None),
    source_type: str = Form(...),
    source_url: Optional[str] = Form(None),
    keywords: Optional[str] = Form(None),
    knowledge_base_id: str = Form(...),
    chunk_method: Optional[str] = Form("general"),
    file: Optional[UploadFile] = File(None),
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建新文档，支持文件上传"""
    service = KnowledgeService(db)
    
    # 处理 knowledge_base_id，转换为整数
    try:
        kb_id = int(knowledge_base_id)
    except (ValueError, TypeError):
        raise HTTPException(status_code=422, detail="Invalid knowledge_base_id: must be a valid integer")
    
    # 处理关键词
    keywords_list = []
    if keywords:
        keywords_list = [kw.strip() for kw in keywords.split(',') if kw.strip()]
    
    document_create = KnowledgeDocumentCreate(
        title=title,
        content=content,
        source_type=source_type,
        source_url=source_url,
        keywords=keywords_list,
        knowledge_base_id=kb_id,
        chunk_method=chunk_method
    )
    
    return service.create_document(document_create, current_user.id, file)

@router.get("/documents", response_model=List[KnowledgeDocumentResponse], summary="获取文档列表")
async def get_documents(
    knowledge_base_id: Optional[int] = Query(None, description="知识库ID"),
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(20, ge=1, le=100, description="返回记录数"),
    source_type: Optional[str] = Query(None, description="来源类型筛选"),
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取文档列表"""
    service = KnowledgeService(db)
    return service.get_documents(knowledge_base_id, skip, limit, source_type)

@router.get("/documents/{document_id}", response_model=KnowledgeDocumentResponse, summary="获取文档详情")
async def get_document(
    document_id: str,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取指定文档的详细信息"""
    try:
        doc_id = int(document_id)
    except (ValueError, TypeError):
        raise HTTPException(status_code=422, detail="Invalid document_id: must be a valid integer")
    
    service = KnowledgeService(db)
    return service.get_document_by_id(doc_id)

@router.put("/documents/{document_id}", response_model=KnowledgeDocumentResponse, summary="更新文档")
async def update_document(
    document_id: str,
    document_update: KnowledgeDocumentUpdate,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新文档信息"""
    try:
        doc_id = int(document_id)
    except (ValueError, TypeError):
        raise HTTPException(status_code=422, detail="Invalid document_id: must be a valid integer")
    
    service = KnowledgeService(db)
    return service.update_document(doc_id, document_update, current_user.id)

@router.delete("/documents/{document_id}", summary="删除文档")
async def delete_document(
    document_id: str,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除文档"""
    try:
        doc_id = int(document_id)
    except (ValueError, TypeError):
        raise HTTPException(status_code=422, detail="Invalid document_id: must be a valid integer")
    
    service = KnowledgeService(db)
    service.delete_document(doc_id, current_user.id)
    return {"message": "文档删除成功"}

# ===== AI模型管理 =====

@router.post("/ai-models", response_model=AIModelResponse, summary="创建AI模型配置")
async def create_ai_model(
    ai_model: AIModelCreate,
    current_user: UserResponse = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """创建AI模型配置"""
    service = KnowledgeService(db)
    return service.create_ai_model(ai_model)

@router.get("/ai-models", response_model=List[AIModelResponse], summary="获取AI模型列表")
async def get_ai_models(
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(20, ge=1, le=100, description="返回记录数"),
    model_type: Optional[str] = Query(None, description="模型类型筛选"),
    provider: Optional[str] = Query(None, description="提供商筛选"),
    current_user: UserResponse = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """获取AI模型配置列表"""
    service = KnowledgeService(db)
    return service.get_ai_models(skip, limit, model_type, provider)

# ===== 统计信息 =====

@router.get("/statistics", response_model=KnowledgeStatistics, summary="获取知识库统计信息")
async def get_knowledge_statistics(
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取知识库统计信息"""
    service = KnowledgeService(db)
    return service.get_statistics()

# ===== 文件下载 =====

@router.get("/documents/{document_id}/download", summary="下载文档文件")
async def download_document(
    document_id: str,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """下载文档文件"""
    from fastapi.responses import FileResponse
    import os
    
    try:
        doc_id = int(document_id)
    except (ValueError, TypeError):
        raise HTTPException(status_code=422, detail="Invalid document_id: must be a valid integer")
    
    service = KnowledgeService(db)
    document = service.get_document_by_id(doc_id)
    
    if not document.file_path or not os.path.exists(document.file_path):
        raise HTTPException(status_code=404, detail="文件不存在")
    
    return FileResponse(
        path=document.file_path,
        filename=document.title,
        media_type='application/octet-stream'
    ) 