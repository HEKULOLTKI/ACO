<template>
  <div class="project-selection-container">
    <!-- 顶部操作栏 -->
    <div class="top-header">
      <div class="header-content">
        <!-- 左侧logo -->
        <div class="header-logo">
          <img src="/src/assets/icon/00005.png" alt="系统标识" class="logo-image">
        </div>
        
        <!-- 右侧用户信息和操作 -->
        <div class="user-actions">
          <div class="user-info">
            <div class="user-avatar">
              <img src="/src/assets/role/头像.svg" alt="用户头像" class="avatar-icon">
              <div class="avatar-ring"></div>
            </div>
            <div class="user-details">
              <div class="username">{{ authStore.user?.username || '管理员' }}</div>
              <div class="user-role">{{ authStore.user?.role || '系统管理员' }}</div>
            </div>
          </div>
          
          <div class="action-buttons">
            <div class="action-btn" @click="openSettings">
              <img src="/src/assets/role/设置.svg" alt="设置" class="action-icon">
              <div class="btn-glow"></div>
              <div class="btn-arrow">→</div>
              <span class="btn-tooltip">系统设置</span>
            </div>
            <div class="action-btn" @click="logout">
              <img src="/src/assets/role/退出.svg" alt="退出" class="action-icon">
              <div class="btn-glow"></div>
              <div class="btn-arrow">→</div>
              <span class="btn-tooltip">退出登录</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 科技背景 -->
    <div class="tech-background">
      <div class="main-background"></div>
      <div class="overlay-effects">
        <div class="light-beams"></div>
        <div class="particles"></div>
        <div class="grid-overlay"></div>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="main-content">
      <div class="content-header">
        <h1 class="content-title">选择项目</h1>
        <p class="content-subtitle">请选择要管理的项目</p>
      </div>

      <!-- 项目列表区域 -->
      <div class="projects-container">
        <!-- 项目列表 -->
        <div class="projects-list" v-if="!isLoading">
          <!-- 创建新项目卡片 -->
          <div class="project-card create-project" @click="showCreateProjectDialog = true">
            <div class="card-inner">
              <div class="card-icon">
                <el-icon :size="32"><Plus /></el-icon>
              </div>
              <div class="card-text">创建新项目</div>
            </div>
          </div>

          <!-- 项目卡片列表 -->
          <div 
            v-for="project in projects" 
            :key="project.id" 
            class="project-card" 
            :class="{ 'active': selectedProjectId === project.id }"
            @click="selectProject(project)"
          >
            <div class="card-glow"></div>
            <div class="card-inner">
              <div class="card-header">
                <div class="project-name">{{ project.name }}</div>
                <div class="project-status" :class="getStatusClass(project.status)">{{ getStatusText(project.status) }}</div>
              </div>
              <div class="card-content">
                <div class="project-description">{{ project.description || '暂无描述' }}</div>
                <div class="project-info">
                  <div class="info-item">
                    <el-icon><Calendar /></el-icon>
                    <span>{{ formatDate(project.created_at) }}</span>
                  </div>
                  <div class="info-item" v-if="project.manager">
                    <el-icon><User /></el-icon>
                    <span>{{ project.manager.username }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 加载中状态 -->
        <div v-if="isLoading" class="loading-container">
          <el-icon class="loading-icon" :size="48"><Loading /></el-icon>
          <div class="loading-text">加载项目中...</div>
        </div>

        <!-- 无项目状态 -->
        <div v-if="!isLoading && projects.length === 0" class="empty-container">
          <el-icon :size="48"><DocumentRemove /></el-icon>
          <div class="empty-text">暂无项目</div>
          <el-button type="primary" @click="showCreateProjectDialog = true">创建新项目</el-button>
        </div>
      </div>

      <!-- 底部操作按钮 -->
      <div class="action-buttons-container" v-if="selectedProjectId !== null">
        <el-button 
          type="primary" 
          size="large" 
          @click="enterProject"
          :loading="enterLoading"
        >
          进入项目
        </el-button>
        <el-button type="default" size="large" @click="cancelSelection">取消选择</el-button>
      </div>
    </div>

    <!-- 创建项目对话框 -->
    <el-dialog
      v-model="showCreateProjectDialog"
      title="创建新项目"
      width="500px"
      :close-on-click-modal="false"
      :show-close="true"
    >
      <el-form
        ref="createProjectFormRef"
        :model="createProjectForm"
        :rules="createProjectRules"
        label-position="top"
      >
        <el-form-item label="项目名称" prop="name">
          <el-input v-model="createProjectForm.name" placeholder="请输入项目名称"></el-input>
        </el-form-item>
        <el-form-item label="项目描述" prop="description">
          <el-input
            v-model="createProjectForm.description"
            type="textarea"
            :rows="3"
            placeholder="请输入项目描述"
          ></el-input>
        </el-form-item>
        <el-form-item label="项目状态" prop="status">
          <el-select v-model="createProjectForm.status" placeholder="请选择项目状态" style="width: 100%">
            <el-option label="活跃" value="active"></el-option>
            <el-option label="暂停" value="paused"></el-option>
            <el-option label="计划中" value="planned"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showCreateProjectDialog = false">取消</el-button>
          <el-button type="primary" @click="createProject" :loading="createLoading">创建</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  Calendar, 
  User, 
  Plus, 
  Loading, 
  DocumentRemove
} from '@element-plus/icons-vue'
import { useAuthStore } from '@/store/modules/auth'
import type { FormInstance, FormRules } from 'element-plus'
import { getProjects, createProject } from '@/api/project'
import type { Project } from '@/types/user'

