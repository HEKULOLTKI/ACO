<template>
  <div class="layout-container">
    <!-- 头部导航栏 -->
    <header class="layout-header">
      <div class="header-left">
        <div class="logo-container">
          
          <div class="logo">
            <div class="logo-icon">
              <!-- 图片3000.png -->
              <img src="@/assets/icon/组 3001.png" alt="logo" class="logo-img" />
            </div>
          </div>
          <!-- image 00005.png -->
          <img src="@/assets/icon/00005.png" alt="logo" class="logo-img" />
        </div>
      </div>
      
      <div class="header-center">
        <div class="search-container">
          <el-input
            v-model="searchValue"
            placeholder="搜索"
            class="search-input"
            :prefix-icon="Search"
            clearable
          />
        </div>
      </div>
      
      <div class="header-right">
        <div class="header-actions">
          <el-tooltip content="刷新" placement="bottom">
            <div class="action-btn" @click="handleRefresh">
              <img src="@/assets/icon/刷新.png" alt="刷新" class="action-icon" />
            </div>
          </el-tooltip>
          
          <el-tooltip content="通知" placement="bottom">
            <div class="action-btn notification-btn" @click="handleNotification">
              <img src="@/assets/icon/组 3000.png" alt="通知" class="action-icon" />
              <span class="notification-badge" v-if="notificationCount > 0">
                {{ notificationCount > 99 ? '99+' : notificationCount }}
              </span>
            </div>
          </el-tooltip>
          
          <el-tooltip content="帮助" placement="bottom">
            <div class="action-btn" @click="handleHelp">
              <img src="@/assets/icon/路径 1998.png" alt="帮助" class="action-icon" />
            </div>
          </el-tooltip>
          
          <el-tooltip content="设置" placement="bottom">
            <div class="action-btn" @click="handleSettings">
              <img src="@/assets/icon/设置 (1).png" alt="设置" class="action-icon" />
            </div>
          </el-tooltip>
        </div>
        
        <el-dropdown trigger="click" class="user-dropdown">
          <div class="user-info">
            <el-avatar :size="36" :src="userStore.user?.photo_data || ''" icon="User" />
            <span class="username">{{ userStore.user?.username || 'admin' }}</span>
            <img src="@/assets/icon/路径 2008.png" alt="下拉箭头" class="dropdown-icon-img" />
          </div>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="goToProfile">
                <img src="@/assets/icon/首页-用户.png" alt="用户" class="menu-icon" />
                个人资料
              </el-dropdown-item>
              <el-dropdown-item divided @click="handleLogout">
                <img src="@/assets/icon/路径 2009.png" alt="退出" class="menu-icon" />
                退出登录
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </header>

    <!-- 侧边栏 -->
    <aside class="layout-sidebar">
      <nav class="sidebar-nav">
        <div class="nav-item" :class="{ active: $route.path === '/dashboard' }" @click="$router.push('/dashboard')">
          <img src="@/assets/icon/首页.png" alt="首页" class="nav-icon-img" />
          <span class="nav-text">系统仪表板</span>
        </div>
        
        <div 
          class="nav-item" 
          :class="{ active: $route.path === '/users' }" 
          @click="$router.push('/users')"
          v-if="userStore.isAdmin"
        >
          <img src="@/assets/icon/首页-用户.png" alt="用户管理" class="nav-icon-img" />
          <span class="nav-text">用户管理</span>
        </div>
        
        <div 
          class="nav-item" 
          :class="{ active: $route.path === '/tasks' }" 
          @click="$router.push('/tasks')"
        >
          <img src="@/assets/icon/任务.png" alt="任务管理" class="nav-icon-img" />
          <span class="nav-text">任务管理</span>
        </div>
        
        <div 
          class="nav-item" 
          :class="{ active: $route.path === '/task-assignment' }" 
          @click="$router.push('/task-assignment')"
          v-if="userStore.isAdmin"
        >
          <img src="@/assets/icon/任务.png" alt="任务下发" class="nav-icon-img" />
          <span class="nav-text">任务下发</span>
        </div>
        
        <div 
          class="nav-item" 
          :class="{ active: $route.path === '/task-progress' }" 
          @click="$router.push('/task-progress')"
        >
          <img src="@/assets/icon/任务.png" alt="任务进度" class="nav-icon-img" />
          <span class="nav-text">任务进度</span>
        </div>
        
        <div class="nav-item" :class="{ active: $route.path === '/devices' }" @click="$router.push('/devices')">
          <img src="@/assets/icon/设备.png" alt="设备管理" class="nav-icon-img" />
          <span class="nav-text">设备管理</span>
        </div>
        
        <div class="nav-item" :class="{ active: $route.path === '/desktop' }" @click="$router.push('/desktop')">
          <img src="@/assets/icon/桌面设置.png" alt="桌面管理" class="nav-icon-img" />
          <span class="nav-text">桌面管理</span>
        </div>
        
        <div 
          class="nav-item" 
          :class="{ active: $route.path === '/settings' }" 
          @click="$router.push('/settings')"
          v-if="userStore.isAdmin"
        >
          <img src="@/assets/icon/系统参数.png" alt="系统设置" class="nav-icon-img" />
          <span class="nav-text">系统设置</span>
        </div>
      </nav>
    </aside>

    <!-- 主内容区域 -->
    <main class="layout-main">
      <div class="main-content">
        <router-view />
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search } from '@element-plus/icons-vue'
import { useAuthStore } from '@/store/modules/auth'

