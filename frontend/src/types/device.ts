// 设备接口定义
export interface Device {
  id: number
  name: string
  type: string
  ip?: string
  status: string
  location?: string
}

// 设备表单数据
export interface DeviceForm {
  id?: number
  name: string
  type: string
  ip?: string
  status: string
  location?: string
}

// 设备创建
export interface DeviceCreate {
  name: string
  type: string
  ip?: string
  status?: string
  location?: string
}

// 设备更新
export interface DeviceUpdate {
  name?: string
  type?: string
  ip?: string
  status?: string
  location?: string
}

// 设备列表响应
export interface DeviceListResponse {
  devices: Device[]
  total: number
  page: number
  page_size: number
}

// 设备搜索参数
export interface DeviceSearchParams {
  skip?: number
  limit?: number
  name?: string
  type?: string
  status?: string
  location?: string
  ip?: string
}

// 设备统计信息
export interface DeviceStatistics {
  total_devices: number
  online_devices: number
  offline_devices: number
  type_statistics: Record<string, number>
}

// 设备状态选项
export const DEVICE_STATUS_OPTIONS = [
  { label: '在线', value: 'online' },
  { label: '离线', value: 'offline' },
  { label: '维护中', value: 'maintenance' }
] as const

// 设备类型选项
export const DEVICE_TYPE_OPTIONS = [
  { label: '服务器', value: 'server' },
  { label: '工作站', value: 'workstation' },
  { label: '路由器', value: 'router' },
  { label: '交换机', value: 'switch' },
  { label: '其他', value: 'other' }
] as const 