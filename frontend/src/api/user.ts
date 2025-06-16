import request from '@/utils/request'
import type { User, UserForm, UserUpdate, BulkImportResult } from '@/types/user'

// 获取用户列表
export const getUserList = (params?: {
  skip?: number
  limit?: number
  role?: string
  user_type?: string
}) => {
  return request.get<User[]>('/users', { params })
}

// 获取用户列表 (别名)
export const getUsers = (params?: {
  skip?: number
  limit?: number
  role?: string
  user_type?: string
}) => {
  return request.get<User[]>('/users', { params })
}

// 创建用户
export const createUser = (data: UserForm) => {
  return request.post<User>('/users', data)
}

// 更新用户
export const updateUser = (id: number, data: UserUpdate) => {
  return request.put<User>(`/users/${id}`, data)
}

// 删除用户
export const deleteUser = (id: number) => {
  return request.delete(`/users/${id}`)
}

// 获取用户详情
export const getUserDetail = (id: number) => {
  return request.get<User>(`/users/${id}`)
}

// 更新用户状态
export const updateUserStatus = (id: number, status: string) => {
  return request.put<User>(`/users/${id}`, { status })
}

// 批量导入用户
export const bulkImportUsers = (file: File) => {
  const formData = new FormData()
  formData.append('file', file)
  return request.post<BulkImportResult>('/users/bulk-import', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

// 下载用户导入模板
export const downloadUserTemplate = () => {
  return request.get('/users/template/download', {
    responseType: 'blob'
  })
} 