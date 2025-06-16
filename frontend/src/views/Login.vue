<template>
  <div class="login-container">
    <!-- 动态背景 -->
    <div class="background-overlay">
      <!-- 渐变网格 -->
      <div class="gradient-grid"></div>
      
      <!-- 浮动粒子 -->
      <div class="particles">
        <div class="particle" v-for="i in 15" :key="i" :style="getParticleStyle(i)"></div>
      </div>
      
      <!-- 光效 -->
      <div class="light-effects">
        <div class="light light-1"></div>
        <div class="light light-2"></div>
        <div class="light light-3"></div>
      </div>
    </div>
    
    <!-- 主要内容区域 -->
    <div class="main-content">
      <!-- 左侧图片区域 -->
      <div class="welcome-section">
        <!-- 标题区域 -->
        <div class="title-section">
          <img src="@/assets/icon/00005.png" alt="系统标题" class="title-image" />
          <div class="subtitle-text">智能化 协同高效 安全可靠</div>
        </div>
        <!-- 主图片区域 -->
        <div class="login-image-container">
          <img src="@/assets/image/login.png" alt="登录页面" class="login-background-image" />
        </div>
      </div>
      
      <!-- 右侧登录区域 -->
      <div class="login-section">
        <div class="login-card">
          <!-- 卡片头部 -->
          <div class="card-header">
            <h2 class="login-title">欢迎回来</h2>
          </div>
          
          <!-- 登录表单 -->
          <div class="card-body">
            <el-form
              ref="loginFormRef"
              :model="loginForm"
              :rules="loginRules"
              class="login-form"
              @submit.prevent="handleLogin"
            >
              <!-- 登录类型选择 -->
              <div class="form-section">
                <h3 class="section-title">选择您的身份</h3>
                <el-form-item prop="loginType">
                  <div class="role-selector-wrapper">
                    <!-- 背景滑块 -->
                    <div class="selector-background">
                      <div 
                        class="active-indicator"
                        :class="{ 'move-right': loginForm.loginType === '操作员' }"
                      ></div>
                    </div>
                    
                    <!-- 角色选项 -->
                    <div class="role-tabs">
                      <div 
                        v-for="(role, index) in roles" 
                        :key="role.value"
                        class="role-tab"
                        :class="{ 
                          active: loginForm.loginType === role.value,
                          'tab-left': index === 0,
                          'tab-right': index === 1
                        }"
                        @click="selectRole(role.value)"
                      >
                        <div class="tab-content">
                          <div class="tab-icon">
                            <div class="icon-wrapper">
                              <el-icon :size="24">
                                <component :is="role.icon" />
                              </el-icon>
                            </div>
                            <div class="icon-glow"></div>
                          </div>
                          <div class="tab-text">
                            <h4>{{ role.title }}</h4>
                            <p>{{ role.subtitle }}</p>
                          </div>
                        </div>
                      </div>
                    </div>
                    
                    <!-- 角色详情卡片 -->
                    <div class="role-details">
                      <transition name="role-fade" mode="out-in">
                        <div 
                          :key="loginForm.loginType"
                          class="role-detail-card"
                        >
                          <div class="detail-header">
                            <div class="detail-icon">
                              <el-icon :size="20">
                                <component :is="currentRole.icon" />
                              </el-icon>
                            </div>
                            <h5>{{ currentRole.title }}</h5>
                          </div>
                          <p class="detail-description">{{ currentRole.description }}</p>
                          <div class="permissions-list">
                            <div 
                              v-for="permission in currentRole.permissions" 
                              :key="permission"
                              class="permission-item"
                            >
                              <el-icon size="14"><Check /></el-icon>
                              <span>{{ permission }}</span>
                            </div>
                          </div>
                        </div>
                      </transition>
                    </div>
                  </div>
                </el-form-item>
              </div>

              <!-- 用户名输入 -->
              <div class="form-section">
                <h3 class="section-title">账户信息</h3>
                <el-form-item prop="username" :show-message="false">
                  <div class="input-wrapper">
                    <el-input
                      v-model="loginForm.username"
                      placeholder="请输入您的用户名"
                      size="large"
                      class="custom-input"
                      clearable
                      @keyup.enter="handleLogin"
                    >
                      <template #prefix>
                        <el-icon class="input-icon"><User /></el-icon>
                      </template>
                    </el-input>
                  </div>
                </el-form-item>
                
                <!-- 密码输入 -->
                <el-form-item prop="password" :show-message="false">
                  <div class="input-wrapper">
                    <el-input
                      v-model="loginForm.password"
                      type="password"
                      placeholder="请输入您的密码"
                      size="large"
                      class="custom-input"
                      show-password
                      clearable
                      @keyup.enter="handleLogin"
                    >
                      <template #prefix>
                        <el-icon class="input-icon"><Lock /></el-icon>
                      </template>
                    </el-input>
                  </div>
                </el-form-item>
              </div>
              
              <!-- 登录按钮 -->
              <el-form-item class="login-button-section">
                <el-button
                  type="primary"
                  size="large"
                  :loading="loading"
                  class="login-button"
                  @click="handleLogin"
                >
                  <template v-if="!loading">
                    <el-icon><Right /></el-icon>
                    登录系统
                  </template>
                  <template v-else>
                    登录中...
                  </template>
                </el-button>
              </el-form-item>
            </el-form>
          </div>
          

        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { 
  User, UserFilled, Lock, Right, Check, InfoFilled
} from '@element-plus/icons-vue'
import { useAuthStore } from '@/store/modules/auth'
import type { LoginForm } from '@/types/user'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

