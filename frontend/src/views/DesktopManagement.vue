<template>
  <div class="desktop-management">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1 class="page-title">协作运维平台云桌面管理</h1>
    </div>

    <!-- 筛选条件栏 -->
    <div class="filter-bar">
      <div class="filter-group">
        <!-- 话题分组 -->
        <div class="filter-item">
          <span class="filter-label">话题分组：</span>
          <el-select v-model="selectedTopic" placeholder="全部分组" class="filter-select" @change="handleTopicChange">
            <el-option label="全部分组" value="all"></el-option>
            <el-option label="办公应用" value="office"></el-option>
            <el-option label="开发环境" value="dev"></el-option>
            <el-option label="测试环境" value="test"></el-option>
            <el-option label="教学环境" value="education"></el-option>
          </el-select>
        </div>

        <!-- 最高管理 -->
        <div class="filter-item">
          <span class="filter-label">最高管理：</span>
          <el-select v-model="selectedManagement" placeholder="选择管理" class="filter-select" @change="handleManagementChange">
            <el-option label="全部管理" value="all"></el-option>
            <el-option label="管理员" value="admin"></el-option>
            <el-option label="普通用户" value="user"></el-option>
            <el-option label="访客" value="guest"></el-option>
          </el-select>
        </div>

        <!-- 模板统计 -->
        <div class="filter-item">
          <span class="filter-label">{{ filteredImageList.length }}个模板：</span>
          <div class="image-stats">
            <span class="stat-item stat-blue">🔵 {{ getStatusCount('running') }}个</span>
            <span class="stat-item stat-black">⚫ {{ getStatusCount('stopped') }}个</span>
            <span class="stat-item stat-red">🔴 {{ getStatusCount('error') }}个</span>
          </div>
        </div>

        <!-- 模板分组 -->
        <div class="filter-item">
          <span class="filter-label">模板分组：</span>
          <el-select v-model="selectedImageGroup" placeholder="选择分组" class="filter-select" @change="handleImageGroupChange">
            <el-option label="全部系统" value="all"></el-option>
            <el-option label="Windows系统" value="windows"></el-option>
            <el-option label="Linux系统" value="linux"></el-option>
          </el-select>
        </div>

        <!-- 内置充值使模块 -->
        <div class="filter-item">
          <el-radio-group v-model="chargeModule" class="charge-module" @change="handleChargeModuleChange">
            <el-radio :label="true" size="small">🔵 内置充值使模块</el-radio>
          </el-radio-group>
        </div>

        <!-- 模板从属管理 -->
        <div class="filter-item">
          <span class="filter-label">模板从属管理：</span>
          <el-select v-model="selectedSubordinate" placeholder="选择管理" class="filter-select" @change="handleSubordinateChange">
            <el-option label="全部管理" value="all"></el-option>
            <el-option label="主管理" value="main"></el-option>
            <el-option label="从管理" value="sub"></el-option>
          </el-select>
        </div>
      </div>
    </div>

    <!-- 操作栏 -->
    <div class="operation-bar">
      <div class="left-operations">
        <!-- 时间筛选 -->
        <div class="time-filter">
          <span class="filter-label">按创建时间排序：</span>
          <el-select v-model="timeSort" placeholder="全部" class="time-select" @change="handleTimeSortChange">
            <el-option label="全部" value="all"></el-option>
            <el-option label="最新创建" value="newest"></el-option>
            <el-option label="最旧创建" value="oldest"></el-option>
          </el-select>
        </div>

        <!-- 搜索框 -->
        <div class="search-box">
          <el-input
            v-model="searchKeyword"
            placeholder="搜索角色名称或系统类型"
            class="search-input"
            :prefix-icon="Search"
            @input="handleSearch"
            clearable
          />
        </div>
      </div>

      <div class="right-operations">
        <!-- 操作按钮 -->
        <el-button type="primary" :icon="Plus" class="action-btn" @click="handleAdd">新增</el-button>
        <el-button type="info" :icon="Edit" class="action-btn" @click="handleEdit" :disabled="selectedItems.length === 0">编辑</el-button>
        <el-button type="warning" class="action-btn" @click="handlePowerOperation" :disabled="selectedItems.length === 0">
          {{ getPowerButtonText() }}
        </el-button>
        <el-button type="success" class="action-btn register-btn" @click="handleRegister">📋 注册模板</el-button>
        <el-button type="danger" class="action-btn delete-btn" @click="handleDelete" :disabled="selectedItems.length === 0">🗑️ 删除模板</el-button>
      </div>
    </div>

    <!-- 模板卡片网格 -->
    <div class="image-grid">
      <div v-for="(image, index) in filteredImageList" :key="index" 
           class="image-card" 
           :class="{ 
             'selected': selectedItems.includes(index),
             'enabled': image.isEnabled,
             'disabled': !image.isEnabled
           }">
        <!-- 选择checkbox -->
        <div class="card-checkbox">
          <el-checkbox v-model="selectedItems" :label="index" @change="handleSelectItem"></el-checkbox>
        </div>

        <!-- 卡片头部 -->
        <div class="card-header">
          <div class="card-title">
            <span class="title-icon">👤</span>
            <span class="title-text">{{ image.name }}</span>
            <span class="system-badge">{{ image.systemDisplayName }}</span>
          </div>
          <div class="card-actions">
            <el-button type="primary" size="small" :icon="Edit" @click="handleEditSingle(index)">编辑</el-button>
            <el-button type="info" size="small" :icon="DocumentCopy" @click="handleCopy(index)">复制</el-button>
            <el-button type="success" size="small" :icon="Download" @click="handleDownload(index)">下载</el-button>
            <el-dropdown trigger="click">
              <el-button type="info" size="small" :icon="MoreFilled">更多</el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="handleViewDetails(index)">查看详情</el-dropdown-item>
                  <el-dropdown-item @click="handleExportConfig(index)">导出配置</el-dropdown-item>
                  <el-dropdown-item @click="handleClone(index)">克隆模板</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </div>

        <!-- 卡片内容 -->
        <div class="card-content">
          <!-- 左侧系统信息 -->
          <div class="system-info">
            <div class="system-icon">
              <div class="os-logo" :class="getOSLogoClass(image.system)">
                <span v-if="image.system.includes('windows')">⊞</span>
                <span v-else>🐧</span>
              </div>
            </div>
            <div class="system-details">
              <div class="os-name">{{ getOSDisplayName(image.system) }}</div>
              <div class="os-arch">{{ getOSArch(image.system) }}</div>
            </div>
          </div>
          
          <!-- 右侧详细信息 -->
          <div class="detail-info">
            <div class="info-row">
              <span class="info-label">系统盘</span>
              <span class="info-value">{{ image.systemDiskUsage }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">数据盘</span>
              <span class="info-value">{{ image.dataDiskUsage }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">创建时间</span>
              <span class="info-value">{{ image.createTime }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">更新时间</span>
              <span class="info-value">{{ image.updateTime }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { Search, Plus, Edit, Delete, DocumentCopy, Download, MoreFilled } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

// 筛选条件
const selectedTopic = ref('all')
const selectedManagement = ref('all')
const selectedImageGroup = ref('all')
const chargeModule = ref(true)
const selectedSubordinate = ref('all')
const timeSort = ref('all')
const searchKeyword = ref('')

// 选中的项目
const selectedItems = ref([])

// 模板数据
const imageList = reactive([
  {
    name: '网络工程师',
    system: 'windows10 64bit',
    systemDisplayName: 'Windows 10',
    systemDiskUsage: '15.2GB/120.0GB',
    dataDiskUsage: '8.5GB/50.0GB',
    createTime: '2024-01-15 09:30:17',
    updateTime: '2024-01-20 14:20:45',
    isEnabled: true,
    status: 'running',
    topic: 'office',
    management: 'admin',
    imageGroup: 'windows'
  },
  {
    name: '系统架构师',
    system: 'windows10 64bit',
    systemDisplayName: 'Windows 10',
    systemDiskUsage: '12.8GB/120.0GB',
    dataDiskUsage: '15.2GB/50.0GB',
    createTime: '2024-01-16 10:15:33',
    updateTime: '2024-01-22 16:45:12',
    isEnabled: true,
    status: 'running',
    topic: 'education',
    management: 'user',
    imageGroup: 'windows'
  },
  {
    name: '系统规划与管理师',
    system: 'windows11 64bit',
    systemDisplayName: 'Windows 11',
    systemDiskUsage: '18.5GB/120.0GB',
    dataDiskUsage: '22.1GB/50.0GB',
    createTime: '2024-01-17 11:00:58',
    updateTime: '2024-01-23 09:30:27',
    isEnabled: true,
    status: 'running',
    topic: 'education',
    management: 'user',
    imageGroup: 'windows'
  },
  {
    name: '系统分析师',
    system: 'windows11 64bit',
    systemDisplayName: 'Windows 11',
    systemDiskUsage: '10.3GB/120.0GB',
    dataDiskUsage: '5.8GB/50.0GB',
    createTime: '2024-01-18 14:20:41',
    updateTime: '2024-01-24 11:15:06',
    isEnabled: true,
    status: 'running',
    topic: 'office',
    management: 'admin',
    imageGroup: 'windows'
  },
  {
    name: '开发者角色',
    system: 'windows11 64bit',
    systemDisplayName: 'Windows 11',
    systemDiskUsage: '25.7GB/150.0GB',
    dataDiskUsage: '35.4GB/100.0GB',
    createTime: '2024-01-19 15:45:29',
    updateTime: '2024-01-25 13:20:18',
    isEnabled: false,
    status: 'stopped',
    topic: 'dev',
    management: 'admin',
    imageGroup: 'windows'
  },
  {
    name: '测试人员角色',
    system: 'windows10 64bit',
    systemDisplayName: 'Windows 10',
    systemDiskUsage: '14.9GB/120.0GB',
    dataDiskUsage: '18.7GB/50.0GB',
    createTime: '2024-01-20 08:30:52',
    updateTime: '2024-01-26 10:40:35',
    isEnabled: false,
    status: 'stopped',
    topic: 'test',
    management: 'user',
    imageGroup: 'windows'
  },
  {
    name: '运维角色',
    system: 'linux ubuntu 20.04',
    systemDisplayName: 'Ubuntu 20.04',
    systemDiskUsage: '8.2GB/80.0GB',
    dataDiskUsage: '12.5GB/100.0GB',
    createTime: '2024-01-21 12:00:14',
    updateTime: '2024-01-27 15:10:49',
    isEnabled: false,
    status: 'stopped',
    topic: 'dev',
    management: 'admin',
    imageGroup: 'linux'
  },
  {
    name: '安全审计角色',
    system: 'linux centos 8',
    systemDisplayName: 'CentOS 8',
    systemDiskUsage: '11.8GB/80.0GB',
    dataDiskUsage: '25.3GB/100.0GB',
    createTime: '2024-01-22 16:30:07',
    updateTime: '2024-01-28 09:25:53',
    isEnabled: false,
    status: 'stopped',
    topic: 'office',
    management: 'admin',
    imageGroup: 'linux'
  }
])

// 计算过滤后的列表
const filteredImageList = computed(() => {
  let filtered = [...imageList]
  
  // 话题分组筛选
  if (selectedTopic.value !== 'all') {
    filtered = filtered.filter(item => item.topic === selectedTopic.value)
  }
  
  // 最高管理筛选
  if (selectedManagement.value !== 'all') {
    filtered = filtered.filter(item => item.management === selectedManagement.value)
  }
  
  // 模板分组筛选
  if (selectedImageGroup.value !== 'all') {
    filtered = filtered.filter(item => item.imageGroup === selectedImageGroup.value)
  }
  
  // 搜索关键词筛选
  if (searchKeyword.value) {
    filtered = filtered.filter(item => 
      item.name.toLowerCase().includes(searchKeyword.value.toLowerCase()) ||
      item.systemDisplayName.toLowerCase().includes(searchKeyword.value.toLowerCase())
    )
  }
  
  // 时间排序
  if (timeSort.value === 'newest') {
    filtered.sort((a, b) => new Date(b.createTime) - new Date(a.createTime))
  } else if (timeSort.value === 'oldest') {
    filtered.sort((a, b) => new Date(a.createTime) - new Date(b.createTime))
  }
  
  return filtered
})

// 获取状态统计
const getStatusCount = (status) => {
  return filteredImageList.value.filter(item => item.status === status).length
}

// 获取电源按钮文本
const getPowerButtonText = () => {
  if (selectedItems.value.length === 0) return '⚡ 电源操作'
  
  const selectedImages = selectedItems.value.map(index => filteredImageList.value[index])
  const runningCount = selectedImages.filter(item => item.status === 'running').length
  const stoppedCount = selectedImages.filter(item => item.status === 'stopped').length
  
  if (runningCount > 0 && stoppedCount === 0) return '🔴 关机'
  if (runningCount === 0 && stoppedCount > 0) return '🔵 开机'
  return '⚡ 混合操作'
}

// 筛选处理函数
const handleTopicChange = () => {
  selectedItems.value = []
}

const handleManagementChange = () => {
  selectedItems.value = []
}

const handleImageGroupChange = () => {
  selectedItems.value = []
}

const handleChargeModuleChange = () => {
  // 充值模块变更逻辑
}

const handleSubordinateChange = () => {
  selectedItems.value = []
}

const handleTimeSortChange = () => {
  selectedItems.value = []
}

const handleSearch = () => {
  selectedItems.value = []
}

// 操作处理函数
const handleAdd = () => {
  ElMessage.success('打开新增模板对话框')
}

const handleEdit = () => {
  if (selectedItems.value.length === 0) {
    ElMessage.warning('请先选择要编辑的模板')
    return
  }
  ElMessage.success(`编辑 ${selectedItems.value.length} 个模板`)
}

const handlePowerOperation = () => {
  if (selectedItems.value.length === 0) {
    ElMessage.warning('请先选择要操作的模板')
    return
  }
  
  const selectedImages = selectedItems.value.map(index => filteredImageList.value[index])
  const runningCount = selectedImages.filter(item => item.status === 'running').length
  const stoppedCount = selectedImages.filter(item => item.status === 'stopped').length
  
  if (runningCount > 0 && stoppedCount === 0) {
    // 全部关机
    selectedItems.value.forEach(index => {
      const actualIndex = imageList.findIndex(item => item === filteredImageList.value[index])
      if (actualIndex !== -1) {
        imageList[actualIndex].status = 'stopped'
        imageList[actualIndex].isEnabled = false
      }
    })
    ElMessage.success(`成功关机 ${selectedItems.value.length} 个模板`)
  } else if (runningCount === 0 && stoppedCount > 0) {
    // 全部开机
    selectedItems.value.forEach(index => {
      const actualIndex = imageList.findIndex(item => item === filteredImageList.value[index])
      if (actualIndex !== -1) {
        imageList[actualIndex].status = 'running'
        imageList[actualIndex].isEnabled = true
      }
    })
    ElMessage.success(`成功开机 ${selectedItems.value.length} 个模板`)
  } else {
    ElMessage.info('混合状态，请分别选择相同状态的模板进行操作')
  }
  
  selectedItems.value = []
}

const handleRegister = () => {
  ElMessage.success('注册模板功能')
}

const handleDelete = () => {
  if (selectedItems.value.length === 0) {
    ElMessage.warning('请先选择要删除的模板')
    return
  }
  ElMessage.error(`删除 ${selectedItems.value.length} 个模板`)
}

const handleSelectItem = () => {
  // 选择项目变更
}

// 单个操作函数
const handleEditSingle = (index) => {
  ElMessage.success(`编辑模板：${filteredImageList.value[index].name}`)
}

const handleCopy = (index) => {
  ElMessage.success(`复制模板：${filteredImageList.value[index].name}`)
}

const handleDownload = (index) => {
  ElMessage.success(`下载模板：${filteredImageList.value[index].name}`)
}

const handleViewDetails = (index) => {
  ElMessage.info(`查看详情：${filteredImageList.value[index].name}`)
}

const handleExportConfig = (index) => {
  ElMessage.success(`导出配置：${filteredImageList.value[index].name}`)
}

const handleClone = (index) => {
  ElMessage.success(`克隆模板：${filteredImageList.value[index].name}`)
}

// 获取操作系统显示名称
const getOSDisplayName = (system) => {
  if (system.includes('windows10')) return 'Windows 10'
  if (system.includes('windows11')) return 'Windows 11'
  if (system.includes('ubuntu')) return 'Ubuntu'
  if (system.includes('centos')) return 'CentOS'
  return 'Unknown OS'
}

// 获取架构
const getOSArch = (system) => {
  return system.includes('64bit') ? '64Bit' : '32Bit'
}

// 获取操作系统Logo样式
const getOSLogoClass = (system) => {
  if (system.includes('windows')) return 'windows-logo'
  return 'linux-logo'
}
</script>

<style scoped>
.desktop-management {
  padding: 20px;
  background: #f5f7fa;
  min-height: 100vh;
}

/* 页面标题 */
.page-header {
  margin-bottom: 20px;
}

.page-title {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin: 0;
}

/* 筛选条件栏 */
.filter-bar {
  background: white;
  padding: 16px 20px;
  border-radius: 8px;
  margin-bottom: 16px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.filter-group {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 24px;
}

.filter-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-label {
  font-size: 14px;
  color: #666;
  white-space: nowrap;
}

.filter-select {
  width: 140px;
}

.image-stats {
  display: flex;
  gap: 12px;
}

.stat-item {
  font-size: 14px;
  padding: 2px 8px;
  border-radius: 4px;
}

.stat-blue {
  color: #1890ff;
}

.stat-black {
  color: #333;
}

.stat-red {
  color: #ff4d4f;
}

.charge-module {
  margin: 0;
}

/* 操作栏 */
.operation-bar {
  background: white;
  padding: 16px 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.left-operations {
  display: flex;
  align-items: center;
  gap: 20px;
}

.time-filter {
  display: flex;
  align-items: center;
  gap: 8px;
}

.time-select {
  width: 100px;
}

.search-input {
  width: 300px;
}

.right-operations {
  display: flex;
  gap: 12px;
}

.action-btn {
  height: 36px;
  font-weight: 500;
}

.register-btn {
  background: #52c41a;
  border-color: #52c41a;
}

.register-btn:hover {
  background: #73d13d;
  border-color: #73d13d;
}

.delete-btn {
  background: #ff4d4f;
  border-color: #ff4d4f;
}

.delete-btn:hover {
  background: #ff7875;
  border-color: #ff7875;
}

/* 模板卡片网格 */
.image-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.image-card {
  border-radius: 12px;
  box-shadow: 0 8px 25px rgba(74, 144, 226, 0.3);
  overflow: hidden;
  transition: transform 0.3s, box-shadow 0.3s, background 0.3s;
  color: white;
  position: relative;
}

.image-card.enabled {
  background: linear-gradient(135deg, #4a90e2 0%, #357abd 50%, #1e5f99 100%);
}

.image-card.disabled {
  background: linear-gradient(135deg, #8c8c8c 0%, #666666 50%, #404040 100%);
  opacity: 0.7;
}

.image-card:hover {
  transform: translateY(-4px);
}

.image-card.enabled:hover {
  box-shadow: 0 12px 35px rgba(74, 144, 226, 0.4);
}

.image-card.disabled:hover {
  box-shadow: 0 12px 35px rgba(140, 140, 140, 0.4);
}

/* 卡片头部 */
.card-header {
  padding: 16px 20px 12px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-title {
  display: flex;
  align-items: center;
  gap: 8px;
}

.title-icon {
  font-size: 18px;
}

.title-text {
  font-size: 16px;
  font-weight: 600;
  color: white;
}

.system-badge {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  backdrop-filter: blur(10px);
}

.card-actions {
  display: flex;
  gap: 8px;
}

.card-actions .el-button {
  height: 28px;
  padding: 4px 12px;
  font-size: 12px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  backdrop-filter: blur(10px);
}

.card-actions .el-button:hover {
  background: rgba(255, 255, 255, 0.2);
}

/* 卡片内容 */
.card-content {
  padding: 20px;
  display: flex;
  gap: 24px;
  align-items: flex-start;
}

/* 左侧系统信息 */
.system-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  min-width: 120px;
}

.system-icon {
  position: relative;
}

.os-logo {
  width: 64px;
  height: 64px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  font-weight: bold;
  backdrop-filter: blur(20px);
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.windows-logo {
  background: rgba(255, 255, 255, 0.15);
  color: white;
}

.linux-logo {
  background: rgba(255, 255, 255, 0.15);
  color: #ffd700;
}

.system-details {
  text-align: center;
}

.os-name {
  font-size: 14px;
  font-weight: 600;
  color: white;
  margin-bottom: 2px;
}

.os-arch {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.8);
}

/* 右侧详细信息 */
.detail-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.info-row:last-child {
  border-bottom: none;
}

.info-label {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.9);
  font-weight: 500;
}

.info-value {
  font-size: 14px;
  color: white;
  font-weight: 600;
  text-align: right;
}

/* 响应式设计 */
@media (max-width: 1400px) {
  .image-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .filter-group {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .operation-bar {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }
  
  .left-operations,
  .right-operations {
    justify-content: center;
  }
  
  .content-row {
    grid-template-columns: 1fr;
  }
}

/* 选择框样式 */
.card-checkbox {
  position: absolute;
  top: 8px;
  left: 8px;
  z-index: 10;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 4px;
  padding: 4px;
}

.image-card.selected {
  border: 2px solid #1890ff;
  box-shadow: 0 0 15px rgba(24, 144, 255, 0.5);
}

/* 操作按钮样式更新 */
.action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.action-btn {
  height: 36px;
  font-weight: 500;
}

.register-btn {
  background: #52c41a;
  border-color: #52c41a;
}

.register-btn:hover {
  background: #73d13d;
  border-color: #73d13d;
}

.delete-btn {
  background: #ff4d4f;
  border-color: #ff4d4f;
}

.delete-btn:hover {
  background: #ff7875;
  border-color: #ff7875;
}
</style>
