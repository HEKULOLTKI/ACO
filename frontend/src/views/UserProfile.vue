<template>
  <div class="user-profile">
    <el-row :gutter="20">
      <!-- 个人信息 -->
      <el-col :span="8">
        <el-card>
          <template #header>
            <span>个人信息</span>
          </template>
          
          <div class="profile-avatar">
            <el-avatar 
              :size="120" 
              :src="userInfo.photo_data || ''" 
              icon="User"
            />
            <el-button type="text" @click="changeAvatar" style="margin-top: 10px;">
              更换头像
            </el-button>
          </div>
          
          <div class="profile-info">
            <div class="info-item">
              <span class="label">用户名:</span>
              <span class="value">{{ userInfo.username }}</span>
            </div>
            <div class="info-item">
              <span class="label">角色:</span>
              <el-tag :type="getRoleType(userInfo.role)">
                {{ getRoleText(userInfo.role) }}
              </el-tag>
            </div>
            <div class="info-item">
              <span class="label">用户类型:</span>
              <span class="value">{{ userInfo.type }}</span>
            </div>
            <div class="info-item">
              <span class="label">状态:</span>
              <el-tag :type="userInfo.status === 'active' ? 'success' : 'danger'">
                {{ userInfo.status === 'active' ? '激活' : '未激活' }}
              </el-tag>
            </div>
            <div class="info-item">
              <span class="label">创建时间:</span>
              <span class="value">{{ userInfo.created_at }}</span>
            </div>
          </div>
        </el-card>
      </el-col>

      <!-- 基本设置 -->
      <el-col :span="8">
        <el-card>
          <template #header>
            <span>基本设置</span>
          </template>
          
          <el-form :model="basicForm" :rules="basicRules" ref="basicFormRef" label-width="100px">
            <el-form-item label="显示名称" prop="displayName">
              <el-input v-model="basicForm.displayName" placeholder="请输入显示名称" />
            </el-form-item>
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="basicForm.email" placeholder="请输入邮箱地址" />
            </el-form-item>
            <el-form-item label="手机号" prop="phone">
              <el-input v-model="basicForm.phone" placeholder="请输入手机号" />
            </el-form-item>
            <el-form-item label="部门" prop="department">
              <el-input v-model="basicForm.department" placeholder="请输入部门" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="saveBasicInfo">
                保存基本信息
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>

      <!-- 安全设置 -->
      <el-col :span="8">
        <el-card>
          <template #header>
            <span>安全设置</span>
          </template>
          
          <el-form :model="securityForm" :rules="securityRules" ref="securityFormRef" label-width="100px">
            <el-form-item label="当前密码" prop="currentPassword">
              <el-input 
                v-model="securityForm.currentPassword" 
                type="password" 
                placeholder="请输入当前密码"
                show-password
              />
            </el-form-item>
            <el-form-item label="新密码" prop="newPassword">
              <el-input 
                v-model="securityForm.newPassword" 
                type="password" 
                placeholder="请输入新密码"
                show-password
              />
            </el-form-item>
            <el-form-item label="确认密码" prop="confirmPassword">
              <el-input 
                v-model="securityForm.confirmPassword" 
                type="password" 
                placeholder="请再次输入新密码"
                show-password
              />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="changePassword">
                修改密码
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
    </el-row>

    <!-- 操作日志 -->
    <el-row style="margin-top: 20px;">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>最近操作记录</span>
              <el-button size="small" @click="loadOperationLogs">
                <el-icon><Refresh /></el-icon>
                刷新
              </el-button>
            </div>
          </template>
          
          <el-table :data="operationLogs" v-loading="loading" style="width: 100%">
            <el-table-column prop="time" label="操作时间" width="180" />
            <el-table-column prop="action" label="操作类型" width="120">
              <template #default="scope">
                <el-tag :type="getActionType(scope.row.action)">
                  {{ scope.row.action }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="module" label="操作模块" width="120" />
            <el-table-column prop="description" label="操作描述" show-overflow-tooltip />
            <el-table-column prop="ip" label="IP地址" width="140" />
            <el-table-column prop="device" label="设备信息" width="150" />
          </el-table>
        </el-card>
      </el-col>
    </el-row>

    <!-- 头像上传对话框 -->
    <el-dialog v-model="avatarDialogVisible" title="更换头像" width="400px">
      <el-upload
        class="avatar-uploader"
        action="#"
        :show-file-list="false"
        :before-upload="beforeAvatarUpload"
        :http-request="handleAvatarUpload"
      >
        <img v-if="imageUrl" :src="imageUrl" class="avatar" />
        <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
      </el-upload>
      <div class="upload-tips">
        <p>支持 JPG、PNG 格式，文件大小不超过 2MB</p>
      </div>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="avatarDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="confirmAvatarUpload">
            确定
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, type FormInstance, type UploadProps } from 'element-plus'
import { Plus, Refresh } from '@element-plus/icons-vue'

