<template>
  <div class="knowledge-documents">
    <!-- 面包屑导航 -->
    <el-breadcrumb separator="/" class="breadcrumb">
      <el-breadcrumb-item @click="goBack" class="breadcrumb-link">知识库</el-breadcrumb-item>
      <el-breadcrumb-item>{{ knowledgeBaseName || '数据集' }}</el-breadcrumb-item>
    </el-breadcrumb>

    <!-- 页面标题和描述 -->
    <div class="page-header">
      <h1 class="page-title">{{ knowledgeBaseName || '数据集' }}</h1>
      <div class="page-description">
        <el-icon class="description-icon"><Warning /></el-icon>
        <span>解析成功后才能问答喵。</span>
      </div>
    </div>

    <!-- 操作栏 -->
    <div class="action-bar">
      <div class="action-left">
        <el-dropdown trigger="click" @command="handleBatchAction">
          <el-button>
            批量
            <el-icon class="el-icon--right"><ArrowDown /></el-icon>
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="delete" :disabled="selectedDocuments.length === 0">
                <el-icon><Delete /></el-icon>
                删除选中
              </el-dropdown-item>
              <el-dropdown-item command="enable" :disabled="selectedDocuments.length === 0">
                <el-icon><Check /></el-icon>
                启用选中
              </el-dropdown-item>
              <el-dropdown-item command="disable" :disabled="selectedDocuments.length === 0">
                <el-icon><Close /></el-icon>
                禁用选中
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
      
      <div class="action-right">
        <el-input
          v-model="searchQuery"
          placeholder="搜索文件"
          class="search-input"
          clearable
          @input="handleSearch"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        <el-button type="primary" @click="showAddDialog">
          <el-icon><Plus /></el-icon>
          新增文件
        </el-button>
      </div>
    </div>

    <!-- 文档表格 -->
    <div class="documents-table">
      <el-table 
        :data="filteredDocuments" 
        v-loading="loading"
        @selection-change="handleSelectionChange"
        stripe
        style="width: 100%"
      >
        <el-table-column type="selection" width="50" />
        
        <el-table-column prop="title" label="名称" min-width="200">
          <template #default="scope">
            <div class="file-info">
              <el-icon class="file-icon"><Document /></el-icon>
              <div class="file-details">
                <div class="file-name">{{ scope.row.title }}</div>
                <div class="file-type" v-if="scope.row.source_type">{{ getFileTypeText(scope.row.source_type) }}</div>
              </div>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column prop="chunk_count" label="分块数" width="100" align="center">
          <template #default="scope">
            <span>{{ scope.row.chunk_count || 0 }}</span>
          </template>
        </el-table-column>
        
        <el-table-column prop="created_at" label="上传日期" width="180">
          <template #default="scope">
            {{ formatDateTime(scope.row.created_at) }}
          </template>
        </el-table-column>
        
        <el-table-column prop="chunk_method" label="切片方法" width="120">
          <template #default="scope">
            <span>{{ scope.row.chunk_method || 'General' }}</span>
          </template>
        </el-table-column>
        
        <el-table-column prop="is_enabled" label="启用" width="80" align="center">
          <template #default="scope">
            <el-switch
              v-model="scope.row.is_enabled"
              @change="toggleDocumentStatus(scope.row)"
            />
          </template>
        </el-table-column>
        
        <el-table-column prop="parse_status" label="解析状态" width="120" align="center">
          <template #default="scope">
            <div class="parse-status">
              <el-tag 
                :type="getParseStatusType(scope.row.parse_status)"
                size="small"
              >
                {{ getParseStatusText(scope.row.parse_status) }}
              </el-tag>
              <el-icon 
                v-if="scope.row.parse_status === 'processing'"
                class="loading-icon"
              >
                <Loading />
              </el-icon>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="scope">
            <el-dropdown trigger="click">
              <el-button text>
                <el-icon><MoreFilled /></el-icon>
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="editDocument(scope.row)">
                    <el-icon><Edit /></el-icon>
                    编辑
                  </el-dropdown-item>
                  <el-dropdown-item @click="downloadDocument(scope.row)" v-if="scope.row.file_path">
                    <el-icon><Download /></el-icon>
                    下载
                  </el-dropdown-item>
                  <el-dropdown-item @click="reprocessDocument(scope.row)">
                    <el-icon><Refresh /></el-icon>
                    重新解析
                  </el-dropdown-item>
                  <el-dropdown-item divided @click="deleteDocument(scope.row)">
                    <el-icon><Delete /></el-icon>
                    删除
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 分页 -->
    <div class="pagination-container">
      <div class="pagination-info">
        总共 {{ total }} 条
      </div>
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 50, 100]"
        :total="total"
        layout="sizes, prev, pager, next"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>

    <!-- 添加/编辑文档对话框 -->
    <el-dialog 
      v-model="dialogVisible" 
      :title="isEdit ? '编辑文档' : '新增文档'"
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
          <el-radio-group v-model="documentForm.source_type">
            <el-radio label="upload">文件上传</el-radio>
            <el-radio label="url">网页链接</el-radio>
            <el-radio label="manual">手动输入</el-radio>
          </el-radio-group>
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
        
        <el-form-item 
          v-if="documentForm.source_type === 'manual'" 
          label="文档内容" 
          prop="content"
        >
          <el-input 
            v-model="documentForm.content" 
            type="textarea" 
            :rows="8"
            placeholder="请输入文档内容"
          />
        </el-form-item>
        
        <el-form-item label="切片方法">
          <el-select v-model="documentForm.chunk_method" placeholder="选择切片方法">
            <el-option label="General" value="general" />
            <el-option label="Semantic" value="semantic" />
            <el-option label="Custom" value="custom" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="关键词">
          <el-input 
            v-model="documentKeywords" 
            placeholder="请输入关键词，用逗号分隔"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitForm" :loading="submitting">
          {{ isEdit ? '更新' : '添加' }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox, type FormInstance } from 'element-plus'
