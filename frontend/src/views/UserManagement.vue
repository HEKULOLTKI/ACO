<template>
  <div class="user-management">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>用户管理</span>
          <div class="header-actions">
            <el-button type="primary" @click="handleBulkImport">
              <el-icon><Upload /></el-icon>
              批量导入用户
            </el-button>
            <el-button type="primary" @click="handleAdd">
              <el-icon><Plus /></el-icon>
              新增用户
            </el-button>
          </div>
        </div>
      </template>

      <!-- 搜索栏 -->
      <div class="search-bar">
        <el-form :model="searchForm" inline>
          <el-form-item label="用户名">
            <el-input 
              v-model="searchForm.username" 
              placeholder="请输入用户名"
              clearable
            />
          </el-form-item>
          <el-form-item label="角色">
            <el-select v-model="searchForm.role" placeholder="选择角色" clearable>
              <el-option label="网络工程师" value="网络工程师" />
              <el-option label="系统架构师" value="系统架构师" />
              <el-option label="系统规划与管理师" value="系统规划与管理师" />
              <el-option label="系统分析师" value="系统分析师" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">
              <el-icon><Search /></el-icon>
              搜索
            </el-button>
            <el-button @click="handleReset">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <!-- 用户表格 -->
      <el-table :data="users" v-loading="loading" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="username" label="用户名" />
        <el-table-column prop="role" label="角色">
          <template #default="scope">
            <el-tag :type="getRoleType(scope.row.role)">
              {{ getRoleText(scope.row.role) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="type" label="类型" />
        <el-table-column prop="status" label="状态">
          <template #default="scope">
            <el-tag :type="scope.row.status === 'active' ? 'success' : 'danger'">
              {{ scope.row.status === 'active' ? '激活' : '未激活' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="照片已上传" width="120">
          <template #default="scope">
            <el-tag :type="scope.row.photo_data ? 'success' : 'info'" size="small">
              {{ scope.row.photo_data ? '已上传' : '未上传' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" />
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button size="small" @click="handleEdit(scope.row)">
              编辑
            </el-button>
            <el-button 
              size="small" 
              type="danger" 
              @click="handleDelete(scope.row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          v-model:current-page="pagination.currentPage"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="pagination.total"
          layout="sizes, prev, pager, next, jumper, total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 新增/编辑用户对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑用户' : '创建新用户'"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="formRef"
        :model="userForm"
        :rules="rules"
        label-width="80px"
        label-position="left"
      >
        <el-form-item label="用户名" prop="username">
          <el-input 
            v-model="userForm.username" 
            placeholder="请输入用户名"
            :disabled="isEdit"
          />
        </el-form-item>
        <el-form-item label="密码" prop="password" v-if="!isEdit">
          <el-input 
            v-model="userForm.password" 
            type="password" 
            placeholder="请输入密码"
            show-password
          />
        </el-form-item>
        <el-form-item label="角色" prop="role">
          <el-select v-model="userForm.role" placeholder="选择角色" style="width: 100%">
            <el-option label="网络工程师" value="网络工程师" />
            <el-option label="系统架构师" value="系统架构师" />
            <el-option label="系统规划与管理师" value="系统规划与管理师" />
            <el-option label="系统分析师" value="系统分析师" />
          </el-select>
        </el-form-item>
        <el-form-item label="类型" prop="type">
          <el-select v-model="userForm.type" placeholder="选择用户类型" style="width: 100%">
            <el-option label="管理员" value="管理员" />
            <el-option label="普通用户" value="操作员" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="userForm.status" placeholder="选择状态" style="width: 100%">
            <el-option label="激活" value="active" />
            <el-option label="未激活" value="inactive" />
          </el-select>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">
            确定
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 批量导入用户对话框 -->
    <el-dialog
      v-model="bulkImportVisible"
      title="批量导入用户"
      width="600px"
      :close-on-click-modal="false"
    >
      <div class="import-content">
        <div class="upload-section">
          <div class="upload-header">
            <span>选择导入文件</span>
            <el-button 
              type="text" 
              @click="downloadTemplate"
              :loading="downloadLoading"
            >
              <el-icon><Download /></el-icon>
              下载导入模板
            </el-button>
          </div>
          <el-upload
            class="upload-area"
            drag
            :auto-upload="false"
            :show-file-list="false"
            :before-upload="beforeUpload"
            accept=".xlsx,.xls,.csv"
            @change="handleFileChange"
          >
            <div class="upload-content">
              <el-icon class="upload-icon"><Plus /></el-icon>
              <div class="upload-text">
                <div class="main-text">添加文件</div>
                <div class="sub-text">
                  请选择要导入的Excel或CSV文件，支持.xls、.xlsx、.csv格式
                </div>
              </div>
            </div>
          </el-upload>
          
          <div v-if="selectedFile" class="file-info">
            <div class="file-name">
              <el-icon><Document /></el-icon>
              {{ selectedFile.name }}
            </div>
            <el-button 
              type="text" 
              @click="clearFile"
              class="clear-btn"
            >
              <el-icon><Delete /></el-icon>
              清除选择
            </el-button>
          </div>
          
          <div v-if="!selectedFile" class="no-file-tips">
            尚未选择文件
          </div>
        </div>
        
        <div class="template-tips">
          <p>下载标准的用户导入模板，包含用户名、密码、角色、用户类型、状态等字段。请使用下载的模板格式填写用户信息。支持Excel(.xlsx)和CSV(.csv)格式。</p>
        </div>
      </div>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="bulkImportVisible = false">取消</el-button>
          <el-button 
            type="primary" 
            @click="handleImport"
            :loading="importLoading"
            :disabled="!selectedFile"
          >
            导入
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 导入结果对话框 -->
    <el-dialog
      v-model="resultVisible"
      title="导入结果"
      width="600px"
    >
      <div class="import-result">
        <div class="result-summary">
          <div class="success-info">
            <el-icon color="#67C23A"><SuccessFilled /></el-icon>
            <span>成功导入 {{ importResult.success_count }} 个用户</span>
          </div>
          <div v-if="importResult.fail_count > 0" class="fail-info">
            <el-icon color="#F56C6C"><CircleCloseFilled /></el-icon>
            <span>失败 {{ importResult.fail_count }} 个用户</span>
          </div>
        </div>
        
        <div v-if="importResult.failed_users.length > 0" class="failed-list">
          <h4>失败列表：</h4>
          <el-table :data="importResult.failed_users" style="width: 100%">
            <el-table-column prop="username" label="用户名" />
            <el-table-column prop="error" label="失败原因" />
          </el-table>
        </div>
      </div>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button type="primary" @click="resultVisible = false">
            确定
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type UploadFile } from 'element-plus'
import { 
  Plus, Search, Upload, Download, Document, Delete, 
  SuccessFilled, CircleCloseFilled 
} from '@element-plus/icons-vue'
import { 
  getUserList, createUser, updateUser, deleteUser, 
  bulkImportUsers, downloadUserTemplate 
} from '@/api/user'
import type { UserForm, UserUpdate, BulkImportResult } from '@/types/user'

interface User {
  id: number
  username: string
  role: string
  type: string
  status: string
  created_at: string
  updated_at: string
}

const loading = ref(false)
const dialogVisible = ref(false)
const bulkImportVisible = ref(false)
const resultVisible = ref(false)
const isEdit = ref(false)
const formRef = ref<FormInstance>()
const downloadLoading = ref(false)
const importLoading = ref(false)
const selectedFile = ref<File | null>(null)

const searchForm = reactive({
  username: '',
  role: ''
})

const userForm = reactive({
  id: 0,
  username: '',
  password: '',
  role: '',
  type: '',
  status: 'active'
})

const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 0
})

const importResult = reactive<BulkImportResult>({
  success_count: 0,
  fail_count: 0,
  failed_users: [],
  message: ''
})

const users = ref<User[]>([])

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度在 6 到 20 个字符', trigger: 'blur' }
  ],
  role: [
    { required: true, message: '请选择角色', trigger: 'change' }
  ],
  type: [
    { required: true, message: '请选择用户类型', trigger: 'change' }
  ],
  status: [
    { required: true, message: '请选择状态', trigger: 'change' }
  ]
}

const getRoleType = (role: string) => {
  switch (role) {
    case '网络工程师':
      return 'primary'
    case '系统架构师':
      return 'success'
    case '系统规划与管理师':
      return 'warning'
    case '系统分析师':
      return 'info'
    default:
      return ''
  }
}

const getRoleText = (role: string) => {
  return role
}

const loadUsers = async () => {
  loading.value = true
  try {
    const params = {
      skip: (pagination.currentPage - 1) * pagination.pageSize,
      limit: pagination.pageSize,
      role: searchForm.role || undefined,
      user_type: undefined
    }
    
    const response = await getUserList(params)
    users.value = response.data || []
    pagination.total = users.value.length
  } catch (error) {
    console.error('加载用户列表失败:', error)
    ElMessage.error('加载用户列表失败')
    users.value = [
      {
        id: 1,
        username: 'admin',
        role: '系统架构师',
        type: '管理员',
        status: 'active',
        created_at: '2024-01-15 10:30',
        updated_at: '2024-01-15 10:30'
      },
      {
        id: 2,
        username: 'operator1',
        role: '网络工程师',
        type: '操作员',
        status: 'active',
        created_at: '2024-01-14 14:20',
        updated_at: '2024-01-14 14:20'
      }
    ]
    pagination.total = users.value.length
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  loadUsers()
}

const handleReset = () => {
  searchForm.username = ''
  searchForm.role = ''
  loadUsers()
}

const handleAdd = () => {
  isEdit.value = false
  dialogVisible.value = true
  resetForm()
}

const handleEdit = (row: User) => {
  isEdit.value = true
  dialogVisible.value = true
  Object.assign(userForm, row)
}

const handleDelete = async (row: User) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除用户 "${row.username}" 吗？`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    await deleteUser(row.id)
    ElMessage.success('删除成功')
    loadUsers()
  } catch (error: any) {
    if (error === 'cancel') {
      return
    }
    console.error('删除用户失败:', error)
    const message = error?.response?.data?.detail || '删除失败'
    ElMessage.error(message)
  }
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    
    if (isEdit.value) {
      const updateData: UserUpdate = {
        role: userForm.role,
        type: userForm.type,
        status: userForm.status
      }
      await updateUser(userForm.id, updateData)
      ElMessage.success('更新成功')
    } else {
      const createData: UserForm = {
        username: userForm.username,
        password: userForm.password,
        role: userForm.role,
        type: userForm.type,
        status: userForm.status
      }
      await createUser(createData)
      ElMessage.success('创建成功')
    }
    
    dialogVisible.value = false
    loadUsers()
  } catch (error: any) {
    console.error('操作失败:', error)
    const message = error?.response?.data?.detail || (isEdit.value ? '更新失败' : '创建失败')
    ElMessage.error(message)
  }
}

const resetForm = () => {
  userForm.id = 0
  userForm.username = ''
  userForm.password = ''
  userForm.role = ''
  userForm.type = ''
  userForm.status = 'active'
}

const handleSizeChange = (val: number) => {
  pagination.pageSize = val
  loadUsers()
}

const handleCurrentChange = (val: number) => {
  pagination.currentPage = val
  loadUsers()
}

// 批量导入相关方法
const handleBulkImport = () => {
  bulkImportVisible.value = true
  selectedFile.value = null
}

const downloadTemplate = async () => {
  downloadLoading.value = true
  try {
    // 使用API下载模板
    const response = await downloadUserTemplate()
    
    // 创建下载链接
    const blob = new Blob([response.data], { 
      type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' 
    })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = '用户导入模板.xlsx'
    link.style.display = 'none'
    
    // 添加到页面并触发下载
    document.body.appendChild(link)
    link.click()
    
    // 清理
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    
    ElMessage.success('模板下载成功')
  } catch (error) {
    console.error('下载模板失败:', error)
    
    // 如果API不可用，使用本地生成的备选方案
    try {
      // 创建Excel工作簿数据 - 列名必须与后端期望的完全一致
      const excelData = [
        ['用户名', '密码', '角色', '用户类型', '状态'],
        ['zhang_san', '123456', '网络工程师', '操作员', 'active'],
        ['li_si', '123456', '系统架构师', '管理员', 'active'],
        ['wang_wu', '123456', '系统规划与管理师', '操作员', 'inactive'],
        ['zhao_liu', '123456', '系统分析师', '操作员', 'active']
      ]
      
      // 创建CSV格式内容（作为备选方案）
      const csvContent = excelData.map(row => 
        row.map(field => `"${field.replace(/"/g, '""')}"`).join(',')
      ).join('\n')
      
      // 创建Blob对象，使用CSV格式
      const blob = new Blob(['\ufeff' + csvContent], { 
        type: 'text/csv;charset=utf-8' 
      })
      
      // 创建下载链接
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = '用户导入模板.csv'
      link.style.display = 'none'
      
      // 添加到页面并触发下载
      document.body.appendChild(link)
      link.click()
      
      // 清理
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)
      
      ElMessage.success('CSV模板下载成功（备选方案）')
    } catch (fallbackError) {
      console.error('备选方案也失败:', fallbackError)
      ElMessage.error('下载模板失败，请联系管理员')
    }
  } finally {
    downloadLoading.value = false
  }
}

