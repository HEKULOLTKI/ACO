<template>
  <div class="project-selection-container">
    <!-- 顶部操作栏 -->
    <div class="top-header">
      <div class="header-content">
        <!-- 左侧00005图片 -->
        <div class="header-logo">
          <img src="@/assets/icon/00005.png" alt="系统标识" class="logo-image">
          <div class="logo-pulse"></div>
        </div>
        
        <!-- 右侧用户信息和操作 -->
        <div class="user-actions">
          <div class="user-info">
            <div class="user-avatar">
              <img src="@/assets/role/头像.svg" alt="用户头像" class="avatar-icon">
              <div class="avatar-ring"></div>
              <div class="status-indicator"></div>
            </div>
            <div class="user-details">
              <div class="username">{{ authStore.user?.username || '管理员' }}</div>
              <div class="user-role">系统管理员</div>
            </div>
          </div>
          
          <div class="action-buttons">
            <div class="action-btn" @click="openSettings">
              <img src="@/assets/role/设置.svg" alt="设置" class="action-icon">
              <div class="btn-glow"></div>
              <div class="btn-ripple"></div>
              <span class="btn-tooltip">系统设置</span>
            </div>
            <div class="action-btn" @click="logout">
              <img src="@/assets/role/退出.svg" alt="退出" class="action-icon">
              <div class="btn-glow"></div>
              <div class="btn-ripple"></div>
              <span class="btn-tooltip">退出登录</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 增强的科技背景 -->
    <div class="tech-background">
      <div class="main-background"></div>
      <div class="overlay-effects">
        <div class="light-beams"></div>
        <div class="particles"></div>
        <div class="grid-overlay"></div>
        <div class="floating-shapes">
          <div class="shape shape-1"></div>
          <div class="shape shape-2"></div>
          <div class="shape shape-3"></div>
        </div>
      </div>
    </div>
    
    <!-- 底部平台 -->
    <div class="platform-base">
      <div class="platform-surface">
        <img src="@/assets/image/组 682.png" alt="底部平台" class="platform-background">
      </div>
      <div class="platform-glow"></div>
      <div class="platform-reflections"></div>
    </div>

    <!-- 主要内容区域 - 项目选择 -->
    <div class="content-area">
      <div class="selection-title">
        <h1 class="title-main">选择项目</h1>
        <p class="title-subtitle">请选择要进入的项目空间</p>
        <div class="title-decoration"></div>
      </div>
      
      <!-- 项目统计信息 -->
      <div class="project-stats">
        <div class="stat-item">
          <div class="stat-number">{{ projectList.length }}</div>
          <div class="stat-label">可用项目</div>
        </div>
        <div class="stat-item">
          <div class="stat-number">{{ onlineProjects }}</div>
          <div class="stat-label">在线项目</div>
        </div>
      </div>
      
      <!-- 项目卡片网格 -->
      <div class="projects-grid" v-if="projectList.length > 0">
        <div 
          v-for="(project, index) in projectList" 
          :key="project.id"
          class="project-card"
          :class="{ 
            'selected': selectedProject === project.id,
            'online': project.status === '在线'
          }"
          :style="{ '--delay': index * 0.1 + 's' }"
          @click="selectProject(project)"
        >
          <div class="card-glow" :class="{ 'active': selectedProject === project.id }"></div>
          <div class="card-border"></div>
          <div class="card-inner">
            <div class="project-icon">
              <el-icon :size="42"><component :is="project.icon" /></el-icon>
              <div class="icon-glow"></div>
              <div class="icon-pulse" v-if="project.status === '在线'"></div>
            </div>
            <div class="project-info">
              <h3>{{ project.name }}</h3>
              <p>{{ project.description }}</p>
              <div class="project-meta">
                <div class="manager-info" v-if="project.manager">
                  <span class="manager-label">负责人:</span>
                  <span class="manager-name">{{ project.manager.username }}</span>
                </div>
                <span class="created-date">创建于 {{ project.created_at ? new Date(project.created_at).toLocaleDateString() : '未知' }}</span>
              </div>
            </div>
            <div class="project-status">
              <el-tag 
                :type="getStatusType(project.status)"
                :class="`status-${project.status}`"
                size="small"
              >
                <span class="status-dot"></span>
                {{ project.status }}
              </el-tag>
            </div>
            <div class="card-actions">
              <div class="card-action planning-action" @click.stop="viewProjectPlanning(project)" title="查看项目策划">
                <el-icon><Document /></el-icon>
              </div>
              <div class="card-action delete-action" @click.stop="removeProject(project)" title="删除项目">
                <el-icon><Delete /></el-icon>
              </div>
            </div>
            <div class="card-arrow">
              <el-icon><ArrowRight /></el-icon>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 空状态 -->
      <div v-else class="empty-state">
        <div class="empty-icon">
          <el-icon :size="64"><Briefcase /></el-icon>
        </div>
        <h3>暂无项目</h3>
        <p>创建您的第一个项目开始工作</p>
      </div>
      
      <!-- 操作按钮 -->
      <div class="action-area">
        <el-button 
          type="primary" 
          size="large" 
          :disabled="!selectedProject"
          @click="enterProject"
          class="enter-button"
          :loading="isEntering"
        >
          <span v-if="!isEntering">进入项目</span>
          <span v-else>正在进入...</span>
          <el-icon class="el-icon--right" v-if="!isEntering"><ArrowRight /></el-icon>
        </el-button>
        
        <el-button 
          type="default"
          size="large" 
          @click="createNewProject"
          class="create-button"
        >
          <el-icon><Plus /></el-icon>
          创建新项目
        </el-button>
        
        <el-button 
          type="default"
          size="large" 
          @click="openImportDialog"
          class="import-button"
        >
          <el-icon><Upload /></el-icon>
          导入项目
        </el-button>
        
        <el-button 
          text
          size="large" 
          @click="refreshProjects"
          class="refresh-button"
          :loading="isRefreshing"
        >
          <el-icon><Refresh /></el-icon>
          {{ isRefreshing ? '刷新中...' : '刷新' }}
        </el-button>
      </div>
    </div>
  </div>
  
  <!-- 导入项目对话框 -->
  <el-dialog
    v-model="importDialogVisible"
    title="导入项目"
    width="500px"
    destroy-on-close
    center
  >
    <div class="import-dialog-content">
      <div class="upload-area">
        <el-upload
          class="upload-dragger"
          drag
          action="#"
          :auto-upload="false"
          :show-file-list="false"
          :on-change="(file: any) => handleFileChange(file.raw as File)"
        >
          <el-icon class="upload-icon"><Upload /></el-icon>
          <div class="upload-text">{{ uploadDragText }}</div>
          <div class="upload-tip">支持 .xlsx, .xls 格式的Excel文件</div>
        </el-upload>
      </div>
      
      <div class="import-instructions">
        <h4>Excel文件格式说明：</h4>
        <p>1. 文件必须包含以下列：name (项目名称), description (项目描述)</p>
        <p>2. 可选列：status (状态), icon (图标), manager_id (负责人ID), planning (项目策划)</p>
        <p>3. 项目名称不能重复</p>
        <p>4. manager_id 需要是系统中已存在的用户ID</p>
      </div>
    </div>
    
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="importDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleImportProjects" :disabled="!importFile">
          开始导入
        </el-button>
      </span>
    </template>
  </el-dialog>

  <!-- 创建新项目对话框 -->
  <el-dialog
    v-model="createDialogVisible"
    title="创建新项目"
    width="600px"
    :close-on-click-modal="false"
    destroy-on-close
    center
    custom-class="create-project-dialog"
  >
    <el-form
      ref="createProjectFormRef"
      :model="createProjectForm"
      :rules="createProjectRules"
      label-width="100px"
      class="create-project-form"
      @submit.prevent
    >
      <el-form-item label="项目名称" prop="name">
        <el-input 
          v-model="createProjectForm.name" 
          placeholder="请输入项目名称 (2-20字符)" 
          class="custom-input"
          clearable
        />
      </el-form-item>
      
      <el-form-item label="项目负责人" prop="manager_name">
        <el-autocomplete
          v-model="createProjectForm.manager_name"
          :fetch-suggestions="querySearch"
          placeholder="输入负责人名称搜索"
          class="full-width custom-input"
          popper-class="manager-autocomplete-dropdown"
          @select="handleManagerSelect"
          :trigger-on-focus="true"
        >
          <template #prefix>
            <el-icon class="input-icon"><User /></el-icon>
          </template>
          <template #suffix>
            <el-icon v-if="createProjectForm.manager_name"><Check /></el-icon>
          </template>
        </el-autocomplete>
      </el-form-item>
      
      <el-form-item label="项目策划" prop="planning_file">
        <el-upload
          ref="uploadRef"
          :auto-upload="false"
          :on-change="handlePlanningFileChange"
          :on-remove="handlePlanningFileRemove"
          :limit="1"
          class="planning-upload"
          accept=".txt,.md,.docx,.pdf"
        >
          <div class="upload-area">
            <el-icon class="upload-icon"><Document /></el-icon>
            <div class="upload-info">
              <span class="upload-text">{{ createProjectForm.planning_file ? '已选择文件' : '选择项目策划文件' }}</span>
              <span class="upload-filename" v-if="createProjectForm.planning_file">
                {{ createProjectForm.planning_file.name }}
              </span>
            </div>
          </div>
          <template #tip>
            <div class="el-upload__tip">
              支持 .txt, .md, .docx, .pdf 格式文件
            </div>
          </template>
        </el-upload>
      </el-form-item>

      <el-form-item label="项目图标" class="icon-selector-item">
        <div class="icon-selector">
          <div 
            v-for="(iconComponent, iconName) in availableIcons" 
            :key="iconName"
            class="icon-option"
            :class="{ active: createProjectForm.icon === iconName }"
            @click="selectIcon(iconName)"
          >
            <div class="icon-wrapper">
              <el-icon><component :is="iconComponent" /></el-icon>
              <div class="icon-glow"></div>
            </div>
          </div>
        </div>
      </el-form-item>

      <el-form-item label="项目描述" prop="description">
        <el-input 
          v-model="createProjectForm.description" 
          type="textarea" 
          placeholder="请输入项目描述 (选填)" 
          :rows="3"
          resize="none"
          class="custom-textarea"
        />
      </el-form-item>
    </el-form>
    
    <template #footer>
      <span class="dialog-footer">
        <el-button 
          @click="createDialogVisible = false"
          class="cancel-button"
        >
          取消
        </el-button>
        <el-button 
          type="primary" 
          @click="handleCreateProject" 
          :loading="isCreating"
          class="submit-button"
        >
          <span class="button-content">
            <el-icon v-if="!isCreating"><Plus /></el-icon>
            {{ isCreating ? '创建中...' : '创建项目' }}
          </span>
        </el-button>
      </span>
    </template>
  </el-dialog>

  <!-- 项目策划详情对话框 -->
  <el-dialog
    v-model="planningDialogVisible"
    title="项目策划详情"
    width="60%"
    destroy-on-close
    center
  >
    <div class="planning-content" v-if="selectedProjectDetails">
      <h3>{{ selectedProjectDetails.name }} - 项目策划</h3>
      
      <div class="planning-info">
        <div class="info-item">
          <span class="label">项目负责人：</span>
          <span class="value">{{ selectedProjectDetails.manager ? selectedProjectDetails.manager.username : '未指定' }}</span>
        </div>
        <div class="info-item">
          <span class="label">项目状态：</span>
          <span class="value">{{ selectedProjectDetails.status }}</span>
        </div>
        <div class="info-item">
          <span class="label">创建时间：</span>
          <span class="value">{{ selectedProjectDetails.created_at ? new Date(selectedProjectDetails.created_at).toLocaleString() : '未知' }}</span>
        </div>
      </div>
      
      <div class="planning-document">
        <div v-if="selectedProjectDetails.planning" class="planning-text">
          <pre>{{ selectedProjectDetails.planning }}</pre>
        </div>
        <div v-else class="no-planning">
          <el-empty description="暂无项目策划内容" />
        </div>
      </div>
    </div>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElMessageBox, ElLoading, type FormInstance, type FormRules, type UploadInstance, type UploadFile, type UploadRawFile } from 'element-plus'
