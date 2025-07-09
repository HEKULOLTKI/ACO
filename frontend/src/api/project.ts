import request from '@/utils/request'
import type { Project } from '@/types/user'

// 获取所有项目
export function getProjects() {
  return request({
    url: '/project',
    method: 'get'
  })
}

// 获取单个项目
export function getProject(id: number) {
  return request({
    url: `/project/${id}`,
    method: 'get'
  })
}

// 创建项目
export function createProject(data: Partial<Project>) {
  return request({
    url: '/project',
    method: 'post',
    data
  })
}

// 更新项目
export function updateProject(id: number, data: Partial<Project>) {
  return request({
    url: `/project/${id}`,
    method: 'put',
    data
  })
}

// 删除项目
export function deleteProject(id: number) {
  return request({
    url: `/project/${id}`,
    method: 'delete'
  })
}

// 导入项目
export function importProjects(formData: FormData) {
  return request({
    url: '/project/import',
    method: 'post',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
} 