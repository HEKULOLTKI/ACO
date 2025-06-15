<template>
  <div class="task-management">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>任务管理</span>
          <div class="header-actions">
            <el-button type="primary" @click="handleBulkImport">
              <el-icon><Upload /></el-icon>
              批量导入任务
            </el-button>
            <el-button type="primary" @click="handleAdd">
              <el-icon><Plus /></el-icon>
              新增任务
            </el-button>
          </div>
        </div>
      </template>

      <!-- 搜索栏 -->
      <div class="search-bar">
        <el-form :model="searchForm" inline>
          <el-form-item label="任务名称">
            <el-input 
              v-model="searchForm.name" 
              placeholder="请输入任务名称"
              clearable
            />
          </el-form-item>
          <el-form-item label="任务类型">
            <el-select v-model="searchForm.type" placeholder="选择任务类型" clearable>
              <el-option label="网络搭建任务" value="网络搭建任务" />
              <el-option label="系统构建任务" value="系统构建任务" />
              <el-option label="运维监管任务" value="运维监管任务" />
              <el-option label="日志安全任务" value="日志安全任务" />
            </el-select>
          </el-form-item>
          <el-form-item label="阶段">
            <el-select v-model="searchForm.phase" placeholder="选择任务阶段" clearable>
              <el-option label="计划阶段" value="计划阶段" />
              <el-option label="执行阶段" value="执行阶段" />
              <el-option label="验收阶段" value="验收阶段" />
              <el-option label="完成阶段" value="完成阶段" />
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

      <!-- 任务表格 -->
      <el-table :data="tasks" v-loading="loading" style="width: 100%">
        <el-table-column prop="id" label="任务ID" width="80" />
        <el-table-column prop="name" label="任务名称" min-width="120" />
        <el-table-column prop="type" label="任务类型" width="120" />
        <el-table-column prop="phase" label="阶段" width="100" />
        <el-table-column prop="description" label="任务描述" show-overflow-tooltip min-width="150" />
        <el-table-column label="执行人" width="120">
          <template #default="scope">
            <span v-if="scope.row.assignments && scope.row.assignments.length > 0">
              {{ scope.row.assignments.map((a: any) => a.username).join(', ') }}
            </span>
            <el-tag v-else type="info" size="small">未分配</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="create_time" label="创建时间" width="150" />
        <el-table-column prop="update_time" label="更新时间" width="150" />
        <el-table-column label="操作" width="160" fixed="right">
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

    <!-- 任务编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑任务' : '新增任务'"
      width="700px"
    >
      <el-form
        ref="formRef"
        :model="taskForm"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="任务名称" prop="name">
          <el-input v-model="taskForm.name" placeholder="请输入任务名称" />
        </el-form-item>
        <el-form-item label="任务类型" prop="type">
          <el-select v-model="taskForm.type" placeholder="选择任务类型">
            <el-option label="网络搭建任务" value="网络搭建任务" />
            <el-option label="系统构建任务" value="系统构建任务" />
            <el-option label="运维监管任务" value="运维监管任务" />
            <el-option label="日志安全任务" value="日志安全任务" />
          </el-select>
        </el-form-item>
        <el-form-item label="阶段" prop="phase">
          <el-select v-model="taskForm.phase" placeholder="选择任务阶段">
            <el-option label="计划阶段" value="计划阶段" />
            <el-option label="执行阶段" value="执行阶段" />
            <el-option label="验收阶段" value="验收阶段" />
            <el-option label="完成阶段" value="完成阶段" />
          </el-select>
        </el-form-item>
        <el-form-item label="任务描述" prop="description">
          <el-input 
            v-model="taskForm.description" 
            type="textarea"
            :rows="4"
            placeholder="请输入任务描述" 
          />
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

    <!-- 批量导入任务对话框 -->
    <el-dialog
      v-model="bulkImportVisible"
      title="批量导入任务"
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
                  请选择要导入的Excel或CSV文件，支持xls、xlsx、csv格式
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
          <p>下载标准的任务导入模板，包含任务名称、任务类型、阶段、任务描述等字段。</p>
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
            <span>成功导入 {{ importResult.success_count }} 个任务</span>
          </div>
          <div v-if="importResult.fail_count > 0" class="fail-info">
            <el-icon color="#F56C6C"><CircleCloseFilled /></el-icon>
            <span>失败 {{ importResult.fail_count }} 个任务</span>
          </div>
        </div>
        
        <div v-if="importResult.failed_tasks.length > 0" class="failed-list">
          <h4>失败列表：</h4>
          <el-table :data="importResult.failed_tasks" style="width: 100%">
            <el-table-column prop="name" label="任务名称" />
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
import { getTasks, getTasksCount, createTask, updateTask, deleteTask, getTask, bulkImportTasks, type TaskBulkImportResult } from '@/api/task'

interface Task {
  id: number
  name: string
  type: string
  phase: string
  description: string
  create_time: string
  update_time: string
  assignments?: any[]
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
  name: '',
  type: '',
  phase: ''
})

const taskForm = reactive({
  id: 0,
  name: '',
  type: '',
  phase: '',
  description: ''
})

const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 0
})

const tasks = ref<Task[]>([])

const importResult = reactive<TaskBulkImportResult>({
  success_count: 0,
  fail_count: 0,
  failed_tasks: [],
  message: ''
})

