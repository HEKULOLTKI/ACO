<template>
  <div class="role-selection-container">
    <!-- 简化的顶部操作栏 -->
    <div class="top-header">
      <div class="header-content">
        <!-- 左侧00005图片 -->
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
              <div class="username">{{ authStore.user?.username || '操作员' }}</div>
              <div class="user-role">{{ authStore.user?.role || '系统用户' }}</div>
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

    <!-- 科技背景 - 使用提供的背景图片 -->
    <div class="tech-background">
      <div class="main-background"></div>
      <div class="overlay-effects">
        <div class="light-beams"></div>
        <div class="particles"></div>
        <div class="grid-overlay"></div>
      </div>
    </div>
    


    <!-- 底部平台 - 使用提供的素材 -->
    <div class="platform-base">
      <div class="platform-surface">
        <img src="/src/assets/image/组 682.png" alt="底部平台" class="platform-background">
      </div>
      <div class="platform-glow"></div>
      <div class="platform-reflections"></div>
    </div>

    <!-- 角色选择区域 - 放在平台上 -->
    <div class="roles-section">
      <!-- 选中指示器 - 动态指向选中角色 -->
      <div class="selection-indicator">
        <div class="selection-arrow" :style="getArrowPosition()">
          <img :src="arrowIcon" alt="选择指示器" class="arrow-icon">
        </div>
      </div>
      
      <div class="roles-grid">
            <div 
              v-for="role in roleOptions" 
              :key="role.value"
          class="role-card"
              :class="{ 
            'selected': selectedRole === role.value,
            'available': true
              }"
              @click="selectRole(role.value)"
              @mouseenter="handleMouseEnter(role.value)"
              @mouseleave="handleMouseLeave"
            >
          <div class="card-glow" :class="{ 'active': selectedRole === role.value }"></div>
          <div class="card-inner">
            <div class="role-3d-icon">
              <div class="icon-platform">
                <img :src="role.iconUrl" :alt="role.label" class="tech-icon">
                <div class="icon-glow"></div>
              </div>
              </div>
            <div class="role-name">{{ role.label }}</div>
          </div>
          <div class="card-base"></div>
              </div>
            </div>
          </div>
          

    
    <!-- 访问权限错误弹窗 -->
    <AccessDeniedDialog 
      :visible="showAccessDenied"
      :message="accessDeniedMessage"
      @close="handleAccessDeniedClose"
      @confirm="handleAccessDeniedConfirm"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  UserFilled, 
  Monitor, 
  Setting, 
  DataAnalysis, 
  Cpu,
  Check,
  Right,
  ArrowLeft 
} from '@element-plus/icons-vue'
import { useAuthStore } from '@/store/modules/auth'
import { USER_ROLE_OPTIONS } from '@/types/user'
import AccessDeniedDialog from '@/components/AccessDeniedDialog.vue'
import arrowIcon from '@/assets/role/箭头.png'

const router = useRouter()
const authStore = useAuthStore()

// 选中的角色
const selectedRole = ref<string>('')
const loading = ref(false)

// 悬浮的角色
const hoveredRole = ref<string>('')

// 鼠标悬浮事件处理
const handleMouseEnter = (roleValue: string) => {
  hoveredRole.value = roleValue
}

const handleMouseLeave = () => {
  hoveredRole.value = ''
}

// 访问权限弹窗
const showAccessDenied = ref(false)
const accessDeniedMessage = ref('')

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

// 角色选项配置
const roleOptions = [
  {
    value: '网络规划设计师',
    label: '网络规划设计师',
    description: '负责网络规划、设计和架构优化',
    icon: Monitor,
    iconUrl: '/src/assets/image/网络工程师.png'
  },
  {
    value: '系统架构设计师',
    label: '系统架构设计师',
    description: '负责系统架构设计和技术选型决策',
    icon: Cpu,
    iconUrl: '/src/assets/image/系统架构工程师.png'
  },
  {
    value: '系统规划与管理师',
    label: '系统规划与管理师',
    description: '负责系统规划、管理和运维',
    icon: Setting,
    iconUrl: '/src/assets/image/数据运维工程师.png'
  },
  {
    value: '系统分析师',
    label: '系统分析师', 
    description: '负责安全日志审计',
    icon: Monitor,
    iconUrl: '/src/assets/image/系统分析师.png'
  },
  {
    value: '孪生平台',
    label: '孪生平台',
    description: '访问数字孪生平台系统',
    icon: DataAnalysis,
    iconUrl: '/src/assets/image/孪生平台.png'
  }
]



// 选择角色
const selectRole = (role: string) => {
  // 检查用户是否有权限使用该角色
  const currentUser = authStore.user
  if (!currentUser) {
    ElMessage.error('用户信息获取失败，请重新登录')
    router.push('/login')
    return
  }
  
  // 如果选择孪生平台，任何人都可以选择，不需要权限验证
  if (role === '孪生平台') {
    selectedRole.value = role
    // 发送JSON数据到用户的IP地址，但包含孪生平台地址信息
    sendUserDataJson()
    return
  }
  
  // 检查操作员是否有权限使用选中的角色
  if (currentUser.type === '操作员' && currentUser.role !== role) {
    accessDeniedMessage.value = `您无权限使用"${role}"角色，您的角色是"${currentUser.role}"`
    showAccessDenied.value = true
    return
  }
  
  selectedRole.value = role
  
  // 直接发送JSON文件
  sendUserDataJson()
}

