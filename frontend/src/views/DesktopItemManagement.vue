<template>
  <div class="desktop-item-management">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1 class="page-title">桌面项目管理</h1>
      <p class="page-subtitle">管理您的桌面快捷方式、文件夹和应用程序</p>
    </div>

    <!-- 操作栏 -->
    <div class="operation-bar">
      <div class="left-operations">
        <!-- 筛选器 -->
        <el-select v-model="typeFilter" placeholder="全部类型" class="type-filter" @change="handleTypeFilter">
          <el-option label="全部类型" value="all"></el-option>
          <el-option label="应用程序" value="application"></el-option>
          <el-option label="文件夹" value="folder"></el-option>
          <el-option label="文件" value="file"></el-option>
          <el-option label="网址" value="url"></el-option>
          <el-option label="其他" value="other"></el-option>
        </el-select>

        <!-- 搜索框 -->
        <el-input
          v-model="searchKeyword"
          placeholder="搜索桌面项目"
          :prefix-icon="Search"
          class="search-input"
          @input="handleSearch"
          clearable
        />
      </div>

      <div class="right-operations">
        <el-button type="primary" :icon="Plus" @click="handleAdd">添加项目</el-button>
        <el-button type="danger" :icon="Delete" @click="handleBatchDelete" :disabled="selectedItems.length === 0">
          批量删除
        </el-button>
      </div>
    </div>

    <!-- 项目列表 -->
    <div class="item-list">
      <el-table
        :data="filteredItems"
        v-loading="loading"
        element-loading-text="加载中..."
        @selection-change="handleSelectionChange"
        class="desktop-table"
      >
        <el-table-column type="selection" width="55" />
        
        <el-table-column label="图标" width="80" align="center">
          <template #default="{ row }">
            <div class="item-icon">
              <span v-if="row.icon">{{ row.icon }}</span>
              <span v-else>{{ getDefaultIcon(row.type) }}</span>
            </div>
          </template>
        </el-table-column>

        <el-table-column prop="name" label="项目名称" min-width="200">
          <template #default="{ row }">
            <div class="item-name">
              <span class="name-text">{{ row.name }}</span>
              <el-tag v-if="row.type" :type="getTypeTagType(row.type)" size="small">
                {{ getTypeDisplayName(row.type) }}
              </el-tag>
            </div>
          </template>
        </el-table-column>

        <el-table-column prop="path" label="路径" min-width="300">
          <template #default="{ row }">
            <div class="item-path">
              <el-tooltip :content="row.path" placement="top" :disabled="!row.path">
                <span class="path-text">{{ row.path || '无' }}</span>
              </el-tooltip>
            </div>
          </template>
        </el-table-column>

        <el-table-column prop="role" label="适用角色" width="120">
          <template #default="{ row }">
            <el-tag v-if="row.role" type="info" size="small">{{ row.role }}</el-tag>
            <span v-else class="no-data">无限制</span>
          </template>
        </el-table-column>

        <el-table-column label="位置" width="100" align="center">
          <template #default="{ row }">
            <span class="position-text">
              {{ row.position_x || 0 }}, {{ row.position_y || 0 }}
            </span>
          </template>
        </el-table-column>

        <el-table-column prop="created_at" label="创建时间" width="160">
          <template #default="{ row }">
            <span>{{ formatDateTime(row.created_at) }}</span>
          </template>
        </el-table-column>

        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button type="danger" size="small" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 添加/编辑弹窗 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="600px"
      @close="handleDialogClose"
    >
      <el-form
        ref="formRef"
        :model="formData"
        :rules="formRules"
        label-width="100px"
        class="desktop-form"
      >
        <el-form-item label="项目名称" prop="name">
          <el-input v-model="formData.name" placeholder="请输入项目名称" />
        </el-form-item>

        <el-form-item label="项目类型" prop="type">
          <el-select v-model="formData.type" placeholder="选择项目类型" class="full-width">
            <el-option label="应用程序" value="application"></el-option>
            <el-option label="文件夹" value="folder"></el-option>
            <el-option label="文件" value="file"></el-option>
            <el-option label="网址" value="url"></el-option>
            <el-option label="其他" value="other"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="路径" prop="path">
          <el-input
            v-model="formData.path"
            type="textarea"
            :rows="3"
            placeholder="请输入文件夹路径、应用程序路径或网址"
          />
          <div class="help-text">
            <p>示例：</p>
            <p>• 应用程序：C:\Program Files\Application\app.exe</p>
            <p>• 文件夹：D:\Documents\Projects</p>
            <p>• 网址：https://www.example.com</p>
          </div>
        </el-form-item>

        <el-form-item label="图标" prop="icon">
          <el-input v-model="formData.icon" placeholder="输入图标字符或Emoji" />
          <div class="icon-suggestions">
            <span class="suggestion-title">常用图标：</span>
            <el-button
              v-for="icon in iconSuggestions"
              :key="icon"
              @click="formData.icon = icon"
              size="small"
              text
            >
              {{ icon }}
            </el-button>
          </div>
        </el-form-item>

        <el-form-item label="适用角色">
          <el-input v-model="formData.role" placeholder="限制特定角色使用（可选）" />
        </el-form-item>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="X坐标">
              <el-input-number v-model="formData.position_x" :min="0" :max="2000" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="Y坐标">
              <el-input-number v-model="formData.position_y" :min="0" :max="2000" />
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit" :loading="submitting">
            {{ isEdit ? '更新' : '创建' }}
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { Search, Plus, Delete } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { desktopItemAPI, type DesktopItem } from '@/api/desktop'

