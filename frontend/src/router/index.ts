import { createRouter, createWebHistory } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/store/modules/auth'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { 
      requiresAuth: false,
      title: '用户登录'
    }
  },
  {
    path: '/role-selection',
    name: 'RoleSelection',
    component: () => import('@/views/RoleSelection.vue'),
    meta: { 
      requiresAuth: true,
      requiresOperator: true,
      title: '角色选择'
    }
  },
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/app',
    name: 'Layout',
    component: () => import('@/components/layout/Layout.vue'),
    redirect: '/dashboard', 
    meta: { requiresAuth: true },
    children: [
      {
        path: '/dashboard',
        name: 'Dashboard',
        component: () => import('@/views/Dashboard.vue'),
        meta: { 
          requiresAuth: true,
          title: '首页'
        }
      },
      {
        path: '/users',
        name: 'UserManagement',
        component: () => import('@/views/UserManagement.vue'),
        meta: { 
          requiresAuth: true,
          requiresAdmin: true,
          title: '用户管理'
        }
      },
      {
        path: '/tasks',
        name: 'TaskManagement',
        component: () => import('@/views/TaskManagement.vue'),
        meta: { 
          requiresAuth: true,
          requiresPermission: 'task:manage',
          title: '任务管理'
        }
      },
      {
        path: '/task-assignment',
        name: 'TaskAssignment',
        component: () => import('@/views/TaskAssignment.vue'),
        meta: { 
          requiresAuth: true,
          requiresAdmin: true,
          title: '任务下发'
        }
      },
      {
        path: '/task-progress',
        name: 'TaskProgress',
        component: () => import('@/views/TaskProgress.vue'),
        meta: { 
          requiresAuth: true,
          title: '任务进度'
        }
      },
      {
        path: '/devices',
        name: 'DeviceManagement',
        component: () => import('@/views/DeviceManagement.vue'),
        meta: { 
          requiresAuth: true,
          title: '设备管理'
        }
      },
      {
        path: '/desktop',
        name: 'DesktopManagement',
        component: () => import('@/views/DesktopManagement.vue'),
        meta: { 
          requiresAuth: true,
          requiresPermission: 'desktop:manage',
          title: '桌面管理'
        }
      },
      {
        path: '/settings',
        name: 'SystemSettings',
        component: () => import('@/views/SystemSettings.vue'),
        meta: { 
          requiresAuth: true,
          requiresAdmin: true,
          title: '系统设置'
        }
      },
      {
        path: '/profile',
        name: 'UserProfile',
        component: () => import('@/views/UserProfile.vue'),
        meta: { 
          requiresAuth: true,
          title: '个人资料'
        }
      }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue'),
    meta: { title: '页面未找到' }
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// 全局前置守卫
router.beforeEach(async (to, from, next) => {
  // 设置页面标题
  if (to.meta.title) {
    document.title = `${to.meta.title} - 多智能体协作运维系统`
  }

  const authStore = useAuthStore()
  
  // 不需要认证的页面直接放行
  if (!to.meta.requiresAuth) {
    // 如果已登录且访问登录页，重定向到仪表板
    if (to.name === 'Login' && authStore.isAuthenticated) {
      next('/dashboard')
    } else {
      next()
    }
    return
  }

  // 需要认证但未登录，重定向到登录页
  if (!authStore.isAuthenticated) {
    ElMessage.warning('请先登录')
    next({
      path: '/login',
      query: { redirect: to.fullPath }
    })
    return
  }

  // 需要管理员权限但用户不是管理员
  if (to.meta.requiresAdmin && !authStore.isAdmin) {
    ElMessage.error('权限不足，需要管理员权限')
    next('/dashboard')
    return
  }

  // 需要操作员权限但用户不是操作员或管理员
  if (to.meta.requiresOperator && !authStore.isOperator) {
    ElMessage.error('权限不足，需要操作员或更高权限')
    next('/dashboard')
    return
  }

  // 需要特定权限
  if (to.meta.requiresPermission && !authStore.hasPermission(to.meta.requiresPermission as string)) {
    ElMessage.error('权限不足，无法访问此功能')
    next('/dashboard')
    return
  }

  // 特殊处理：操作员访问角色选择页面
  if (to.name === 'RoleSelection') {
    const user = authStore.user
    if (user && user.type === '管理员') {
      // 管理员不需要角色选择，直接跳转到主页
      next('/dashboard')
      return
    }
  }

  // 特殊处理：操作员登录后需要先选择角色
  if (to.name !== 'RoleSelection' && to.meta.requiresAuth) {
    const user = authStore.user
    const selectedRole = localStorage.getItem('selectedRole')
    
    if (user && user.type === '操作员' && !selectedRole) {
      // 操作员未选择角色，重定向到角色选择页面
      next('/role-selection')
      return
    }
  }

  next()
})

export default router
