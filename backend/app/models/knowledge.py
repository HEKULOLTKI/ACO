from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, Boolean, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class KnowledgeBase(Base):
    """AI知识库模型"""
    __tablename__ = "knowledge_bases"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, comment="知识库名称")
    description = Column(Text, comment="知识库描述")
    category = Column(String(100), comment="知识库分类")
    tags = Column(JSON, comment="标签")
    is_public = Column(Boolean, default=True, comment="是否公开")
    status = Column(String(50), default='active', comment="状态：active/inactive/archived")
    creator_id = Column(Integer, ForeignKey("users.id"), comment="创建者ID")
    assigned_engineer_id = Column(Integer, ForeignKey("users.id"), comment="分配的工程师ID")
    created_at = Column(TIMESTAMP, server_default=func.now(), comment="创建时间")
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 关联关系
    creator = relationship("User", back_populates="knowledge_bases", foreign_keys=[creator_id])
    assigned_engineer = relationship("User", foreign_keys=[assigned_engineer_id])
    documents = relationship("KnowledgeDocument", back_populates="knowledge_base", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<KnowledgeBase(id={self.id}, name='{self.name}', category='{self.category}')>"

class KnowledgeDocument(Base):
    """知识库文档模型"""
    __tablename__ = "knowledge_documents"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False, comment="文档标题") 
    content = Column(Text, comment="文档内容")
    source_type = Column(String(50), comment="来源类型：manual/upload/web/api")
    source_url = Column(String(1000), comment="来源URL")
    file_path = Column(String(1000), comment="文件路径")
    file_type = Column(String(255), comment="文件类型")
    file_size = Column(Integer, comment="文件大小(字节)")
    keywords = Column(JSON, comment="关键词")
    embedding_vector = Column(Text, comment="向量化表示")
    is_processed = Column(Boolean, default=False, comment="是否已处理")
    parse_status = Column(String(50), default='success', comment="解析状态：pending/processing/success/failed")
    chunk_method = Column(String(50), default='general', comment="切片方法：general/semantic/custom")
    chunk_count = Column(Integer, default=0, comment="分块数量")
    is_enabled = Column(Boolean, default=True, comment="是否启用")
    knowledge_base_id = Column(Integer, ForeignKey("knowledge_bases.id"), comment="所属知识库ID")
    creator_id = Column(Integer, ForeignKey("users.id"), comment="创建者ID")
    created_at = Column(TIMESTAMP, server_default=func.now(), comment="创建时间")
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 关联关系
    knowledge_base = relationship("KnowledgeBase", back_populates="documents")
    creator = relationship("User")
    
    def __repr__(self):
        return f"<KnowledgeDocument(id={self.id}, title='{self.title}', type='{self.source_type}')>"

class AIModel(Base):
    """AI模型配置"""
    __tablename__ = "ai_models"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, comment="模型名称")
    model_type = Column(String(100), comment="模型类型：embedding/chat/completion")
    provider = Column(String(100), comment="提供商：openai/azure/local")
    api_endpoint = Column(String(500), comment="API端点")
    api_key = Column(String(500), comment="API密钥")
    config_params = Column(JSON, comment="模型配置参数")
    is_default = Column(Boolean, default=False, comment="是否为默认模型")
    status = Column(String(50), default='active', comment="状态")
    created_at = Column(TIMESTAMP, server_default=func.now(), comment="创建时间")
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    def __repr__(self):
        return f"<AIModel(id={self.id}, name='{self.name}', type='{self.model_type}')>" 