// 获取指示点位置 - 适应网格布局
const getArrowPosition = () => {
  if (!hoveredRole.value) {
    return { display: 'none' }
  }
  
  const hoveredIndex = roleOptions.findIndex(role => role.value === hoveredRole.value)
  if (hoveredIndex === -1) {
    return { display: 'none' }
  }
  
  // 根据屏幕宽度获取当前网格列数
  const getGridColumns = () => {
    const width = window.innerWidth
    if (width <= 480) return 1      // 超小屏幕：1列
    if (width <= 768) return 2      // 手机：2列
    if (width <= 1200) return 3     // 平板：3列
    if (width <= 1400) return 4     // 中等屏幕：4列
    return 5                        // 大屏幕：5列
  }
  
  const columns = getGridColumns()
  const cardWidth = 280
  const gap = 55
  
  // 计算悬浮卡片在当前行中的列位置（0开始）
  const columnIndex = hoveredIndex % columns
  
  // 计算网格容器的总宽度
  const gridWidth = columns * cardWidth + (columns - 1) * gap
  
  // 计算悬浮卡片在当前行中的位置
  const firstCardCenter = -(gridWidth / 2) + (cardWidth / 2)
  const hoveredCardCenter = firstCardCenter + columnIndex * (cardWidth + gap)
  
  const position = {
    left: `calc(50% + ${hoveredCardCenter}px)`,
    transform: 'translateX(-50%)',
    transition: 'left 0.3s cubic-bezier(0.23, 1, 0.32, 1)',
    display: 'block'
  }
  
  return position
}

// 发送用户数据JSON
const sendUserDataJson = async () => {
  const currentUser = authStore.user
  if (!currentUser) {
    ElMessage.error('用户信息获取失败，请重新登录')
    return
  }

  loading.value = true
  try {
    // 模拟角色验证过程
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // 获取用户完整信息（包括数据库信息和明文密码）
    let userCompleteInfo = null
    try {
      const token = localStorage.getItem('token') || authStore.token
      console.log('🔍 开始获取用户完整信息...')
      console.log('🔑 使用token:', token ? `${token.substring(0, 20)}...` : 'null')
      
      if (!token) {
        console.warn('⚠️ 未找到认证token，无法获取用户信息')
        ElMessage.warning('认证信息缺失，将使用默认配置')
        throw new Error('No token available')
      }
      
      const userInfoResponse = await fetch('http://127.0.0.1:8000/api/auth/user-complete-info', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        }
      })
      
      if (userInfoResponse.ok) {
        userCompleteInfo = await userInfoResponse.json()
        console.log('✅ 获取用户完整信息成功:', userCompleteInfo)
        console.log('🌐 用户IP地址:', userCompleteInfo?.sync_info?.session?.ip_address)
        console.log('👤 用户信息数量:', userCompleteInfo?.users?.length || 0)
        console.log('🔐 包含明文密码:', userCompleteInfo?.users?.[0]?.password ? '是' : '否')
      } else {
        const errorText = await userInfoResponse.text()
        console.warn('❌ 获取用户完整信息失败:', userInfoResponse.status, errorText)
        
        if (userInfoResponse.status === 401) {
          console.warn('🔐 认证失败，可能是token已过期')
          ElMessage.warning('登录状态已过期，但仍可使用角色选择功能')
          // 不进行自动跳转，保持在角色选择界面
        }
        
        ElMessage.warning('获取用户信息失败，将使用默认配置')
      }
    } catch (userInfoError: any) {
      console.error('❌ 获取用户完整信息时发生错误:', userInfoError)
      
      if (userInfoError.message === 'No token available') {
        console.warn('🔑 Token不可用，跳过用户信息获取')
      } else {
        ElMessage.warning('网络错误，将使用默认配置')
      }
    }
    
    // 构建发送的数据
    const token = localStorage.getItem('token') || authStore.token
    let userDataToSend
    
    // 如果选择的是孪生平台，只发送孪生平台地址信息
    if (selectedRole.value === '孪生平台') {
      userDataToSend = {
        action: 'twin_platform_access',
        twin_platform: {
          url: 'http://172.17.10.100/',
          ip: '172.17.10.100',
          name: '数字孪生平台',
          description: '数字孪生平台系统访问地址'
        },
        timestamp: new Date().toISOString(),
        operator: {
          user_id: currentUser.id,
          username: currentUser.username,
          operator_role: currentUser.role,
          operator_type: currentUser.type
        }
      }
      console.log('✅ 构建孪生平台地址信息JSON数据')
    } else {
      // 其他角色发送完整的用户数据
      userDataToSend = userCompleteInfo || {
        action: 'user_data_sync',
        sync_info: {
          sync_type: 'fallback_user_export',
          sync_time: new Date().toISOString(),
          operator: {
            user_id: currentUser.id,
            username: currentUser.username,
            operator_role: currentUser.role,
            operator_type: currentUser.type,
            token: token // 添加当前用户的token
          },
          session: {
            ip_address: 'unknown',
            user_agent: 'unknown',
            login_time: Date.now() / 1000
          },
          data_source: {
            database: 'user_management',
            table: 'users',
            version: '1.0',
            environment: 'production'
          }
        },
        users: [
          {
            id: currentUser.id,
            username: currentUser.username,
            password: '123456', // 默认密码
            role: currentUser.role,
            type: currentUser.type,
            status: currentUser.status,
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString()
          }
        ],
        sync_summary: {
          total_users: 1,
          active_users: 1,
          inactive_users: 0,
          roles: [currentUser.role],
          types: [currentUser.type],
          sync_id: `sync_${Date.now()}`,
          compression: 'none'
        }
      }
    }
    
    // 确保token始终被添加到发送的数据中（仅对完整用户数据）
    if (selectedRole.value !== '孪生平台' && userDataToSend && userDataToSend.sync_info && userDataToSend.sync_info.operator) {
      userDataToSend.sync_info.operator.token = token
    }
    
    // 向用户登录的IP地址发送JSON数据
    const userIP = userCompleteInfo?.sync_info?.session?.ip_address
    const targetUrl = userIP && userIP !== 'unknown' && userIP !== 'null'
      ? `http://${userIP}:8800/upload`
      : 'http://127.0.0.1:8800/upload' // 备用地址
    
    console.log('📤 准备发送数据:')
    console.log('   用户IP:', userIP)
    console.log('   目标地址:', targetUrl)
    console.log('   数据类型:', selectedRole.value === '孪生平台' ? '孪生平台地址信息' : '完整用户数据')
    console.log('   数据大小:', JSON.stringify(userDataToSend).length, '字节')
    if (selectedRole.value === '孪生平台') {
      console.log('   孪生平台地址:', userDataToSend.twin_platform?.url)
    } else {
      console.log('   用户数量:', userDataToSend.users?.length || 0)
      console.log('   包含Token:', token ? '是' : '否')
      if (token) {
        console.log('   Token前缀:', token.substring(0, 20) + '...')
      }
    }
    
    try {
      // 增加超时时间和更详细的错误处理
      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), 10000) // 10秒超时
      
      const response = await fetch(targetUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userDataToSend),
        signal: controller.signal
      })
      
      clearTimeout(timeoutId)
      
      console.log('📥 收到响应:', response.status, response.statusText)
      
      if (response.ok) {
        const responseData = await response.text()
        console.log('✅ 用户信息发送成功! 响应:', responseData)
        ElMessage.success(`用户信息发送成功！已向您的终端发送 ${userDataToSend.users.length} 个用户信息`)
      } else {
        const errorText = await response.text()
        console.warn('⚠️ 服务器响应错误:', response.status, errorText)
        ElMessage.warning(`用户信息发送响应错误(${response.status})，但不影响系统使用`)
      }
    } catch (uploadError: any) {
      console.error('❌ 用户信息发送时发生错误:', uploadError)
      
      // 更详细的错误分析
      if (uploadError.name === 'AbortError') {
        console.warn('⏰ 请求超时 - 目标服务可能没有响应')
        ElMessage.warning('连接超时：目标终端可能没有服务运行，但不影响系统使用')
      } else if (uploadError.message && uploadError.message.includes('Failed to fetch')) {
        console.warn('🚫 网络连接错误 - 无法访问目标地址')
        ElMessage.warning('网络连接失败：无法访问您的终端地址，请检查网络连接或启动接收服务')
      } else {
        console.warn('❓ 未知错误:', uploadError.message || uploadError)
        ElMessage.warning('用户信息发送失败：' + (uploadError.message || uploadError) + '，但不影响系统使用')
      }
      
      // 提供解决建议
      if (userIP && userIP !== '127.0.0.1') {
        console.log('💡 解决建议:')
        console.log('   1. 在您的终端设备上启动用户信息接收服务')
        console.log('   2. 确保防火墙允许8800端口访问')
        console.log('   3. 检查网络连接是否正常')
        console.log('   4. 用户数据已准备完成，可通过其他方式获取')
      }
    }
    
    if (selectedRole.value === '孪生平台') {
      ElMessage.success(`已发送孪生平台地址信息，即将退出系统`)
    } else {
      ElMessage.success(`已发送用户数据JSON文件，即将退出系统`)
    }
    
    // 保存选中的角色到本地存储
    localStorage.setItem('selectedRole', selectedRole.value)
    
    // 延迟1.5秒后退出登录并返回登录界面
    setTimeout(async () => {
      await authStore.logoutAction()
      router.push('/login')
    }, 1500)
    
  } catch (error) {
    ElMessage.error('发送用户数据失败，请重试')
  } finally {
    loading.value = false
  }
}



