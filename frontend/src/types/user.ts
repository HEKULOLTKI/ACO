// 用户基础接口
export interface User {
  id: number
  username: string
  role: string
  type: string
  status: string
  photo_data?: string
  created_at: string
  updated_at: string
}

// 登录表单
export interface LoginForm {
  username: string
  password: string
  loginType?: string
}

// 用户创建表单
export interface UserForm {
  username: string
  password: string
  role: string
  type: string
  status: string
}

// 用户更新表单
export interface UserUpdate {
  role?: string
  type?: string
  status?: string
  photo_data?: string
}

// 用户档案
export interface UserProfile {
  id: number
  username: string
  role: string
  type: string
  status: string
  photo_data?: string
}

// 登录响应
export interface LoginResponse {
  access_token: string
  token_type: string
  user: User
}

// 用户状态选项
export const USER_STATUS_OPTIONS = [
  { label: '活跃', value: 'active' },
  { label: '非活跃', value: 'inactive' }
] as const

// 用户类型选项
export const USER_TYPE_OPTIONS = [
  { label: '管理员', value: '管理员' },
  { label: '操作员', value: '操作员' }
] as const

// 用户角色选项
export const USER_ROLE_OPTIONS = [
  { label: '网络规划设计师', value: '网络规划设计师' },
  { label: '系统架构设计师', value: '系统架构设计师' },
  { label: '系统规划与管理师', value: '系统规划与管理师' },
  { label: '系统分析师', value: '系统分析师' }
] as const

// 批量导入结果
export interface BulkImportResult {
  success_count: number
  fail_count: number
  failed_users: Array<{
    username: string
    error: string
  }>
  message: string
} 