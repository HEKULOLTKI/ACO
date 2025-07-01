<template>
  <div class="knowledge-management">
    <!-- 页面标题 -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">
          <el-icon class="title-icon"><Collection /></el-icon>
          AI知识库管理
        </h1>
        <div class="header-description">
          <span>管理您的知识库，构建智能问答系统</span>
        </div>
      </div>
      <div class="header-actions">
        <el-button @click="loadData" size="large">
          <el-icon><Refresh /></el-icon>
          刷新数据
        </el-button>
      </div>
    </div>

        <!-- 统计面板 -->
    <div class="stats-panel">
      <div class="stats-overview">
        <div class="overview-title">
          <h2>数据概览</h2>
          <p>实时监控您的知识库运营状况</p>
        </div>
        <div class="overview-actions">
          <el-button type="primary" @click="showCreateDialog" size="large">
            <el-icon><Plus /></el-icon>
            新建知识库
          </el-button>
          <el-dropdown trigger="click" @command="handleQuickAction">
            <el-button size="large">
              更多操作
              <el-icon class="el-icon--right"><ArrowDown /></el-icon>
            </el-button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="import">
                  <el-icon><Upload /></el-icon>
                  导入知识库
                </el-dropdown-item>
                <el-dropdown-item command="template">
                  <el-icon><Files /></el-icon>
                  知识库模板
                </el-dropdown-item>
                <el-dropdown-item command="export">
                  <el-icon><Download /></el-icon>
                  导出数据
                </el-dropdown-item>
                <el-dropdown-item divided command="settings">
                  <el-icon><Setting /></el-icon>
                  系统设置
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
      
      <div class="stats-grid">
        <div class="stats-card primary">
          <div class="stats-content">
            <div class="stats-main">
              <div class="stats-value">{{ statistics.total_knowledge_bases }}</div>
              <div class="stats-label">知识库总数</div>
            </div>
            <div class="stats-icon">
              <el-icon><Folder /></el-icon>
            </div>
          </div>
          <div class="stats-footer">
            <div class="stats-trend positive">
              <el-icon><TrendCharts /></el-icon>
              <span>较上月增长 12%</span>
            </div>
          </div>
        </div>

        <div class="stats-card success">
          <div class="stats-content">
            <div class="stats-main">
              <div class="stats-value">{{ statistics.total_documents }}</div>
              <div class="stats-label">文档总数</div>
            </div>
            <div class="stats-icon">
              <el-icon><Document /></el-icon>
            </div>
          </div>
          <div class="stats-footer">
            <div class="stats-trend positive">
              <el-icon><TrendCharts /></el-icon>
              <span>较上月增长 8%</span>
            </div>
          </div>
        </div>

        <div class="stats-card warning">
          <div class="stats-content">
            <div class="stats-main">
              <div class="stats-value">{{ statistics.categories.length }}</div>
              <div class="stats-label">分类数量</div>
            </div>
            <div class="stats-icon">
              <el-icon><CollectionTag /></el-icon>
            </div>
          </div>
          <div class="stats-footer">
            <div class="stats-trend positive">
              <el-icon><TrendCharts /></el-icon>
              <span>本月新增 3 个</span>
            </div>
          </div>
        </div>

        <div class="stats-card info">
          <div class="stats-content">
            <div class="stats-main">
              <div class="stats-value">{{ activeKnowledgeBases }}</div>
              <div class="stats-label">活跃知识库</div>
            </div>
            <div class="stats-icon">
              <el-icon><DataAnalysis /></el-icon>
            </div>
          </div>
          <div class="stats-footer">
            <div class="stats-trend positive">
              <el-icon><TrendCharts /></el-icon>
              <span>活跃度提升 15%</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="main-content">
      <!-- 侧边栏 -->
      <div class="sidebar">
        <el-card class="sidebar-card">
          <template #header>
            <div class="card-header">
              <el-icon><Filter /></el-icon>
              <span>筛选</span>
            </div>
          </template>
          
          <!-- 搜索 -->
          <div class="filter-section">
            <el-input
              v-model="searchQuery"
              placeholder="搜索知识库..."
              clearable
              @input="handleSearch"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
          </div>

          <!-- 分类筛选 -->
          <div class="filter-section">
            <div class="filter-title">分类</div>
            <el-radio-group v-model="selectedCategory" @change="handleCategoryChange">
              <el-radio label="">全部分类</el-radio>
              <el-radio 
                v-for="category in statistics.categories" 
                :key="category.category"
                :label="category.category"
              >
                {{ category.category }} ({{ category.count }})
              </el-radio>
            </el-radio-group>
          </div>

          <!-- 状态筛选 -->
          <div class="filter-section">
            <div class="filter-title">状态</div>
            <el-radio-group v-model="selectedStatus" @change="handleStatusChange">
              <el-radio label="">全部状态</el-radio>
              <el-radio label="active">启用</el-radio>
              <el-radio label="inactive">禁用</el-radio>
              <el-radio label="archived">归档</el-radio>
            </el-radio-group>
          </div>

          <!-- 排序 -->
          <div class="filter-section">
            <div class="filter-title">排序</div>
            <el-select v-model="sortBy" @change="handleSort" placeholder="选择排序方式">
              <el-option label="创建时间（最新）" value="created_desc" />
              <el-option label="创建时间（最旧）" value="created_asc" />
              <el-option label="名称（A-Z）" value="name_asc" />
              <el-option label="名称（Z-A）" value="name_desc" />
              <el-option label="文档数量" value="document_count" />
            </el-select>
          </div>
        </el-card>

        <!-- 最近访问 -->
        <el-card class="sidebar-card">
          <template #header>
            <div class="card-header">
              <el-icon><Clock /></el-icon>
              <span>最近访问</span>
            </div>
          </template>
          <div class="recent-list">
            <div 
              v-for="item in recentKnowledgeBases" 
              :key="item.id"
              class="recent-item"
              @click="goToDocuments(item)"
            >
              <div class="recent-icon">
                <el-icon><Folder /></el-icon>
              </div>
              <div class="recent-info">
                <div class="recent-name">{{ item.name }}</div>
                <div class="recent-time">{{ formatTime(item.updated_at) }}</div>
              </div>
            </div>
          </div>
        </el-card>
      </div>

      <!-- 主要内容 -->
      <div class="content-area">
        <!-- 工具栏 -->
        <div class="toolbar">
          <div class="toolbar-left">
            <el-button-group>
              <el-button 
                :type="viewMode === 'card' ? 'primary' : ''" 
                @click="viewMode = 'card'"
              >
                <el-icon><Grid /></el-icon>
                卡片视图
              </el-button>
              <el-button 
                :type="viewMode === 'list' ? 'primary' : ''" 
                @click="viewMode = 'list'"
              >
                <el-icon><List /></el-icon>
                列表视图
              </el-button>
            </el-button-group>
          </div>
          <div class="toolbar-right">
            <span class="result-count">共 {{ filteredKnowledgeBases.length }} 个知识库</span>
          </div>
        </div>

        <!-- 知识库内容 -->
        <div class="knowledge-content" v-loading="loading">
          <!-- 卡片视图 -->
          <div v-if="viewMode === 'card'" class="knowledge-cards-grid">
            <div 
              class="knowledge-card" 
              v-for="item in filteredKnowledgeBases" 
              :key="item.id"
              @click="goToDocuments(item)"
            >
              <!-- 卡片头部 -->
              <div class="card-header">
                <div class="card-avatar">
                  <el-avatar 
                    :size="50"
                    class="engineer-avatar"
                    :style="{ backgroundColor: getRandomColor(item.id) }"
                  >
                    <span class="avatar-text">{{ item.name.charAt(0) }}</span>
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
                      <el-dropdown-item @click="duplicateItem(item)">
                        <el-icon><CopyDocument /></el-icon>
                        复制
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
                  <el-tag v-if="item.category" size="small" class="card-tag">
                    <el-icon><CollectionTag /></el-icon>
                    {{ item.category }}
                  </el-tag>
                  <el-tag 
                    :type="item.is_public ? 'success' : 'warning'" 
                    size="small" 
                    class="card-tag"
                  >
                    <el-icon>
                      <Unlock v-if="item.is_public" />
                      <Lock v-else />
                    </el-icon>
                    {{ item.is_public ? '公开' : '私有' }}
                  </el-tag>
                  <el-tag 
                    :type="item.status === 'active' ? 'success' : item.status === 'inactive' ? 'danger' : 'info'" 
                    size="small" 
                    class="card-tag"
                  >
                    <el-icon>
                      <CircleCheck v-if="item.status === 'active'" />
                      <CircleClose v-else-if="item.status === 'inactive'" />
                      <Folder v-else />
                    </el-icon>
                    {{ getStatusText(item.status) }}
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
                  <div class="info-item">
                    <el-icon><View /></el-icon>
                    <span>{{ getRandomViews(item.id) }} 次访问</span>
                  </div>
                </div>
                <div class="card-time">{{ formatTime(item.created_at) }}</div>
              </div>
            </div>
          </div>

          <!-- 列表视图 -->
          <div v-else class="knowledge-table">
            <el-table 
              :data="filteredKnowledgeBases" 
              stripe
              style="width: 100%"
              @row-click="goToDocuments"
            >
              <el-table-column prop="name" label="知识库名称" min-width="200">
                <template #default="scope">
                  <div class="table-name">
                    <el-avatar 
                      :size="32"
                      :style="{ backgroundColor: getRandomColor(scope.row.id) }"
                    >
                      <span class="avatar-text">{{ scope.row.name.charAt(0) }}</span>
                    </el-avatar>
                    <div class="name-info">
                      <div class="name-text">{{ scope.row.name }}</div>
                      <div class="name-desc" v-if="scope.row.description">{{ scope.row.description }}</div>
                    </div>
                  </div>
                </template>
              </el-table-column>
              
              <el-table-column prop="category" label="分类" width="120">
                <template #default="scope">
                  <el-tag v-if="scope.row.category" size="small">{{ scope.row.category }}</el-tag>
                  <span v-else class="text-gray">未分类</span>
                </template>
              </el-table-column>
              
              <el-table-column prop="document_count" label="文档数" width="100" align="center">
                <template #default="scope">
                  <span class="document-count">{{ scope.row.document_count || 0 }}</span>
                </template>
              </el-table-column>
              
              <el-table-column prop="status" label="状态" width="100" align="center">
                <template #default="scope">
                  <el-tag 
                    :type="scope.row.status === 'active' ? 'success' : scope.row.status === 'inactive' ? 'danger' : 'info'" 
                    size="small"
                  >
                    {{ getStatusText(scope.row.status) }}
                  </el-tag>
                </template>
              </el-table-column>
              
              <el-table-column prop="is_public" label="访问权限" width="100" align="center">
                <template #default="scope">
                  <el-tag 
                    :type="scope.row.is_public ? 'success' : 'warning'" 
                    size="small"
                  >
                    {{ scope.row.is_public ? '公开' : '私有' }}
                  </el-tag>
                </template>
              </el-table-column>
              
              <el-table-column prop="created_at" label="创建时间" width="180">
                <template #default="scope">
                  {{ formatTime(scope.row.created_at) }}
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
                        <el-dropdown-item @click="goToDocuments(scope.row)">
                          <el-icon><Document /></el-icon>
                          文档管理
                        </el-dropdown-item>
                        <el-dropdown-item @click="editItem(scope.row)">
                          <el-icon><Edit /></el-icon>
                          编辑
                        </el-dropdown-item>
                        <el-dropdown-item @click="duplicateItem(scope.row)">
                          <el-icon><CopyDocument /></el-icon>
                          复制
                        </el-dropdown-item>
                        <el-dropdown-item divided @click="deleteItem(scope.row)">
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
          
          <!-- 空状态 -->
          <div v-if="filteredKnowledgeBases.length === 0 && !loading" class="empty-state">
            <el-empty description="暂无知识库数据" :image-size="160">
              <template #image>
                <el-icon class="empty-icon"><Folder /></el-icon>
              </template>
              <template #description>
                <p>还没有创建知识库</p>
                <p>立即创建您的第一个知识库吧</p>
              </template>
              <el-button type="primary" @click="showCreateDialog" size="large">
                <el-icon><Plus /></el-icon>
                创建知识库
              </el-button>
            </el-empty>
          </div>
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
  Plus, Refresh, Folder, Document, Collection, MoreFilled, Edit, Delete, UserFilled,
  ArrowDown, CollectionTag, DataAnalysis, TrendCharts, Upload, Files, Setting, Unlock, Lock, 
  CircleCheck, CircleClose, Grid, List, Filter, Search, CopyDocument, View, Download
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

