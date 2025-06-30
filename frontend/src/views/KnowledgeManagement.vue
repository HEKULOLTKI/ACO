<template>
  <div class="knowledge-management">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1 class="page-title">AI知识库管理</h1>
      <div class="header-actions">
        <el-button type="primary" @click="showCreateDialog">
          <el-icon><Plus /></el-icon>
          新建知识库
        </el-button>
        <el-button @click="loadData">
          <el-icon><Refresh /></el-icon>
          刷新
        </el-button>
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-grid">
      <el-card class="stats-card">
        <div class="stats-content">
          <div class="stats-icon">
            <el-icon><Folder /></el-icon>
          </div>
          <div class="stats-info">
            <div class="stats-value">{{ statistics.total_knowledge_bases }}</div>
            <div class="stats-label">知识库总数</div>
          </div>
        </div>
      </el-card>

      <el-card class="stats-card">
        <div class="stats-content">
          <div class="stats-icon">
            <el-icon><Document /></el-icon>
          </div>
          <div class="stats-info">
            <div class="stats-value">{{ statistics.total_documents }}</div>
            <div class="stats-label">文档总数</div>
          </div>
        </div>
      </el-card>

      <el-card class="stats-card">
        <div class="stats-content">
          <div class="stats-icon">
            <el-icon><Collection /></el-icon>
          </div>
          <div class="stats-info">
            <div class="stats-value">{{ statistics.categories.length }}</div>
            <div class="stats-label">分类数量</div>
          </div>
        </div>
      </el-card>
    </div>

    <!-- 知识库卡片网格 -->
    <div class="knowledge-section">
      <div class="section-header">
        <h2 class="section-title">知识库列表</h2>
      </div>
      
      <div class="knowledge-cards-container" v-loading="loading">
        <div class="knowledge-cards-grid">
          <div 
            class="knowledge-card" 
            v-for="item in knowledgeBases" 
            :key="item.id"
            @click="goToDocuments(item)"
          >
            <!-- 卡片头部 -->
            <div class="card-header">
              <div class="card-avatar">
                <el-avatar 
                  :size="40"
                  :icon="UserFilled"
                  class="engineer-avatar"
                >
                  <el-icon><UserFilled /></el-icon>
                </el-avatar>
              </div>
              <el-dropdown trigger="hover" @click.stop>
                <div class="card-more">
                  <el-icon><MoreFilled /></el-icon>
                </div>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item @click="goToDocuments(item)">
                      <el-icon><Document /></el-icon>
                      文档管理
                    </el-dropdown-item>
                    <el-dropdown-item @click="editItem(item)">
                      <el-icon><Edit /></el-icon>
                      编辑
                    </el-dropdown-item>
                    <el-dropdown-item divided @click="deleteItem(item)">
                      <el-icon><Delete /></el-icon>
                      删除
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
            
            <!-- 卡片内容 -->
            <div class="card-body">
              <h3 class="card-title">{{ item.name }}</h3>
              <p class="card-description" v-if="item.description">{{ item.description }}</p>
              
              <!-- 标签区域 -->
              <div class="card-tags" v-if="item.category || item.is_public !== undefined">
                <el-tag v-if="item.category" size="small" class="card-tag">{{ item.category }}</el-tag>
                <el-tag 
                  :type="item.is_public ? 'success' : 'warning'" 
                  size="small" 
                  class="card-tag"
                >
                  {{ item.is_public ? '公开' : '私有' }}
                </el-tag>
                <el-tag 
                  :type="item.status === 'active' ? 'success' : 'danger'" 
                  size="small" 
                  class="card-tag"
                >
                  {{ item.status === 'active' ? '启用' : '禁用' }}
                </el-tag>
              </div>
            </div>
            
            <!-- 卡片底部 -->
            <div class="card-footer">
              <div class="card-info">
                <div class="info-item">
                  <el-icon><Document /></el-icon>
                  <span>{{ item.document_count || 0 }} 文档</span>
                </div>
              </div>
              <div class="card-time">{{ formatTime(item.created_at) }}</div>
            </div>
          </div>
        </div>
        
        <!-- 空状态 -->
        <div v-if="knowledgeBases.length === 0 && !loading" class="empty-state">
          <el-empty description="暂无知识库数据">
            <el-button type="primary" @click="showCreateDialog">创建第一个知识库</el-button>
          </el-empty>
        </div>
      </div>
    </div>

    <!-- 创建/编辑对话框 -->
    <el-dialog 
      v-model="dialogVisible" 
      :title="isEdit ? '编辑知识库' : '创建知识库'"
      width="600px"
    >
      <el-form 
        :model="form" 
        :rules="rules" 
        ref="formRef"
        label-width="100px"
      >
        <el-form-item label="知识库名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入知识库名称" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input 
            v-model="form.description" 
            type="textarea" 
            :rows="3"
            placeholder="请输入知识库描述"
          />
        </el-form-item>
        <el-form-item label="分类">
          <el-input v-model="form.category" placeholder="请输入分类" />
        </el-form-item>
        <el-form-item label="公开状态">
          <el-switch v-model="form.is_public" />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="form.status">
            <el-option label="启用" value="active" />
            <el-option label="禁用" value="inactive" />
            <el-option label="归档" value="archived" />
          </el-select>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitForm" :loading="submitting">
          {{ isEdit ? '更新' : '创建' }}
        </el-button>
      </template>
    </el-dialog>

    <!-- 文档管理对话框 -->
    <el-dialog 
      v-model="documentDialogVisible" 
      :title="`${selectedKnowledgeBase?.name} - 文档管理`"
      width="1000px"
      top="5vh"
    >
      <div class="document-management">
        <!-- 文档操作按钮 -->
        <div class="document-actions">
          <el-button type="primary" @click="showAddDocumentDialog">
            <el-icon><Plus /></el-icon>
            添加文档
          </el-button>
          <el-button @click="loadDocuments">
            <el-icon><Refresh /></el-icon>
            刷新
          </el-button>
        </div>

        <!-- 文档列表 -->
        <el-table :data="documents" v-loading="documentLoading" stripe>
          <el-table-column prop="id" label="ID" width="60" />
          <el-table-column prop="title" label="文档标题" min-width="200" />
          <el-table-column prop="source_type" label="来源类型" width="100">
            <template #default="scope">
              <el-tag size="small">{{ scope.row.source_type }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="file_path" label="文件" width="120">
            <template #default="scope">
              <el-button 
                v-if="scope.row.file_path" 
                size="small" 
                type="primary" 
                text
                @click="downloadDocument(scope.row)"
              >
                下载
              </el-button>
              <span v-else class="text-gray">无文件</span>
            </template>
          </el-table-column>
          <el-table-column prop="keywords" label="关键词" min-width="150">
            <template #default="scope">
              <el-tag 
                v-for="keyword in scope.row.keywords" 
                :key="keyword" 
                size="small" 
                class="keyword-tag"
              >
                {{ keyword }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="创建时间" width="180">
            <template #default="scope">
              {{ formatTime(scope.row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="150" fixed="right">
            <template #default="scope">
              <el-button size="small" @click="editDocument(scope.row)">
                编辑
              </el-button>
              <el-button 
                size="small" 
                type="danger" 
                @click="deleteDocument(scope.row)"
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-dialog>

    <!-- 添加/编辑文档对话框 -->
    <el-dialog 
      v-model="addDocumentDialogVisible" 
      :title="isEditDocument ? '编辑文档' : '添加文档'"
      width="700px"
    >
      <el-form 
        :model="documentForm" 
        :rules="documentRules" 
        ref="documentFormRef"
        label-width="100px"
      >
        <el-form-item label="文档标题" prop="title">
          <el-input v-model="documentForm.title" placeholder="请输入文档标题" />
        </el-form-item>
        <el-form-item label="来源类型" prop="source_type">
          <el-select v-model="documentForm.source_type" placeholder="请选择来源类型">
            <el-option label="文件上传" value="upload" />
            <el-option label="网页链接" value="url" />
            <el-option label="手动输入" value="manual" />
          </el-select>
        </el-form-item>
        <el-form-item 
          v-if="documentForm.source_type === 'url'" 
          label="来源链接" 
          prop="source_url"
        >
          <el-input v-model="documentForm.source_url" placeholder="请输入网页链接" />
        </el-form-item>
        <el-form-item 
          v-if="documentForm.source_type === 'upload'" 
          label="文件上传"
        >
          <el-upload
            ref="uploadRef"
            :auto-upload="false"
            :show-file-list="true"
            :limit="1"
            accept=".txt,.doc,.docx,.pdf,.md"
            :on-change="handleFileChange"
          >
            <el-button>选择文件</el-button>
            <template #tip>
              <div class="el-upload__tip">
                支持 .txt/.doc/.docx/.pdf/.md 格式文件
              </div>
            </template>
          </el-upload>
        </el-form-item>
        <el-form-item label="文档内容">
          <el-input 
            v-model="documentForm.content" 
            type="textarea" 
            :rows="8"
            placeholder="请输入文档内容（如果上传文件则可选）"
          />
        </el-form-item>
        <el-form-item label="关键词">
          <el-input 
            v-model="documentKeywords" 
            placeholder="请输入关键词，用逗号分隔"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="addDocumentDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitDocumentForm" :loading="documentSubmitting">
          {{ isEditDocument ? '更新' : '添加' }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox, type FormInstance } from 'element-plus'
import { 
  Plus, Refresh, Folder, Document, Collection, MoreFilled, Edit, Delete, UserFilled
} from '@element-plus/icons-vue'
import {
  getKnowledgeBases, 
  createKnowledgeBase, 
  updateKnowledgeBase, 
  deleteKnowledgeBase,
  getKnowledgeStatistics,
  getDocuments,
  createDocument,
  updateDocument,
  deleteDocument as deleteDocumentApi,
  downloadDocument as downloadDocumentApi,
  type KnowledgeBase, 
  type KnowledgeStatistics,
  type KnowledgeDocument
} from '@/api/knowledge'

// 路由
const router = useRouter()

// 响应式数据
const loading = ref(false)
const submitting = ref(false)
const dialogVisible = ref(false)
const isEdit = ref(false)
const editId = ref(0)

// 文档管理相关
const documentDialogVisible = ref(false)
const addDocumentDialogVisible = ref(false)
const documentLoading = ref(false)
const documentSubmitting = ref(false)
const isEditDocument = ref(false)
const editDocumentId = ref(0)
const selectedKnowledgeBase = ref<KnowledgeBase | null>(null)
const documents = ref<KnowledgeDocument[]>([])
const selectedFile = ref<File | null>(null)

const statistics = ref<KnowledgeStatistics>({
  total_knowledge_bases: 0,
  total_documents: 0,
  categories: [],
  recent_documents: []
})

const knowledgeBases = ref<KnowledgeBase[]>([])

// 表单数据
const form = reactive({
  name: '',
  description: '',
  category: '',
  is_public: true,
  status: 'active'
})

// 文档表单数据
const documentForm = reactive({
  title: '',
  content: '',
  source_type: 'manual' as 'upload' | 'url' | 'manual',
  source_url: '',
  knowledge_base_id: 0
})

const documentKeywords = ref('')

// 表单引用
const formRef = ref<FormInstance>()
const documentFormRef = ref<FormInstance>()
const uploadRef = ref<any>()

// 表单验证规则
const rules = {
  name: [
    { required: true, message: '请输入知识库名称', trigger: 'blur' }
  ]
}

const documentRules = {
  title: [
    { required: true, message: '请输入文档标题', trigger: 'blur' }
  ],
  source_type: [
    { required: true, message: '请选择来源类型', trigger: 'change' }
  ],
  source_url: [
    { required: true, message: '请输入来源链接', trigger: 'blur' }
  ]
}

// 方法
const loadData = async () => {
  await Promise.all([
    loadStatistics(),
    loadKnowledgeBases()
  ])
}

const loadStatistics = async () => {
  try {
    const response = await getKnowledgeStatistics()
    statistics.value = response.data
  } catch (error) {
    console.error('加载统计信息失败:', error)
  }
}

const loadKnowledgeBases = async () => {
  loading.value = true
  try {
    const response = await getKnowledgeBases()
    knowledgeBases.value = response.data
  } catch (error) {
    console.error('加载知识库列表失败:', error)
    ElMessage.error('加载知识库列表失败')
  } finally {
    loading.value = false
  }
}

const showCreateDialog = () => {
  resetForm()
  isEdit.value = false
  dialogVisible.value = true
}

const resetForm = () => {
  form.name = ''
  form.description = ''
  form.category = ''
  form.is_public = true
  form.status = 'active'
}

const submitForm = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    submitting.value = true
    
    if (isEdit.value) {
      await updateKnowledgeBase(editId.value.toString(), form)
      ElMessage.success('知识库更新成功')
    } else {
      await createKnowledgeBase(form)
      ElMessage.success('知识库创建成功')
    }
    
    dialogVisible.value = false
    loadKnowledgeBases()
    loadStatistics()
  } catch (error) {
    console.error('操作失败:', error)
    ElMessage.error('操作失败')
  } finally {
    submitting.value = false
  }
}

const editItem = (item: KnowledgeBase) => {
  Object.assign(form, {
    name: item.name,
    description: item.description,
    category: item.category,
    is_public: item.is_public,
    status: item.status
  })
  isEdit.value = true
  editId.value = item.id
  dialogVisible.value = true
}

const deleteItem = async (item: KnowledgeBase) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除知识库"${item.name}"吗？此操作将同时删除该知识库下的所有文档。`,
      '删除确认',
      { type: 'warning' }
    )
    
    await deleteKnowledgeBase(item.id.toString())
    ElMessage.success('知识库删除成功')
    loadKnowledgeBases()
    loadStatistics()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
      ElMessage.error('删除失败')
    }
  }
}

// 文档管理方法
const goToDocuments = (knowledgeBase: KnowledgeBase) => {
  router.push({
    path: `/knowledge/${knowledgeBase.id}/documents`,
    query: { name: knowledgeBase.name }
  })
}

const showDocumentDialog = (knowledgeBase: KnowledgeBase) => {
  selectedKnowledgeBase.value = knowledgeBase
  documentDialogVisible.value = true
  loadDocuments()
}

const loadDocuments = async () => {
  if (!selectedKnowledgeBase.value) return
  
  documentLoading.value = true
  try {
    const response = await getDocuments({ knowledge_base_id: selectedKnowledgeBase.value.id.toString() })
    documents.value = response.data
  } catch (error) {
    console.error('加载文档失败:', error)
    ElMessage.error('加载文档失败')
  } finally {
    documentLoading.value = false
  }
}

const showAddDocumentDialog = () => {
  resetDocumentForm()
  isEditDocument.value = false
  addDocumentDialogVisible.value = true
}

const resetDocumentForm = () => {
  documentForm.title = ''
  documentForm.content = ''
  documentForm.source_type = 'manual'
  documentForm.source_url = ''
  documentForm.knowledge_base_id = selectedKnowledgeBase.value?.id || 0
  documentKeywords.value = ''
  selectedFile.value = null
  if (uploadRef.value) {
    uploadRef.value.clearFiles()
  }
}

const handleFileChange = (file: any) => {
  selectedFile.value = file.raw
}

const submitDocumentForm = async () => {
  if (!documentFormRef.value) return
  
  // 验证知识库ID是否有效
  if (!documentForm.knowledge_base_id || documentForm.knowledge_base_id <= 0) {
    ElMessage.error('请选择有效的知识库')
    return
  }
  
  try {
    await documentFormRef.value.validate()
    documentSubmitting.value = true
    
    const formData = new FormData()
    formData.append('title', documentForm.title)
    formData.append('source_type', documentForm.source_type)
    formData.append('knowledge_base_id', documentForm.knowledge_base_id.toString())
    
    if (documentForm.content) {
      formData.append('content', documentForm.content)
    }
    
    if (documentForm.source_url) {
      formData.append('source_url', documentForm.source_url)
    }
    
    if (documentKeywords.value) {
      formData.append('keywords', documentKeywords.value)
    }
    
    if (selectedFile.value) {
      formData.append('file', selectedFile.value)
    }
    
    if (isEditDocument.value) {
      // 对于编辑文档，我们需要构建更新数据对象而不是FormData
      const updateData: any = {
        title: documentForm.title,
        content: documentForm.content,
        source_url: documentForm.source_url
      }
      
      if (documentKeywords.value) {
        updateData.keywords = documentKeywords.value.split(',').map(k => k.trim()).filter(k => k)
      }
      
      await updateDocument(editDocumentId.value.toString(), updateData)
      ElMessage.success('文档更新成功')
    } else {
      await createDocument(formData)
      ElMessage.success('文档添加成功')
    }
    
    addDocumentDialogVisible.value = false
    loadDocuments()
    loadStatistics()
  } catch (error) {
    console.error('操作失败:', error)
    ElMessage.error('操作失败')
  } finally {
    documentSubmitting.value = false
  }
}

const editDocument = (document: KnowledgeDocument) => {
  Object.assign(documentForm, {
    title: document.title,
    content: document.content || '',
    source_type: document.source_type,
    source_url: document.source_url || '',
    knowledge_base_id: document.knowledge_base_id
  })
  documentKeywords.value = document.keywords ? document.keywords.join(',') : ''
  isEditDocument.value = true
  editDocumentId.value = document.id
  addDocumentDialogVisible.value = true
}

const deleteDocument = async (document: KnowledgeDocument) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除文档"${document.title}"吗？`,
      '删除确认',
      { type: 'warning' }
    )
    
    await deleteDocumentApi(document.id.toString())
    ElMessage.success('文档删除成功')
    loadDocuments()
    loadStatistics()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
      ElMessage.error('删除失败')
    }
  }
}

