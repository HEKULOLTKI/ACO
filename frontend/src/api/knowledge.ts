import request from '@/utils/request'

export interface KnowledgeBase {
  id: number
  name: string
  description?: string
  category?: string
  tags?: string[]
  is_public: boolean
  status: string
  creator_id: number
  document_count: number
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
  model_config?: Record<string, any>
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
}) => {
  return request.post('/knowledge/bases', data)
}

export const getKnowledgeBases = (params?: {
  skip?: number
  limit?: number
  category?: string
  status?: string
}) => {
  return request.get<KnowledgeBase[]>('/knowledge/bases', { params })
}

export const getKnowledgeBase = (id: number) => {
  return request.get<KnowledgeBase>(`/knowledge/bases/${id}`)
}

export const updateKnowledgeBase = (id: number, data: {
  name?: string
  description?: string
  category?: string
  tags?: string[]
  is_public?: boolean
  status?: string
}) => {
  return request.put(`/knowledge/bases/${id}`, data)
}

export const deleteKnowledgeBase = (id: number) => {
  return request.delete(`/knowledge/bases/${id}`)
}

// ===== 文档管理 =====

export const createDocument = (formData: FormData) => {
  return request.post('/knowledge/documents', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

export const getDocuments = (params?: {
  knowledge_base_id?: number
  skip?: number
  limit?: number
  source_type?: string
}) => {
  return request.get<KnowledgeDocument[]>('/knowledge/documents', { params })
}

export const getDocument = (id: number) => {
  return request.get<KnowledgeDocument>(`/knowledge/documents/${id}`)
}

export const updateDocument = (id: number, data: {
  title?: string
  content?: string
  source_url?: string
  keywords?: string[]
}) => {
  return request.put(`/knowledge/documents/${id}`, data)
}

export const deleteDocument = (id: number) => {
  return request.delete(`/knowledge/documents/${id}`)
}

export const downloadDocument = (id: number) => {
  return request.get(`/knowledge/documents/${id}/download`, {
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
  model_config?: Record<string, any>
  is_default?: boolean
  status?: string
}) => {
  return request.post('/knowledge/ai-models', data)
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