<template>
  <div class="not-found">
    <div class="not-found-container">
      <div class="not-found-content">
        <div class="error-code">404</div>
        <div class="error-message">
          <h2>页面未找到</h2>
          <p>抱歉，您访问的页面不存在或已被移除。</p>
        </div>
        <div class="error-actions">
          <el-button type="primary" @click="goHome">
            <el-icon><HomeFilled /></el-icon>
            返回首页
          </el-button>
          <el-button @click="goBack">
            <el-icon><ArrowLeft /></el-icon>
            返回上页
          </el-button>
        </div>
      </div>
      <div class="not-found-image">
        <svg 
          width="400" 
          height="300" 
          viewBox="0 0 400 300" 
          xmlns="http://www.w3.org/2000/svg"
        >
          <!-- 简单的404图标 -->
          <circle cx="200" cy="150" r="120" fill="#f5f5f5" stroke="#ddd" stroke-width="2"/>
          <text x="200" y="170" text-anchor="middle" font-size="60" font-weight="bold" fill="#999">
            404
          </text>
          <path d="M140 120 Q200 80 260 120" stroke="#ccc" stroke-width="3" fill="none"/>
          <circle cx="170" cy="130" r="8" fill="#999"/>
          <circle cx="230" cy="130" r="8" fill="#999"/>
        </svg>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { HomeFilled, ArrowLeft } from '@element-plus/icons-vue'

const router = useRouter()

const goHome = () => {
  router.push('/')
}

const goBack = () => {
  if (window.history.length > 1) {
    router.go(-1)
  } else {
    router.push('/')
  }
}
</script>

<style scoped lang="scss">
.not-found {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.not-found-container {
  background: white;
  border-radius: 16px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  padding: 60px 40px;
  max-width: 800px;
  width: 100%;
  display: flex;
  align-items: center;
  gap: 60px;

  @media (max-width: 768px) {
    flex-direction: column;
    gap: 30px;
    padding: 40px 20px;
  }
}

.not-found-content {
  flex: 1;
  text-align: center;

  .error-code {
    font-size: 120px;
    font-weight: bold;
    color: #667eea;
    line-height: 1;
    margin-bottom: 20px;
    text-shadow: 2px 2px 4px rgba(102, 126, 234, 0.3);

    @media (max-width: 768px) {
      font-size: 80px;
    }
  }

  .error-message {
    margin-bottom: 40px;

    h2 {
      font-size: 32px;
      color: #333;
      margin: 0 0 15px 0;
      font-weight: 600;

      @media (max-width: 768px) {
        font-size: 24px;
      }
    }

    p {
      font-size: 16px;
      color: #666;
      margin: 0;
      line-height: 1.6;
    }
  }

  .error-actions {
    display: flex;
    gap: 15px;
    justify-content: center;

    @media (max-width: 768px) {
      flex-direction: column;
      align-items: center;

      .el-button {
        width: 200px;
      }
    }

    .el-button {
      padding: 12px 24px;
      font-size: 16px;
      border-radius: 8px;
      transition: all 0.3s;

      &:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
      }
    }
  }
}

.not-found-image {
  flex-shrink: 0;

  @media (max-width: 768px) {
    svg {
      width: 300px;
      height: 225px;
    }
  }

  @media (max-width: 480px) {
    svg {
      width: 250px;
      height: 187px;
    }
  }
}
</style> 