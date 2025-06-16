<template>
  <div class="demo-container">
    <div class="demo-content">
      <h1>访问权限错误弹窗 - 演示页面</h1>
      
      <div class="demo-buttons">
        <button 
          class="demo-btn" 
          @click="showDialog1"
        >
          显示默认弹窗
        </button>
        
        <button 
          class="demo-btn" 
          @click="showDialog2"
        >
          显示自定义消息弹窗
        </button>
        
        <button 
          class="demo-btn" 
          @click="showDialog3"
        >
          模拟角色权限错误
        </button>
      </div>
      
      <div class="usage-code">
        <h3>使用方法：</h3>
        <pre><code>
// 1. 导入组件
import AccessDeniedDialog from '@/components/AccessDeniedDialog.vue'

// 2. 在模板中使用
&lt;AccessDeniedDialog 
  :visible="showAccessDenied"
  :message="errorMessage"
  @close="handleClose"
  @confirm="handleConfirm"
/&gt;

// 3. 在script中控制显示
const showAccessDenied = ref(false)
const errorMessage = ref('您没有权限访问此功能')

const handleClose = () => {
  showAccessDenied.value = false
}

const handleConfirm = () => {
  // 处理确认逻辑
  console.log('用户点击了确认')
}
        </code></pre>
      </div>
    </div>
    
    <!-- 访问权限错误弹窗 -->
    <AccessDeniedDialog 
      :visible="dialogVisible"
      :message="currentMessage"
      @close="handleClose"
      @confirm="handleConfirm"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import AccessDeniedDialog from '@/components/AccessDeniedDialog.vue'

const dialogVisible = ref(false)
const currentMessage = ref('')

const showDialog1 = () => {
  currentMessage.value = '您没有权限访问此功能'
  dialogVisible.value = true
}

const showDialog2 = () => {
  currentMessage.value = '您的权限等级不足，请联系管理员申请相关权限'
  dialogVisible.value = true
}

const showDialog3 = () => {
  currentMessage.value = '您没有权限访问 软件开发工程师功能'
  dialogVisible.value = true
}

const handleClose = () => {
  dialogVisible.value = false
}

const handleConfirm = () => {
  console.log('用户点击了确认按钮')
  // 可以在这里添加其他逻辑，比如记录日志、跳转页面等
}
</script>

<style scoped>
.demo-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Orbitron', monospace;
  padding: 20px;
}

.demo-content {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  padding: 40px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  max-width: 800px;
  width: 100%;
}

h1 {
  color: #ffffff;
  text-align: center;
  margin-bottom: 40px;
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
}

.demo-buttons {
  display: flex;
  gap: 20px;
  justify-content: center;
  margin-bottom: 40px;
  flex-wrap: wrap;
}

.demo-btn {
  padding: 12px 24px;
  background: linear-gradient(145deg, rgba(0, 150, 255, 0.8), rgba(0, 100, 200, 0.9));
  border: 2px solid rgba(0, 255, 255, 0.6);
  border-radius: 6px;
  color: #ffffff;
  font-family: 'Orbitron', monospace;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.demo-btn:hover {
  background: linear-gradient(145deg, rgba(0, 180, 255, 0.9), rgba(0, 120, 220, 1));
  border-color: rgba(0, 255, 255, 0.8);
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
  transform: translateY(-2px);
}

.usage-code {
  background: rgba(0, 0, 0, 0.3);
  border-radius: 8px;
  padding: 20px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.usage-code h3 {
  color: #00ffff;
  margin-bottom: 15px;
  margin-top: 0;
}

pre {
  background: rgba(0, 0, 0, 0.5);
  border-radius: 4px;
  padding: 15px;
  overflow-x: auto;
  margin: 0;
}

code {
  color: #ffffff;
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  font-size: 12px;
  line-height: 1.5;
}

@media (max-width: 768px) {
  .demo-content {
    padding: 20px;
  }
  
  .demo-buttons {
    flex-direction: column;
    align-items: center;
  }
  
  .demo-btn {
    width: 200px;
  }
  
  code {
    font-size: 10px;
  }
}
</style> 