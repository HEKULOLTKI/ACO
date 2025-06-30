import request from '@/utils/request'

// ===== 类型定义 =====

export interface KnowledgeBase {
  id: number
  name: string
  description?: string
  category?: string
  tags?: string[]
  is_public: boolean
  status: string
  creator_id: number
  assigned_engineer_id?: number
  assigned_engineer_name?: string
  assigned_engineer_photo?: string
  document_count?: number
  created_at: string
  updated_at: string
}

export interface KnowledgeDocument {
  id: number
  title: string
  content?: string
  source_type: string
  source_url?: string
  file_path?: string
  file_type?: string
  file_size?: number
  keywords?: string[]
  is_processed: boolean
  parse_status: string
  chunk_method: string
  chunk_count: number
  is_enabled: boolean
  knowledge_base_id: number
  creator_id: number
  created_at: string
  updated_at: string
}

export interface AIModel {
  id: number
  name: string
  model_type: string
  provider: string
  api_endpoint?: string
  api_key?: string
  config_params?: Record<string, any>
  is_default: boolean
  status: string
  created_at: string
  updated_at: string
}

export interface KnowledgeStatistics {
  total_knowledge_bases: number
  total_documents: number
  categories: Array<{ category: string; count: number }>
  recent_documents: KnowledgeDocument[]
}

// ===== 知识库管理 =====

export const createKnowledgeBase = (data: {
  name: string
  description?: string
  category?: string
  tags?: string[]
  is_public?: boolean
  status?: string
  assigned_engineer_id?: number
}) => {
  return request.post<KnowledgeBase>('/knowledge/bases', data)
}

export const getKnowledgeBases = (params?: {
  skip?: number
  limit?: number
  category?: string
  status?: string
}) => {
  return request.get<KnowledgeBase[]>('/knowledge/bases', { params })
}

export const getKnowledgeBase = (knowledgeBaseId: string) => {
  return request.get<KnowledgeBase>(`/knowledge/bases/${knowledgeBaseId}`)
}

export const updateKnowledgeBase = (knowledgeBaseId: string, data: {
  name?: string
  description?: string
  category?: string
  tags?: string[]
  is_public?: boolean
  status?: string
  assigned_engineer_id?: number
}) => {
  return request.put<KnowledgeBase>(`/knowledge/bases/${knowledgeBaseId}`, data)
}

export const deleteKnowledgeBase = (knowledgeBaseId: string) => {
  return request.delete(`/knowledge/bases/${knowledgeBaseId}`)
}

// ===== 文档管理 =====

export const createDocument = (formData: FormData) => {
  return request.post<KnowledgeDocument>('/knowledge/documents', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

export const getDocuments = (params?: {
  knowledge_base_id?: string
  skip?: number
  limit?: number
  source_type?: string
}) => {
  return request.get<KnowledgeDocument[]>('/knowledge/documents', { params })
}

export const getDocument = (documentId: string) => {
  return request.get<KnowledgeDocument>(`/knowledge/documents/${documentId}`)
}

export const updateDocument = (documentId: string, data: {
  title?: string
  content?: string
  source_url?: string
  keywords?: string[]
  parse_status?: string
  chunk_method?: string
  chunk_count?: number
  is_enabled?: boolean
}) => {
  return request.put<KnowledgeDocument>(`/knowledge/documents/${documentId}`, data)
}

export const deleteDocument = (documentId: string) => {
  return request.delete(`/knowledge/documents/${documentId}`)
}

export const downloadDocument = (documentId: string) => {
  return request.get(`/knowledge/documents/${documentId}/download`, {
    responseType: 'blob'
  })
}

// ===== AI模型管理 =====

export const createAIModel = (data: {
  name: string
  model_type: string
  provider: string
  api_endpoint?: string
  api_key?: string
  config_params?: Record<string, any>
  is_default?: boolean
  status?: string
}) => {
  return request.post<AIModel>('/knowledge/ai-models', data)
}

export const getAIModels = (params?: {
  skip?: number
  limit?: number
  model_type?: string
  provider?: string
}) => {
  return request.get<AIModel[]>('/knowledge/ai-models', { params })
}

// ===== 统计信息 =====

export const getKnowledgeStatistics = () => {
  return request.get<KnowledgeStatistics>('/knowledge/statistics')
} 