const router = useRouter()
const route = useRoute()
const userStore = useAuthStore()

// 响应式数据
const searchValue = ref('')
const notificationCount = ref(5)

const goToProfile = () => {
  router.push('/profile')
}

const handleLogout = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要退出登录吗？',
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    await userStore.logoutAction()
    ElMessage.success('已成功退出登录')
    router.push('/login')
  } catch (error) {
    // 用户取消了操作
  }
}

// 头部操作方法
const handleRefresh = () => {
  ElMessage.success('页面已刷新')
  window.location.reload()
}

const handleNotification = () => {
  ElMessage.info('暂无新通知')
}

const handleHelp = () => {
  window.open('http://localhost:8000/docs', '_blank')
}

const handleSettings = () => {
  router.push('/settings')
}
</script>

<style scoped lang="scss">
.layout-container {
  display: grid;
  grid-template-areas: 
    "header header"
    "sidebar main";
  grid-template-columns: 280px 1fr;
  grid-template-rows: 64px 1fr;
  height: 100vh;
  width: 100vw;
  background: #f5f7fa;
}

.layout-header {
  grid-area: header;
  background: #162035;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  height: 64px;
}

.header-left {
  flex: 0 0 auto;
  
  .logo-container {
    display: flex;
    align-items: center;
    gap: 12px;
  }
  
  .logo {
    .logo-icon {
      .cube-icon {
        position: relative;
        width: 32px;
        height: 32px;
        transform-style: preserve-3d;
        transform: rotateX(-15deg) rotateY(15deg);
        
        .cube-face {
          position: absolute;
          width: 32px;
          height: 32px;
          border: 2px solid #3498db;
          
          &.cube-front {
            background: linear-gradient(135deg, #3498db, #2980b9);
            transform: translateZ(16px);
          }
          
          &.cube-right {
            background: linear-gradient(135deg, #2980b9, #21618c);
            transform: rotateY(90deg) translateZ(16px);
          }
          
          &.cube-top {
            background: linear-gradient(135deg, #5dade2, #3498db);
            transform: rotateX(90deg) translateZ(16px);
          }
        }
      }
    }
  }

  .system-title {
    color: white;
    font-size: 20px;
    font-weight: 600;
    margin: 0;
    text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
  }
}

.header-center {
  flex: 1;
  max-width: 600px;
  margin: 0 32px;
  
  .search-container {
    .search-input {
      :deep(.el-input__wrapper) {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        transition: all 0.3s ease;
        
        &:hover {
          border-color: rgba(255, 255, 255, 0.3);
          background: rgba(255, 255, 255, 0.15);
        }
        
        &.is-focus {
          border-color: #3498db;
          background: rgba(255, 255, 255, 0.2);
          box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
        }
      }
      
      :deep(.el-input__inner) {
        color: white;
        
        &::placeholder {
          color: rgba(255, 255, 255, 0.6);
        }
      }
      
      :deep(.el-input__prefix-inner) {
        color: rgba(255, 255, 255, 0.7);
      }
    }
  }
}

.header-right {
  flex: 0 0 auto;
  display: flex;
  align-items: center;
  gap: 16px;
  
  .header-actions {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-right: 16px;
    
    .action-btn {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 36px;
      height: 36px;
      border-radius: 8px;
      cursor: pointer;
      transition: all 0.3s ease;
      color: rgba(255, 255, 255, 0.8);
      background: rgba(255, 255, 255, 0.1);
      position: relative;
      
      &:hover {
        background: rgba(255, 255, 255, 0.2);
        color: white;
        transform: translateY(-1px);
      }
      
      .el-icon {
        font-size: 16px;
      }
      
      .action-icon {
        width: 16px;
        height: 16px;
        object-fit: contain;
        filter: brightness(0) invert(1);
        opacity: 0.8;
        transition: opacity 0.3s ease;
      }
      
      &:hover .action-icon {
        opacity: 1;
      }
      
      &.notification-btn {
        .notification-badge {
          position: absolute;
          top: -4px;
          right: -4px;
          background: #e74c3c;
          color: white;
          font-size: 10px;
          padding: 1px 5px;
          border-radius: 8px;
          min-width: 16px;
          height: 16px;
          display: flex;
          align-items: center;
          justify-content: center;
          font-weight: 600;
          line-height: 1;
        }
      }
    }
  }
  
  .user-dropdown {
    .user-info {
      display: flex;
      align-items: center;
      gap: 12px;
      cursor: pointer;
      padding: 8px 16px;
      border-radius: 8px;
      transition: all 0.3s ease;
      background: rgba(255, 255, 255, 0.1);
      
      &:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateY(-1px);
      }
    }

    .username {
      font-size: 14px;
      color: white;
      font-weight: 500;
    }

    .dropdown-icon {
      color: white;
      font-size: 12px;
    }
    
    .dropdown-icon-img {
      width: 12px;
      height: 12px;
      object-fit: contain;
      filter: brightness(0) invert(1);
    }
    
    .menu-icon {
      width: 14px;
      height: 14px;
      object-fit: contain;
      margin-right: 8px;
    }
  }
}

.layout-sidebar {
  grid-area: sidebar;
  background: #162035;
  overflow-y: auto;
  box-shadow: 2px 0 12px rgba(0, 0, 0, 0.1);
}

.sidebar-nav {
  padding: 24px 0;
  
  .nav-group {
    margin: 4px 12px;
  }
  
  .nav-item {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 16px 24px;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    color: #bdc3c7;
    position: relative;
    
    &:hover {
      background: rgba(52, 152, 219, 0.1);
      color: #3498db;
      transform: translateX(4px);
    }
    
    &.active {
      background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
      color: white;
      box-shadow: 0 4px 12px rgba(52, 152, 219, 0.3);
      
      &::before {
        content: '';
        position: absolute;
        left: -12px;
        top: 50%;
        transform: translateY(-50%);
        width: 4px;
        height: 24px;
        background: #3498db;
        border-radius: 2px;
      }
    }
    
    &.nav-parent {
      .expand-icon {
        margin-left: auto;
        font-size: 14px;
        transition: transform 0.3s ease;
        
        &.rotated {
          transform: rotate(90deg);
        }
      }
    }
    
    &.nav-child {
      margin: 2px 0;
      padding: 12px 24px 12px 64px;
      font-size: 13px;
      
      &:hover {
        transform: translateX(2px);
        background: rgba(52, 152, 219, 0.08);
      }
      
      &.active {
        background: rgba(52, 152, 219, 0.15);
        color: #3498db;
        
        &::before {
          display: none;
        }
      }
    }
    
    .nav-icon {
      font-size: 20px;
      color: inherit;
    }
    
    .nav-icon-img {
      width: 20px;
      height: 20px;
      object-fit: contain;
      filter: brightness(0) invert(1);
      opacity: 0.7;
      transition: all 0.3s ease;
    }
    
    &:hover .nav-icon-img {
      opacity: 1;
      filter: brightness(0) invert(1);
    }
    
    &.active .nav-icon-img {
      opacity: 1;
      filter: brightness(0) invert(1);
      transform: scale(1.1);
    }
    
    .nav-text {
      font-size: 14px;
      font-weight: 500;
    }
  }
  
  .nav-submenu {
    background: rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    margin-top: 4px;
    overflow: hidden;
  }
}

.layout-main {
  grid-area: main;
  overflow-y: auto;
  background: #f8fafc;
}

.main-content {
  padding: 32px;
  min-height: 100%;
  max-width: 1600px;
  margin: 0 auto;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .layout-container {
    grid-template-areas: 
      "header"
      "main";
    grid-template-columns: 1fr;
    grid-template-rows: 64px 1fr;
  }
  
  .layout-sidebar {
    display: none;
  }
  
  .header-center {
    margin: 0 16px;
  }
  
  .header-right .header-actions {
    gap: 6px;
    margin-right: 12px;
    
    .action-btn {
      width: 32px;
      height: 32px;
      
      .el-icon {
        font-size: 14px;
      }
    }
  }
}

@media (max-width: 768px) {
  .layout-header {
    padding: 0 16px;
  }
  
  .header-left .system-title {
    font-size: 16px;
  }
  
  .header-center {
    margin: 0 12px;
    max-width: 300px;
  }
  
  .header-right .header-actions {
    gap: 4px;
    margin-right: 8px;
    
    .action-btn {
      width: 28px;
      height: 28px;
      
      .el-icon {
        font-size: 12px;
      }
    }
  }
  
  .main-content {
    padding: 20px;
  }
}

@media (max-width: 480px) {
  .header-left {
    .logo {
      display: none;
    }
    
    .system-title {
      font-size: 14px;
    }
  }
  
  .header-center {
    margin: 0 8px;
    max-width: 200px;
  }
  
  .header-right .header-actions {
    .action-btn:not(.notification-btn) {
      display: none;
    }
  }
}
</style> 