const router = useRouter()
const authStore = useAuthStore()

// 项目数据
const projects = ref<Project[]>([])
const isLoading = ref(true)
const selectedProjectId = ref<number | null>(null)
const enterLoading = ref(false)

// 创建项目
const showCreateProjectDialog = ref(false)
const createProjectFormRef = ref<FormInstance>()
const createLoading = ref(false)
const createProjectForm = ref({
  name: '',
  description: '',
  status: 'active'
})
const createProjectRules: FormRules = {
  name: [
    { required: true, message: '请输入项目名称', trigger: 'blur' },
    { min: 2, max: 50, message: '项目名称长度应为2-50个字符', trigger: 'blur' }
  ],
  description: [
    { max: 200, message: '项目描述不能超过200个字符', trigger: 'blur' }
  ],
  status: [
    { required: true, message: '请选择项目状态', trigger: 'change' }
  ]
}

// 顶部菜单操作
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

// 获取项目状态样式
const getStatusClass = (status: string): string => {
  const statusMap: Record<string, string> = {
    'active': 'status-active',
    'paused': 'status-paused',
    'planned': 'status-planned',
    'completed': 'status-completed'
  }
  return statusMap[status] || 'status-default'
}

// 获取项目状态文本
const getStatusText = (status: string): string => {
  const textMap: Record<string, string> = {
    'active': '活跃',
    'paused': '暂停',
    'planned': '计划中',
    'completed': '已完成'
  }
  return textMap[status] || status
}

// 格式化日期
const formatDate = (dateStr?: string): string => {
  if (!dateStr) return '未知日期'
  
  const date = new Date(dateStr)
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  
  return `${year}-${month}-${day}`
}

// 选择项目
const selectProject = (project: Project) => {
  selectedProjectId.value = project.id
}

// 取消选择
const cancelSelection = () => {
  selectedProjectId.value = null
}

// 进入项目
const enterProject = async () => {
  if (!selectedProjectId.value) {
    ElMessage.warning('请先选择一个项目')
    return
  }
  
  enterLoading.value = true
  try {
    // 保存选中的项目到本地存储
    localStorage.setItem('selectedProject', selectedProjectId.value.toString())
    
    // 可以在这里添加其他项目相关的初始化逻辑
    
    ElMessage.success('项目加载成功，正在进入...')
    
    // 跳转到仪表盘
    setTimeout(() => {
      router.push('/dashboard')
    }, 500)
  } catch (error) {
    console.error('进入项目失败:', error)
    ElMessage.error('进入项目失败，请重试')
  } finally {
    enterLoading.value = false
  }
}

// 创建项目
const createProject = async () => {
  if (!createProjectFormRef.value) return
  
  try {
    await createProjectFormRef.value.validate()
    
    createLoading.value = true
    
    // 调用创建项目API
    const response = await createProject(createProjectForm.value)
    
    ElMessage.success('项目创建成功')
    showCreateProjectDialog.value = false
    
    // 重新加载项目列表
    loadProjects()
    
  } catch (error) {
    console.error('创建项目失败:', error)
    ElMessage.error('创建项目失败，请重试')
  } finally {
    createLoading.value = false
  }
}