import { 
  Briefcase, 
  Monitor, 
  Setting, 
  DataAnalysis, 
  Cpu,
  ArrowRight,
  Plus,
  Refresh,
  Delete,
  Upload,
  Document,
  User,
  Check
} from '@element-plus/icons-vue'
import { useAuthStore } from '@/store/modules/auth'
import type { Project } from '@/types/user'
import { getProjects, createProject, deleteProject, importProjects, getProject } from '@/api/project'
import { searchUsers } from '@/api/user'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

// 加载状态
const isEntering = ref(false)
const isRefreshing = ref(false)
const isCreating = ref(false)

// 项目列表
const projectList = ref<Project[]>([])
// 加载标志
const isLoading = ref(false)
// 导入弹窗可见性
const importDialogVisible = ref(false)
// 导入文件
const importFile = ref<File | null>(null)
// 拖拽提示文字
const uploadDragText = ref('点击上传或拖拽Excel文件到此处')

// 项目详情相关
const planningDialogVisible = ref(false)
const selectedProjectDetails = ref<Project | null>(null)

// 创建项目对话框
const createDialogVisible = ref(false)
const createProjectFormRef = ref<FormInstance>()
const uploadRef = ref<UploadInstance>()

const createProjectForm = reactive({
  name: '',
  manager_id: null as number | null,
  manager_name: '',
  planning_file: null as File | null,
  planning_content: '',
  icon: 'Briefcase', // 新增图标属性
  description: '' // 新增描述属性
})