const downloadDocument = async (doc: KnowledgeDocument) => {
  try {
    const response = await downloadDocumentApi(doc.id.toString())
    // 处理文件下载
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.download = doc.title
    link.click()
    window.URL.revokeObjectURL(url)
  } catch (error) {
    console.error('下载失败:', error)
    ElMessage.error('下载失败')
  }
}

// 工具方法
const formatTime = (time: string) => {
  return new Date(time).toLocaleString()
}

// 组件挂载时加载数据
onMounted(() => {
  loadData()
})
</script>

<style scoped lang="scss">
.knowledge-management {
  padding: 20px;
  
  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    
    .page-title {
      font-size: 24px;
      font-weight: 600;
      color: #303133;
      margin: 0;
    }
    
    .header-actions {
      display: flex;
      gap: 10px;
    }
  }
  
  .stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    margin-bottom: 20px;
    
    .stats-card {
      .stats-content {
        display: flex;
        align-items: center;
        gap: 15px;
        
        .stats-icon {
          width: 48px;
          height: 48px;
          border-radius: 8px;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          display: flex;
          align-items: center;
          justify-content: center;
          color: white;
          font-size: 24px;
        }
        
        .stats-info {
          flex: 1;
          
          .stats-value {
            font-size: 28px;
            font-weight: 600;
            color: #303133;
            line-height: 1;
          }
          
          .stats-label {
            font-size: 14px;
            color: #909399;
            margin-top: 4px;
          }
        }
      }
    }
  }
  
  .text-gray {
    color: #909399;
  }
  
  /* 知识库卡片样式 */
  .knowledge-section {
    .section-header {
      margin-bottom: 20px;
      
      .section-title {
        font-size: 18px;
        font-weight: 600;
        color: #303133;
        margin: 0;
      }
    }
    
    .knowledge-cards-container {
      .knowledge-cards-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 20px;
        
        .knowledge-card {
          background: white;
          border-radius: 12px;
          padding: 20px;
          box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
          transition: all 0.3s ease;
          cursor: pointer;
          border: 1px solid #f0f0f0;
          
          &:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
            border-color: #e6f7ff;
          }
          
          .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
            
            .card-avatar {
              display: flex;
              align-items: center;
              justify-content: center;
              
              .engineer-avatar {
                border: 2px solid #e6f7ff;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
                transition: all 0.3s ease;
                
                &:hover {
                  transform: scale(1.1);
                  border-color: #1890ff;
                }
              }
            }
            
            .card-more {
              width: 32px;
              height: 32px;
              border-radius: 50%;
              display: flex;
              align-items: center;
              justify-content: center;
              color: #909399;
              cursor: pointer;
              transition: all 0.3s ease;
              
              &:hover {
                background: #f5f7fa;
                color: #303133;
              }
            }
          }
          
          .card-body {
            margin-bottom: 16px;
            
            .card-title {
              font-size: 16px;
              font-weight: 600;
              color: #303133;
              margin: 0 0 8px 0;
              line-height: 1.4;
            }
            
            .card-description {
              font-size: 14px;
              color: #606266;
              line-height: 1.5;
              margin: 0 0 12px 0;
              display: -webkit-box;
              -webkit-line-clamp: 2;
              -webkit-box-orient: vertical;
              overflow: hidden;
            }
            
            .card-tags {
              display: flex;
              flex-wrap: wrap;
              gap: 6px;
              
              .card-tag {
                font-size: 12px;
              }
            }
          }
          
          .card-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-top: 12px;
            border-top: 1px solid #f0f0f0;
            
            .card-info {
              display: flex;
              align-items: center;
              gap: 12px;
              
              .info-item {
                display: flex;
                align-items: center;
                gap: 4px;
                font-size: 14px;
                color: #606266;
                
                .el-icon {
                  font-size: 16px;
                  color: #909399;
                }
              }
            }
            
            .card-time {
              font-size: 12px;
              color: #909399;
            }
          }
        }
      }
      
      .empty-state {
        text-align: center;
        padding: 40px 20px;
      }
    }
  }
  
  .document-management {
    .document-actions {
      margin-bottom: 16px;
      display: flex;
      gap: 10px;
    }
    
    .keyword-tag {
      margin-right: 4px;
      margin-bottom: 4px;
    }
  }
}
</style> 