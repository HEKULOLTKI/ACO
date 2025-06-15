// 基础任务类型
export interface Task {
  id: number
  name: string
  type: string
  phase: string
  status: string
  description: string
  create_time: string
  update_time: string
}

// 任务表单类型
export interface TaskForm {
  name: string
  type: string  
  phase: string
  description: string
}

// 任务分配类型
export interface TaskAssignment {
  id: number
  task_id: number
  user_id?: number
  username: string
  status: string
  progress: number
  performance_score: number
  comments?: string
  assigned_at: string
  last_update: string
  // 任务信息
  task_name?: string
  task_type?: string
  task_phase?: string
}

// 任务分配表单类型
export interface TaskAssignmentForm {
  task_id: number
  username: string
  comments?: string
}

// 任务进度类型
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

// 任务进度更新类型
export interface TaskProgressUpdate {
  status?: string
  progress?: number
  performance_score?: number
  comments?: string
}

// 任务统计类型
export interface TaskStats {
  total: number
  inProgress: number
  completed: number
  paused: number
  avgProgress: number
}

// 图表数据类型
export interface TaskChartData {
  statusDistribution: {
    name: string
    value: number
  }[]
  progressTrend: {
    name: string
    value: number
  }[]
}

// 用户类型（用于任务分配）
export interface TaskUser {
  id: number
  username: string
  role: string
  type: string
}

// 可用任务类型（用于任务分配）
export interface AvailableTask {
  id: number
  name: string
  type: string
  phase: string
  description: string
}

// 任务历史记录类型
export interface TaskHistory {
  id: number
  assignment_id: number
  status: string
  progress: number
  performance_score: number
  comments: string
  updated_at: string
  updated_by: string
}

// 任务状态枚举
export enum TaskStatus {
  UNASSIGNED = '未分配',
  IN_PROGRESS = '进行中',
  COMPLETED = '已完成',
  PAUSED = '已暂停'
}

// 任务类型枚举
export enum TaskType {
  NETWORK_BUILD = '网络搭建任务',
  SYSTEM_BUILD = '系统构建任务', 
  OPERATION_MONITOR = '运维监管任务',
  LOG_SECURITY = '日志安全任务'
}

// 任务阶段枚举
export enum TaskPhase {
  PLANNING = '计划阶段',
  EXECUTION = '执行阶段',
  ACCEPTANCE = '验收阶段',
  COMPLETION = '完成阶段'
}

// API响应类型
export interface TaskListResponse {
  items: Task[]
  total: number
  page: number
  size: number
}

export interface TaskAssignmentListResponse {
  items: TaskAssignment[]
  total: number
  page: number
  size: number
}

export interface TaskProgressListResponse {
  items: TaskProgress[]
  total: number
  page: number
  size: number
}

// 搜索参数类型
export interface TaskSearchParams {
  name?: string
  type?: string
  phase?: string
  page?: number
  size?: number
}

export interface TaskAssignmentSearchParams {
  taskName?: string
  username?: string
  status?: string
  page?: number
  size?: number
}

export interface TaskProgressSearchParams {
  taskName?: string
  username?: string
  status?: string
  dateRange?: string[]
  page?: number
  size?: number
} 