// 返回登录
const goBack = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要返回登录页面吗？这将退出当前登录状态。',
      '确认返回',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    await authStore.logoutAction()
    ElMessage.success('已退出登录')
    router.push('/login')
  } catch (error) {
    // 用户取消了操作
  }
}

// 处理访问权限错误弹窗关闭
const handleAccessDeniedClose = () => {
  showAccessDenied.value = false
}

// 处理访问权限错误弹窗确认
const handleAccessDeniedConfirm = () => {
  showAccessDenied.value = false
  // 可以在这里添加其他逻辑，比如跳转到帮助页面或联系管理员
  ElMessage.info('如需申请更多权限，请联系系统管理员')
}

// 组件挂载时检查用户类型
onMounted(() => {
  const currentUser = authStore.user
  if (!currentUser) {
    router.push('/login')
    return
  }
  
  // 管理员也可以访问角色选择页面，不自动跳转
  // 如果是操作员但没有设置角色，需要选择角色
  if (currentUser.type === '操作员' && !currentUser.role) {
    ElMessage.info('请选择您的角色以继续使用系统')
  }
  


  
  // 监听窗口大小变化，重新计算指示器位置
  window.addEventListener('resize', () => {
    // 触发响应式更新，让指示器位置重新计算
    if (hoveredRole.value) {
      const currentRole = hoveredRole.value
      hoveredRole.value = ''
      setTimeout(() => {
        hoveredRole.value = currentRole
      }, 50)
    }
  })
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');

.role-selection-container {
  width: 100%;
  height: 100vh;
  position: relative;
  overflow: hidden;
  font-family: 'Orbitron', monospace;
  color: #00ffff;
}

/* 简化的顶部操作栏 - 完全透明背景 */
.top-header {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100px;
  z-index: 200;
  background: transparent;
}

.header-content {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 40px;
  background: transparent;
}

/* 左侧Logo */
.header-logo {
  display: flex;
  align-items: center;
  height: 100%;
}

.logo-image {
  height: 45px;
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
  position: relative;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 30px;
  height: 100%;
  padding-right: 20px;
}

.user-info {
  position: relative;
  display: flex;
  align-items: center;
  gap: 15px;
  height: 60px;
  padding: 0 20px;
  background: rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(0, 255, 255, 0.2);
  border-radius: 30px;
  backdrop-filter: blur(5px);
  animation: userInfoGlow 3s ease-in-out infinite alternate;
}

.user-avatar {
  position: relative;
  width: 45px;
  height: 45px;
  border-radius: 50%;
  overflow: hidden;
  animation: avatarFloat 4s ease-in-out infinite;
}

.avatar-icon {
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: brightness(1.1) saturate(1.2);
}

.avatar-ring {
  position: absolute;
  top: -3px;
  left: -3px;
  width: calc(100% + 6px);
  height: calc(100% + 6px);
  border-radius: 50%;
  border: 2px solid rgba(0, 255, 255, 0.7);
  animation: iconRingPulse 2s ease-in-out infinite alternate;
}

.user-details {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
  gap: 2px;
}

.username {
  font-size: 16px;
  font-weight: 600;
  color: #ffffff;
  text-shadow: 0 0 12px rgba(0, 255, 255, 0.8);
  letter-spacing: 1px;
  animation: usernameGlow 2.5s ease-in-out infinite alternate;
}

.user-role {
  font-size: 13px;
  font-weight: 400;
  color: rgba(255, 255, 255, 0.8);
  text-shadow: 0 0 8px rgba(0, 150, 255, 0.6);
  letter-spacing: 0.5px;
}

.action-buttons {
  position: relative;
  display: flex;
  align-items: center;
  gap: 15px;
  height: 100%;
}

.action-btn {
  position: relative;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(0, 255, 255, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.23, 1, 0.32, 1);
  backdrop-filter: blur(5px);
  animation: btnFloat 3s ease-in-out infinite;
}

.action-btn:hover {
  transform: translateY(-3px) scale(1.1);
  border-color: rgba(0, 255, 255, 0.8);
  box-shadow: 
    0 8px 25px rgba(0, 255, 255, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.action-btn:hover .btn-glow {
  opacity: 1;
}

.action-btn:hover .btn-tooltip {
  opacity: 1;
  transform: translateX(-50%) translateY(5px);
}

.action-icon {
  width: 28px;
  height: 28px;
  object-fit: contain;
  filter: brightness(1.2) drop-shadow(0 0 5px rgba(0, 255, 255, 0.5));
  transition: all 0.3s ease;
  z-index: 2;
}

.action-btn:hover .action-icon {
  filter: brightness(1.5) drop-shadow(0 0 10px rgba(0, 255, 255, 0.8));
}

.btn-arrow {
  position: absolute;
  top: 50%;
  right: -15px;
  transform: translateY(-50%);
  font-size: 18px;
  color: rgba(0, 255, 255, 0.9);
  opacity: 0;
  transition: all 0.3s cubic-bezier(0.23, 1, 0.32, 1);
  pointer-events: none;
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.8);
  z-index: 3;
}

.action-btn:hover .btn-arrow {
  opacity: 1;
  right: -25px;
  animation: arrowBounce 1s ease-in-out infinite;
}

.btn-glow {
  position: absolute;
  top: -3px;
  left: -3px;
  right: -3px;
  bottom: -3px;
  background: linear-gradient(
    45deg,
    rgba(0, 255, 255, 0.6),
    rgba(0, 150, 255, 0.8),
    rgba(0, 255, 255, 0.6)
  );
  border-radius: 50%;
  opacity: 0;
  transition: opacity 0.3s ease;
  filter: blur(8px);
  z-index: 1;
  animation: btnGlowRotate 2s linear infinite;
}

.btn-tooltip {
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%) translateY(0);
  background: linear-gradient(
    135deg,
    rgba(0, 20, 40, 0.95),
    rgba(0, 40, 80, 0.9)
  );
  color: #ffffff;
  padding: 8px 12px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 500;
  white-space: nowrap;
  pointer-events: none;
  opacity: 0;
  transition: all 0.3s cubic-bezier(0.23, 1, 0.32, 1);
  border: 1px solid rgba(0, 255, 255, 0.3);
  backdrop-filter: blur(10px);
  z-index: 10;
}

/* 科技背景 - 覆盖整个屏幕包括顶部 */
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
    ellipse at center top,
    rgba(0, 255, 255, 0.1),
    rgba(0, 100, 255, 0.05),
    transparent 70%
  );
  animation: breathe 4s ease-in-out infinite;
}

