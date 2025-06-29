import request from '@/utils/request'

/**
 * 发送PDF预览请求到客户端（后端主动发送JSON到客户端）
 */
export function sendPDFToClient(filename: string) {
  return request({
    url: '/pdf/send-to-client',
    method: 'post',
    params: {
      filename
    }
  })
}

/**
 * 获取PDF预览JSON数据（新增）
 * 客户端主动请求，用于获取PDF预览数据后自行发送到客户端
 */
export function getPDFPreviewData(filename: string) {
  return request({
    url: '/pdf/get-preview-data',
    method: 'get',
    params: {
      filename
    }
  })
}

/**
 * 获取可用的项目报告列表
 */
export function getAvailableReports() {
  return request({
    url: '/pdf/reports/list',
    method: 'get'
  })
}

/**
 * 获取PDF文件列表
 */
export function getPDFFiles(directory?: string) {
  return request({
    url: '/pdf/files',
    method: 'get',
    params: {
      directory: directory || 'uploads/progress_reports'
    }
  })
}

/**
 * 获取PDF文件信息
 */
export function getPDFInfo(filePath: string) {
  return request({
    url: '/pdf/info',
    method: 'get',
    params: {
      file_path: filePath
    }
  })
}

/**
 * 获取PDF页面图像
 */
export function getPDFPage(filePath: string, pageNumber: number, options?: {
  zoom?: number
  maxWidth?: number
  maxHeight?: number
  includeText?: boolean
}) {
  return request({
    url: '/pdf/page',
    method: 'get',
    params: {
      file_path: filePath,
      page_number: pageNumber,
      ...options
    }
  })
}

/**
 * 获取PDF完整预览
 */
export function getPDFPreview(filePath: string, thumbnailOnly?: boolean) {
  return request({
    url: '/pdf/preview',
    method: 'get',
    params: {
      file_path: filePath,
      thumbnail_only: thumbnailOnly
    }
  })
} 