// 表单引用
const loginFormRef = ref<FormInstance>()

// 登录表单数据
const loginForm = reactive<LoginForm>({
  username: '',
  password: '',
  loginType: '管理员'
})

// 角色选项
const roles = [
  {
    value: '管理员',
    title: '系统管理员',
    subtitle: '全权管理',
    description: '拥有系统全部权限，可以管理用户、配置系统设置',
    icon: UserFilled,
    permissions: ['用户管理', '系统设置', '设备管理', '任务调度']
  },
  {
    value: '操作员',
    title: '系统操作员',
    subtitle: '日常运维',
    description: '负责日常运维操作，获取任务，执行监控和维护任务',
    icon: User,
    permissions: ['设备监控', '任务执行', '数据查看', '报告生成']
  }
]



// 表单验证规则
const loginRules: FormRules = {
  loginType: [
    { required: true, message: '请选择登录类型', trigger: 'change' }
  ],
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 2, max: 50, message: '用户名长度应在2-50个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 50, message: '密码长度应在6-50个字符', trigger: 'blur' }
  ]
}

// 加载状态
const loading = ref(false)

// 粒子样式
const getParticleStyle = (index: number) => {
  const size = Math.random() * 6 + 2
  const left = Math.random() * 100
  const animationDelay = Math.random() * 20
  const animationDuration = Math.random() * 10 + 15
  
  return {
    width: `${size}px`,
    height: `${size}px`,
    left: `${left}%`,
    animationDelay: `${animationDelay}s`,
    animationDuration: `${animationDuration}s`
  }
}

// 选择角色
const selectRole = (roleValue: string) => {
  loginForm.loginType = roleValue
}

// 当前选中的角色
const currentRole = computed(() => {
  return roles.find(role => role.value === loginForm.loginType) || roles[0]
})