.particles {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.particles::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    radial-gradient(2px 2px at 20px 30px, rgba(0, 255, 255, 0.5), transparent),
    radial-gradient(2px 2px at 40px 70px, rgba(255, 255, 255, 0.3), transparent),
    radial-gradient(1px 1px at 190px 40px, rgba(0, 255, 255, 0.4), transparent),
    radial-gradient(1px 1px at 90px 40px, rgba(255, 255, 255, 0.2), transparent);
  background-repeat: repeat;
  background-size: 250px 250px;
  animation: sparkle 20s linear infinite;
}

.grid-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    linear-gradient(rgba(0, 255, 255, 0.1) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 255, 255, 0.1) 1px, transparent 1px);
  background-size: 50px 50px;
  opacity: 0.3;
  animation: gridMove 30s linear infinite;
}





/* 底部平台 */
.platform-base {
  position: absolute;
  bottom: 180px;
  left: 50%;
  transform: translateX(-50%);
  width: 1600px;
  height: 200px;
  z-index: 1;
  perspective: 800px;
}

.platform-surface {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: flex-end;
      justify-content: center;
}

.platform-background {
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
  height: auto;
  max-height: 100%;
  object-fit: contain;
  filter: drop-shadow(0 0 20px rgba(0, 255, 255, 0.3));
  opacity: 0.8;
  z-index: 1;
}

.platform-glow {
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 80%;
  height: 20px;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(0, 255, 255, 0.3),
    rgba(0, 150, 255, 0.4),
    rgba(0, 255, 255, 0.3),
    transparent
  );
  filter: blur(10px);
  animation: platformGlow 3s ease-in-out infinite alternate;
}

.platform-reflections {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    180deg,
    transparent 70%,
    rgba(0, 255, 255, 0.1) 85%,
    rgba(0, 255, 255, 0.2) 100%
  );
  pointer-events: none;
}