// 加载项目列表
const loadProjects = async () => {
  isLoading.value = true
  try {
    const response = await getProjects()
    projects.value = response.data || []
  } catch (error) {
    console.error('加载项目失败:', error)
    ElMessage.error('加载项目失败，请刷新页面重试')
    
    // 示例数据（仅在API调用失败时使用）
    projects.value = [
      {
        id: 1,
        name: '多智能体协作平台开发项目',
        description: '开发基于多智能体协作的运维平台系统，提供设备管理、任务分发等功能',
        status: 'active',
        created_at: '2023-06-15T08:30:00Z',
        updated_at: '2023-07-10T14:20:00Z',
        manager_id: 1,
        manager: {
          id: 1,
          username: '系统管理员',
          role: '系统管理员',
          type: '管理员',
          status: 'active'
        }
      },
      {
        id: 2,
        name: '智能运维系统升级项目',
        description: '对现有运维系统进行AI能力升级，增加智能分析和预测功能',
        status: 'planned',
        created_at: '2023-08-05T09:15:00Z',
        updated_at: '2023-08-05T09:15:00Z',
        manager_id: 1,
        manager: {
          id: 1,
          username: '系统管理员',
          role: '系统管理员',
          type: '管理员',
          status: 'active'
        }
      }
    ]
  } finally {
    isLoading.value = false
  }
}

// 页面加载时获取项目列表
onMounted(() => {
  loadProjects()
})
</script>

<style scoped lang="scss">
.project-selection-container {
  width: 100%;
  height: 100vh;
  position: relative;
  overflow: hidden;
  font-family: 'Microsoft YaHei', '微软雅黑', sans-serif;
  color: #ffffff;
}

/* 顶部操作栏 */
.top-header {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 80px;
  z-index: 200;
  background: rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  box-shadow: 0 1px 10px rgba(0, 0, 0, 0.1);
}

.header-content {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 40px;
}

/* 左侧Logo */
.header-logo {
  display: flex;
  align-items: center;
  height: 100%;
}

.logo-image {
  height: 40px;
  width: auto;
  object-fit: contain;
  filter: drop-shadow(0 0 10px rgba(0, 255, 255, 0.3));
  transition: all 0.3s ease;
}

.logo-image:hover {
  filter: drop-shadow(0 0 15px rgba(0, 255, 255, 0.5));
  transform: scale(1.05);
}

/* 右侧用户信息和操作 */
.user-actions {
  display: flex;
  align-items: center;
  gap: 20px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 6px 16px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 30px;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.user-avatar {
  position: relative;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  overflow: hidden;
}

.avatar-icon {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-ring {
  position: absolute;
  top: -2px;
  left: -2px;
  width: calc(100% + 4px);
  height: calc(100% + 4px);
  border-radius: 50%;
  border: 2px solid rgba(255, 255, 255, 0.6);
  animation: ringPulse 2s ease-in-out infinite;
}

@keyframes ringPulse {
  0%, 100% {
    opacity: 0.6;
    transform: scale(1);
  }
  50% {
    opacity: 0.9;
    transform: scale(1.05);
  }
}

.user-details {
  display: flex;
  flex-direction: column;
}

.username {
  font-size: 16px;
  font-weight: 600;
  color: #ffffff;
}

.user-role {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.8);
}

.action-buttons {
  display: flex;
  gap: 12px;
}

.action-btn {
  position: relative;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}

.action-icon {
  width: 22px;
  height: 22px;
  object-fit: contain;
}

.btn-glow {
  position: absolute;
  top: -3px;
  left: -3px;
  right: -3px;
  bottom: -3px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.4), transparent 70%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.action-btn:hover .btn-glow {
  opacity: 1;
}

.btn-arrow {
  position: absolute;
  top: 50%;
  right: -20px;
  transform: translateY(-50%);
  font-size: 16px;
  color: rgba(255, 255, 255, 0.8);
  opacity: 0;
  transition: all 0.3s ease;
}

.action-btn:hover .btn-arrow {
  opacity: 1;
  right: -25px;
}

.btn-tooltip {
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%) translateY(10px);
  background: rgba(0, 0, 0, 0.7);
  color: #ffffff;
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 12px;
  white-space: nowrap;
  pointer-events: none;
  opacity: 0;
  transition: all 0.3s ease;
  z-index: 10;
}

.action-btn:hover .btn-tooltip {
  opacity: 1;
  transform: translateX(-50%) translateY(5px);
}

/* 科技背景 */
.tech-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  z-index: 1;
}