const beforeUpload = (file: File) => {
  // 检查文件类型
  const isValidFile = file.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' || 
                      file.type === 'application/vnd.ms-excel' ||
                      file.type === 'text/csv' ||
                      file.name.endsWith('.xlsx') ||
                      file.name.endsWith('.xls') ||
                      file.name.endsWith('.csv')
  
  if (!isValidFile) {
    ElMessage.error('只能上传Excel或CSV文件(.xlsx, .xls, .csv)!')
    return false
  }
  
  // 检查文件大小
  const isLt10M = file.size / 1024 / 1024 < 10
  if (!isLt10M) {
    ElMessage.error('文件大小不能超过10MB!')
    return false
  }
  
  return false // 阻止自动上传
}

const handleFileChange = (file: UploadFile) => {
  if (file.raw) {
    selectedFile.value = file.raw
    ElMessage.success(`已选择文件: ${file.name}`)
  }
}

const clearFile = () => {
  selectedFile.value = null
  ElMessage.info('已清除文件选择')
}

const handleImport = async () => {
  if (!selectedFile.value) {
    ElMessage.error('请选择要导入的文件')
    return
  }
  
  // 再次验证文件类型
  const isValidFile = selectedFile.value.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' || 
                      selectedFile.value.type === 'application/vnd.ms-excel' ||
                      selectedFile.value.type === 'text/csv' ||
                      selectedFile.value.name.endsWith('.xlsx') ||
                      selectedFile.value.name.endsWith('.xls') ||
                      selectedFile.value.name.endsWith('.csv')
  
  if (!isValidFile) {
    ElMessage.error('请选择正确的Excel或CSV文件格式')
    return
  }
  
  // 验证文件大小
  if (selectedFile.value.size > 10 * 1024 * 1024) {
    ElMessage.error('文件大小不能超过10MB')
    return
  }
  
  console.log('开始导入文件:', {
    name: selectedFile.value.name,
    size: selectedFile.value.size,
    type: selectedFile.value.type
  })
  
  importLoading.value = true
  try {
    const response = await bulkImportUsers(selectedFile.value)
    
    // 处理导入结果
    if (response.data) {
      Object.assign(importResult, response.data)
      bulkImportVisible.value = false
      resultVisible.value = true
      
      // 显示导入成功消息
      if (importResult.success_count > 0) {
        ElMessage.success(`成功导入 ${importResult.success_count} 个用户`)
      }
      
      // 刷新用户列表
      await loadUsers()
    } else {
      ElMessage.error('导入失败：响应数据格式错误')
    }
  } catch (error: any) {
    console.error('批量导入失败:', error)
    console.error('错误详情:', {
      response: error?.response,
      message: error?.message,
      status: error?.response?.status
    })
    
    // 更详细的错误处理
    let errorMessage = '批量导入失败'
    if (error?.response?.data?.detail) {
      errorMessage = error.response.data.detail
    } else if (error?.response?.data?.message) {
      errorMessage = error.response.data.message
    } else if (error?.message) {
      errorMessage = error.message
    }
    
    ElMessage.error(errorMessage)
    
    // 根据不同的错误类型给出不同的建议
    if (errorMessage.includes('zip') || errorMessage.includes('格式错误')) {
      ElMessage.info('建议：请重新下载模板，确保使用最新的Excel模板格式')
    } else if (errorMessage.includes('缺少必要列')) {
      ElMessage.info('建议：请检查Excel表头是否包含：用户名、密码、角色、用户类型、状态')
    } else if (errorMessage.includes('数据行都无效')) {
      ElMessage.info('建议：请检查数据行是否填写完整，不能有空白字段')
    }
  } finally {
    importLoading.value = false
  }
}