/* 角色选择区域 - 放在平台上 */
.roles-section {
  position: absolute;
  bottom: 300px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 50;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  max-width: 1600px;
}

.selection-indicator {
  position: absolute;
  top: -50px;
  left: 0;
  width: 100%;
  height: 40px;
  pointer-events: none;
  z-index: 100;
}

.selection-arrow {
  position: absolute;
  top: 0;
  width: 40px;
  height: 40px;
  display: none;
  animation: arrowFloat 2s ease-in-out infinite alternate;
  z-index: 101;
}

.arrow-icon {
  width: 100%;
  height: 100%;
  object-fit: contain;
  filter: 
    brightness(1.5) 
    saturate(1.2) 
    drop-shadow(0 0 8px rgba(0, 255, 255, 0.8))
    drop-shadow(0 0 15px rgba(0, 255, 255, 0.6))
    drop-shadow(0 0 25px rgba(0, 255, 255, 0.4))
    drop-shadow(0 0 35px rgba(255, 255, 255, 0.3));
  transition: all 0.3s ease;
  animation: arrowGlow 3s ease-in-out infinite alternate;
}

/* 箭头发光动画 */
@keyframes arrowGlow {
  0% {
    filter: 
      brightness(1.5) 
      saturate(1.2) 
      drop-shadow(0 0 8px rgba(0, 255, 255, 0.8))
      drop-shadow(0 0 15px rgba(0, 255, 255, 0.6))
      drop-shadow(0 0 25px rgba(0, 255, 255, 0.4))
      drop-shadow(0 0 35px rgba(255, 255, 255, 0.3));
  }
  100% {
    filter: 
      brightness(2) 
      saturate(1.5) 
      drop-shadow(0 0 12px rgba(0, 255, 255, 1))
      drop-shadow(0 0 20px rgba(0, 255, 255, 0.8))
      drop-shadow(0 0 30px rgba(0, 255, 255, 0.6))
      drop-shadow(0 0 40px rgba(255, 255, 255, 0.5));
  }
}

.roles-grid {
  display: grid;
  /* 🎯 网格布局 - 5列网格，每列自适应内容大小 */
  grid-template-columns: repeat(5, minmax(280px, 1fr));
  gap: 55px;      /* 网格间距 - 行间距和列间距 */
  justify-content: center;
  justify-items: center;  /* 水平居中每个网格项 */
  align-items: end;       /* 垂直底部对齐 */
  max-width: 1900px;
  perspective: 1200px;
  margin: 0 auto;         /* 整个网格容器居中 */
  
  /* 🎬 网格布局过渡动画 */
  transition: all 0.6s cubic-bezier(0.23, 1, 0.32, 1);
}

/* 角色卡片 - 网格布局优化 */
.role-card {
  position: relative;
  /* 📦 网格布局中的卡片尺寸 */
  width: 280px;   /* 卡片宽度 */
  height: 340px;  /* 卡片高度 */
  cursor: pointer;
  transform-style: preserve-3d;
  transition: all 0.6s cubic-bezier(0.4, 0.0, 0.2, 1);
  transform-origin: center center;
  will-change: transform;
  
  /* 🎯 网格项动画效果 */
  opacity: 0;
  transform: translateY(50px) scale(0.8);
  animation: gridItemFadeIn 0.8s cubic-bezier(0.23, 1, 0.32, 1) forwards;
}

/* 为每个卡片添加不同的延迟 */
.role-card:nth-child(1) { animation-delay: 0.1s; }
.role-card:nth-child(2) { animation-delay: 0.2s; }
.role-card:nth-child(3) { animation-delay: 0.3s; }
.role-card:nth-child(4) { animation-delay: 0.4s; }
.role-card:nth-child(5) { animation-delay: 0.5s; }

/* 悬浮时的流动边框效果 */
.role-card:hover {
  z-index: 10;  /* 确保悬浮卡片在最上层 */
  transition: all 0.4s ease;
}

.role-card.selected {
  z-index: 15;
}

/* 添加科技风流动边框效果 */
.role-card:hover::before {
  content: '';
  position: absolute;
  top: -3px;
  left: -3px;
  right: -3px;
  bottom: -3px;
  background: linear-gradient(
    90deg,
    rgba(0, 255, 255, 0.8),
    rgba(0, 150, 255, 1),
    rgba(100, 200, 255, 0.8),
    rgba(0, 255, 255, 1),
    rgba(0, 150, 255, 0.6),
    rgba(255, 255, 255, 0.9),
    rgba(0, 255, 255, 0.8)
  );
  background-size: 300% 100%;
  border-radius: 12px;
  z-index: -1;
  animation: techFlowingBorder 2s linear infinite;
  filter: blur(1px);
}

/* 添加内层流动线条 */
.role-card:hover::after {
  content: '';
  position: absolute;
  top: -1px;
  left: -1px;
  right: -1px;
  bottom: -1px;
  background: linear-gradient(
    45deg,
    transparent,
    rgba(0, 255, 255, 0.6),
    transparent,
    rgba(0, 150, 255, 0.8),
    transparent,
    rgba(0, 255, 255, 0.6),
    transparent
  );
  background-size: 200% 200%;
  border-radius: 10px;
  z-index: -1;
  animation: techInnerFlow 1.5s linear infinite reverse;
}

/* 科技风流动边框动画 */
@keyframes techFlowingBorder {
  0% {
    background-position: 0% 0%;
  }
  100% {
    background-position: 300% 0%;
  }
}

/* 内层流动动画 */
@keyframes techInnerFlow {
  0% {
    background-position: 0% 0%;
  }
  100% {
    background-position: 200% 200%;
  }
}

/* 箭头浮动动画 */
@keyframes arrowFloat {
  0% {
    transform: translateY(0px) scale(1);
  }
  100% {
    transform: translateY(-8px) scale(1.1);
  }
}

