<template>
  <div class="pdf-preview-container">
    <div class="header">
      <h2>📄 项目报告预览</h2>
      <div class="header-actions">
        <button @click="refreshFiles" class="refresh-btn" :disabled="loading">
          <span v-if="loading">🔄 刷新中...</span>
          <span v-else>🔄 刷新文件列表</span>
        </button>
      </div>
    </div>

    <!-- 错误提示 -->
    <div v-if="errorMessage" class="error-message">
      <span>❌ {{ errorMessage }}</span>
      <button @click="clearError" class="close-error">✕</button>
    </div>

    <!-- 成功提示 -->
    <div v-if="successMessage" class="success-message">
      <span>✅ {{ successMessage }}</span>
      <button @click="clearSuccess" class="close-success">✕</button>
    </div>

    <!-- 说明信息 -->
    <div class="info-banner">
      <div class="info-content">
        <h3>📋 客户端预览说明</h3>
        <p>点击"发送到客户端"按钮将向您的客户端发送PDF预览请求，客户端将自动打开PDF文件。</p>
        <p>请确保您的客户端服务正在运行并监听端口 8800。</p>
        <p>当前用户IP: <strong>{{ userIP || '正在获取...' }}</strong></p>
      </div>
    </div>

    <!-- 文件列表 -->
    <div class="file-list">
      <div v-if="files.length === 0 && !loading" class="no-files">
        <div class="no-files-icon">📂</div>
        <div class="no-files-text">暂无PDF文件</div>
        <div class="no-files-hint">请将PDF文件放入 uploads/progress_reports 目录</div>
      </div>
      
      <div class="files-grid">
        <div v-for="file in files" :key="file.file_path" class="file-card">
          <div class="file-icon">📄</div>
          <div class="file-info">
            <div class="file-name" :title="file.filename">{{ file.filename }}</div>
            <div class="file-meta">
              <span class="file-size">{{ formatFileSize(file.file_size) }}</span>
              <span class="file-time">{{ formatDate(file.modification_time) }}</span>
            </div>
          </div>
          <div class="file-action">
            <button 
              class="preview-btn" 
              @click="sendToClient(file)" 
              :disabled="sendingFile === file.filename"
            >
              <span v-if="sendingFile === file.filename">📤 发送中...</span>
              <span v-else>📤 发送到客户端</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 发送历史记录 -->
    <div class="send-history" v-if="sendHistory.length > 0">
      <h3>📋 最近发送记录</h3>
      <div class="history-list">
        <div v-for="(record, index) in sendHistory.slice(0, 10)" :key="index" class="history-item">
          <div class="history-content">
            <div class="history-filename">{{ record.filename }}</div>
            <div class="history-time">{{ record.time }}</div>
            <div class="history-status" :class="record.status">
              <span v-if="record.status === 'success'">✅ 发送成功</span>
              <span v-else-if="record.status === 'warning'">⚠️ 发送警告</span>
              <span v-else>❌ 发送失败</span>
            </div>
            <div class="history-target">目标: {{ record.target_ip }}</div>
            <div class="history-message">{{ record.message }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { sendPDFToClient, getPDFFiles, getPDFPreviewData } from '@/api/pdf'
import axios from 'axios'

export default {
  name: 'PDFPreview',
  setup() {
    const files = ref([])
    const loading = ref(false)
    const errorMessage = ref('')
    const successMessage = ref('')
    const sendingFile = ref('')
    const userIP = ref('')
    const sendHistory = ref([])

    // 错误处理
    const showError = (message) => {
      errorMessage.value = message
      setTimeout(() => {
        errorMessage.value = ''
      }, 5000)
    }

    const showSuccess = (message) => {
      successMessage.value = message
      setTimeout(() => {
        successMessage.value = ''
      }, 3000)
    }

    const clearError = () => {
      errorMessage.value = ''
    }

    const clearSuccess = () => {
      successMessage.value = ''
    }

    // 获取用户IP地址
    const fetchUserIP = async () => {
      try {
        const token = localStorage.getItem('token')
        if (!token) return

        const response = await axios.get('/auth/user-session-info', {
          headers: {
            'Authorization': `Bearer ${token}`
          },
          baseURL: '/api'
        })
        
        if (response.data && response.data.ip_address) {
          userIP.value = response.data.ip_address
        }
      } catch (error) {
        console.error('获取用户IP失败:', error)
        userIP.value = '获取失败'
      }
    }

    // 获取PDF文件列表
    const fetchFiles = async () => {
      loading.value = true
      errorMessage.value = ''
      try {
        const response = await getPDFFiles('uploads/progress_reports')
        files.value = response.data.files
        showSuccess(`成功加载 ${response.data.files.length} 个PDF文件`)
      } catch (error) {
        console.error('获取文件列表失败:', error)
        showError('获取文件列表失败，请检查网络连接')
      } finally {
        loading.value = false
      }
    }

    // 发送PDF到客户端（新方式：由后端主动发送）
    const sendToClient = async (file) => {
      if (sendingFile.value) return

      sendingFile.value = file.filename
      try {
        console.log('📤 请求后端发送PDF预览数据到客户端...')
        console.log('   文件名:', file.filename)
        
        // 调用后端接口，让后端主动发送JSON到客户端
        const response = await sendPDFToClient(file.filename)
        const result = response.data || response
        
        console.log('✅ 后端响应:', result)
        
        // 记录发送历史
        const historyRecord = {
          filename: file.filename,
          time: new Date().toLocaleString('zh-CN'),
          status: result.status || 'success',
          target_ip: result.target_ip || userIP.value || 'unknown',
          message: result.message || 'PDF预览请求已发送'
        }
        
        sendHistory.value.unshift(historyRecord)
        
        if (result.status === 'success') {
          showSuccess(result.message || `PDF预览请求已成功发送到客户端`)
          console.log('📥 下载URL:', result.download_url)
          console.log('🎯 目标IP:', result.target_ip)
        } else if (result.status === 'warning') {
          showError(result.message || '客户端响应异常，但不影响使用')
        }
        
      } catch (error) {
        console.error('❌ 发送PDF预览请求失败:', error)
        
        let errorMessage = '发送PDF预览请求失败'
        if (error.response?.status === 503) {
          errorMessage = '无法连接到客户端，请确保客户端服务正在运行'
        } else if (error.response?.status === 504) {
          errorMessage = '连接客户端超时'
        } else if (error.response?.data?.detail) {
          errorMessage = error.response.data.detail
        }
        
        // 记录失败历史
        const historyRecord = {
          filename: file.filename,
          time: new Date().toLocaleString('zh-CN'),
          status: 'error',
          target_ip: userIP.value || 'unknown',
          message: errorMessage
        }
        sendHistory.value.unshift(historyRecord)
        
        showError(errorMessage)
        
        // 提供解决建议
        console.log('💡 解决建议:')
        console.log('   1. 确保客户端PDF服务正在运行')
        console.log('   2. 检查防火墙是否允许8800端口')
        console.log('   3. 验证网络连接是否正常')
        console.log('   4. 确保用户已登录且IP地址已记录')
        
      } finally {
        sendingFile.value = ''
      }
    }

    // 刷新文件列表
    const refreshFiles = () => {
      fetchFiles()
    }

    // 辅助函数
    const formatFileSize = (bytes) => {
      if (bytes === 0) return '0 Bytes'
      const k = 1024
      const sizes = ['Bytes', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    }

    const formatDate = (timestamp) => {
      return new Date(timestamp * 1000).toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    // 生命周期
    onMounted(() => {
      fetchFiles()
      fetchUserIP()
    })

    return {
      files,
      loading,
      errorMessage,
      successMessage,
      sendingFile,
      userIP,
      sendHistory,
      showError,
      showSuccess,
      clearError,
      clearSuccess,
      sendToClient,
      refreshFiles,
      formatFileSize,
      formatDate
    }
  }
}
</script>

<style scoped>
.pdf-preview-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #e0e0e0;
}

.header h2 {
  margin: 0;
  color: #333;
  font-size: 24px;
}

.refresh-btn {
  padding: 10px 20px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
}

.refresh-btn:hover:not(:disabled) {
  background: #0056b3;
}

.refresh-btn:disabled {
  background: #6c757d;
  cursor: not-allowed;
}

.error-message, .success-message {
  padding: 12px 16px;
  margin-bottom: 16px;
  border-radius: 6px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.error-message {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.success-message {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.close-error, .close-success {
  background: none;
  border: none;
  font-size: 16px;
  cursor: pointer;
  padding: 0;
  margin-left: 10px;
}

.info-banner {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 20px;
  border-radius: 10px;
  margin-bottom: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.info-content h3 {
  margin: 0 0 10px 0;
  font-size: 18px;
}

.info-content p {
  margin: 8px 0;
  line-height: 1.5;
}

.info-content strong {
  color: #ffd700;
}

.file-list {
  margin-bottom: 30px;
}

.no-files {
  text-align: center;
  padding: 60px 20px;
  color: #666;
}

.no-files-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.no-files-text {
  font-size: 18px;
  margin-bottom: 8px;
}

.no-files-hint {
  font-size: 14px;
  color: #999;
}

.files-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.file-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 20px;
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
  display: flex;
  align-items: center;
  gap: 15px;
}

.file-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.file-icon {
  font-size: 36px;
  flex-shrink: 0;
}

.file-info {
  flex: 1;
  min-width: 0;
}

.file-name {
  font-weight: bold;
  font-size: 16px;
  margin-bottom: 8px;
  color: #333;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.file-meta {
  display: flex;
  gap: 15px;
  font-size: 13px;
  color: #666;
}

.file-action {
  flex-shrink: 0;
}

.preview-btn {
  padding: 10px 16px;
  background: #28a745;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  font-weight: bold;
  transition: background-color 0.3s;
  min-width: 120px;
}

.preview-btn:hover:not(:disabled) {
  background: #218838;
}

.preview-btn:disabled {
  background: #6c757d;
  cursor: not-allowed;
}

.send-history {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.send-history h3 {
  margin: 0 0 15px 0;
  color: #333;
  font-size: 18px;
}

.history-list {
  max-height: 400px;
  overflow-y: auto;
}

.history-item {
  background: white;
  border: 1px solid #dee2e6;
  border-radius: 6px;
  padding: 15px;
  margin-bottom: 10px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.history-filename {
  font-weight: bold;
  color: #333;
  margin-bottom: 5px;
}

.history-time {
  font-size: 12px;
  color: #6c757d;
  margin-bottom: 5px;
}

.history-status {
  font-weight: bold;
  margin-bottom: 5px;
}

.history-status.success {
  color: #28a745;
}

.history-status.warning {
  color: #ffc107;
}

.history-status.error {
  color: #dc3545;
}

.history-target {
  font-size: 13px;
  color: #6c757d;
  margin-bottom: 5px;
}

.history-message {
  font-size: 13px;
  color: #495057;
}
</style> 