import { 
  Warning, ArrowDown, Delete, Check, Close, Search, Plus, Document, 
  MoreFilled, Edit, Download, Refresh, Loading
} from '@element-plus/icons-vue'
import {
  getDocuments,
  createDocument,
  updateDocument,
  deleteDocument as deleteDocumentApi,
  downloadDocument as downloadDocumentApi,
  type KnowledgeDocument
} from '@/api/knowledge'

const route = useRoute()
const router = useRouter()

// 响应式数据
const loading = ref(false)
const submitting = ref(false)
const dialogVisible = ref(false)
const isEdit = ref(false)
const editDocumentId = ref(0)
const searchQuery = ref('')
const selectedDocuments = ref<KnowledgeDocument[]>([])
const selectedFile = ref<File | null>(null)

// 分页数据
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 知识库信息
const getKnowledgeBaseId = () => {
  const id = route.params.id
  // 处理各种可能的输入情况
  if (!id) return ''
  
  // 如果是数组，取第一个元素
  const idStr = Array.isArray(id) ? id[0] : id
  
  // 确保是字符串类型
  if (typeof idStr !== 'string') return ''
  
  // 检查是否是有效的ID字符串
  if (!idStr.trim()) {
    console.error('无效的知识库ID:', id)
    return ''
  }
  
  return idStr
}
const knowledgeBaseId = ref(getKnowledgeBaseId())
const knowledgeBaseName = ref(route.query.name as string || '')

// 文档列表
const documents = ref<KnowledgeDocument[]>([])

// 表单数据
const documentForm = reactive({
  title: '',
  content: '',
  source_type: 'upload' as 'upload' | 'url' | 'manual',
  source_url: '',
  chunk_method: 'general',
  knowledge_base_id: 0 // 将在 resetForm 中动态设置
})

const documentKeywords = ref('')

// 表单引用
const documentFormRef = ref<FormInstance>()
const uploadRef = ref<any>()

// 表单验证规则
const documentRules = {
  title: [
    { required: true, message: '请输入文档标题', trigger: 'blur' }
  ],
  source_url: [
    { required: true, message: '请输入来源链接', trigger: 'blur' }
  ],
  content: [
    { required: true, message: '请输入文档内容', trigger: 'blur' }
  ]
}

