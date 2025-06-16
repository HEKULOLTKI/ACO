// API响应基础接口
export interface ApiResponse<T = any> {
  data: T
  message?: string
  code?: number
}

// 分页参数
export interface PaginationParams {
  skip?: number
  limit?: number
}

// 分页响应
export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  size: number
  pages: number
}

// 登录表单
export interface LoginForm {
  username: string
  password: string
}

// 错误响应
export interface ErrorResponse {
  detail: string
}

// API请求配置
export interface RequestConfig {
  timeout?: number
  headers?: Record<string, string>
} 