// 新增的响应式变量
const activeKnowledgeBases = ref(0)
const searchQuery = ref('')
const selectedCategory = ref('')
const selectedStatus = ref('')
const sortBy = ref('created_desc')
const viewMode = ref('card')
const recentKnowledgeBases = ref<KnowledgeBase[]>([])
const filteredKnowledgeBases = ref<KnowledgeBase[]>([])

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
    initializeData()
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

// 新增方法
const handleQuickAction = (command: string) => {
  switch (command) {
    case 'import':
      ElMessage.info('导入知识库功能开发中...')
      break
    case 'template':
      ElMessage.info('知识库模板功能开发中...')
      break
    case 'export':
      ElMessage.info('导出数据功能开发中...')
      break
    case 'settings':
      ElMessage.info('系统设置功能开发中...')
      break
    default:
      break
  }
}

const handleSearch = () => {
  filterKnowledgeBases()
}

const handleCategoryChange = () => {
  filterKnowledgeBases()
}

const handleStatusChange = () => {
  filterKnowledgeBases()
}

const handleSort = () => {
  filterKnowledgeBases()
}

const duplicateItem = async (item: KnowledgeBase) => {
  try {
    const newItem = {
      name: `${item.name} - 副本`,
      description: item.description,
      category: item.category,
      is_public: item.is_public,
      status: item.status
    }
    await createKnowledgeBase(newItem)
    ElMessage.success('知识库复制成功')
    loadKnowledgeBases()
    loadStatistics()
  } catch (error) {
    console.error('复制失败:', error)
    ElMessage.error('复制失败')
  }
}

