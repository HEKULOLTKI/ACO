<template>
  <div class="system-settings">
    <el-row :gutter="20">
      <!-- 基本设置 -->
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>基本设置</span>
          </template>
          
          <el-form :model="basicSettings" label-width="120px">
            <el-form-item label="系统名称">
              <el-input v-model="basicSettings.systemName" />
            </el-form-item>
            <el-form-item label="系统描述">
              <el-input 
                v-model="basicSettings.systemDescription" 
                type="textarea"
                :rows="3"
              />
            </el-form-item>
            <el-form-item label="管理员邮箱">
              <el-input v-model="basicSettings.adminEmail" />
            </el-form-item>
            <el-form-item label="会话超时时间">
              <el-select v-model="basicSettings.sessionTimeout">
                <el-option label="15分钟" :value="15" />
                <el-option label="30分钟" :value="30" />
                <el-option label="1小时" :value="60" />
                <el-option label="2小时" :value="120" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="saveBasicSettings">
                保存基本设置
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>

      <!-- 安全设置 -->
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>安全设置</span>
          </template>
          
          <el-form :model="securitySettings" label-width="120px">
            <el-form-item label="密码最小长度">
              <el-input-number 
                v-model="securitySettings.minPasswordLength" 
                :min="6"
                :max="20"
              />
            </el-form-item>
            <el-form-item label="登录失败限制">
              <el-input-number 
                v-model="securitySettings.maxFailedAttempts" 
                :min="3"
                :max="10"
              />
            </el-form-item>
            <el-form-item label="账户锁定时间">
              <el-select v-model="securitySettings.lockoutDuration">
                <el-option label="10分钟" :value="10" />
                <el-option label="30分钟" :value="30" />
                <el-option label="1小时" :value="60" />
                <el-option label="24小时" :value="1440" />
              </el-select>
            </el-form-item>
            <el-form-item label="启用双因子认证">
              <el-switch v-model="securitySettings.twoFactorEnabled" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="saveSecuritySettings">
                保存安全设置
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px;">
      <!-- 系统状态 -->
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>系统状态</span>
          </template>
          
          <div class="status-grid">
            <div class="status-item">
              <span class="label">系统版本:</span>
              <span class="value">{{ systemStatus.version }}</span>
            </div>
            <div class="status-item">
              <span class="label">运行时间:</span>
              <span class="value">{{ systemStatus.uptime }}</span>
            </div>
            <div class="status-item">
              <span class="label">数据库状态:</span>
              <el-tag :type="systemStatus.dbStatus === 'connected' ? 'success' : 'danger'">
                {{ systemStatus.dbStatus === 'connected' ? '已连接' : '未连接' }}
              </el-tag>
            </div>
            <div class="status-item">
              <span class="label">在线用户:</span>
              <span class="value">{{ systemStatus.onlineUsers }}</span>
            </div>
            <div class="status-item">
              <span class="label">内存使用:</span>
              <el-progress :percentage="systemStatus.memoryUsage" />
            </div>
            <div class="status-item">
              <span class="label">磁盘使用:</span>
              <el-progress :percentage="systemStatus.diskUsage" />
            </div>
          </div>
        </el-card>
      </el-col>

      <!-- 系统维护 -->
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>系统维护</span>
          </template>
          
          <div class="maintenance-actions">
            <el-button 
              type="warning" 
              @click="clearCache"
              :loading="loading.clearCache"
            >
              <el-icon><Delete /></el-icon>
              清除缓存
            </el-button>
            
            <el-button 
              type="info" 
              @click="exportLogs"
              :loading="loading.exportLogs"
            >
              <el-icon><Download /></el-icon>
              导出日志
            </el-button>
            
            <el-button 
              type="primary" 
              @click="backupDatabase"
              :loading="loading.backupDatabase"
            >
              <el-icon><Upload /></el-icon>
              备份数据库
            </el-button>
            
            <el-button 
              type="danger" 
              @click="restartSystem"
              :loading="loading.restartSystem"
            >
              <el-icon><Refresh /></el-icon>
              重启系统
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 系统日志 -->
    <el-row style="margin-top: 20px;">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>系统日志</span>
              <el-button size="small" @click="refreshLogs">
                <el-icon><Refresh /></el-icon>
                刷新
              </el-button>
            </div>
          </template>
          
          <el-table :data="systemLogs" v-loading="loading.logs" style="width: 100%">
            <el-table-column prop="time" label="时间" width="180" />
            <el-table-column prop="level" label="级别" width="100">
              <template #default="scope">
                <el-tag :type="getLogLevelType(scope.row.level)">
                  {{ scope.row.level }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="module" label="模块" width="120" />
            <el-table-column prop="message" label="消息" show-overflow-tooltip />
            <el-table-column prop="user" label="用户" width="100" />
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Delete, Download, Upload, Refresh } from '@element-plus/icons-vue'