const rules = {
  name: [
    { required: true, message: '请输入任务名称', trigger: 'blur' },
    { min: 2, max: 50, message: '任务名称长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择任务类型', trigger: 'change' }
  ],
  phase: [
    { required: true, message: '请选择任务阶段', trigger: 'change' }
  ],
  description: [
    { required: true, message: '请输入任务描述', trigger: 'blur' },
    { min: 5, max: 500, message: '任务描述长度在 5 到 500 个字符', trigger: 'blur' }
  ]
}

const loadTasks = async () => {
  loading.value = true
  try {
    const response = await getTasks({
      skip: (pagination.currentPage - 1) * pagination.pageSize,
      limit: pagination.pageSize,
      task_type: searchForm.type || undefined
    })
    
    // 直接使用任务数据，不获取分配信息
    tasks.value = response.data || []
    
    // 获取总数
    const countResponse = await getTasksCount({
      task_type: searchForm.type || undefined
    })
    pagination.total = countResponse.data?.count || 0
  } catch (error) {
    ElMessage.error('加载任务列表失败')
    console.error('加载任务失败:', error)
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  pagination.currentPage = 1
  loadTasks()
}

const handleReset = () => {
  searchForm.name = ''
  searchForm.type = ''
  searchForm.phase = ''
  pagination.currentPage = 1
  loadTasks()
}

const handleAdd = () => {
  isEdit.value = false
  dialogVisible.value = true
  resetForm()
}

const handleEdit = (row: Task) => {
  isEdit.value = true
  dialogVisible.value = true
  Object.assign(taskForm, row)
}

const handleDelete = async (row: Task) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除任务 "${row.name}" 吗？`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    await deleteTask(row.id)
    ElMessage.success('删除成功')
    loadTasks()
  } catch (error: any) {
    if (error?.message !== 'cancel') {
      ElMessage.error('删除失败')
      console.error('删除任务失败:', error)
    }
  }
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    
    if (isEdit.value) {
      await updateTask(taskForm.id, {
        name: taskForm.name,
        type: taskForm.type,
        phase: taskForm.phase,
        description: taskForm.description
      })
    } else {
      await createTask({
        name: taskForm.name,
        type: taskForm.type,
        phase: taskForm.phase,
        description: taskForm.description,
        status: '未分配'
      })
    }
    
    ElMessage.success(isEdit.value ? '更新成功' : '创建成功')
    dialogVisible.value = false
    loadTasks()
  } catch (error: any) {
    ElMessage.error(isEdit.value ? '更新失败' : '创建失败')
    console.error('保存任务失败:', error)
  }
}

const resetForm = () => {
  taskForm.id = 0
  taskForm.name = ''
  taskForm.type = ''
  taskForm.phase = ''
  taskForm.description = ''
}

const handleSizeChange = (val: number) => {
  pagination.pageSize = val
  pagination.currentPage = 1
  loadTasks()
}

const handleCurrentChange = (val: number) => {
  pagination.currentPage = val
  loadTasks()
}

// 批量导入相关方法
const handleBulkImport = () => {
  bulkImportVisible.value = true
  selectedFile.value = null
}

const downloadTemplate = async () => {
  downloadLoading.value = true
  try {
    // 创建CSV内容，包含标题行和示例数据
    const csvData = [
      ['任务名称', '任务类型', '阶段', '任务描述'],
              ['网络架构设计', '网络搭建任务', '计划阶段', '设计企业网络拓扑结构和配置方案'],
        ['服务器环境搭建', '系统构建任务', '执行阶段', '搭建生产环境服务器和应用系统'],
        ['监控系统配置', '运维监管任务', '配置阶段', '配置系统监控和告警机制'],
        ['日志安全审计', '日志安全任务', '监控阶段', '分析系统日志并识别安全威胁']
    ]
    
    // 将数组转换为CSV格式字符串
    const csvContent = csvData.map(row => 
      row.map(field => `"${field.replace(/"/g, '""')}"`).join(',')
    ).join('\n')
    
    // 添加BOM头，确保中文正确显示
    const BOM = '\uFEFF'
    const blob = new Blob([BOM + csvContent], { 
      type: 'text/csv;charset=utf-8;' 
    })
    
    // 创建下载链接
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = '任务导入模板.csv'
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
    ElMessage.error('下载模板失败')
  } finally {
    downloadLoading.value = false
  }
}

const beforeUpload = (file: File) => {
  const isExcel = file.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' || 
                  file.type === 'application/vnd.ms-excel' ||
                  file.type === 'text/csv'
  if (!isExcel) {
    ElMessage.error('只能上传Excel或CSV文件!')
    return false
  }
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
  }
}

const clearFile = () => {
  selectedFile.value = null
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
    const response = await bulkImportTasks(selectedFile.value)
    
    // 处理导入结果
    if (response.data) {
      Object.assign(importResult, response.data)
      bulkImportVisible.value = false
      resultVisible.value = true
      
      // 显示导入成功消息
      if (importResult.success_count > 0) {
        ElMessage.success(`成功导入 ${importResult.success_count} 个任务`)
      }
      
      // 刷新任务列表
      await loadTasks()
    } else {
      ElMessage.error('导入失败：响应数据格式错误')
    }
  } catch (error: any) {
    console.error('批量导入失败:', error)
    const errorMsg = error?.response?.data?.detail || error?.message || '批量导入失败'
    ElMessage.error(errorMsg)
  } finally {
    importLoading.value = false
  }
}

onMounted(() => {
  loadTasks()
})
</script>

<style scoped lang="scss">
.task-management {
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