// 响应式数据
const loading = ref(false)
const dialogVisible = ref(false)
const isEdit = ref(false)
const submitting = ref(false)
const typeFilter = ref('all')
const searchKeyword = ref('')
const selectedItems = ref<DesktopItem[]>([])
const items = ref<DesktopItem[]>([])

// 表单相关
const formRef = ref()
const formData = reactive<Partial<DesktopItem>>({
  name: '',
  type: 'application',
  path: '',
  icon: '',
  role: '',
  position_x: 0,
  position_y: 0
})

// 表单验证规则
const formRules = {
  name: [
    { required: true, message: '请输入项目名称', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择项目类型', trigger: 'change' }
  ],
  path: [
    { required: true, message: '请输入路径', trigger: 'blur' }
  ]
}

// 图标建议
const iconSuggestions = [
  '📁', '📂', '📄', '📋', '💻', '🖥️', '⚙️', '🔧', '🛠️', '🌐',
  '📊', '📈', '📉', '🎯', '⭐', '🔥', '✨', '🎨', '📱', '💡'
]

// 计算属性
const dialogTitle = computed(() => isEdit.value ? '编辑桌面项目' : '添加桌面项目')

const filteredItems = computed(() => {
  let filtered = [...items.value]
  
  // 类型筛选
  if (typeFilter.value !== 'all') {
    filtered = filtered.filter(item => item.type === typeFilter.value)
  }
  
  // 搜索筛选
  if (searchKeyword.value) {
    const keyword = searchKeyword.value.toLowerCase()
    filtered = filtered.filter(item =>
      item.name.toLowerCase().includes(keyword) ||
      (item.path && item.path.toLowerCase().includes(keyword)) ||
      (item.role && item.role.toLowerCase().includes(keyword))
    )
  }
  
  return filtered
})

// 生命周期
onMounted(() => {
  loadItems()
})

// 方法
const loadItems = async () => {
  try {
    loading.value = true
    const response = await desktopItemAPI.getItems()
    items.value = response
  } catch (error) {
    console.error('加载桌面项目失败:', error)
    ElMessage.error('加载桌面项目失败')
  } finally {
    loading.value = false
  }
}

const handleAdd = () => {
  isEdit.value = false
  resetForm()
  dialogVisible.value = true
}

const handleEdit = (item: DesktopItem) => {
  isEdit.value = true
  Object.assign(formData, item)
  dialogVisible.value = true
}

const handleDelete = async (item: DesktopItem) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除项目 "${item.name}" 吗？`,
      '确认删除',
      {
        confirmButtonText: '删除',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await desktopItemAPI.deleteItem(item.id as number)
    ElMessage.success('删除成功')
    loadItems()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
      ElMessage.error('删除失败')
    }
  }
}

const handleBatchDelete = async () => {
  if (selectedItems.value.length === 0) {
    ElMessage.warning('请选择要删除的项目')
    return
  }

  try {
    await ElMessageBox.confirm(
      `确定要删除选中的 ${selectedItems.value.length} 个项目吗？`,
      '确认批量删除',
      {
        confirmButtonText: '删除',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    for (const item of selectedItems.value) {
      await desktopItemAPI.deleteItem(item.id as number)
    }

    ElMessage.success('批量删除成功')
    selectedItems.value = []
    loadItems()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('批量删除失败:', error)
      ElMessage.error('批量删除失败')
    }
  }
}

const handleSubmit = async () => {
  try {
    await formRef.value.validate()
    submitting.value = true

    if (isEdit.value) {
      await desktopItemAPI.updateItem(formData.id as number, formData)
      ElMessage.success('更新成功')
    } else {
      await desktopItemAPI.createItem(formData as Omit<DesktopItem, 'id' | 'user_id' | 'created_at'>)
      ElMessage.success('创建成功')
    }

    dialogVisible.value = false
    loadItems()
  } catch (error) {
    console.error('保存失败:', error)
    ElMessage.error('保存失败')
  } finally {
    submitting.value = false
  }
}

const handleSelectionChange = (selection: DesktopItem[]) => {
  selectedItems.value = selection
}

const handleDialogClose = () => {
  resetForm()
}

const resetForm = () => {
  Object.assign(formData, {
    name: '',
    type: 'application',
    path: '',
    icon: '',
    role: '',
    position_x: 0,
    position_y: 0
  })
  formRef.value?.clearValidate()
}

const handleTypeFilter = () => {
  // 类型筛选变化时重置选择
  selectedItems.value = []
}

const handleSearch = () => {
  // 搜索时重置选择
  selectedItems.value = []
}

// 工具方法
const getDefaultIcon = (type?: string) => {
  const iconMap: Record<string, string> = {
    application: '💻',
    folder: '📁',
    file: '📄',
    url: '🌐',
    other: '⚙️'
  }
  return iconMap[type || ''] || '📄'
}

const getTypeDisplayName = (type: string) => {
  const nameMap: Record<string, string> = {
    application: '应用程序',
    folder: '文件夹',
    file: '文件',
    url: '网址',
    other: '其他'
  }
  return nameMap[type] || type
}

const getTypeTagType = (type: string) => {
  const typeMap: Record<string, string> = {
    application: 'primary',
    folder: 'success',
    file: 'info',
    url: 'warning',
    other: ''
  }
  return typeMap[type] || ''
}

const formatDateTime = (dateTime?: string) => {
  if (!dateTime) return '未知'
  return new Date(dateTime).toLocaleString('zh-CN')
}
</script>

<style scoped>
.desktop-item-management {
  padding: 20px;
  background: #f5f7fa;
  min-height: 100vh;
}

.page-header {
  margin-bottom: 20px;
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin: 0 0 8px 0;
}

.page-subtitle {
  color: #666;
  margin: 0;
  font-size: 14px;
}

.operation-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 16px 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.left-operations {
  display: flex;
  gap: 16px;
  align-items: center;
}

.right-operations {
  display: flex;
  gap: 12px;
}

.type-filter {
  width: 120px;
}

.search-input {
  width: 300px;
}

.item-list {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.desktop-table {
  width: 100%;
}

.item-icon {
  font-size: 20px;
  text-align: center;
}

.item-name {
  display: flex;
  align-items: center;
  gap: 8px;
}

.name-text {
  font-weight: 500;
}

.item-path {
  max-width: 300px;
}

.path-text {
  display: block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: #666;
  font-family: monospace;
  font-size: 12px;
}

.position-text {
  font-family: monospace;
  font-size: 12px;
  color: #666;
}

.no-data {
  color: #999;
  font-size: 12px;
}

.desktop-form {
  padding: 0 20px;
}

.full-width {
  width: 100%;
}

.help-text {
  margin-top: 8px;
  font-size: 12px;
  color: #666;
  line-height: 1.4;
}

.help-text p {
  margin: 4px 0;
}

.icon-suggestions {
  margin-top: 8px;
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.suggestion-title {
  font-size: 12px;
  color: #666;
}

.dialog-footer {
  text-align: right;
}

:deep(.el-table) {
  border-radius: 0;
}

:deep(.el-table th) {
  background-color: #fafafa;
  color: #333;
  font-weight: 600;
}

:deep(.el-table td) {
  border-bottom: 1px solid #f0f0f0;
}

:deep(.el-table--border) {
  border: none;
}

:deep(.el-table--border::after) {
  display: none;
}

:deep(.el-table::before) {
  display: none;
}
</style> 