// 计算属性
const filteredDocuments = computed(() => {
  if (!searchQuery.value) {
    return documents.value
  }
  return documents.value.filter(doc => 
    doc.title.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

// 方法
const goBack = () => {
  router.push('/knowledge')
}

const loadDocuments = async () => {
  // 检查知识库ID是否有效
  if (!knowledgeBaseId.value || !knowledgeBaseId.value.trim()) {
    ElMessage.error('无效的知识库ID')
    router.push('/knowledge')
    return
  }

  loading.value = true
  try {
    // 构建请求参数，确保所有参数都是正确的类型
    const params: any = {
      skip: (currentPage.value - 1) * pageSize.value,
      limit: pageSize.value
    }
    
    // 添加知识库ID到参数中
    if (knowledgeBaseId.value && knowledgeBaseId.value.trim()) {
      params.knowledge_base_id = knowledgeBaseId.value
    }
    
    const response = await getDocuments(params)
    documents.value = response.data
    // 由于后端没有返回总数，我们需要估算
    // 如果返回的数据少于limit，说明已经是最后一页
    if (response.data.length < pageSize.value) {
      total.value = (currentPage.value - 1) * pageSize.value + response.data.length
    } else {
      // 如果返回数据等于limit，可能还有更多数据，估算总数
      total.value = currentPage.value * pageSize.value + 1
    }
  } catch (error) {
    console.error('加载文档失败:', error)
    ElMessage.error('加载文档失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  // 搜索功能已通过计算属性实现
}

const handleSelectionChange = (selection: KnowledgeDocument[]) => {
  selectedDocuments.value = selection
}

const handleBatchAction = async (command: string) => {
  if (selectedDocuments.value.length === 0) {
    ElMessage.warning('请先选择要操作的文档')
    return
  }

  try {
    switch (command) {
      case 'delete':
        await ElMessageBox.confirm('确定要删除选中的文档吗？', '批量删除', {
          type: 'warning'
        })
        for (const doc of selectedDocuments.value) {
          await deleteDocumentApi(doc.id.toString())
        }
        ElMessage.success('批量删除成功')
        break
      case 'enable':
        // 批量启用逻辑
        for (const doc of selectedDocuments.value) {
          await updateDocument(doc.id.toString(), { is_enabled: true })
        }
        ElMessage.success('批量启用成功')
        break
      case 'disable':
        // 批量禁用逻辑
        for (const doc of selectedDocuments.value) {
          await updateDocument(doc.id.toString(), { is_enabled: false })
        }
        ElMessage.success('批量禁用成功')
        break
    }
    loadDocuments()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('批量操作失败')
    }
  }
}

const showAddDialog = () => {
  resetForm()
  isEdit.value = false
  dialogVisible.value = true
}

const resetForm = () => {
  documentForm.title = ''
  documentForm.content = ''
  documentForm.source_type = 'upload'
  documentForm.source_url = ''
  documentForm.chunk_method = 'general'
  documentForm.knowledge_base_id = knowledgeBaseId.value ? parseInt(knowledgeBaseId.value) : 0
  documentKeywords.value = ''
  selectedFile.value = null
  if (uploadRef.value) {
    uploadRef.value.clearFiles()
  }
}

const handleFileChange = (file: any) => {
  selectedFile.value = file.raw
}

const submitForm = async () => {
  if (!documentFormRef.value) return
  
  // 验证知识库ID是否有效
  if (!documentForm.knowledge_base_id || documentForm.knowledge_base_id <= 0) {
    ElMessage.error('知识库ID无效，请刷新页面重试')
    return
  }
  
  try {
    await documentFormRef.value.validate()
    submitting.value = true
    
    if (isEdit.value) {
      // 对于编辑文档，我们需要构建更新数据对象而不是FormData
      const updateData: any = {
        title: documentForm.title,
        content: documentForm.content,
        source_url: documentForm.source_url,
        chunk_method: documentForm.chunk_method
      }
      
      if (documentKeywords.value) {
        updateData.keywords = documentKeywords.value.split(',').map(k => k.trim()).filter(k => k)
      }
      
      await updateDocument(editDocumentId.value.toString(), updateData)
      ElMessage.success('文档更新成功')
    } else {
      const formData = new FormData()
      formData.append('title', documentForm.title)
      formData.append('source_type', documentForm.source_type)
      formData.append('chunk_method', documentForm.chunk_method)
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
      
      await createDocument(formData)
      ElMessage.success('文档添加成功')
    }
    
    dialogVisible.value = false
    loadDocuments()
  } catch (error) {
    console.error('操作失败:', error)
    ElMessage.error('操作失败')
  } finally {
    submitting.value = false
  }
}

const editDocument = (document: KnowledgeDocument) => {
  Object.assign(documentForm, {
    title: document.title,
    content: document.content || '',
    source_type: document.source_type,
    source_url: document.source_url || '',
    chunk_method: document.chunk_method || 'general',
    knowledge_base_id: document.knowledge_base_id
  })
  documentKeywords.value = document.keywords ? document.keywords.join(',') : ''
  isEdit.value = true
  editDocumentId.value = document.id
  dialogVisible.value = true
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

const toggleDocumentStatus = async (document: KnowledgeDocument) => {
  try {
    await updateDocument(document.id.toString(), { is_enabled: document.is_enabled })
    ElMessage.success(document.is_enabled ? '已启用' : '已禁用')
  } catch (error) {
    console.error('状态更新失败:', error)
    ElMessage.error('状态更新失败')
    // 恢复原状态
    document.is_enabled = !document.is_enabled
  }
}

const reprocessDocument = async (document: KnowledgeDocument) => {
  try {
    await ElMessageBox.confirm('确定要重新解析此文档吗？', '重新解析', {
      type: 'warning'
    })
    // TODO: 调用重新解析API
    ElMessage.success('已开始重新解析')
    loadDocuments()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('重新解析失败')
    }
  }
}

const handleSizeChange = (val: number) => {
  pageSize.value = val
  currentPage.value = 1
  loadDocuments()
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
  loadDocuments()
}

// 工具方法
const formatDateTime = (time: string) => {
  return new Date(time).toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getFileTypeText = (type: string) => {
  const typeMap: Record<string, string> = {
    upload: '文件上传',
    url: '网页链接',
    manual: '手动输入'
  }
  return typeMap[type] || type
}

const getParseStatusType = (status: string) => {
  const statusMap: Record<string, string> = {
    pending: 'warning',
    processing: 'primary',
    success: 'success',
    failed: 'danger'
  }
  return statusMap[status] || 'info'
}

const getParseStatusText = (status: string) => {
  const statusMap: Record<string, string> = {
    pending: '待解析',
    processing: '解析中',
    success: '成功',
    failed: '失败'
  }
  return statusMap[status] || '未知'
}

// 组件挂载时加载数据
onMounted(() => {
  // 初始化表单的 knowledge_base_id
  documentForm.knowledge_base_id = knowledgeBaseId.value ? parseInt(knowledgeBaseId.value) : 0
  loadDocuments()
})
</script>

<style scoped lang="scss">
.knowledge-documents {
  padding: 20px;
  background: #f8fafc;
  min-height: 100vh;

  .breadcrumb {
    margin-bottom: 16px;
    
    .breadcrumb-link {
      cursor: pointer;
      color: #409eff;
      
      &:hover {
        text-decoration: underline;
      }
    }
  }

  .page-header {
    margin-bottom: 24px;
    
    .page-title {
      font-size: 24px;
      font-weight: 600;
      color: #303133;
      margin: 0 0 8px 0;
    }
    
    .page-description {
      display: flex;
      align-items: center;
      gap: 6px;
      color: #e6a23c;
      font-size: 14px;
      
      .description-icon {
        font-size: 16px;
      }
    }
  }

  .action-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    
    .action-left {
      // 批量操作区域
    }
    
    .action-right {
      display: flex;
      align-items: center;
      gap: 12px;
      
      .search-input {
        width: 250px;
      }
    }
  }

  .documents-table {
    background: white;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
    margin-bottom: 20px;
    
    .file-info {
      display: flex;
      align-items: center;
      gap: 12px;
      
      .file-icon {
        font-size: 20px;
        color: #409eff;
      }
      
      .file-details {
        .file-name {
          font-weight: 500;
          color: #303133;
          margin-bottom: 2px;
        }
        
        .file-type {
          font-size: 12px;
          color: #909399;
        }
      }
    }
    
    .parse-status {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 4px;
      
      .loading-icon {
        animation: rotate 2s linear infinite;
      }
    }
  }

  .pagination-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
    
    .pagination-info {
      color: #606266;
      font-size: 14px;
    }
  }
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style> 