interface UserInfo {
  id: number
  username: string
  role: string
  type: string
  status: string
  photo_data?: string
  created_at: string
}

interface OperationLog {
  id: number
  time: string
  action: string
  module: string
  description: string
  ip: string
  device: string
}

const loading = ref(false)
const avatarDialogVisible = ref(false)
const imageUrl = ref('')
const basicFormRef = ref<FormInstance>()
const securityFormRef = ref<FormInstance>()

const userInfo = ref<UserInfo>({
  id: 1,
  username: 'admin',
          role: '系统架构设计师',
  type: '管理员',
  status: 'active',
  created_at: '2024-01-10 10:30:00'
})

const basicForm = reactive({
  displayName: 'Admin User',
  email: 'admin@example.com',
  phone: '13888888888',
  department: '技术部'
})

const securityForm = reactive({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const operationLogs = ref<OperationLog[]>([])

const basicRules = {
  displayName: [
    { required: true, message: '请输入显示名称', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ]
}

const securityRules = {
  currentPassword: [
    { required: true, message: '请输入当前密码', trigger: 'blur' }
  ],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度在 6 到 20 个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请再次输入新密码', trigger: 'blur' },
    {
      validator: (rule: any, value: string, callback: Function) => {
        if (value !== securityForm.newPassword) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

const getRoleType = (role: string) => {
  switch (role) {
    case '网络规划设计师':
      return 'primary'
          case '系统架构设计师':
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

const getActionType = (action: string) => {
  switch (action) {
    case '登录':
      return 'success'
    case '创建':
      return 'primary'
    case '更新':
      return 'warning'
    case '删除':
      return 'danger'
    default:
      return 'info'
  }
}

const changeAvatar = () => {
  avatarDialogVisible.value = true
}

const beforeAvatarUpload: UploadProps['beforeUpload'] = (rawFile) => {
  if (rawFile.type !== 'image/jpeg' && rawFile.type !== 'image/png') {
    ElMessage.error('头像只能是 JPG 或 PNG 格式!')
    return false
  } else if (rawFile.size / 1024 / 1024 > 2) {
    ElMessage.error('头像大小不能超过 2MB!')
    return false
  }
  return true
}

const handleAvatarUpload = (options: any) => {
  const reader = new FileReader()
  reader.onload = (e) => {
    imageUrl.value = e.target?.result as string
  }
  reader.readAsDataURL(options.file)
}

const confirmAvatarUpload = () => {
  if (imageUrl.value) {
    userInfo.value.photo_data = imageUrl.value
    ElMessage.success('头像更新成功')
    avatarDialogVisible.value = false
  } else {
    ElMessage.warning('请先选择头像')
  }
}

const saveBasicInfo = async () => {
  if (!basicFormRef.value) return
  
  try {
    await basicFormRef.value.validate()
    ElMessage.success('基本信息保存成功')
  } catch (error) {
    console.error('表单验证失败:', error)
  }
}

const changePassword = async () => {
  if (!securityFormRef.value) return
  
  try {
    await securityFormRef.value.validate()
    ElMessage.success('密码修改成功')
    // 清空密码表单
    securityForm.currentPassword = ''
    securityForm.newPassword = ''
    securityForm.confirmPassword = ''
  } catch (error) {
    console.error('表单验证失败:', error)
  }
}

const loadOperationLogs = async () => {
  loading.value = true
  try {
    // 模拟操作日志数据
    operationLogs.value = [
      {
        id: 1,
        time: '2024-01-15 14:30:25',
        action: '登录',
        module: '用户管理',
        description: '用户登录系统',
        ip: '192.168.1.100',
        device: 'Windows 10 Chrome'
      },
      {
        id: 2,
        time: '2024-01-15 14:25:10',
        action: '创建',
        module: '任务管理',
        description: '创建新任务：系统维护',
        ip: '192.168.1.100',
        device: 'Windows 10 Chrome'
      },
      {
        id: 3,
        time: '2024-01-15 14:20:45',
        action: '更新',
        module: '用户管理',
        description: '更新用户信息',
        ip: '192.168.1.100',
        device: 'Windows 10 Chrome'
      }
    ]
  } catch (error) {
    ElMessage.error('加载操作日志失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadOperationLogs()
})
</script>

<style scoped lang="scss">
.user-profile {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .profile-avatar {
    text-align: center;
    margin-bottom: 20px;
  }

  .profile-info {
    .info-item {
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

  .avatar-uploader {
    text-align: center;

    .avatar {
      width: 178px;
      height: 178px;
      display: block;
      border-radius: 6px;
    }

    .avatar-uploader-icon {
      font-size: 28px;
      color: #8c939d;
      width: 178px;
      height: 178px;
      border: 1px dashed #d9d9d9;
      border-radius: 6px;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: border-color 0.3s;

      &:hover {
        border-color: #409eff;
      }
    }
  }

  .upload-tips {
    text-align: center;
    margin-top: 10px;

    p {
      font-size: 12px;
      color: #999;
      margin: 0;
    }
  }
}
</style> 