.card-glow {
  position: absolute;
  top: -8px;
  left: -8px;
  right: -8px;
  bottom: -8px;
  background: linear-gradient(
    45deg,
    rgba(0, 255, 255, 0.4),
    rgba(0, 150, 255, 0.6),
    rgba(255, 100, 200, 0.4),
    rgba(0, 255, 255, 0.4)
  );
  background-size: 400% 400%;
  border-radius: 16px;
  opacity: 0;
  transition: all 0.6s ease;
  filter: blur(12px);
  animation: glowGradientShift 3s ease-in-out infinite;
}

/* 悬浮时关闭原有发光效果，使用流动边框 */
.role-card:hover .card-glow {
  opacity: 0;
  transition: opacity 0.4s ease;
}

.card-glow.active {
  opacity: 1;
  animation: cardPulse 2s ease-in-out infinite, glowGradientShift 3s ease-in-out infinite;
}

/* 渐变色动画 */
@keyframes glowGradientShift {
  0%, 100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
}

.card-inner {
  position: relative;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    145deg,
    rgba(0, 30, 80, 0.95),
    rgba(0, 50, 120, 0.9),
    rgba(0, 30, 80, 0.95)
  );
  border-radius: 8px;
  border: 2px solid rgba(0, 255, 255, 0.3);
  backdrop-filter: blur(15px);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 20px;
  box-shadow: 
    0 10px 30px rgba(0, 0, 0, 0.5),
    inset 0 1px 0 rgba(255, 255, 255, 0.1),
    0 0 20px rgba(0, 255, 255, 0.1);
  transition: all 0.5s ease;
}

.role-card:hover .card-inner {
  border-color: rgba(0, 255, 255, 0.9);
  border-width: 2px;
  background: linear-gradient(
    145deg,
    rgba(15, 45, 95, 0.98),
    rgba(25, 75, 145, 0.95),
    rgba(15, 45, 95, 0.98)
  );
  box-shadow: 
    0 15px 35px rgba(0, 0, 0, 0.6),
    inset 0 1px 0 rgba(255, 255, 255, 0.2),
    inset 0 0 10px rgba(0, 255, 255, 0.1);
  transition: all 0.4s ease;
}

.role-card.selected .card-inner {
  border-color: rgba(0, 255, 255, 0.8);
  background: linear-gradient(
    145deg,
    rgba(20, 40, 80, 0.95),
    rgba(40, 80, 160, 0.9),
    rgba(20, 40, 80, 0.95)
  );
}

.role-3d-icon {
  position: relative;
  /* 🎯 修改图标容器大小 */
  width: 240px;   /* 图标容器宽度 - 调整此值改变图标区域大小 */
  height: 240px;  /* 图标容器高度 - 调整此值改变图标区域大小 */
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-platform {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  transform-style: preserve-3d;
}

  .tech-icon {
    /* 🖼️ 修改图标实际大小 */
    width: 240px;   /* 图标实际宽度 - 调整此值改变图标显示大小 */
    height: 240px;  /* 图标实际高度 - 调整此值改变图标显示大小 */
    object-fit: contain;
    filter: drop-shadow(0 0 20px rgba(0, 255, 255, 0.6));
    transition: all 0.5s ease;
    animation: iconFloat 3s ease-in-out infinite;
  }

.role-card:hover .tech-icon {
  filter: 
    drop-shadow(0 0 25px rgba(0, 255, 255, 0.8))
    brightness(1.1)
    contrast(1.1);
  transform: scale(1.05);  /* 轻微放大 */
  transition: all 0.4s ease;
}

.role-card.selected .tech-icon {
  filter: drop-shadow(0 0 40px rgba(0, 255, 255, 1));
  transform: scale(1.15);
}

.icon-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 260px;
  height: 260px;
  transform: translate(-50%, -50%);
  background: radial-gradient(
    circle,
    rgba(0, 255, 255, 0.2),
    rgba(0, 255, 255, 0.1),
    transparent 70%
  );
  border-radius: 50%;
  animation: iconGlow 2s ease-in-out infinite alternate;
}

.role-name {
  font-size: 20px;
  font-weight: 700;
  color: #ffffff;
  text-align: center;
  text-shadow: 0 0 15px rgba(0, 255, 255, 0.6);
  letter-spacing: 1px;
  transition: all 0.3s ease;
}

.role-card:hover .role-name {
  color: #ffffff;
  text-shadow: 
    0 0 15px rgba(0, 255, 255, 0.9),
    0 0 25px rgba(0, 150, 255, 0.6);
  animation: textPulse 2s ease-in-out infinite alternate;
}

/* 文字脉冲动画 */
@keyframes textPulse {
  0% {
    text-shadow: 
      0 0 15px rgba(0, 255, 255, 0.9),
      0 0 25px rgba(0, 150, 255, 0.6);
  }
  100% {
    text-shadow: 
      0 0 20px rgba(0, 255, 255, 1),
      0 0 35px rgba(0, 150, 255, 0.8);
  }
}

.role-card.selected .role-name {
  color: #00ffff;
  text-shadow: 0 0 25px rgba(0, 255, 255, 1);
  animation: textGlow 1.5s ease-in-out infinite alternate;
}



.card-base {
  position: absolute;
  bottom: -12px;
  left: 10px;
  right: 10px;
  height: 8px;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(0, 255, 255, 0.4),
    rgba(0, 150, 255, 0.6),
    rgba(0, 255, 255, 0.4),
    transparent
  );
  border-radius: 4px;
  transform: perspective(100px) rotateX(45deg);
  box-shadow: 0 2px 10px rgba(0, 255, 255, 0.3);
  animation: cardBasePulse 3s ease-in-out infinite alternate;
}





/* 确认按钮 */
.action-section {
  position: absolute;
  bottom: 120px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 200;
}

