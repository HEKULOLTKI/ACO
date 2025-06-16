import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import 'element-plus/dist/index.css'
import 'element-plus/theme-chalk/dark/css-vars.css'

import App from './App.vue'
import router from './router'

// 创建应用实例
const app = createApp(App)

// 创建Pinia实例
const pinia = createPinia()

// 注册Element Plus图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

// 使用插件
app.use(pinia)
app.use(router)
app.use(ElementPlus, {
  // Element Plus配置
  size: 'default',
  zIndex: 3000,
})

// 挂载应用
app.mount('#app')

// 开发环境配置
if (import.meta.env.DEV) {
  console.log('🚀 多智能体协作运维系统 - 前端已启动')
  console.log('📖 开发模式:', import.meta.env.MODE)
  console.log('🔗 API地址:', import.meta.env.VITE_API_BASE_URL || '/api')
}
