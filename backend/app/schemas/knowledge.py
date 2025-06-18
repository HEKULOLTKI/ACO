from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any, Union
from datetime import datetime

class KnowledgeBaseBase(BaseModel):
    """知识库基础模式"""
    name: str = Field(description="知识库名称")
    description: Optional[str] = Field(default=None, description="知识库描述")
    category: Optional[str] = Field(default=None, description="知识库分类")
    tags: Optional[List[str]] = Field(default=None, description="标签")
    is_public: bool = Field(default=True, description="是否公开")
    status: str = Field(default="active", description="状态")

class KnowledgeBaseCreate(KnowledgeBaseBase):
    """创建知识库请求模式"""
    pass

class KnowledgeBaseUpdate(BaseModel):
    """更新知识库请求模式"""
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    is_public: Optional[bool] = None
    status: Optional[str] = None

class KnowledgeBaseResponse(KnowledgeBaseBase):
    """知识库响应模式"""
    id: int
    creator_id: int
    document_count: Optional[int] = 0
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class KnowledgeDocumentBase(BaseModel):
    """知识库文档基础模式"""
    title: str = Field(description="文档标题")
    content: Optional[str] = Field(default=None, description="文档内容")
    source_type: str = Field(description="来源类型")
    source_url: Optional[str] = Field(default=None, description="来源URL")
    keywords: Optional[List[str]] = Field(default=None, description="关键词")

class KnowledgeDocumentCreate(KnowledgeDocumentBase):
    """创建知识库文档请求模式"""
    knowledge_base_id: int = Field(description="所属知识库ID")

class KnowledgeDocumentUpdate(BaseModel):
    """更新知识库文档请求模式"""
    title: Optional[str] = None
    content: Optional[str] = None
    source_url: Optional[str] = None
    keywords: Optional[List[str]] = None

class KnowledgeDocumentResponse(KnowledgeDocumentBase):
    """知识库文档响应模式"""
    id: int
    file_path: Optional[str] = None
    file_type: Optional[str] = None
    file_size: Optional[int] = None
    is_processed: bool = False
    knowledge_base_id: int
    creator_id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class AIModelBase(BaseModel):
    """AI模型基础模式"""
    name: str = Field(description="模型名称")
    model_type: str = Field(description="模型类型")
    provider: str = Field(description="提供商")
    api_endpoint: Optional[str] = Field(default=None, description="API端点")
    api_key: Optional[str] = Field(default=None, description="API密钥")
    config_params: Optional[Dict[str, Any]] = Field(default=None, description="模型配置参数")
    is_default: bool = Field(default=False, description="是否为默认模型")
    status: str = Field(default="active", description="状态")

class AIModelCreate(AIModelBase):
    """创建AI模型请求模式"""
    pass

class AIModelUpdate(BaseModel):
    """更新AI模型请求模式"""
    name: Optional[str] = None
    model_type: Optional[str] = None
    provider: Optional[str] = None
    api_endpoint: Optional[str] = None
    api_key: Optional[str] = None
    config_params: Optional[Dict[str, Any]] = None
    is_default: Optional[bool] = None
    status: Optional[str] = None

class AIModelResponse(AIModelBase):
    """AI模型响应模式"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class KnowledgeSearchRequest(BaseModel):
    """知识库搜索请求"""
    query: str = Field(description="搜索查询")
    knowledge_base_ids: Optional[List[int]] = Field(default=None, description="指定知识库ID")
    top_k: int = Field(default=5, description="返回结果数量")
    similarity_threshold: float = Field(default=0.7, description="相似度阈值")

class KnowledgeSearchResult(BaseModel):
    """知识库搜索结果"""
    document_id: int
    title: str
    content: str
    similarity: float
    knowledge_base_name: str
    source_type: str
    created_at: datetime

class KnowledgeStatistics(BaseModel):
    """知识库统计信息"""
    total_knowledge_bases: int
    total_documents: int
    categories: List[Dict[str, Union[str, int]]]
    recent_documents: List[KnowledgeDocumentResponse] 