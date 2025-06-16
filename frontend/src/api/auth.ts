import request from '@/utils/request'
import type { LoginForm, User, LoginResponse } from '@/types/user'

// 用户登录
export const login = (data: LoginForm) => {
  const formData = new FormData()
  formData.append('username', data.username)
  formData.append('password', data.password)
  formData.append('login_type', data.loginType)
  
  return request.post<LoginResponse>('/auth/login', formData, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  })
}

// 用户登出
export const logout = () => {
  return request.post('/auth/logout')
}

// 获取当前用户信息
export const getCurrentUser = () => {
  return request.get<User>('/auth/me')
}

// 刷新访问令牌
export const refreshToken = () => {
  return request.post<LoginResponse>('/auth/refresh')
} 