import request from '@/utils/request'

export interface TaskProgress {
  id: number
  task_id: number
  task_name: string
  task_type: string
  username: string
  status: string
  progress: number
  performance_score: number
  comments: string
  assigned_at: string
  last_update: string
}

export interface TaskProgressStats {
  total: number
  inProgress: number
  completed: number
  paused: number
  avgProgress: number
}

export interface TaskProgressUpdate {
  status?: string
  progress?: number
  performance_score?: number
  comments?: string
}

export interface ProgressChartData {
  statusDistribution: {
    name: string
    value: number
  }[]
  progressTrend: {
    name: string
    value: number
  }[]
}

// 获取任务进度列表
export const getTaskProgressList = (params?: {
  page?: number
  size?: number
  taskName?: string
  username?: string
  status?: string
  dateRange?: string[]
}) => {
  return request.get<{
    items: TaskProgress[]
    total: number
    page: number
    size: number
  }>('/task-progress', { params })
}

// 获取任务进度统计
export const getTaskProgressStats = () => {
  return request.get<TaskProgressStats>('/task-progress/stats')
}

// 获取任务进度图表数据
export const getTaskProgressCharts = () => {
  return request.get<ProgressChartData>('/task-progress/charts')
}

// 更新任务进度
export const updateTaskProgress = (assignmentId: number, data: TaskProgressUpdate) => {
  return request.put<TaskProgress>(`/task-progress/${assignmentId}`, data)
}

// 获取任务进度详情
export const getTaskProgressDetail = (assignmentId: number) => {
  return request.get<TaskProgress>(`/task-progress/${assignmentId}`)
}

// 获取用户任务进度
export const getUserTaskProgress = (username: string, params?: {
  page?: number
  size?: number
  status?: string
}) => {
  return request.get<{
    items: TaskProgress[]
    total: number
    page: number
    size: number
  }>(`/task-progress/user/${username}`, { params })
}

// 获取任务类型进度统计
export const getTaskTypeProgressStats = () => {
  return request.get<{
    task_type: string
    total: number
    completed: number
    avg_progress: number
  }[]>('/task-progress/type-stats')
}

// 批量更新任务进度
export const bulkUpdateTaskProgress = (data: {
  assignment_ids: number[]
  updates: TaskProgressUpdate
}) => {
  return request.put<TaskProgress[]>('/task-progress/bulk-update', data)
}

// 导出任务进度报告
export const exportTaskProgressReport = (params?: {
  dateRange?: string[]
  status?: string
  format?: 'excel' | 'pdf'
}) => {
  return request.get('/task-progress/export', { 
    params,
    responseType: 'blob'
  })
}

// 获取任务进度历史记录
export const getTaskProgressHistory = (assignmentId: number) => {
  return request.get<{
    id: number
    assignment_id: number
    status: string
    progress: number
    performance_score: number
    comments: string
    updated_at: string
    updated_by: string
  }[]>(`/task-progress/${assignmentId}/history`)
} 