// 处理登录
const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  try {
    await loginFormRef.value.validate()
    loading.value = true
    
    const loginResponse = await authStore.loginAction(loginForm)
    const user = loginResponse.user
    
    // 验证用户类型是否匹配
    if (user.type !== loginForm.loginType) {
      ElMessage.error(`您的账户类型是"${user.type}"，请选择正确的登录类型`)
      return
    }
    
    ElMessage.success('登录成功！')
    
    // 根据用户类型进行不同的跳转
    if (user.type === '管理员') {
      // 管理员直接进入主页面
      const redirect = route.query.redirect as string
      router.push(redirect || '/dashboard')
    } else if (user.type === '操作员') {
      // 操作员进入角色选择界面
      router.push('/role-selection')
    }
    
  } catch (error: any) {
    console.error('登录失败:', error)
    ElMessage.error(error.response?.data?.detail || '登录失败，请检查用户名和密码')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped lang="scss">
// 全局容器
.login-container {
  position: relative;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

// 背景层
.background-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, 
    #667eea 0%, 
    #764ba2 25%, 
    #954d9d 50%, 
    #764ba2 75%, 
    #667eea 100%);
  background-size: 400% 400%;
  animation: gradientShift 15s ease infinite;
}

@keyframes gradientShift {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

// 渐变网格
.gradient-grid {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px);
  background-size: 50px 50px;
  animation: gridMove 20s linear infinite;
}

@keyframes gridMove {
  0% { transform: translate(0, 0); }
  100% { transform: translate(50px, 50px); }
}

// 浮动粒子
.particles {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  
  .particle {
    position: absolute;
    background: rgba(255, 255, 255, 0.6);
    border-radius: 50%;
    animation: particleFloat linear infinite;
  }
}

@keyframes particleFloat {
  0% {
    transform: translateY(100vh) rotate(0deg);
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    transform: translateY(-100px) rotate(360deg);
    opacity: 0;
  }
}

// 光效
.light-effects {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  
  .light {
    position: absolute;
    border-radius: 50%;
    filter: blur(40px);
    animation: lightPulse 4s ease-in-out infinite alternate;
    
    &.light-1 {
      width: 300px;
      height: 300px;
      background: rgba(148, 163, 184, 0.2);
      top: 20%;
      left: 10%;
      animation-delay: 0s;
    }
    
    &.light-2 {
      width: 400px;
      height: 400px;
      background: rgba(203, 213, 225, 0.15);
      top: 50%;
      right: 15%;
      animation-delay: 1.5s;
    }
    
    &.light-3 {
      width: 250px;
      height: 250px;
      background: rgba(100, 116, 139, 0.2);
      bottom: 20%;
      left: 20%;
      animation-delay: 3s;
    }
  }
}

@keyframes lightPulse {
  0% { transform: scale(1) rotate(0deg); opacity: 0.3; }
  100% { transform: scale(1.2) rotate(180deg); opacity: 0.6; }
}

// 主要内容区域
.main-content {
  position: relative;
  z-index: 10;
  display: grid;
  grid-template-columns: 1fr 450px;
  width: 100%;
  height: 100vh;
  min-height: 700px;
}

// 左侧图片区域
.welcome-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
  
  .title-section {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    padding-left: 60px;
    margin-bottom: 20px;
    margin-top: 40px;
    
    .title-image {
      max-width: 90%;
      height: auto;
      object-fit: contain;
      transform: scale(1.2);
      transform-origin: left center;
    }
    
    .subtitle-text {
      color: white;
      font-size: 18px;
      font-weight: 500;
      margin-top: 15px;
      letter-spacing: 2px;
      text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
  }
  
  .login-image-container {
    width: 100%;
    flex: 1;
    display: flex;
    align-items: flex-start;
    justify-content: center;
    margin-top: 30px;
    
    .login-background-image {
      width: 80%;
      height: 80%;
      object-fit: contain;
    }
  }
}



// 右侧登录区域
.login-section {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
}

.login-card {
  width: 100%;
  max-width: 400px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  overflow: hidden;
  animation: cardSlideIn 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

@keyframes cardSlideIn {
  0% {
    opacity: 0;
    transform: translateX(40px) scale(0.95);
  }
  100% {
    opacity: 1;
    transform: translateX(0) scale(1);
  }
}

.card-header {
  padding: 28px 28px 24px;
  text-align: center;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  
  .login-title {
    font-size: 24px;
    font-weight: 700;
    color: #1a202c;
    margin: 0;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
}

.card-body {
  padding: 24px 28px 20px;
}

// 表单样式
.login-form {
  .form-section {
    margin-bottom: 20px;
    
    .section-title {
      font-size: 15px;
      font-weight: 600;
      color: #374151;
      margin: 0 0 14px 0;
      display: flex;
      align-items: center;
      gap: 6px;
      
      &::before {
        content: '';
        width: 3px;
        height: 14px;
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 2px;
      }
    }
  }
  
  // 角色选择器
  .role-selector-wrapper {
    position: relative;
    
    // 背景滑块
    .selector-background {
      position: relative;
      height: 56px;
      background: rgba(248, 250, 252, 0.8);
      border-radius: 14px;
      border: 2px solid #e5e7eb;
      margin-bottom: 16px;
      overflow: hidden;
      
      .active-indicator {
        position: absolute;
        top: 4px;
        left: 4px;
        width: calc(50% - 4px);
        height: calc(100% - 8px);
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 
          0 4px 12px rgba(102, 126, 234, 0.3),
          0 2px 4px rgba(102, 126, 234, 0.2);
        
        &::before {
          content: '';
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          background: linear-gradient(135deg, rgba(255,255,255,0.2) 0%, transparent 100%);
          border-radius: 12px;
        }
        
        &.move-right {
          transform: translateX(100%);
        }
      }
    }
    
    // 角色标签页
    .role-tabs {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 56px;
      display: flex;
      z-index: 2;
      
      .role-tab {
        flex: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s ease;
        min-width: 0;
        position: relative;
        
        &.active {
          .tab-content {
            .tab-icon {
              .icon-wrapper {
                color: white !important;
                transform: scale(1.1);
              }
              
              .icon-glow {
                opacity: 1;
                animation: iconPulse 2s ease-in-out infinite;
              }
            }
            
            .tab-text {
              h4 {
                color: white !important;
                font-weight: 700 !important;
                font-size: 13px !important;
                line-height: 1.3 !important;
              }
              
              p {
                color: rgba(255, 255, 255, 0.9) !important;
                font-size: 11px !important;
                line-height: 1.3 !important;
              }
            }
          }
        }
        
        // 确保两个角色卡片样式完全一致
        &:first-child.active,
        &:last-child.active {
          .tab-content {
            .tab-icon {
              .icon-wrapper {
                color: white !important;
                transform: scale(1.1);
              }
            }
            
            .tab-text {
              h4 {
                color: white !important;
                font-weight: 700 !important;
                font-size: 13px !important;
                line-height: 1.3 !important;
                margin: 0 !important;
              }
              
              p {
                color: rgba(255, 255, 255, 0.9) !important;
                font-size: 11px !important;
                line-height: 1.3 !important;
                margin: 0 !important;
              }
            }
          }
        }
        
        .tab-content {
          display: flex;
          align-items: center;
          gap: 8px;
          padding: 12px 14px;
          width: 100%;
          height: 100%;
          box-sizing: border-box;
          
          .tab-icon {
            position: relative;
            flex-shrink: 0;
            width: 24px;
            height: 24px;
            
            .icon-wrapper {
              display: flex;
              align-items: center;
              justify-content: center;
              color: #667eea !important;
              transition: all 0.3s ease;
              width: 100%;
              height: 100%;
              
              .el-icon {
                font-size: 24px !important;
              }
            }
            
            .icon-glow {
              position: absolute;
              top: 50%;
              left: 50%;
              width: 40px;
              height: 40px;
              background: radial-gradient(circle, rgba(255,255,255,0.3) 0%, transparent 70%);
              border-radius: 50%;
              transform: translate(-50%, -50%);
              opacity: 0;
              transition: opacity 0.3s ease;
            }
          }
          
          .tab-text {
            flex: 1;
            min-width: 0;
            
            h4 {
              font-size: 13px !important;
              font-weight: 600 !important;
              color: #6b7280 !important;
              margin: 0 !important;
              line-height: 1.3 !important;
              transition: all 0.3s ease;
            }
            
            p {
              font-size: 11px !important;
              color: #9ca3af !important;
              margin: 0 !important;
              line-height: 1.3 !important;
              transition: all 0.3s ease;
            }
          }
        }
      }
    }
    
    // 角色详情卡片
    .role-details {
      margin-top: 14px;
      
      .role-detail-card {
        padding: 16px;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.02), rgba(118, 75, 162, 0.02));
        border: 1px solid rgba(102, 126, 234, 0.1);
        border-radius: 12px;
        position: relative;
        overflow: hidden;
        
        &::before {
          content: '';
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 2px;
          background: linear-gradient(90deg, #667eea, #764ba2);
        }
        
        .detail-header {
          display: flex;
          align-items: center;
          gap: 10px;
          margin-bottom: 10px;
          
          .detail-icon {
            width: 32px;
            height: 32px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 8px;
            color: white;
            box-shadow: 0 3px 8px rgba(102, 126, 234, 0.3);
          }
          
          h5 {
            font-size: 15px;
            font-weight: 600;
            color: #374151;
            margin: 0;
          }
        }
        
        .detail-description {
          font-size: 13px;
          color: #6b7280;
          line-height: 1.5;
          margin: 0 0 14px 0;
          word-wrap: break-word;
          overflow-wrap: break-word;
        }
        
        .permissions-list {
          display: grid;
          grid-template-columns: repeat(2, 1fr);
          gap: 8px;
          
          .permission-item {
            display: flex;
            align-items: center;
            gap: 6px;
            padding: 6px 10px;
            background: rgba(16, 185, 129, 0.05);
            border: 1px solid rgba(16, 185, 129, 0.1);
            border-radius: 6px;
            font-size: 12px;
            color: #374151;
            transition: all 0.3s ease;
            
            &:hover {
              background: rgba(16, 185, 129, 0.1);
              transform: translateY(-1px);
            }
            
            .el-icon {
              color: #10b981;
            }
          }
        }
      }
    }
  }
  
  @keyframes iconPulse {
    0%, 100% { 
      opacity: 0.6; 
      transform: translate(-50%, -50%) scale(1);
    }
    50% { 
      opacity: 1; 
      transform: translate(-50%, -50%) scale(1.2);
    }
  }
  
  // 角色切换动画
  .role-fade-enter-active,
  .role-fade-leave-active {
    transition: all 0.3s ease;
  }
  
  .role-fade-enter-from {
    opacity: 0;
    transform: translateY(10px);
  }
  
  .role-fade-leave-to {
    opacity: 0;
    transform: translateY(-10px);
  }
  
  // 输入框样式
  .input-wrapper {
    position: relative;
    margin-bottom: 16px;
    width: 100%;
    
    .custom-input {
      width: 100%;
      
      :deep(.el-input__wrapper) {
        width: 100%;
        border-radius: 12px;
        border: 2px solid #e5e7eb;
        box-shadow: none;
        background: rgba(248, 250, 252, 0.8);
        backdrop-filter: blur(10px);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        padding: 2px 14px;
        
        &:hover {
          border-color: #c7d2fe;
          background: rgba(248, 250, 252, 0.95);
        }
        
        &.is-focus {
          border-color: #667eea;
          background: white;
          box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
          transform: translateY(-1px);
        }
      }
      
      :deep(.el-input__inner) {
        width: 100%;
        height: 42px;
        font-size: 14px;
        color: #374151;
        font-weight: 500;
        
        &::placeholder {
          color: #9ca3af;
        }
      }
      
      .input-icon {
        color: #667eea;
        font-size: 16px;
      }
    }
  }
  
  // 确保表单项宽度一致
  .el-form-item {
    width: 100%;
    margin-bottom: 0;
    
    :deep(.el-form-item__content) {
      width: 100%;
    }
  }
  
  // 登录按钮
  .login-button-section {
    margin-top: 20px;
    margin-bottom: 0;
  }
  
  .login-button {
    width: 100%;
    height: 44px;
    font-size: 15px;
    font-weight: 600;
    border-radius: 12px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border: none;
    box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
    
    &::before {
      content: '';
      position: absolute;
      top: 0;
      left: -100%;
      width: 100%;
      height: 100%;
      background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
      transition: left 0.5s ease;
    }
    
    &:hover {
      transform: translateY(-3px);
      box-shadow: 0 8px 32px rgba(102, 126, 234, 0.4);
      
      &::before {
        left: 100%;
      }
    }
    
    &:active {
      transform: translateY(-1px);
    }
    
    .el-icon {
      margin-right: 8px;
    }
  }
}

// 响应式设计
@media (max-width: 1200px) {
  .main-content {
    grid-template-columns: 1fr 380px;
  }
  
  .welcome-section {
    padding: 30px;
    
    .welcome-content .brand-section .brand-title {
      font-size: 32px;
    }
  }
  
  .login-card {
    max-width: 360px;
  }
}

@media (max-width: 1024px) {
  .main-content {
    grid-template-columns: 1fr 350px;
  }
  
  .login-card {
    max-width: 340px;
  }
  
  .card-header {
    padding: 24px 20px 20px;
  }
  
  .card-body {
    padding: 20px;
  }
  
  .card-footer {
    padding: 16px 20px 20px;
  }
}

@media (max-width: 768px) {
  .main-content {
    grid-template-columns: 1fr;
    min-height: 100vh;
  }
  
  .welcome-section {
    display: none;
  }
  
  .login-section {
    padding: 16px;
    background: none;
    border-left: none;
  }
  
  .login-card {
    max-width: 100%;
    max-height: none;
    border-radius: 16px;
  }
  
  .card-header {
    padding: 20px 20px 16px;
  }
  
  .card-body {
    padding: 16px 20px;
  }
  
  .card-footer {
    padding: 16px 20px 20px;
  }
  
  .form-section {
    margin-bottom: 20px;
  }
  
  .selector-background {
    height: 48px;
  }
  
  .role-tabs {
    height: 48px;
  }
}

@media (max-width: 480px) {
  .login-section {
    padding: 12px;
  }
  
  .login-card {
    border-radius: 12px;
  }
  
  .card-header {
    padding: 16px 16px 12px;
    
    .login-title {
      font-size: 20px;
    }
    
    .login-subtitle {
      font-size: 13px;
    }
  }
  
  .card-body {
    padding: 12px 16px;
  }
  
  .card-footer {
    padding: 12px 16px 16px;
  }
  
  .form-section {
    margin-bottom: 16px;
    
    .section-title {
      font-size: 14px;
      margin-bottom: 12px;
    }
  }
  
  .selector-background {
    height: 44px;
  }
  
  .role-tabs {
    height: 44px;
  }
  
  .role-detail-card {
    padding: 14px;
  }
  
  .login-button {
    height: 44px;
    font-size: 15px;
  }
  
  .demo-banner {
    flex-direction: column;
    text-align: center;
    padding: 12px;
    
    .demo-text h4 {
      font-size: 12px;
    }
    
    .demo-accounts {
      justify-content: center;
      gap: 4px;
      
      .account-tag {
        font-size: 10px;
        padding: 2px 4px;
      }
    }
  }
}
</style> 