import request from '@/utils/request'

// 系统状态相关接口
export const getSystemStatus = () => {
  return request.get('/system/status')
}

export const getSystemStats = () => {
  return request.get('/system/stats')
}

export const getSystemHealth = () => {
  return request.get('/system/health')
}

// 项目报告相关接口
export const generateProjectReport = () => {
  return request.post('/system/reports/generate')
}

export const getProjectReports = () => {
  return request.get('/system/reports')
}

export const downloadProjectReport = (filename: string) => {
  return request.get(`/system/reports/download/${filename}`, {
    responseType: 'blob'
  })
}

export const deleteProjectReport = (filename: string) => {
  return request.delete(`/system/reports/${filename}`)
}

// 系统维护相关接口
export const clearSystemCache = () => {
  return request.post('/system/cache/clear')
}

export const exportSystemLogs = () => {
  return request.get('/system/logs/export', {
    responseType: 'blob'
  })
} 