interface SystemLog {
  id: number
  time: string
  level: string
  module: string
  message: string
  user: string
}

const basicSettings = reactive({
  systemName: '多智能体协作运维系统',
  systemDescription: '基于Vue3和FastAPI的前后端分离多智能体协作运维系统',
  adminEmail: 'admin@example.com',
  sessionTimeout: 30
})

const securitySettings = reactive({
  minPasswordLength: 6,
  maxFailedAttempts: 5,
  lockoutDuration: 30,
  twoFactorEnabled: false
})

const systemStatus = reactive({
  version: 'v1.0.0',
  uptime: '5天 12小时 30分钟',
  dbStatus: 'connected',
  onlineUsers: 8,
  memoryUsage: 65,
  diskUsage: 45
})

const loading = reactive({
  clearCache: false,
  exportLogs: false,
  backupDatabase: false,
  restartSystem: false,
  logs: false
})

const systemLogs = ref<SystemLog[]>([])

const getLogLevelType = (level: string) => {
  switch (level.toLowerCase()) {
    case 'error':
      return 'danger'
    case 'warning':
      return 'warning'
    case 'info':
      return 'success'
    case 'debug':
      return 'info'
    default:
      return ''
  }
}

const saveBasicSettings = async () => {
  try {
    // 模拟保存
    await new Promise(resolve => setTimeout(resolve, 1000))
    ElMessage.success('基本设置保存成功')
  } catch (error) {
    ElMessage.error('保存失败')
  }
}

const saveSecuritySettings = async () => {
  try {
    // 模拟保存
    await new Promise(resolve => setTimeout(resolve, 1000))
    ElMessage.success('安全设置保存成功')
  } catch (error) {
    ElMessage.error('保存失败')
  }
}

const clearCache = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要清除系统缓存吗？',
      '确认清除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    loading.clearCache = true
    await new Promise(resolve => setTimeout(resolve, 2000))
    loading.clearCache = false
    ElMessage.success('缓存清除成功')
  } catch (error) {
    loading.clearCache = false
  }
}

const exportLogs = async () => {
  loading.exportLogs = true
  try {
    await new Promise(resolve => setTimeout(resolve, 1500))
    ElMessage.success('日志导出成功')
  } catch (error) {
    ElMessage.error('日志导出失败')
  } finally {
    loading.exportLogs = false
  }
}

const backupDatabase = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要备份数据库吗？',
      '确认备份',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'info',
      }
    )
    
    loading.backupDatabase = true
    await new Promise(resolve => setTimeout(resolve, 3000))
    loading.backupDatabase = false
    ElMessage.success('数据库备份成功')
  } catch (error) {
    loading.backupDatabase = false
  }
}

const restartSystem = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要重启系统吗？重启后将断开所有用户连接。',
      '确认重启',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'danger',
      }
    )
    
    loading.restartSystem = true
    await new Promise(resolve => setTimeout(resolve, 2000))
    ElMessage.success('系统重启中...')
  } catch (error) {
    loading.restartSystem = false
  }
}

const loadSystemLogs = async () => {
  loading.logs = true
  try {
    // 模拟日志数据
    systemLogs.value = [
      {
        id: 1,
        time: '2024-01-15 14:30:25',
        level: 'INFO',
        module: '用户管理',
        message: '用户admin登录成功',
        user: 'admin'
      },
      {
        id: 2,
        time: '2024-01-15 14:25:10',
        level: 'WARNING',
        module: '系统监控',
        message: 'CPU使用率达到80%',
        user: 'system'
      },
      {
        id: 3,
        time: '2024-01-15 14:20:45',
        level: 'ERROR',
        module: '数据库',
        message: '数据库连接超时',
        user: 'system'
      },
      {
        id: 4,
        time: '2024-01-15 14:15:30',
        level: 'INFO',
        module: '任务管理',
        message: '任务"系统维护"创建成功',
        user: 'operator1'
      }
    ]
  } catch (error) {
    ElMessage.error('加载系统日志失败')
  } finally {
    loading.logs = false
  }
}

const refreshLogs = () => {
  loadSystemLogs()
}

onMounted(() => {
  loadSystemLogs()
})
</script>

<style scoped lang="scss">
.system-settings {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .status-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 16px;

    .status-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 10px 0;
      border-bottom: 1px solid #f0f0f0;

      &:last-child {
        border-bottom: none;
      }

      .label {
        font-size: 14px;
        color: #666;
        font-weight: 500;
      }

      .value {
        font-size: 14px;
        color: #333;
        font-weight: 600;
      }
    }
  }

  .maintenance-actions {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 15px;

    .el-button {
      justify-self: stretch;
    }
  }
}
</style> 