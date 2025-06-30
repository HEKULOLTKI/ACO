import request from '@/utils/request'

// 桌面项目相关类型定义
export interface DesktopItem {
  id?: number
  name: string
  type?: string
  path?: string
  icon?: string
  role?: string
  position_x?: number
  position_y?: number
  user_id?: number
  created_at?: string
}

export interface ToolboxTool {
  id?: number
  name: string
  command?: string
  icon?: string
  create_time?: string
}

// 桌面项目API
export const desktopItemAPI = {
  // 获取桌面项目列表
  getItems(): Promise<DesktopItem[]> {
    return request.get('/desktop/items')
  },

  // 创建桌面项目
  createItem(data: Omit<DesktopItem, 'id' | 'user_id' | 'created_at'>): Promise<DesktopItem> {
    return request.post('/desktop/items', data)
  },

  // 获取单个桌面项目
  getItem(id: number): Promise<DesktopItem> {
    return request.get(`/desktop/items/${id}`)
  },

  // 更新桌面项目
  updateItem(id: number, data: Partial<DesktopItem>): Promise<DesktopItem> {
    return request.put(`/desktop/items/${id}`, data)
  },

  // 删除桌面项目
  deleteItem(id: number): Promise<{ message: string }> {
    return request.delete(`/desktop/items/${id}`)
  }
}

// 工具箱API
export const toolboxAPI = {
  // 获取工具列表
  getTools(): Promise<ToolboxTool[]> {
    return request.get('/desktop/tools')
  },

  // 创建工具
  createTool(data: Omit<ToolboxTool, 'id' | 'create_time'>): Promise<ToolboxTool> {
    return request.post('/desktop/tools', data)
  },

  // 更新工具
  updateTool(id: number, data: Partial<ToolboxTool>): Promise<ToolboxTool> {
    return request.put(`/desktop/tools/${id}`, data)
  },

  // 删除工具
  deleteTool(id: number): Promise<{ message: string }> {
    return request.delete(`/desktop/tools/${id}`)
  }
} 