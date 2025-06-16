import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login, logout, getCurrentUser } from '@/api/auth'
import type { User, LoginForm, LoginResponse } from '@/types/user'

export const useAuthStore = defineStore('auth', () => {
  // 状态
  const token = ref<string>(localStorage.getItem('token') || '')
  const user = ref<User | null>(
    localStorage.getItem('user') ? JSON.parse(localStorage.getItem('user')!) : null
  )
  const loading = ref(false)

  // 计算属性
  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.type === '管理员')
  const isOperator = computed(() => 
    user.value?.type === '管理员' || user.value?.type === '操作员'
  )

  // 登录操作
  const loginAction = async (loginForm: LoginForm): Promise<LoginResponse> => {
    loading.value = true
    try {
      const response = await login(loginForm)
      const { access_token, user: userInfo } = response.data
      
      // 存储token和用户信息
      token.value = access_token
      user.value = userInfo
      
      localStorage.setItem('token', access_token)
      localStorage.setItem('user', JSON.stringify(userInfo))
      
      return response.data
    } catch (error) {
      throw error
    } finally {
      loading.value = false
    }
  }

  // 登出操作
  const logoutAction = async (skipApi = false) => {
    if (!skipApi && token.value) {
      try {
        await logout()
      } catch (error) {
        console.error('登出请求失败:', error)
        // 不要因为API调用失败就阻止清除本地状态
      }
    }
    
    // 清除本地存储
    token.value = ''
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    localStorage.removeItem('selectedRole')
  }

  // 获取当前用户信息
  const fetchCurrentUser = async () => {
    if (!token.value) return
    
    try {
      const response = await getCurrentUser()
      user.value = response.data
      localStorage.setItem('user', JSON.stringify(response.data))
    } catch (error) {
      console.error('获取用户信息失败:', error)
      // 如果获取失败，清除认证信息
      logoutAction()
    }
  }

  // 更新用户信息
  const updateUser = (newUser: User) => {
    user.value = newUser
    localStorage.setItem('user', JSON.stringify(newUser))
  }

  // 检查权限
  const hasPermission = (permission: string): boolean => {
    if (!user.value) return false
    
    // 管理员拥有所有权限
    if (user.value.type === '管理员') return true
    
    // 操作员权限检查
    if (user.value.type === '操作员') {
      const selectedRole = localStorage.getItem('selectedRole')
      
      // 操作员必须选择角色后才有权限
      if (!selectedRole) return false
      
      // 检查操作员的角色是否匹配
      if (selectedRole !== user.value.role) return false
      
      // 根据不同角色定义不同权限
      const rolePermissions: Record<string, string[]> = {
        '系统分析师': ['user:read', 'device:read', 'task:read'],
        '网络工程师': ['device:all', 'task:read'],
        '系统架构工程师': ['task:manage', 'device:all'],
        '数据运维工程师': ['task:manage', 'desktop:manage', 'device:all'],
        '孪生平台': ['desktop:manage', 'task:read', 'device:read']
      }
      
      const allowedPermissions = rolePermissions[selectedRole] || []
      return allowedPermissions.includes(permission)
    }
    
    return false
  }

  // 检查角色权限
  const hasRolePermission = (requiredRole: string): boolean => {
    if (!user.value) return false
    
    // 管理员拥有所有角色权限
    if (user.value.type === '管理员') return true
    
    // 操作员角色权限检查
    if (user.value.type === '操作员') {
      const selectedRole = localStorage.getItem('selectedRole')
      return selectedRole === requiredRole && selectedRole === user.value.role
    }
    
    return false
  }

      return {
    // 状态
    token,
    user,
    loading,
    
    // 计算属性
    isAuthenticated,
    isAdmin,
    isOperator,
    
    // 方法
    loginAction,
    logoutAction,
    fetchCurrentUser,
    updateUser,
    hasPermission,
    hasRolePermission
  }
}) 