.tech-confirm-button {
  position: relative;
  width: 200px;
  height: 60px;
  background: linear-gradient(
    145deg,
    rgba(0, 100, 200, 0.8),
    rgba(0, 150, 255, 0.9),
    rgba(0, 100, 200, 0.8)
  );
  border: 2px solid rgba(0, 255, 255, 0.6);
  border-radius: 8px;
  color: #ffffff;
  font-family: 'Orbitron', monospace;
  font-size: 16px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.23, 1, 0.32, 1);
  backdrop-filter: blur(10px);
}

.tech-confirm-button:hover {
  transform: translateY(-3px) scale(1.05);
  border-color: rgba(0, 255, 255, 1);
  box-shadow: 
    0 10px 30px rgba(0, 255, 255, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.tech-confirm-button:active {
  transform: translateY(-1px) scale(1.02);
}

.button-text {
  position: relative;
  z-index: 2;
  display: block;
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
}

.button-glow {
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  background: linear-gradient(
    45deg,
    rgba(0, 255, 255, 0.4),
    rgba(0, 150, 255, 0.6),
    rgba(0, 255, 255, 0.4)
  );
  border-radius: 10px;
  opacity: 0;
  transition: opacity 0.3s ease;
  filter: blur(8px);
  z-index: 1;
}

.tech-confirm-button:hover .button-glow {
  opacity: 1;
  animation: rotateGlow 2s linear infinite;
}

.button-particles {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 3;
}

.tech-confirm-button:hover .button-particles::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    radial-gradient(1px 1px at 10% 20%, rgba(255, 255, 255, 0.8), transparent),
    radial-gradient(1px 1px at 80% 80%, rgba(0, 255, 255, 0.6), transparent),
    radial-gradient(1px 1px at 90% 10%, rgba(255, 255, 255, 0.4), transparent);
  background-size: 50px 50px;
  animation: sparkle 1.5s linear infinite;
}

/* 动画效果 */
@keyframes breathe {
  0%, 100% { opacity: 0.6; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.05); }
}

@keyframes sparkle {
  0% { transform: translateY(0) rotate(0deg); }
  100% { transform: translateY(-100px) rotate(360deg); }
}

@keyframes gridMove {
  0% { transform: translate(0, 0); }
  100% { transform: translate(50px, 50px); }
}

/* 顶部栏动画 */
@keyframes topBarGlow {
  0% { opacity: 0.6; }
  100% { opacity: 1; }
}

@keyframes linePulse {
  0%, 100% { opacity: 0.3; transform: scaleX(0.5); }
  50% { opacity: 1; transform: scaleX(1); }
}

@keyframes particlesMove {
  0% { transform: translateX(0); }
  100% { transform: translateX(100px); }
}

@keyframes dateTimeGlow {
  0% { opacity: 0.6; }
  100% { opacity: 1; }
}

@keyframes titleBgPulse {
  0% { opacity: 0.6; transform: translate(-50%, -50%) scaleX(0.8); }
  100% { opacity: 1; transform: translate(-50%, -50%) scaleX(1); }
}

@keyframes titleTextGlow {
  0% { 
    text-shadow: 
      0 0 25px rgba(0, 255, 255, 1),
      0 0 50px rgba(0, 255, 255, 0.6),
      0 0 75px rgba(0, 255, 255, 0.3);
  }
  100% { 
    text-shadow: 
      0 0 35px rgba(0, 255, 255, 1),
      0 0 70px rgba(0, 255, 255, 0.8),
      0 0 100px rgba(0, 255, 255, 0.5);
  }
}

@keyframes decoSlideLeft {
  0% { transform: translateY(-50%) translateX(0); opacity: 0.6; }
  100% { transform: translateY(-50%) translateX(-20px); opacity: 1; }
}

@keyframes decoSlideRight {
  0% { transform: translateY(-50%) rotate(180deg) translateX(0); opacity: 0.6; }
  100% { transform: translateY(-50%) rotate(180deg) translateX(-20px); opacity: 1; }
}

@keyframes iconRingPulse {
  0%, 100% { opacity: 0.6; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.1); }
}

@keyframes titleGradient {
  0%, 100% { background-position: 0% 50%; }
  25% { background-position: 100% 50%; }
  50% { background-position: 100% 100%; }
  75% { background-position: 0% 100%; }
}



@keyframes userInfoGlow {
  0% {
    box-shadow: 0 0 20px rgba(0, 255, 255, 0.2);
  }
  100% {
    box-shadow: 0 0 30px rgba(0, 255, 255, 0.4);
  }
}

@keyframes avatarFloat {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
  }
  25% {
    transform: translateY(-2px) rotate(1deg);
  }
  75% {
    transform: translateY(2px) rotate(-1deg);
  }
}

@keyframes usernameGlow {
  0% {
    text-shadow: 0 0 12px rgba(0, 255, 255, 0.8);
  }
  100% {
    text-shadow: 0 0 18px rgba(0, 255, 255, 1);
  }
}

@keyframes btnFloat {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-2px);
  }
}

