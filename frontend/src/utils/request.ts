import axios, { type AxiosResponse, type AxiosError } from 'axios'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/store/modules/auth'
import router from '@/router'
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'

// 配置NProgress
NProgress.configure({ showSpinner: false })

// 防止重复登出的标志
let isLoggingOut = false

// 创建axios实例
const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器
request.interceptors.request.use(
  (config) => {
    // 显示进度条
    NProgress.start()
    
    // 获取token
    const authStore = useAuthStore()
    if (authStore.token) {
      config.headers.Authorization = `Bearer ${authStore.token}`
    }
    
    return config
  },
  (error) => {
    NProgress.done()
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  (response: AxiosResponse) => {
    NProgress.done()
    return response
  },
  (error: AxiosError) => {
    NProgress.done()
    
    // 处理响应错误
    if (error.response) {
      const status = error.response.status
      const data = error.response.data as any
      
      switch (status) {
        case 401:
          // 未授权，清除token并跳转到登录页
          if (!isLoggingOut) {
            isLoggingOut = true
            const authStore = useAuthStore()
            // 跳过API调用以避免循环
            authStore.logoutAction(true)
            router.push('/login')
            ElMessage.error('登录已过期，请重新登录')
            // 重置标志，防止永久锁定
            setTimeout(() => {
              isLoggingOut = false
            }, 1000)
          }
          break
        case 403:
          ElMessage.error('权限不足，无法访问该资源')
          break
        case 404:
          ElMessage.error('请求的资源不存在')
          break
        case 422:
          // 验证错误
          if (data.detail && Array.isArray(data.detail)) {
            const errorMsg = data.detail.map((err: any) => err.msg).join(', ')
            ElMessage.error(`参数验证错误: ${errorMsg}`)
          } else {
            ElMessage.error(data.detail || '参数验证错误')
          }
          break
        case 500:
          ElMessage.error('服务器内部错误，请稍后重试')
          break
        default:
          ElMessage.error(data?.detail || `请求失败 (${status})`)
      }
    } else if (error.request) {
      // 网络错误
      ElMessage.error('网络连接失败，请检查网络设置')
    } else {
      ElMessage.error('请求配置错误')
    }
    
    return Promise.reject(error)
  }
)

export default request 