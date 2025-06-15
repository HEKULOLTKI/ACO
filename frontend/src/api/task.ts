import request from '@/utils/request'

export interface Task {
  id: number
  name: string
  type: string
  phase: string
  description: string
  status: string
  create_time: string
  update_time: string
}

export interface TaskAssignment {
  id: number
  task_id: number
  user_id?: number
  username: string
  assigned_at: string
  status: string
  progress: number
  performance_score: number
  comments?: string
  last_update: string
  // 任务信息
  task_name?: string
  task_type?: string
  task_phase?: string
}

export interface TaskWithAssignments extends Task {
  assignments: TaskAssignment[]
}

export interface TaskStats {
  total_tasks: number
  completed_tasks: number
  in_progress_tasks: number
  average_score: number
}

export interface TaskForm {
  name: string
  type: string
  phase: string
  description: string
  status?: string
}

// 批量导入结果
export interface TaskBulkImportResult {
  success_count: number
  fail_count: number
  failed_tasks: Array<{
    name: string
    error: string
  }>
  message: string
}

// 获取任务列表
export const getTasks = (params?: any) => {
  return request.get<Task[]>('/tasks', { params })
}

// 获取任务总数
export const getTasksCount = (params?: any) => {
  return request.get<{ count: number }>('/tasks/count', { params })
}

// 获取任务详情
export const getTask = (id: number) => {
  return request.get<Task>(`/tasks/${id}`)
}

// 创建任务
export const createTask = (data: TaskForm) => {
  return request.post<Task>('/tasks', data)
}

// 更新任务
export const updateTask = (id: number, data: Partial<TaskForm>) => {
  return request.put<Task>(`/tasks/${id}`, data)
}

// 删除任务
export const deleteTask = (id: number) => {
  return request.delete(`/tasks/${id}`)
}

// 获取任务分配列表
export const getTaskAssignments = (params?: {
  skip?: number
  limit?: number
  status?: string
}) => {
  return request.get<TaskAssignment[]>('/task-assignments', { params })
}

// 获取我的任务
export const getMyTasks = (params?: { status?: string }) => {
  return request.get<TaskAssignment[]>('/my-tasks', { params })
}

// 获取我的任务统计
export const getMyTaskStats = () => {
  return request.get<TaskStats>('/my-task-stats')
}

// 创建任务分配
export const createTaskAssignment = (data: Omit<TaskAssignment, 'id' | 'assigned_at' | 'last_update'>) => {
  return request.post<TaskAssignment>('/task-assignments', data)
}

// 更新任务分配
export const updateTaskAssignment = (assignmentId: number, data: {
  status?: string
  progress?: number
  performance_score?: number
  comments?: string
}) => {
  return request.put<TaskAssignment>(`/task-assignments/${assignmentId}`, data)
}

// 更新我的任务
export const updateMyTask = (assignmentId: number, data: {
  status?: string
  progress?: number
  comments?: string
}) => {
  return request.put<TaskAssignment>(`/my-tasks/${assignmentId}`, data)
}

// 批量导入任务
export const bulkImportTasks = (file: File) => {
  const formData = new FormData()
  formData.append('file', file)
  return request.post<TaskBulkImportResult>('/tasks/bulk-import', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
} 