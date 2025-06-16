<template>
  <div class="device-management">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>设备管理</span>
          <div class="header-actions">
            <el-button type="primary" @click="handleBatchImport">
              <el-icon><Upload /></el-icon>
              批量导入设备
            </el-button>
            <el-button type="primary" @click="handleAdd">
              <el-icon><Plus /></el-icon>
              新增设备
            </el-button>
          </div>
        </div>
      </template>

      <!-- 搜索栏 -->
      <div class="search-bar">
        <el-form :model="searchForm" inline>
          <el-form-item label="设备名称">
            <el-input 
              v-model="searchForm.name" 
              placeholder="请输入设备名称"
              clearable
            />
          </el-form-item>
          <el-form-item label="状态">
            <el-select v-model="searchForm.status" placeholder="选择状态" clearable>
              <el-option 
                v-for="option in DEVICE_STATUS_OPTIONS" 
                :key="option.value"
                :label="option.label" 
                :value="option.value" 
              />
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

      <!-- 设备表格 -->
      <el-table :data="devices" v-loading="loading" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="设备名称" />
        <el-table-column prop="type" label="设备类型" />
        <el-table-column prop="ip" label="IP地址" />
        <el-table-column prop="status" label="状态">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              <el-icon style="margin-right: 4px;">
                <component :is="getStatusIcon(scope.row.status)" />
              </el-icon>
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="location" label="位置" />
        <el-table-column label="操作" width="300">
          <template #default="scope">
            <el-button size="small" @click="handleViewDetail(scope.row)">
              详情
            </el-button>
            <el-button 
              size="small" 
              :type="scope.row.status === 'online' ? 'warning' : 'success'"
              @click="handleToggleStatus(scope.row)"
            >
              {{ scope.row.status === 'online' ? '停用' : '启用' }}
            </el-button>
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

    <!-- 设备编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑设备' : '新增设备'"
      width="600px"
    >
      <el-form
        ref="formRef"
        :model="deviceForm"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="设备名称" prop="name">
          <el-input v-model="deviceForm.name" placeholder="请输入设备名称" />
        </el-form-item>
        <el-form-item label="设备类型" prop="type">
          <el-select v-model="deviceForm.type" placeholder="选择设备类型">
            <el-option 
              v-for="option in DEVICE_TYPE_OPTIONS" 
              :key="option.value"
              :label="option.label" 
              :value="option.value" 
            />
          </el-select>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="deviceForm.status" placeholder="选择状态">
            <el-option 
              v-for="option in DEVICE_STATUS_OPTIONS" 
              :key="option.value"
              :label="option.label" 
              :value="option.value" 
            />
          </el-select>
        </el-form-item>
        <el-form-item label="IP地址" prop="ip">
          <el-input v-model="deviceForm.ip" placeholder="请输入设备IP地址" />
        </el-form-item>
        <el-form-item label="位置" prop="location">
          <el-input v-model="deviceForm.location" placeholder="请输入设备位置" />
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

    <!-- 批量导入设备对话框 -->
    <el-dialog
      v-model="importDialogVisible"
      title="批量导入设备"
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
          <p>下载标准的设备导入模板，包含设备名称、设备类型、设备IP、状态、位置等字段。</p>
        </div>
      </div>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="importDialogVisible = false">取消</el-button>
          <el-button 
            type="primary" 
            @click="handleImportSubmit"
            :loading="importing"
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
            <span>成功导入 {{ importResult.success_count }} 个设备</span>
          </div>
          <div v-if="importResult.failure_count > 0" class="fail-info">
            <el-icon color="#F56C6C"><CircleCloseFilled /></el-icon>
            <span>失败 {{ importResult.failure_count }} 个设备</span>
          </div>
        </div>
        
        <div v-if="importResult.failure_details.length > 0" class="failed-list">
          <h4>失败列表：</h4>
          <el-table :data="importResult.failure_details" style="width: 100%">
            <el-table-column prop="row" label="行号" width="80" />
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

    <!-- 设备详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="设备详情"
      width="800px"
    >
      <div v-if="currentDevice" class="device-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="设备ID">{{ currentDevice.id }}</el-descriptions-item>
          <el-descriptions-item label="设备名称">{{ currentDevice.name }}</el-descriptions-item>
          <el-descriptions-item label="设备类型">{{ currentDevice.type }}</el-descriptions-item>
          <el-descriptions-item label="IP地址">{{ currentDevice.ip }}</el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="getStatusType(currentDevice.status)">
              <el-icon style="margin-right: 4px;">
                <component :is="getStatusIcon(currentDevice.status)" />
              </el-icon>
              {{ getStatusText(currentDevice.status) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="设备位置">{{ currentDevice.location }}</el-descriptions-item>
          <el-descriptions-item label="创建时间">暂无</el-descriptions-item>
          <el-descriptions-item label="更新时间">暂无</el-descriptions-item>
          <el-descriptions-item label="备注说明" :span="2">
            暂无备注
          </el-descriptions-item>
        </el-descriptions>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance } from 'element-plus'
import { Plus, Search, Connection, Refresh, Warning, Upload, Download, Document, Delete, SuccessFilled, CircleCloseFilled } from '@element-plus/icons-vue'
import { 
  getDevices, 
  createDevice, 
  updateDevice, 
  deleteDevice, 
  updateDeviceStatus,
  downloadImportTemplate,
  importDevices
} from '@/api/device'
import type { Device, DeviceForm } from '@/types/device'
import { DEVICE_STATUS_OPTIONS, DEVICE_TYPE_OPTIONS } from '@/types/device'

const loading = ref(false)
const dialogVisible = ref(false)
const detailDialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref<FormInstance>()

// 批量导入相关
const importDialogVisible = ref(false)
const resultVisible = ref(false)
const importing = ref(false)
const downloadLoading = ref(false)
const selectedFile = ref<File | null>(null)

// 导入结果
const importResult = reactive({
  success_count: 0,
  failure_count: 0,
  success_devices: [],
  failure_details: []
})

const searchForm = reactive({
  name: '',
  status: ''
})

const deviceForm = reactive<DeviceForm>({
  id: 0,
  name: '',
  type: '',
  ip: '',
  status: 'offline',
  location: ''
})

const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 0
})