const createProjectRules: FormRules = {
  name: [
    { required: true, message: '请输入项目名称', trigger: 'blur' },
    { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' },
  ],
  manager_name: [
    { required: true, message: '请选择一个项目负责人', trigger: 'change' },
  ],
}

// 图标映射
const iconMap: Record<string, any> = {
  'Briefcase': Briefcase,
  'Monitor': Monitor,
  'Setting': Setting,
  'DataAnalysis': DataAnalysis,
  'Cpu': Cpu
}

const availableIcons = computed(() => {
  return {
    Briefcase,
    Monitor,
    Setting,
    DataAnalysis,
    Cpu,
    // 可以添加更多图标
  }
})

const selectedProject = ref<number | null>(null)

// 计算在线项目数量
const onlineProjects = computed(() => {
  return projectList.value.filter(p => p.status === '在线').length
})

// 获取状态标签类型
const getStatusType = (status: string) => {
  switch (status) {
    case '在线':
      return 'success'
    case '开发中':
      return 'warning'
    case '维护中':
      return 'info'
    default:
      return ''
  }
}

// 选择项目
const selectProject = (project: Project) => {
  selectedProject.value = project.id
}

// 进入项目
const enterProject = async () => {
  if (!selectedProject.value) {
    ElMessage.warning('请先选择一个项目')
    return
  }
  
  isEntering.value = true
  
  try {
    // 模拟加载时间
    await new Promise(resolve => setTimeout(resolve, 800))
    
    // 保存选择的项目
    const project = projectList.value.find(p => p.id === selectedProject.value)
    if (project) {
      localStorage.setItem('selectedProject', JSON.stringify(project))
      
      ElMessage.success(`正在进入"${project.name}"...`)
      
      // 检查是否有重定向URL
      const redirect = route.query.redirect as string
      router.push(redirect || '/dashboard')
    }
  } catch (error) {
    ElMessage.error('进入项目失败，请重试')
  } finally {
    isEntering.value = false
  }
}

// 创建新项目
const createNewProject = () => {
  // 重置表单
  if (createProjectFormRef.value) {
    createProjectFormRef.value.resetFields()
  }
  uploadRef.value?.clearFiles()
  
  createProjectForm.name = ''
  createProjectForm.manager_id = null
  createProjectForm.manager_name = ''
  createProjectForm.planning_file = null
  createProjectForm.planning_content = ''
  createProjectForm.icon = 'Briefcase' // 重置图标
  createProjectForm.description = '' // 重置描述
  
  createDialogVisible.value = true
}

// 负责人搜索
const querySearch = async (queryString: string, cb: (arg: any) => void) => {
  if (queryString) {
    try {
      const { data: users } = await searchUsers(queryString)
      const results = users.map(user => ({
        value: user.username,
        id: user.id
      }))
      cb(results)
    } catch (error) {
      console.error('搜索用户失败:', error)
      cb([])
    }
  } else {
    cb([])
  }
}

const handleManagerSelect = (item: { value: string, id: number }) => {
  createProjectForm.manager_id = item.id
  createProjectForm.manager_name = item.value
}

// 策划文件处理
const handlePlanningFileChange = (file: UploadFile) => {
  createProjectForm.planning_file = file.raw as UploadRawFile
}

const handlePlanningFileRemove = () => {
  createProjectForm.planning_file = null
}

// 读取文件内容
const readPlanningFile = async (): Promise<string> => {
  return new Promise((resolve, reject) => {
    if (!createProjectForm.planning_file) {
      return resolve('')
    }
    
    const reader = new FileReader()
    reader.onload = (e) => {
      resolve(e.target?.result as string)
    }
    reader.onerror = (e) => {
      console.error('文件读取失败:', e)
      reject(new Error('文件读取失败'))
    }

    // 如果是PDF，使用readAsDataURL，否则使用readAsText
    if (createProjectForm.planning_file.type === 'application/pdf') {
      reader.readAsDataURL(createProjectForm.planning_file)
    } else {
      reader.readAsText(createProjectForm.planning_file)
    }
  })
}

// 提交创建项目
const handleCreateProject = async () => {
  if (!createProjectFormRef.value) return
  
  await createProjectFormRef.value.validate(async (valid) => {
    if (valid) {
      isCreating.value = true
      try {
        const planningContent = await readPlanningFile()
        
        const projectData = {
          name: createProjectForm.name,
          manager_id: createProjectForm.manager_id === null ? undefined : createProjectForm.manager_id,
          planning: planningContent,
          description: createProjectForm.description || '新建项目，等待配置', // 使用表单中的描述
          status: '开发中',
          icon: createProjectForm.icon,
        }
        
        await createProject(projectData)
        ElMessage.success(`项目 "${projectData.name}" 创建成功`)
        
        createDialogVisible.value = false
        await fetchProjects()
        
      } catch (error: any) {
        ElMessage.error(`创建失败: ${error.response?.data?.detail || '未知错误'}`)
      } finally {
        isCreating.value = false
      }
    }
  })
}

// 选择图标
const selectIcon = (iconName: string) => {
  createProjectForm.icon = iconName
}


// 删除项目
const removeProject = async (project: Project) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除项目"${project.name}"吗？此操作不可恢复！`, 
      '删除确认', 
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    // 显示加载中
    const loading = ElLoading.service({
      lock: true,
      text: '删除项目中...',
      background: 'rgba(0, 0, 0, 0.7)'
    })
    
    try {
      await deleteProject(project.id)
      
      // 重新获取项目列表
      await fetchProjects()
      
      // 如果删除的是当前选中的项目，清除选择
      if (selectedProject.value === project.id) {
        selectedProject.value = null
      }
      
      ElMessage.success(`项目"${project.name}"已成功删除`)
    } catch (error: any) {
      ElMessage.error(`删除项目失败: ${error.response?.data?.detail || '未知错误'}`)
    } finally {
      // 关闭加载
      loading.close()
    }
  } catch {
    // 用户取消删除
  }
}

// 打开导入项目对话框
const openImportDialog = () => {
  importDialogVisible.value = true
  importFile.value = null
  uploadDragText.value = '点击上传或拖拽Excel文件到此处'
}

// 处理文件变更
const handleFileChange = (file: File) => {
  importFile.value = file
  uploadDragText.value = file.name
  return false // 阻止自动上传
}

// 导入项目
const handleImportProjects = async () => {
  if (!importFile.value) {
    ElMessage.warning('请先选择要导入的Excel文件')
    return
  }
  
  // 检查文件类型
  const allowedTypes = ['.xlsx', '.xls']
  const fileName = importFile.value.name
  const isValidType = allowedTypes.some(type => fileName.toLowerCase().endsWith(type))
  
  if (!isValidType) {
    ElMessage.error('只支持Excel格式的文件(.xlsx, .xls)')
    return
  }
  
  // 显示加载中
  const loading = ElLoading.service({
    lock: true,
    text: '导入项目中...',
    background: 'rgba(0, 0, 0, 0.7)'
  })
  
  try {
    const formData = new FormData()
    formData.append('file', importFile.value)
    
    const { data: result } = await importProjects(formData)
    
    // 重新获取项目列表
    await fetchProjects()
    
    // 关闭对话框
    importDialogVisible.value = false
    
    // 显示导入结果
    if (result.success_count > 0) {
      ElMessage.success(result.message)
      
      // 如果有失败的项目，显示详情
      if (result.fail_count > 0) {
        showImportFailures(result.failed_projects)
      }
    } else {
      ElMessage.warning(result.message)
      if (result.fail_count > 0) {
        showImportFailures(result.failed_projects)
      }
    }
  } catch (error: any) {
    ElMessage.error(`导入失败: ${error.response?.data?.detail || '未知错误'}`)
  } finally {
    loading.close()
  }
}

// 显示导入失败详情
const showImportFailures = (failedProjects: any[]) => {
  if (!failedProjects || failedProjects.length === 0) return
  
  let message = '<div>以下项目导入失败:</div>'
  message += '<ul style="text-align:left;padding-left:20px;">'
  
  failedProjects.forEach(project => {
    message += `<li>${project.name}: ${project.error}</li>`
  })
  
  message += '</ul>'
  
  ElMessageBox.alert(message, '导入失败详情', {
    dangerouslyUseHTMLString: true,
    confirmButtonText: '确定'
  })
}

// 查看项目策划
const viewProjectPlanning = async (project: Project) => {
  try {
    // 如果已经有详细信息，直接显示
    if (project.planning) {
      selectedProjectDetails.value = project
      planningDialogVisible.value = true
      return
    }
    
    // 否则获取项目详细信息
    const { data } = await getProject(project.id)
    selectedProjectDetails.value = {
      ...data,
      icon: iconMap[data.icon] || Briefcase
    }
    planningDialogVisible.value = true
  } catch (error) {
    ElMessage.error('获取项目详情失败')
  }
}

// 获取项目列表
const fetchProjects = async () => {
  isLoading.value = true
  isRefreshing.value = true
  
  try {
    const { data: response } = await getProjects()
    
    // 处理返回的项目数据，添加图标组件
    projectList.value = response.map((project: any) => ({
      ...project,
      icon: iconMap[project.icon] || Briefcase
    }))
    
    ElMessage.success('项目列表已刷新')
  } catch (error) {
    ElMessage.error('获取项目列表失败，请重试')
    console.error('获取项目列表错误:', error)
  } finally {
    isLoading.value = false
    isRefreshing.value = false
  }
}

// 刷新项目列表
const refreshProjects = async () => {
  await fetchProjects()
}

// 顶部操作方法
const openSettings = () => {
  ElMessage.info('系统设置功能开发中...')
}

const logout = async () => {
  try {
    await ElMessageBox.confirm('确定要退出登录吗？', '退出确认', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await authStore.logoutAction()
    ElMessage.success('已退出登录')
    router.push('/login')
  } catch {
    // 用户取消退出
  }
}

// 页面加载时检查是否有已选择的项目
onMounted(async () => {
  // 加载项目列表
  await fetchProjects()
  
  const savedProject = localStorage.getItem('selectedProject')
  if (savedProject) {
    try {
      const project = JSON.parse(savedProject)
      selectedProject.value = project.id
    } catch (error) {
      console.error('解析已保存的项目失败:', error)
    }
  }
})
</script>

<style scoped lang="scss">
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.8;
    transform: scale(1.05);
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
}

@keyframes ripple {
  0% {
    transform: scale(0);
    opacity: 1;
  }
  100% {
    transform: scale(4);
    opacity: 0;
  }
}

@keyframes shine {
  0% {
    left: -100%;
  }
  100% {
    left: 100%;
  }
}

@keyframes statusPulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.6;
    transform: scale(1.3);
  }
}

@keyframes titlePulse {
  0% {
    text-shadow: 0 0 15px rgba(79, 172, 254, 0.5);
  }
  100% {
    text-shadow: 0 0 25px rgba(79, 172, 254, 0.8);
  }
}

@keyframes numberPulse {
  0% {
    text-shadow: 0 0 10px rgba(79, 172, 254, 0.5);
    transform: scale(1);
  }
  100% {
    text-shadow: 0 0 20px rgba(79, 172, 254, 0.8);
    transform: scale(1.05);
  }
}

.project-selection-container {
  position: relative;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  background: #0a0e1a;
}

// 顶部操作栏优化
.top-header {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 80px;
  z-index: 100;
  backdrop-filter: blur(20px);
  background: rgba(10, 14, 26, 0.8);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  
  .header-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 100%;
    padding: 0 40px;
  }
  
  .header-logo {
    position: relative;
    height: 48px;
    
    .logo-image {
      height: 100%;
      object-fit: contain;
      filter: drop-shadow(0 0 10px rgba(79, 172, 254, 0.5));
    }
    
    .logo-pulse {
      position: absolute;
      top: 50%;
      left: 50%;
      width: 60px;
      height: 60px;
      border: 2px solid rgba(79, 172, 254, 0.3);
      border-radius: 50%;
      transform: translate(-50%, -50%);
      animation: pulse 2s infinite;
    }
  }
}

// 用户操作区优化
.user-actions {
  display: flex;
  align-items: center;
  gap: 24px;
  
  .user-info {
    display: flex;
    align-items: center;
    gap: 16px;
    
    .user-avatar {
      position: relative;
      width: 44px;
      height: 44px;
      
      .avatar-icon {
        width: 100%;
        height: 100%;
        object-fit: cover;
        border-radius: 50%;
        border: 2px solid rgba(79, 172, 254, 0.5);
      }
      
      .avatar-ring {
        position: absolute;
        top: -4px;
        left: -4px;
        right: -4px;
        bottom: -4px;
        border-radius: 50%;
        border: 2px solid rgba(255, 255, 255, 0.3);
        animation: pulse 3s infinite;
      }
      
      .status-indicator {
        position: absolute;
        bottom: 2px;
        right: 2px;
        width: 12px;
        height: 12px;
        background: #00ff88;
        border: 2px solid #0a0e1a;
        border-radius: 50%;
        box-shadow: 0 0 8px rgba(0, 255, 136, 0.6);
      }
    }
    
    .user-details {
      color: white;
      
      .username {
        font-weight: 600;
        font-size: 16px;
        margin-bottom: 2px;
      }
      
      .user-role {
        font-size: 12px;
        color: rgba(255, 255, 255, 0.6);
      }
    }
  }
  
  .action-buttons {
    display: flex;
    gap: 12px;
    
    .action-btn {
      position: relative;
      width: 44px;
      height: 44px;
      background: rgba(255, 255, 255, 0.1);
      border: 1px solid rgba(255, 255, 255, 0.2);
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      overflow: hidden;
      
      &:hover {
        background: rgba(79, 172, 254, 0.2);
        border-color: rgba(79, 172, 254, 0.5);
        transform: translateY(-2px);
        
        .btn-glow {
          opacity: 1;
        }
        
        .btn-tooltip {
          opacity: 1;
          transform: translateY(0);
        }
      }
      
      &:active {
        .btn-ripple {
          animation: ripple 0.6s ease-out;
        }
      }
      
      .action-icon {
        width: 22px;
        height: 22px;
        filter: brightness(1.2);
      }
      
      .btn-glow {
        position: absolute;
        top: -10px;
        left: -10px;
        right: -10px;
        bottom: -10px;
        border-radius: 16px;
        background: radial-gradient(circle, rgba(79, 172, 254, 0.4) 0%, rgba(79, 172, 254, 0) 70%);
        opacity: 0;
        transition: opacity 0.3s;
      }
      
      .btn-ripple {
        position: absolute;
        width: 20px;
        height: 20px;
        background: rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        transform: scale(0);
      }
      
      .btn-tooltip {
        position: absolute;
        bottom: -35px;
        left: 50%;
        transform: translateX(-50%) translateY(10px);
        background: rgba(0, 0, 0, 0.9);
        color: white;
        padding: 6px 12px;
        border-radius: 6px;
        font-size: 12px;
        white-space: nowrap;
        opacity: 0;
        transition: all 0.3s;
        pointer-events: none;
        
        &::before {
          content: '';
          position: absolute;
          top: -4px;
          left: 50%;
          transform: translateX(-50%);
          border-left: 4px solid transparent;
          border-right: 4px solid transparent;
          border-bottom: 4px solid rgba(0, 0, 0, 0.9);
        }
      }
    }
  }
}

// 增强的科技背景
.tech-background {
  overflow: hidden;
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
  
  .main-background {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: radial-gradient(ellipse at center, 
      #1a2332 0%, 
      #0f1419 50%, 
      #0a0e1a 100%);
  }
  
  .overlay-effects {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    
    .grid-overlay {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background-image: 
        linear-gradient(rgba(79, 172, 254, 0.1) 1px, transparent 1px),
        linear-gradient(90deg, rgba(79, 172, 254, 0.1) 1px, transparent 1px);
      background-size: 60px 60px;
      opacity: 0.3;
    }
    
    .floating-shapes {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      
      .shape {
        position: absolute;
        background: rgba(79, 172, 254, 0.1);
        border-radius: 50%;
        animation: float 8s ease-in-out infinite;
        
        &.shape-1 {
          width: 120px;
          height: 120px;
          top: 20%;
          left: 10%;
          animation-delay: 0s;
        }
        
        &.shape-2 {
          width: 80px;
          height: 80px;
          top: 60%;
          right: 15%;
          animation-delay: 2s;
        }
        
        &.shape-3 {
          width: 100px;
          height: 100px;
          bottom: 30%;
          left: 20%;
          animation-delay: 4s;
        }
        
        &.shape-4 {
          width: 60px;
          height: 60px;
          top: 40%;
          right: 25%;
          animation-delay: 1s;
        }
      }
    }
  }
}

// 底部平台优化
.platform-base {
  position: absolute;
  left: 0;
  right: 0;
  bottom: -20px;
  height: 15vh;
  z-index: 2;
  
  .platform-surface {
    position: relative;
    width: 100%;
    height: 100%;
    
    .platform-background {
      width: 100%;
      height: 100%;
      object-fit: cover;
      opacity: 0.8;
      filter: hue-rotate(10deg) brightness(1.1);
    }
  }
  
  .platform-glow {
    position: absolute;
    top: -60px;
    left: 0;
    right: 0;
    height: 60px;
    background: linear-gradient(to top, 
      rgba(79, 172, 254, 0.3) 0%,
      rgba(0, 242, 254, 0.1) 50%, 
      transparent 100%);
  }
}

// 主要内容区域优化
.content-area {
  position: relative;
  z-index: 10;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100vh;
  padding: 100px 20px 120px;
  
  .selection-title {
    text-align: center;
    margin-bottom: 32px;
    color: white;
    animation: fadeInUp 0.8s ease-out, titlePulse 3s infinite alternate;
    text-shadow: 0 0 15px rgba(79, 172, 254, 0.5);
    
    .title-main {
      font-size: 48px;
      margin: 0 0 16px 0;
      font-weight: 800;
      background: linear-gradient(135deg, #ffffff 0%, #00f2fe 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      text-shadow: 0 6px 12px rgba(0, 0, 0, 0.4);
    }
    
    .title-subtitle {
      font-size: 18px;
      margin: 0 0 20px 0;
      color: rgba(255, 255, 255, 0.7);
    }
    
    .title-decoration {
      width: 60px;
      height: 3px;
      background: linear-gradient(90deg, transparent, #4facfe, transparent);
      margin: 0 auto;
      border-radius: 2px;
    }
  }
  
  .project-stats {
    display: flex;
    gap: 40px;
    margin-bottom: 40px;
    animation: fadeInUp 0.8s ease-out 0.2s both;
    padding: 15px 25px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    backdrop-filter: blur(8px);
    
    .stat-item {
      text-align: center;
      color: white;
      
      .stat-number {
        font-size: 42px;
        font-weight: 700;
        color: #4facfe;
        text-shadow: 0 0 10px rgba(79, 172, 254, 0.5);
        animation: numberPulse 2s infinite alternate;
        margin-bottom: 4px;
      }
      
      .stat-label {
        font-size: 14px;
        color: rgba(255, 255, 255, 0.6);
      }
    }
  }
  
  .projects-grid {
    > div:nth-child(1) .project-card { animation-delay: 0.1s; }
    > div:nth-child(2) .project-card { animation-delay: 0.2s; }
    > div:nth-child(3) .project-card { animation-delay: 0.3s; }
    > div:nth-child(4) .project-card { animation-delay: 0.4s; }
    > div:nth-child(5) .project-card { animation-delay: 0.5s; }
    > div:nth-child(6) .project-card { animation-delay: 0.6s; }
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 32px;
    max-width: 1400px;
    width: 100%;
    padding: 0 20px;
    perspective: 1000px;
    
    .project-card {
      position: relative;
      height: 280px;
      border-radius: 24px;
      background: linear-gradient(145deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.08));
      backdrop-filter: blur(24px);
      border: 1px solid rgba(79, 172, 254, 0.2);
      transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
      cursor: pointer;
      overflow: hidden;
      animation: fadeInUp 0.6s ease-out both;
      opacity: 0;
      box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
      
      &:hover {
        transform: translateY(-12px) scale(1.05) rotateY(3deg);
        background: linear-gradient(135deg, rgba(79, 172, 254, 0.25), rgba(102, 102, 255, 0.25));
        border-color: rgba(79, 172, 254, 0.9);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3), 0 0 30px rgba(79, 172, 254, 0.4);
        
        .card-glow {
          opacity: 0.6;
        }
        
        .card-arrow {
          opacity: 1;
          transform: translateX(0);
        }
      }
      
      &.selected {
        background: rgba(79, 172, 254, 0.2);
        border-color: rgba(79, 172, 254, 0.8);
        transform: translateY(-8px) scale(1.02);
        
        .card-glow {
          opacity: 1;
        }
        
        .card-arrow {
          opacity: 1;
          transform: translateX(0);
        }
      }
      
      &.online {
        .project-icon .icon-pulse {
          display: block;
        }
      }
      
      .card-glow {
        position: absolute;
        top: -30px;
        left: -30px;
        right: -30px;
        bottom: -30px;
        background: radial-gradient(circle, rgba(79, 172, 254, 0.6) 0%, rgba(0, 242, 254, 0) 70%);
        opacity: 0;
        transition: opacity 0.4s;
        z-index: -1;
      }
      
      .card-border {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        border-radius: 16px;
        padding: 1px;
        background: linear-gradient(135deg, rgba(79, 172, 254, 0.5), transparent, rgba(0, 242, 254, 0.5));
        mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        mask-composite: exclude;
      }
      
      .card-inner {
        display: flex;
        flex-direction: column;
        height: 100%;
        padding: 24px;
        position: relative;
        z-index: 2;
        
        .project-icon {
          position: relative;
          width: 70px;
          height: 70px;
          background: rgba(79, 172, 254, 0.2);
          border: 2px solid rgba(79, 172, 254, 0.3);
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          margin-bottom: 16px;
          color: #4facfe;
          
          .icon-glow {
            position: absolute;
            top: -8px;
            left: -8px;
            right: -8px;
            bottom: -8px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(79, 172, 254, 0.4) 0%, rgba(79, 172, 254, 0) 70%);
          }
          
          .icon-pulse {
            display: none;
            position: absolute;
            top: -4px;
            left: -4px;
            right: -4px;
            bottom: -4px;
            border: 2px solid #00ff88;
            border-radius: 50%;
            animation: pulse 2s infinite;
          }
        }
        
        .project-info {
          flex: 1;
          
          h3 {
            color: white;
            margin: 0 0 10px 0;
            font-size: 20px;
            font-weight: 600;
            line-height: 1.3;
          }
          
          p {
            color: rgba(255, 255, 255, 0.7);
            margin: 0 0 16px 0;
            font-size: 14px;
            line-height: 1.5;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
          }
          
          .project-meta {
            display: flex;
            flex-direction: column;
            gap: 6px;
            
            .manager-info {
              display: flex;
              align-items: center;
              gap: 4px;
              
              .manager-label {
                color: rgba(255, 255, 255, 0.6);
                font-size: 12px;
              }
              
              .manager-name {
                color: rgba(79, 172, 254, 0.9);
                font-size: 12px;
                font-weight: 500;
              }
            }
            
            .created-date {
              color: rgba(255, 255, 255, 0.5);
              font-size: 13px;
              padding-top: 5px;
            }
          }
        }
        
        .project-status {
          align-self: flex-start;
          margin-bottom: 8px;
          transform: translateY(4px);
          
          .el-tag {
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: white;
            
            .status-dot {
              display: inline-block;
              width: 10px;
              height: 10px;
              border-radius: 50%;
              margin-right: 8px;
              background: currentColor;
              box-shadow: 0 0 10px currentColor, 0 0 20px currentColor;
              animation: statusPulse 2s infinite;
            }
            
            &.status-在线 {
              background: rgba(0, 255, 136, 0.2);
              border-color: rgba(0, 255, 136, 0.5);
              color: #00ff88;
            }
            
            &.status-开发中 {
              background: rgba(255, 193, 7, 0.2);
              border-color: rgba(255, 193, 7, 0.5);
              color: #ffc107;
            }
            
            &.status-维护中 {
              background: rgba(108, 117, 125, 0.2);
              border-color: rgba(108, 117, 125, 0.5);
              color: #6c757d;
            }
          }
        }
        
        .card-actions {
          position: absolute;
          top: 16px;
          right: 16px;
          display: flex;
          gap: 8px;
          z-index: 3;
        }
        
        .card-action {
          background: rgba(255, 255, 255, 0.1);
          border: 1px solid rgba(255, 255, 255, 0.2);
          border-radius: 12px;
          width: 36px;
          height: 36px;
          display: flex;
          align-items: center;
          justify-content: center;
          cursor: pointer;
          transition: all 0.3s;
          color: rgba(255, 255, 255, 0.7);
          
          &:hover {
            background: rgba(255, 255, 255, 0.2);
            border-color: rgba(255, 255, 255, 0.5);
            color: white;
          }
        }
        
        .card-arrow {
          position: absolute;
          top: 24px;
          right: 24px;
          color: rgba(255, 255, 255, 0.5);
          font-size: 20px;
          opacity: 0;
          transform: translateX(-10px);
          transition: all 0.3s;
        }
      }
    }
  }
  
  .empty-state {
    text-align: center;
    color: rgba(255, 255, 255, 0.6);
    animation: fadeInUp 0.8s ease-out;
    padding: 50px 30px;
    border-radius: 20px;
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    max-width: 500px;
    width: 100%;
    
    .empty-icon {
      font-size: 90px;
      margin-bottom: 20px;
      color: rgba(79, 172, 254, 0.3);
      animation: float 3s ease-in-out infinite;
    }
    
    h3 {
      margin: 0 0 8px 0;
      color: white;
    }
    
    p {
      margin: 0;
    }
  }
  
  .action-area {
    margin-top: 48px;
    display: flex;
    gap: 16px;
    flex-wrap: wrap;
    justify-content: center;
    animation: fadeInUp 0.8s ease-out 0.4s both;
    
    .enter-button {
      min-width: 200px;
      height: 56px;
      font-size: 16px;
      font-weight: 600;
      background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
      border: none;
      border-radius: 16px;
      transition: all 0.3s; 
      box-shadow: 0 8px 30px rgba(79, 172, 254, 0.4);
      position: relative;
      overflow: hidden;
      
      &:after {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
          to right, rgba(255,255,255,0) 0%,
          rgba(255,255,255,0.3) 50%,
          rgba(255,255,255,0) 100%
        );
        transform: rotate(30deg);
        animation: shine 3s infinite;
      }
      
      &:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(79, 172, 254, 0.4);
      }
      
      &:disabled {
        background: rgba(255, 255, 255, 0.1);
        color: rgba(255, 255, 255, 0.5);
        transform: none;
        box-shadow: none;
      }
    }
    
    .create-button {
      height: 56px;
      font-size: 16px;
      background: rgba(255, 255, 255, 0.1);
      border: 1px solid rgba(255, 255, 255, 0.2);
      border-radius: 16px;
      color: white;
      transition: all 0.3s, background-position 1s ease;
      background-image: linear-gradient(to right, rgba(79, 172, 254, 0) 0%, rgba(79, 172, 254, 0.2) 50%, rgba(79, 172, 254, 0) 100%);
      background-size: 200% auto;
      background-position: 0 center;
      
      &:hover {
        background: rgba(255, 255, 255, 0.2);
        border-color: rgba(79, 172, 254, 0.5);
        transform: translateY(-2px);
      }
    }
    
    .import-button {
      height: 56px;
      font-size: 16px;
      background: rgba(255, 255, 255, 0.1);
      border: 1px solid rgba(255, 255, 255, 0.2);
      border-radius: 16px;
      color: white;
      transition: all 0.3s;
      
      &:hover {
        background: rgba(255, 255, 255, 0.2);
        border-color: rgba(79, 172, 254, 0.5);
      }
    }
    
    .refresh-button {
      height: 56px;
      font-size: 16px;
      color: rgba(255, 255, 255, 0.7);
      transition: all 0.3s;
      
      &:hover {
        color: #4facfe;
      }
    }
  }
}

// 响应式设计
@media (max-width: 1200px) {
  .projects-grid {
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  }
}

@media (max-width: 768px) {
  .content-area {
    padding: 100px 16px 120px;
    
    .selection-title {
      font-size: 24px;
      padding: 0 15px;
    }
    
    .selection-title .title-main {
      font-size: 36px;
    }
    
    .project-stats {
      flex-direction: column;
      gap: 15px;
      padding: 15px;
      
      .stat-item .stat-number {
        font-size: 24px;
      }
    }
    
    .projects-grid {
      grid-template-columns: 1fr;
      gap: 16px;
      padding: 0 15px;
    }
    
    .action-area {
      flex-direction: column;
      align-items: center;
      padding: 0 15px;
      
      .enter-button,
      .create-button {
        width: 100%;
        max-width: 300px;
        height: 56px;
      }
    }
    
    .project-card {
      height: auto;
      min-height: 260px;
    }
  }
  
  .top-header .header-content {
    padding: 0 20px;
  }
  
  .user-actions {
    gap: 16px;
    
    .user-details {
      display: none;
    }
  }
}

// 导入对话框样式
.import-dialog-content {
  .upload-area {
    margin-bottom: 20px;
    
    .upload-dragger {
      width: 100%;
      height: 180px;
      border: 2px dashed #4facfe;
      border-radius: 12px;
      
      :deep(.el-upload-dragger) {
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        border: none;
        
        &:hover {
          border-color: #4facfe;
        }
        
        .upload-icon {
          font-size: 48px;
          color: #4facfe;
          margin-bottom: 16px;
        }
        
        .upload-text {
          font-size: 16px;
          margin-bottom: 8px;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
          max-width: 90%;
        }
        
        .upload-tip {
          font-size: 14px;
          color: rgba(0, 0, 0, 0.5);
        }
      }
    }
  }
  
  .import-instructions {
    background: #f7f9ff;
    padding: 12px 16px;
    border-radius: 8px;
    border-left: 4px solid #4facfe;
    
    h4 {
      margin-top: 0;
      margin-bottom: 8px;
      font-weight: 600;
    }
    
    p {
      margin: 4px 0;
      font-size: 14px;
    }
  }
}

.planning-content {
  .planning-info {
    display: flex;
    flex-wrap: wrap;
    margin-bottom: 20px;
    gap: 16px;
    
    .info-item {
      display: flex;
      align-items: center;
      
      .label {
        font-weight: bold;
        margin-right: 8px;
        color: #606266;
      }
      
      .value {
        color: #303133;
      }
    }
  }
  
  .planning-document {
    margin-top: 24px;
    border: 1px solid #e4e7ed;
    border-radius: 8px;
    padding: 16px;
    background: #f8f9fa;
    min-height: 300px;
    
    .planning-text {
      pre {
        white-space: pre-wrap;
        word-break: break-word;
        font-family: inherit;
        margin: 0;
        color: #303133;
        line-height: 1.6;
      }
    }
    
    .no-planning {
      display: flex;
      align-items: center;
      justify-content: center;
      height: 300px;
    }
  }
}

.create-project-form {
  .full-width {
    width: 100%;
  }
  
  // 新增自定义样式
  .custom-input {
    :deep(.el-input__wrapper) {
      border-radius: 12px;
      background: #f7f9ff;
      border: 2px solid transparent;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
      padding: 6px 14px;
      transition: all 0.3s;
      
      &:hover {
        border-color: rgba(79, 172, 254, 0.3);
        background: white;
      }
      
      &.is-focus {
        border-color: #4facfe;
        box-shadow: 0 0 0 3px rgba(79, 172, 254, 0.1);
        background: white;
      }
    }

    .input-icon {
      color: #4facfe;
    }
  }
  
  .custom-textarea {
    :deep(.el-textarea__inner) {
      border-radius: 12px;
      background: #f7f9ff;
      border: 2px solid transparent;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
      padding: 12px 14px;
      transition: all 0.3s;
      
      &:hover {
        border-color: rgba(79, 172, 254, 0.3);
        background: white;
      }
      
      &:focus {
        border-color: #4facfe;
        box-shadow: 0 0 0 3px rgba(79, 172, 254, 0.1);
        background: white;
      }
    }
  }
  
  .planning-upload {
    width: 100%;
    
    :deep(.el-upload) {
      width: 100%;
    }
    
    .upload-area {
      display: flex;
      align-items: center;
      gap: 12px;
      width: 100%;
      height: 80px;
      border: 2px dashed #dcdfe6;
      border-radius: 12px;
      padding: 0 20px;
      background: #f7f9ff;
      cursor: pointer;
      transition: all 0.3s;
      
      &:hover {
        border-color: #4facfe;
        background: white;
        box-shadow: 0 0 0 3px rgba(79, 172, 254, 0.1);
        
        .upload-icon {
          color: #4facfe;
          transform: scale(1.1);
        }
      }
      
      .upload-icon {
        font-size: 36px;
        color: #909399;
        transition: all 0.3s;
      }
      
      .upload-info {
        display: flex;
        flex-direction: column;
        
        .upload-text {
          font-size: 16px;
          font-weight: 500;
          color: #606266;
        }
        
        .upload-filename {
          font-size: 13px;
          color: #4facfe;
          margin-top: 4px;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
          max-width: 300px;
        }
      }
    }
    
    :deep(.el-upload__tip) {
      margin-top: 8px;
      font-size: 13px;
      color: #909399;
      text-align: center;
    }
  }
  
  .icon-selector-item {
    margin-bottom: 24px;
  }
  
  .icon-selector {
    display: flex;
    gap: 16px;
    flex-wrap: wrap;
    
    .icon-option {
      width: 60px;
      height: 60px;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 12px;
      background: #f7f9ff;
      cursor: pointer;
      position: relative;
      border: 2px solid transparent;
      transition: all 0.3s;
      
      &:hover {
        background: white;
        border-color: rgba(79, 172, 254, 0.3);
        transform: translateY(-2px);
        
        .icon-wrapper {
          color: #4facfe;
          transform: scale(1.1);
          
          .icon-glow {
            opacity: 0.5;
          }
        }
      }
      
      &.active {
        background: white;
        border-color: #4facfe;
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(79, 172, 254, 0.2);
        
        &::after {
          content: '';
          position: absolute;
          bottom: -10px;
          left: 50%;
          transform: translateX(-50%);
          width: 6px;
          height: 6px;
          background: #4facfe;
          border-radius: 50%;
        }
        
        .icon-wrapper {
          color: #4facfe;
          transform: scale(1.1);
          
          .icon-glow {
            opacity: 0.8;
          }
        }
      }
      
      .icon-wrapper {
        position: relative;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        color: #909399;
        transition: all 0.3s;
        
        .icon-glow {
          position: absolute;
          top: 50%;
          left: 50%;
          width: 40px;
          height: 40px;
          background: radial-gradient(circle, rgba(79, 172, 254, 0.5) 0%, rgba(79, 172, 254, 0) 70%);
          border-radius: 50%;
          transform: translate(-50%, -50%);
          opacity: 0;
          transition: all 0.3s;
        }
      }
    }
  }
}

// 创建项目对话框全局样式
:deep(.create-project-dialog) {
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 16px 32px rgba(0, 0, 0, 0.2), 0 4px 8px rgba(0, 0, 0, 0.1);
  
  .el-dialog__header {
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    padding: 20px 24px;
    border-bottom: none;
    position: relative;
    
    &::after {
      content: '';
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      height: 1px;
      background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.5), transparent);
    }
    
    .el-dialog__title {
      color: white;
      font-size: 20px;
      font-weight: 600;
    }
    
    .el-dialog__headerbtn {
      top: 20px;
      
      .el-dialog__close {
        color: white;
        
        &:hover {
          color: white;
          opacity: 0.8;
        }
      }
    }
  }
  
  .el-dialog__body {
    padding: 30px 24px 20px;
  }
  
  .el-dialog__footer {
    padding: 16px 24px 24px;
    border-top: none;
  }
  
  .dialog-footer {
    display: flex;
    justify-content: center;
    gap: 16px;
    width: 100%;
    
    .cancel-button {
      min-width: 120px;
      height: 44px;
      border-radius: 12px;
      font-size: 15px;
      background: rgba(0, 0, 0, 0.05);
      border: none;
      color: #606266;
      transition: all 0.3s;
      
      &:hover {
        background: rgba(0, 0, 0, 0.08);
        color: #303133;
      }
    }
    
    .submit-button {
      min-width: 160px;
      height: 44px;
      border-radius: 12px;
      font-size: 15px;
      font-weight: 600;
      background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
      border: none;
      color: white;
      transition: all 0.3s;
      box-shadow: 0 8px 16px rgba(79, 172, 254, 0.3);
      position: relative;
      overflow: hidden;
      
      &:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 20px rgba(79, 172, 254, 0.4);
        
        &::after {
          animation: shine 1.5s ease-out infinite;
        }
      }
      
      &:active {
        transform: translateY(0);
      }
      
      &::after {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
          to right, 
          rgba(255, 255, 255, 0) 0%,
          rgba(255, 255, 255, 0.3) 50%,
          rgba(255, 255, 255, 0) 100%
        );
        transform: rotate(30deg);
      }
      
      .button-content {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        position: relative;
        z-index: 1;
      }
    }
  }
}

// 下拉菜单样式
:deep(.manager-autocomplete-dropdown) {
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  padding: 8px;
  
  .el-autocomplete-suggestion__list {
    padding: 0;
    
    li {
      padding: 12px 16px;
      border-radius: 8px;
      margin-bottom: 4px;
      transition: all 0.3s;
      
      &:last-child {
        margin-bottom: 0;
      }
      
      &:hover, &.highlighted {
        background: rgba(79, 172, 254, 0.1);
      }
    }
  }
}
</style>