const getRandomColor = (id: number) => {
  const colors = [
    '#667eea', '#764ba2', '#f093fb', '#f5576c',
    '#4facfe', '#00f2fe', '#a8edea', '#fed6e3',
    '#c471ed', '#12c2e9', '#c21500', '#ffc500'
  ]
  return colors[id % colors.length]
}

const getStatusText = (status: string) => {
  const statusMap: Record<string, string> = {
    active: '启用',
    inactive: '禁用',
    archived: '归档'
  }
  return statusMap[status] || status
}



const getRandomViews = (id: number) => {
  return 50 + (id * 13) % 500
}

const filterKnowledgeBases = () => {
  let filtered = [...knowledgeBases.value]

  // 搜索过滤
  if (searchQuery.value) {
    filtered = filtered.filter(item => 
      item.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      (item.description && item.description.toLowerCase().includes(searchQuery.value.toLowerCase()))
    )
  }

  // 分类过滤
  if (selectedCategory.value) {
    filtered = filtered.filter(item => item.category === selectedCategory.value)
  }

  // 状态过滤
  if (selectedStatus.value) {
    filtered = filtered.filter(item => item.status === selectedStatus.value)
  }

  // 排序
  switch (sortBy.value) {
    case 'created_desc':
      filtered.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
      break
    case 'created_asc':
      filtered.sort((a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime())
      break
    case 'name_asc':
      filtered.sort((a, b) => a.name.localeCompare(b.name))
      break
    case 'name_desc':
      filtered.sort((a, b) => b.name.localeCompare(a.name))
      break
    case 'document_count':
      filtered.sort((a, b) => (b.document_count || 0) - (a.document_count || 0))
      break
  }

  filteredKnowledgeBases.value = filtered
}

// 初始化数据
const initializeData = () => {
  activeKnowledgeBases.value = knowledgeBases.value.filter(item => item.status === 'active').length
  recentKnowledgeBases.value = knowledgeBases.value
    .slice()
    .sort((a, b) => new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime())
    .slice(0, 5)
  filteredKnowledgeBases.value = [...knowledgeBases.value]
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
    margin-bottom: 30px;
    
    .header-content {
      .page-title {
        font-size: 28px;
        font-weight: 700;
        color: #303133;
        margin: 0 0 8px 0;
        display: flex;
        align-items: center;
        gap: 12px;
        
        .title-icon {
          font-size: 32px;
          color: #667eea;
        }
      }
      
      .header-description {
        font-size: 16px;
        color: #909399;
      }
    }
    
    .header-actions {
      display: flex;
      gap: 12px;
    }
  }
  
  .stats-panel {
    margin-bottom: 40px;
    
    .stats-overview {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 32px;
      padding: 24px;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      border-radius: 20px;
      color: white;
      
      .overview-title {
        h2 {
          font-size: 28px;
          font-weight: 700;
          margin: 0 0 8px 0;
          color: white;
        }
        
        p {
          font-size: 16px;
          margin: 0;
          opacity: 0.9;
        }
      }
      
      .overview-actions {
        display: flex;
        gap: 12px;
        
        .el-button {
          border-color: rgba(255, 255, 255, 0.3);
          
          &.el-button--primary {
            background: rgba(255, 255, 255, 0.2);
            border-color: rgba(255, 255, 255, 0.3);
            
            &:hover {
              background: rgba(255, 255, 255, 0.3);
            }
          }
          
          &:not(.el-button--primary) {
            background: transparent;
            color: white;
            
            &:hover {
              background: rgba(255, 255, 255, 0.1);
            }
          }
        }
      }
    }
    
    .stats-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 24px;
      
      .stats-card {
        background: white;
        border-radius: 20px;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
        overflow: hidden;
        position: relative;
        
        &::before {
          content: '';
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          height: 4px;
          background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        }
        
        &:hover {
          transform: translateY(-6px);
          box-shadow: 0 12px 32px rgba(0, 0, 0, 0.15);
        }
        
        &.primary::before {
          background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        }
        
        &.success::before {
          background: linear-gradient(90deg, #52c41a 0%, #389e0d 100%);
        }
        
        &.warning::before {
          background: linear-gradient(90deg, #faad14 0%, #d48806 100%);
        }
        
        &.info::before {
          background: linear-gradient(90deg, #1890ff 0%, #096dd9 100%);
        }
        
        .stats-content {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 28px 24px 20px;
          
          .stats-main {
            flex: 1;
            
            .stats-value {
              font-size: 36px;
              font-weight: 800;
              color: #303133;
              line-height: 1;
              margin-bottom: 8px;
            }
            
            .stats-label {
              font-size: 16px;
              color: #606266;
              font-weight: 500;
            }
          }
          
          .stats-icon {
            width: 64px;
            height: 64px;
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 32px;
            opacity: 0.1;
            color: #303133;
          }
        }
        
        .stats-footer {
          padding: 16px 24px 24px;
          border-top: 1px solid #f0f2f5;
          
          .stats-trend {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 14px;
            font-weight: 500;
            
            &.positive {
              color: #52c41a;
              
              .el-icon {
                font-size: 16px;
              }
            }
          }
        }
      }
    }
  }
  
  .text-gray {
    color: #909399;
  }
  

  
  .main-content {
    display: flex;
    gap: 24px;
    
    .sidebar {
      flex: 0 0 280px;
      
      .sidebar-card {
        margin-bottom: 20px;
        
        .card-header {
          display: flex;
          align-items: center;
          gap: 8px;
          font-size: 16px;
          font-weight: 600;
          color: #303133;
        }
        
        .filter-section {
          margin-bottom: 20px;
          
          .filter-title {
            font-size: 14px;
            font-weight: 600;
            color: #606266;
            margin-bottom: 8px;
          }
          
          .el-radio-group {
            display: flex;
            flex-direction: column;
            gap: 8px;
            
            .el-radio {
              margin-right: 0;
            }
          }
        }
        
        .recent-list {
          .recent-item {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 8px;
            border-radius: 6px;
            cursor: pointer;
            transition: background-color 0.3s;
            
            &:hover {
              background-color: #f5f7fa;
            }
            
            .recent-icon {
              width: 32px;
              height: 32px;
              border-radius: 6px;
              background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
              display: flex;
              align-items: center;
              justify-content: center;
              color: white;
              font-size: 16px;
            }
            
            .recent-info {
              flex: 1;
              
              .recent-name {
                font-size: 14px;
                font-weight: 600;
                color: #303133;
                margin-bottom: 2px;
              }
              
              .recent-time {
                font-size: 12px;
                color: #909399;
              }
            }
          }
        }
      }
    }
    
    .content-area {
      flex: 1;
      
      .toolbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
        padding: 16px;
        background: white;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        
        .toolbar-left {
          display: flex;
          gap: 12px;
        }
        
        .toolbar-right {
          .result-count {
            font-size: 14px;
            color: #909399;
            font-weight: 500;
          }
        }
      }
      
              .knowledge-content {
          .knowledge-cards-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
            gap: 28px;
            
            .knowledge-card {
              background: white;
              border-radius: 20px;
              padding: 28px;
              box-shadow: 0 6px 24px rgba(0, 0, 0, 0.08);
              transition: all 0.3s ease;
              cursor: pointer;
              border: 2px solid transparent;
              position: relative;
              overflow: hidden;
              
              &::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 5px;
                background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
              }
              
              &:hover {
                transform: translateY(-8px);
                box-shadow: 0 16px 40px rgba(0, 0, 0, 0.15);
                border-color: #667eea;
                
                .card-avatar .engineer-avatar {
                  transform: scale(1.1);
                  border-color: #667eea;
                }
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
                  margin-bottom: 20px;
                  
                  .card-title {
                    font-size: 18px;
                    font-weight: 700;
                    color: #303133;
                    margin: 0 0 12px 0;
                    line-height: 1.4;
                  }
                  
                  .card-description {
                    font-size: 14px;
                    color: #606266;
                    line-height: 1.6;
                    margin: 0 0 16px 0;
                    display: -webkit-box;
                    -webkit-line-clamp: 2;
                    -webkit-box-orient: vertical;
                    overflow: hidden;
                    min-height: 40px;
                  }
                  
                  .card-tags {
                    display: flex;
                    flex-wrap: wrap;
                    gap: 8px;
                    margin-bottom: 16px;
                    
                    .card-tag {
                      font-size: 12px;
                      border-radius: 12px;
                      padding: 4px 8px;
                      display: flex;
                      align-items: center;
                      gap: 4px;
                      
                      .el-icon {
                        font-size: 14px;
                      }
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
        
        .knowledge-table {
          background: white;
          border-radius: 12px;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
          overflow: hidden;
          
          .table-name {
            display: flex;
            align-items: center;
            gap: 12px;
            
            .name-info {
              .name-text {
                font-weight: 600;
                color: #303133;
                margin-bottom: 4px;
              }
              
              .name-desc {
                font-size: 12px;
                color: #909399;
                line-height: 1.4;
              }
            }
          }
          
          .document-count {
            font-weight: 600;
            color: #667eea;
          }
        }

        .empty-state {
          text-align: center;
          padding: 80px 40px;
          background: white;
          border-radius: 20px;
          box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
          
          .empty-icon {
            font-size: 140px;
            color: #e1e8ff;
            margin-bottom: 32px;
            opacity: 0.8;
          }
          
          p {
            font-size: 16px;
            color: #606266;
            margin: 10px 0;
            line-height: 1.6;
            
            &:first-child {
              font-size: 20px;
              font-weight: 600;
              color: #303133;
              margin-bottom: 8px;
            }
          }
          
          .el-button {
            margin-top: 24px;
            padding: 12px 32px;
            font-size: 16px;
            border-radius: 12px;
          }
        }
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
  
  // 响应式设计
  @media (max-width: 1200px) {
    .main-content {
      flex-direction: column;
      
      .sidebar {
        flex: none;
        width: 100%;
        
        .sidebar-card {
          .filter-section {
            .el-radio-group {
              flex-direction: row;
              flex-wrap: wrap;
            }
          }
        }
      }
    }
    
    .stats-panel {
      .stats-overview {
        flex-direction: column;
        gap: 20px;
        text-align: center;
        
        .overview-actions {
          width: 100%;
          justify-content: center;
        }
      }
      
      .stats-grid {
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      }
    }
  }
  
  @media (max-width: 768px) {
    padding: 16px;
    
    .page-header {
      flex-direction: column;
      align-items: flex-start;
      gap: 16px;
      
      .header-content .page-title {
        font-size: 24px;
        
        .title-icon {
          font-size: 28px;
        }
      }
    }
    
    .stats-panel {
      .stats-overview {
        padding: 20px;
        
        .overview-title h2 {
          font-size: 24px;
        }
        
        .overview-actions {
          flex-direction: column;
          
          .el-button {
            width: 100%;
          }
        }
      }
      
      .stats-grid {
        grid-template-columns: 1fr;
      }
    }
    
    .main-content {
      .content-area {
        .knowledge-content .knowledge-cards-grid {
          grid-template-columns: 1fr;
          gap: 20px;
          
          .knowledge-card {
            padding: 20px;
            
                         .card-body {
               .card-title {
                 font-size: 16px;
               }
             }
          }
        }
        
        .empty-state {
          padding: 60px 20px;
          
          .empty-icon {
            font-size: 100px;
          }
          
          p:first-child {
            font-size: 18px;
          }
          
          .el-button {
            padding: 10px 24px;
            font-size: 14px;
          }
        }
      }
    }
  }
}
</style> 