@keyframes btnGlowRotate {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

@keyframes arrowBounce {
  0%, 100% {
    transform: translateY(-50%) translateX(0);
  }
  50% {
    transform: translateY(-50%) translateX(5px);
  }
}





@keyframes cardPulse {
  0%, 100% { opacity: 0.6; }
  50% { opacity: 1; }
}

@keyframes iconFloat {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  33% { transform: translateY(-5px) rotate(1deg); }
  66% { transform: translateY(3px) rotate(-1deg); }
}

@keyframes iconGlow {
  0% { opacity: 0.3; transform: translate(-50%, -50%) scale(1); }
  100% { opacity: 0.6; transform: translate(-50%, -50%) scale(1.1); }
}

@keyframes textGlow {
  0% { text-shadow: 0 0 25px rgba(0, 255, 255, 1); }
  100% { text-shadow: 0 0 35px rgba(0, 255, 255, 1), 0 0 50px rgba(0, 255, 255, 0.8); }
}



/* 新的动画关键帧 */




@keyframes dotPulse {
  0%, 100% {
    opacity: 0.4;
    transform: scale(1);
  }
  50% {
    opacity: 1;
    transform: scale(1.2);
  }
}







@keyframes platformGlow {
  0% { opacity: 0.6; }
  100% { opacity: 1; }
}

@keyframes rotateGlow {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes cardBasePulse {
  0% { 
    opacity: 0.6; 
    box-shadow: 0 2px 10px rgba(0, 255, 255, 0.3);
  }
  100% { 
    opacity: 1; 
    box-shadow: 0 4px 20px rgba(0, 255, 255, 0.6);
  }
}

/* 网格项淡入动画 */
@keyframes gridItemFadeIn {
  0% {
    opacity: 0;
    transform: translateY(50px) scale(0.8) rotateY(-15deg);
  }
  60% {
    opacity: 0.8;
    transform: translateY(-10px) scale(1.05) rotateY(5deg);
  }
  100% {
    opacity: 1;
    transform: translateY(0) scale(1) rotateY(0deg);
  }
}

/* 响应式设计 - 🔧 修改不同屏幕尺寸下的卡片和图标大小 */
@media (max-width: 1600px) {
  .roles-grid {
    grid-template-columns: repeat(5, minmax(260px, 1fr));  /* 保持5列，但减小最小宽度 */
    gap: 45px;      /* 减少网格间距 */
    max-width: 1650px;
  }
  
  .role-card {
    /* 📦 1600px以下屏幕的卡片尺寸 */
    width: 260px;   /* 调整卡片宽度 */
    height: 320px;  /* 调整卡片高度 */
  }
  
      .tech-icon {
      /* 🖼️ 1600px以下屏幕的图标尺寸 */
      width: 220px;   /* 调整图标宽度 */
      height: 220px;  /* 调整图标高度 */
    }
  
  .role-3d-icon {
    /* 🎯 1600px以下屏幕的图标容器尺寸 */
    width: 220px;   /* 调整图标容器宽度 */
    height: 220px;  /* 调整图标容器高度 */
  }
  
  .icon-glow {
    width: 260px;
    height: 260px;
  }
  
  .platform-base {
    width: 1600px;
  }
}

@media (max-width: 1400px) {
  .roles-grid {
    grid-template-columns: repeat(4, minmax(220px, 1fr));  /* 改为4列布局 */
    gap: 35px;      /* 保持舒适的视觉间距 */
    max-width: 1300px;
  }
  
  .role-card {
    /* 📦 1400px以下屏幕的卡片尺寸 */
    width: 220px;   /* 调整卡片宽度 */
    height: 280px;  /* 调整卡片高度 */
  }
  
  .tech-icon {
    /* 🖼️ 1400px以下屏幕的图标尺寸 */
    width: 180px;   /* 调整图标宽度 */
    height: 180px;  /* 调整图标高度 */
  }
  
  .role-3d-icon {
    /* 🎯 1400px以下屏幕的图标容器尺寸 */
    width: 180px;   /* 调整图标容器宽度 */
    height: 180px;  /* 调整图标容器高度 */
  }
  
  .platform-base {
    width: 1200px;
  }
}

@media (max-width: 1200px) {
  .roles-grid {
    grid-template-columns: repeat(3, minmax(200px, 1fr));  /* 改为3列布局 */
    gap: 30px;      /* 即使在较小屏幕上也保持良好间距 */
    max-width: 900px;
  }
  
  .role-card {
    /* 📦 1200px以下屏幕的卡片尺寸 */
    width: 200px;   /* 调整卡片宽度 */
    height: 260px;  /* 调整卡片高度 */
  }
  
  .tech-icon {
    /* 🖼️ 1200px以下屏幕的图标尺寸 */
    width: 140px;   /* 调整图标宽度 */
    height: 140px;  /* 调整图标高度 */
  }
  
  .role-3d-icon {
    /* 🎯 1200px以下屏幕的图标容器尺寸 */
    width: 160px;   /* 调整图标容器宽度 */
    height: 160px;  /* 调整图标容器高度 */
  }
  
  .platform-base {
    width: 1000px;
  }
}

/* 超小屏幕 (480px以下) - 单列布局 */
@media (max-width: 480px) {
  .roles-grid {
    grid-template-columns: 1fr;  /* 单列布局，让卡片完全填充宽度 */
    gap: 20px;
    max-width: 300px;
  }
  
  .role-card {
    width: 100%;    /* 卡片填充整个网格单元 */
    min-width: 250px;
    height: 280px;
  }
  
  .tech-icon {
    width: 100px;
    height: 100px;
  }
  
  .role-3d-icon {
    width: 120px;
    height: 120px;
  }
}

@media (max-width: 768px) {

  .roles-grid {
    grid-template-columns: repeat(2, minmax(160px, 1fr));  /* 手机端改为2列布局 */
    gap: 25px;      /* 手机端也保持合适的间距 */
    max-width: 650px;
  }
  
  .role-card {
    /* 📦 768px以下屏幕(手机)的卡片尺寸 */
    width: 160px;   /* 调整卡片宽度 */
    height: 220px;  /* 调整卡片高度 */
  }
  
  .tech-icon {
    /* 🖼️ 768px以下屏幕(手机)的图标尺寸 */
    width: 120px;   /* 调整图标宽度 */
    height: 120px;  /* 调整图标高度 */
  }
  
  .role-3d-icon {
    /* 🎯 768px以下屏幕(手机)的图标容器尺寸 */
    width: 140px;   /* 调整图标容器宽度 */
    height: 140px;  /* 调整图标容器高度 */
  }
    
  .role-name {
    font-size: 16px;
  }
    
  .platform-base {
    width: 800px;
  }
  
  .tech-confirm-button {
    width: 160px;
    height: 50px;
    font-size: 14px;
  }
}
</style> 