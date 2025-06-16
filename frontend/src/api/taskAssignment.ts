import request from '@/utils/request'

export interface TaskAssignment {
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

export interface Task {
  id: number
  name: string
  type: string
  phase: string
  description: string
}

export interface User {
  id: number
  username: string
  role: string
  type: string
}

export interface TaskAssignmentForm {
  task_id: number
  username: string
  comments?: string
}

export interface TaskAssignmentUpdate {
  status?: string
  progress?: number
  performance_score?: number
  comments?: string
}

// 获取任务分配列表
export const getTaskAssignments = (params?: {
  page?: number
  size?: number
  taskName?: string
  username?: string
  status?: string
}) => {
  return request.get<{
    items: TaskAssignment[]
    total: number
    page: number
    size: number
  }>('/task-assignments', { params })
}

// 获取可分配的任务列表
export const getAvailableTasks = () => {
  return request.get<Task[]>('/tasks/available')
}

// 获取可分配的用户列表
export const getAvailableUsers = () => {
  return request.get<User[]>('/users/available')
}

// 分配任务
export const assignTask = (data: TaskAssignmentForm) => {
  return request.post<TaskAssignment>('/task-assignments', data)
}

// 重新分配任务
export const reassignTask = (data: TaskAssignmentForm & { old_assignment_id?: number }) => {
  return request.post<TaskAssignment>('/task-assignments/reassign', data)
}

// 更新任务分配
export const updateTaskAssignment = (assignmentId: number, data: TaskAssignmentUpdate) => {
  return request.put<TaskAssignment>(`/task-assignments/${assignmentId}`, data)
}

// 撤销任务分配
export const revokeTaskAssignment = (assignmentId: number) => {
  return request.delete(`/task-assignments/${assignmentId}`)
}

// 获取任务分配详情
export const getTaskAssignmentDetail = (assignmentId: number) => {
  return request.get<TaskAssignment>(`/task-assignments/${assignmentId}`)
}

// 批量分配任务
export const bulkAssignTasks = (data: {
  task_ids: number[]
  usernames: string[]
  comments?: string
}) => {
  return request.post<TaskAssignment[]>('/task-assignments/bulk', data)
}

// 获取任务分配统计
export const getTaskAssignmentStats = () => {
  return request.get<{
    total_assignments: number
    in_progress: number
    completed: number
    paused: number
    avg_progress: number
  }>('/task-assignments/stats')
} 