const devices = ref<Device[]>([])
const currentDevice = ref<Device | null>(null)

const rules = {
  name: [
    { required: true, message: '请输入设备名称', trigger: 'blur' },
    { min: 2, max: 30, message: '设备名称长度在 2 到 30 个字符', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择设备类型', trigger: 'change' }
  ],
  ip: [
    { pattern: /^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/, message: '请输入正确的IP地址格式', trigger: 'blur' }
  ],
  status: [
    { required: true, message: '请选择状态', trigger: 'change' }
  ],
  location: [
    { required: true, message: '请输入设备位置', trigger: 'blur' }
  ]
}

const getStatusType = (status: string) => {
  switch (status) {
    case 'online':
      return 'success'
    case 'offline':
      return 'danger'
    case 'maintenance':
      return 'warning'
    default:
      return 'info'
  }
}

const getStatusText = (status: string) => {
  switch (status) {
    case 'online':
      return '在线'
    case 'offline':
      return '离线'
    case 'maintenance':
      return '维护中'
    default:
      return status
  }
}

const getStatusIcon = (status: string) => {
  switch (status) {
    case 'online':
      return Connection
    case 'offline':
      return Refresh
    case 'maintenance':
      return Warning
    default:
      return Connection
  }
}

const loadDevices = async () => {
  loading.value = true
  try {
    const response = await getDevices({
      skip: (pagination.currentPage - 1) * pagination.pageSize,
      limit: pagination.pageSize,
      name: searchForm.name || undefined,
      status: searchForm.status || undefined
    })
    
    devices.value = response.data.devices
    pagination.total = response.data.total
  } catch (error) {
    console.error('获取设备列表失败:', error)
    ElMessage.error('加载设备列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  loadDevices()
}

const handleReset = () => {
  searchForm.name = ''
  searchForm.status = ''
  loadDevices()
}

const handleAdd = () => {
  isEdit.value = false
  dialogVisible.value = true
  resetForm()
}

const handleViewDetail = (row: Device) => {
  currentDevice.value = row
  detailDialogVisible.value = true
}

const handleEdit = (row: Device) => {
  isEdit.value = true
  dialogVisible.value = true
  Object.assign(deviceForm, row)
}

const handleToggleStatus = async (row: Device) => {
  const newStatus = row.status === 'online' ? 'offline' : 'online'
  const action = newStatus === 'online' ? '启用' : '停用'
  
  try {
    await ElMessageBox.confirm(
      `确定要${action}设备 "${row.name}" 吗？`,
      `确认${action}`,
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    await updateDeviceStatus(row.id, newStatus)
    ElMessage.success(`设备${action}成功`)
    loadDevices()
  } catch (error: any) {
    if (error.message !== 'cancel') {
      console.error('更新设备状态失败:', error)
      ElMessage.error('更新设备状态失败')
    }
  }
}

const handleDelete = async (row: Device) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除设备 "${row.name}" 吗？`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    await deleteDevice(row.id)
    ElMessage.success('删除成功')
    loadDevices()
  } catch (error: any) {
    if (error.message !== 'cancel') {
      console.error('删除设备失败:', error)
      ElMessage.error('删除设备失败')
    }
  }
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    
    if (isEdit.value && deviceForm.id) {
      // 更新设备
      await updateDevice(deviceForm.id, {
        name: deviceForm.name,
        type: deviceForm.type,
        ip: deviceForm.ip,
        status: deviceForm.status,
        location: deviceForm.location
      })
      ElMessage.success('更新成功')
    } else {
      // 创建设备
      await createDevice({
        name: deviceForm.name,
        type: deviceForm.type,
        ip: deviceForm.ip,
        status: deviceForm.status,
        location: deviceForm.location
      })
      ElMessage.success('创建成功')
    }
    
    dialogVisible.value = false
    loadDevices()
  } catch (error: any) {
    console.error('操作失败:', error)
    ElMessage.error(isEdit.value ? '更新失败' : '创建失败')
  }
}

const resetForm = () => {
  deviceForm.id = 0
  deviceForm.name = ''
  deviceForm.type = ''
  deviceForm.ip = ''
  deviceForm.status = 'offline'
  deviceForm.location = ''
}

const handleSizeChange = (val: number) => {
  pagination.pageSize = val
  loadDevices()
}

const handleCurrentChange = (val: number) => {
  pagination.currentPage = val
  loadDevices()
}

// 批量导入相关方法
const handleBatchImport = () => {
  importDialogVisible.value = true
  selectedFile.value = null
}

const downloadTemplate = async () => {
  downloadLoading.value = true
  try {
    // 创建CSV内容，包含标题行和示例数据
    const csvData = [
      ['设备名称', '设备类型', '设备IP', '状态', '位置'],
      ['Web服务器001', '服务器', '192.168.1.100', 'online', '机房A-机柜01'],
      ['DB服务器001', '数据库服务器', '192.168.1.200', 'offline', '机房B-机柜01'],
      ['交换机001', '交换机', '192.168.1.1', 'online', '机房A-网络区']
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
    link.download = '设备导入模板.csv'
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

const handleFileChange = (file: any) => {
  if (file.raw) {
    selectedFile.value = file.raw
  }
}

const clearFile = () => {
  selectedFile.value = null
}

const handleImportSubmit = async () => {
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
  
  importing.value = true
  try {
    const response = await importDevices(selectedFile.value)
    
    // 处理导入结果
    if (response.data) {
      Object.assign(importResult, response.data)
      importDialogVisible.value = false
      resultVisible.value = true
      
      // 显示导入成功消息
      if (importResult.success_count > 0) {
        ElMessage.success(`成功导入 ${importResult.success_count} 个设备`)
      }
      
      // 刷新设备列表
      await loadDevices()
    } else {
      ElMessage.error('导入失败：响应数据格式错误')
    }
  } catch (error: any) {
    console.error('批量导入失败:', error)
    const errorMsg = error?.response?.data?.detail || error?.message || '批量导入失败'
    ElMessage.error(errorMsg)
  } finally {
    importing.value = false
  }
}

onMounted(() => {
  loadDevices()
})
</script>

<style scoped lang="scss">
.device-management {
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

  // 批量导入样式
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
      padding: 10px;
      background: #f0f9ff;
      border-left: 4px solid #409eff;
      
      p {
        margin: 0;
        color: #606266;
        font-size: 13px;
        line-height: 1.4;
      }
    }
  }

  .import-result {
    .result-summary {
      margin-bottom: 20px;
      
      .success-info, .fail-info {
        display: flex;
        align-items: center;
        margin-bottom: 10px;
        
        .el-icon {
          margin-right: 8px;
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

  .device-detail {
    .el-descriptions {
      margin-top: 20px;
    }
  }
}
</style> 