.main-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url('/src/assets/image/背景.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

.overlay-effects {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.light-beams {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(
    ellipse at center,
    rgba(100, 100, 255, 0.2),
    rgba(0, 100, 255, 0.1),
    transparent 70%
  );
  animation: breathe 4s ease-in-out infinite;
}

@keyframes breathe {
  0%, 100% {
    opacity: 0.6;
  }
  50% {
    opacity: 1;
  }
}

.particles {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.grid-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    linear-gradient(rgba(100, 149, 237, 0.1) 1px, transparent 1px),
    linear-gradient(90deg, rgba(100, 149, 237, 0.1) 1px, transparent 1px);
  background-size: 50px 50px;
  opacity: 0.3;
}

/* 主要内容区域 */
.main-content {
  position: relative;
  z-index: 10;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 100px 40px 40px;
  box-sizing: border-box;
}

.content-header {
  text-align: center;
  margin-bottom: 40px;
}

.content-title {
  font-size: 36px;
  font-weight: 700;
  margin: 0 0 10px;
  background: linear-gradient(135deg, #ffffff 0%, #8cb4ff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 2px 10px rgba(0, 100, 255, 0.3);
}

.content-subtitle {
  font-size: 18px;
  color: rgba(255, 255, 255, 0.8);
  margin: 0;
}

/* 项目列表区域 */
.projects-container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.projects-list {
  width: 100%;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 30px;
  padding: 20px 0;
}

/* 项目卡片 */
.project-card {
  position: relative;
  height: 200px;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 10px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.project-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  border-color: rgba(255, 255, 255, 0.3);
}

.project-card.active {
  border-color: rgba(100, 149, 237, 0.8);
  box-shadow: 0 0 0 2px rgba(100, 149, 237, 0.3), 0 10px 30px rgba(0, 0, 0, 0.2);
}

.card-glow {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(
    circle at center,
    rgba(100, 149, 237, 0.3),
    transparent 70%
  );
  opacity: 0;
  transition: opacity 0.3s ease;
}

.project-card:hover .card-glow,
.project-card.active .card-glow {
  opacity: 1;
}

.card-inner {
  position: relative;
  width: 100%;
  height: 100%;
  padding: 20px;
  display: flex;
  flex-direction: column;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.project-name {
  font-size: 20px;
  font-weight: 600;
  color: #ffffff;
}

.project-status {
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
}

.status-active {
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
  border: 1px solid rgba(16, 185, 129, 0.4);
}

.status-paused {
  background: rgba(245, 158, 11, 0.2);
  color: #f59e0b;
  border: 1px solid rgba(245, 158, 11, 0.4);
}

.status-planned {
  background: rgba(59, 130, 246, 0.2);
  color: #3b82f6;
  border: 1px solid rgba(59, 130, 246, 0.4);
}

.status-completed {
  background: rgba(107, 114, 128, 0.2);
  color: #9ca3af;
  border: 1px solid rgba(107, 114, 128, 0.4);
}

.card-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.project-description {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.5;
  margin-bottom: 15px;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

.project-info {
  display: flex;
  gap: 20px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: rgba(255, 255, 255, 0.7);
}

.info-item .el-icon {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.7);
}

/* 创建项目卡片 */
.create-project {
  display: flex;
  align-items: center;
  justify-content: center;
  border-style: dashed;
  background: rgba(255, 255, 255, 0.05);
}

.create-project .card-inner {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 15px;
}

.card-icon {
  width: 64px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  color: #ffffff;
  transition: all 0.3s ease;
}

.create-project:hover .card-icon {
  background: rgba(100, 149, 237, 0.2);
  transform: scale(1.1);
}

.card-text {
  font-size: 16px;
  font-weight: 500;
  color: #ffffff;
}

/* 加载和空状态 */
.loading-container,
.empty-container {
  width: 100%;
  padding: 80px 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 20px;
}

.loading-icon {
  color: #ffffff;
  animation: rotating 2s linear infinite;
}

@keyframes rotating {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.loading-text,
.empty-text {
  font-size: 16px;
  color: rgba(255, 255, 255, 0.8);
  margin-top: 15px;
}

/* 底部操作按钮 */
.action-buttons-container {
  margin-top: 40px;
  display: flex;
  gap: 20px;
}

/* 媒体查询 */
@media (max-width: 768px) {
  .projects-list {
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 20px;
  }
  
  .header-content {
    padding: 0 20px;
  }
  
  .user-info {
    padding: 4px 12px;
  }
  
  .user-avatar {
    width: 36px;
    height: 36px;
  }
  
  .username {
    font-size: 14px;
  }
  
  .user-role {
    font-size: 11px;
  }
  
  .content-title {
    font-size: 28px;
  }
  
  .content-subtitle {
    font-size: 16px;
  }
}

@media (max-width: 480px) {
  .projects-list {
    grid-template-columns: 1fr;
  }
  
  .action-buttons {
    gap: 8px;
  }
  
  .action-btn {
    width: 36px;
    height: 36px;
  }
  
  .content-title {
    font-size: 24px;
  }
  
  .content-subtitle {
    font-size: 14px;
  }
}
</style> 