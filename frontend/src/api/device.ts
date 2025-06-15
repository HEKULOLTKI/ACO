import request from '@/utils/request'
import type { 
  Device, 
  DeviceCreate, 
  DeviceUpdate, 
  DeviceListResponse, 
  DeviceSearchParams,
  DeviceStatistics
} from '@/types/device'

// 获取设备列表
export const getDevices = (params?: DeviceSearchParams) => {
  return request.get<DeviceListResponse>('/devices', { params })
}

// 获取单个设备详情
export const getDevice = (id: number) => {
  return request.get<Device>(`/devices/${id}`)
}

// 创建设备
export const createDevice = (data: DeviceCreate) => {
  return request.post<Device>('/devices', data)
}

// 更新设备
export const updateDevice = (id: number, data: DeviceUpdate) => {
  return request.put<Device>(`/devices/${id}`, data)
}

// 删除设备
export const deleteDevice = (id: number) => {
  return request.delete(`/devices/${id}`)
}

// 批量删除设备
export const batchDeleteDevices = (ids: number[]) => {
  return request.delete('/devices/batch', { data: ids })
}

// 更新设备状态
export const updateDeviceStatus = (id: number, status: string) => {
  return request.put(`/devices/${id}/status`, { status })
}

// 批量更新设备状态
export const batchUpdateDeviceStatus = (ids: number[], status: string) => {
  return request.post('/devices/batch/status', { device_ids: ids, status })
}

// 获取设备统计信息
export const getDeviceStatistics = () => {
  return request.get<DeviceStatistics>('/devices/statistics')
}

// 导出设备数据
export const exportDevices = (params?: DeviceSearchParams) => {
  return request.get('/devices/export', { 
    params, 
    responseType: 'blob' 
  })
}

// 下载导入模板
export const downloadImportTemplate = () => {
  return request.get('/devices/template/download', {
    responseType: 'blob'
  })
}

// 导入设备
export const importDevices = (file: File) => {
  const formData = new FormData()
  formData.append('file', file)
  
  return request.post('/devices/import', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
} 