onMounted(() => {
  loadUsers()
})
</script>

<style scoped lang="scss">
.user-management {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    
    .header-actions {
      display: flex;
      gap: 10px;
    }
  }

  .search-bar {
    margin-bottom: 20px;
    padding: 20px;
    background: #f5f5f5;
    border-radius: 4px;
  }

  .pagination {
    margin-top: 20px;
    text-align: right;
  }
}

.import-content {
  .upload-section {
    margin-bottom: 20px;
    
    .upload-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 15px;
      
      span {
        font-weight: 500;
        color: #303133;
      }
    }
    
    .upload-area {
      :deep(.el-upload-dragger) {
        width: 100%;
        height: 120px;
        border: 2px dashed #d9d9d9;
        border-radius: 6px;
        cursor: pointer;
        position: relative;
        overflow: hidden;
        transition: border-color 0.2s cubic-bezier(0.645, 0.045, 0.355, 1);
        
        &:hover {
          border-color: #409eff;
        }
      }
    }
    
    .upload-content {
      display: flex;
      align-items: center;
      justify-content: center;
      height: 100%;
      
      .upload-icon {
        font-size: 28px;
        color: #8c939d;
        margin-right: 16px;
      }
      
      .upload-text {
        .main-text {
          color: #606266;
          font-size: 14px;
          text-align: center;
        }
        
        .sub-text {
          color: #909399;
          font-size: 12px;
          margin-top: 2px;
          text-align: center;
        }
      }
    }
    
    .file-info {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 10px;
      background: #f0f9ff;
      border: 1px solid #b3d8ff;
      border-radius: 4px;
      margin-top: 10px;
      
      .file-name {
        display: flex;
        align-items: center;
        color: #409eff;
        font-size: 14px;
        
        .el-icon {
          margin-right: 5px;
        }
      }
      
      .clear-btn {
        color: #f56c6c;
        font-size: 12px;
      }
    }
    
    .no-file-tips {
      text-align: center;
      color: #909399;
      font-size: 12px;
      margin-top: 10px;
    }
  }
  
  .template-tips {
    padding: 12px;
    background: #f0f9ff;
    border-left: 4px solid #409eff;
    border-radius: 4px;
    
    p {
      margin: 0;
      color: #409eff;
      font-size: 13px;
      line-height: 1.5;
    }
  }
}

.import-result {
  .result-summary {
    display: flex;
    gap: 20px;
    margin-bottom: 20px;
    
    .success-info,
    .fail-info {
      display: flex;
      align-items: center;
      
      .el-icon {
        margin-right: 8px;
        font-size: 16px;
      }
      
      span {
        font-size: 14px;
      }
    }
    
    .success-info span {
      color: #67C23A;
    }
    
    .fail-info span {
      color: #F56C6C;
    }
  }
  
  .failed-list {
    h4 {
      margin: 0 0 10px 0;
      color: #303133;
      font-size: 14px;
    }
  }
}
</style> 