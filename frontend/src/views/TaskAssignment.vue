<template>
  <div class="task-assignment">
    <!-- 主要内容区域 -->
    <div class="assignment-layout">
      <!-- 左侧：任务区域 -->
      <div class="left-panel">
        <!-- 任务下发列表 -->
        <el-card shadow="never" class="task-card">
          <template #header>
            <div class="card-header">
              <span>🔖 任务下发列表</span>
            </div>
          </template>
          
          <div class="task-list">
            <el-table 
              :data="availableTasks" 
              v-loading="loading"
              @current-change="handleTaskSelection"
              highlight-current-row
              height="320"
              style="width: 100%"
            >
              <el-table-column prop="id" label="任务ID" width="80" />
              <el-table-column prop="name" label="任务名称" min-width="200" show-overflow-tooltip />
              <el-table-column prop="type" label="任务类型" width="120" />
              <el-table-column prop="phase" label="阶段任务" width="120" />
            </el-table>
          </div>
        </el-card>

        <!-- 任务详情 -->
        <el-card shadow="never" class="task-detail-card">
          <template #header>
            <div class="card-header">
              <el-icon><Document /></el-icon>
              <span>任务详情</span>
            </div>
          </template>
          
          <div class="task-detail">
            <div v-if="selectedTask" class="detail-content">
              <div class="detail-grid">
                <div class="detail-item">
                  <label class="detail-label">任务名称</label>
                  <div class="detail-value">{{ selectedTask.name }}</div>
                </div>
                <div class="detail-item">
                  <label class="detail-label">任务类型</label>
                  <div class="detail-value">{{ selectedTask.type }}</div>
                </div>
                <div class="detail-item">
                  <label class="detail-label">任务阶段</label>
                  <div class="detail-value">{{ selectedTask.phase }}</div>
                </div>
                <div class="detail-item">
                  <label class="detail-label">任务状态</label>
                  <div class="detail-value">
                    <el-tag :type="getStatusType((selectedTask as any).status || '未分配')">{{ (selectedTask as any).status || '未分配' }}</el-tag>
                  </div>
                </div>
                <div class="detail-item">
                  <label class="detail-label">创建时间</label>
                  <div class="detail-value">{{ formatDate(selectedTask.create_time) }}</div>
                </div>
                <div class="detail-item">
                  <label class="detail-label">更新时间</label>
                  <div class="detail-value">{{ formatDate(selectedTask.update_time) }}</div>
                </div>
                <div class="detail-item detail-description">
                  <label class="detail-label">任务描述</label>
                  <div class="detail-value">{{ selectedTask.description || '对生产环境进行全面的安全漏洞扫描，包括操作系统、应用程序和网络设备' }}</div>
                </div>
              </div>
            </div>
            <div v-else class="placeholder">
              <el-icon><InfoFilled /></el-icon>
              <span>选择任务查看详情</span>
            </div>
          </div>
        </el-card>
      </div>

      <!-- 右侧：执行人选择区域 -->
      <div class="right-panel">
        <!-- 选择执行人 -->
        <el-card shadow="never" class="user-selection-card">
          <template #header>
            <div class="card-header">
              <span>👥 选择执行人</span>
            </div>
          </template>

          <div class="user-selection">
            <!-- 可选执行人（左侧） -->
            <div class="available-users-section">
              <div class="section-header">
                <span>选择执行人 ({{ availableUsers.length }}/20 项)</span>
              </div>
              <div class="user-list available" :class="{ loading: userLoading }">
                <div 
                  v-for="user in availableUsers" 
                  :key="user.username"
                  class="user-item"
                  @click="toggleUser(user, 'available')"
                >
                  <el-checkbox :model-value="checkedAvailableUsers.includes(user.username)" />
                  <span>{{ user.username }}</span>
                </div>
                <div v-if="availableUsers.length === 0 && !userLoading" class="empty-state">
                  暂无可选用户
                </div>
              </div>
            </div>

            <!-- 传输按钮 -->
            <div class="transfer-buttons">
              <el-button 
                type="primary" 
                circle 
                :disabled="checkedAvailableUsers.length === 0"
                @click="addSelectedUsers"
                class="transfer-btn"
              >
                <el-icon><ArrowRight /></el-icon>
              </el-button>
            </div>

            <!-- 已选执行人（右侧） -->
            <div class="selected-users-section">
              <div class="section-header">
                <el-icon><Check /></el-icon>
                <span>已选执行人 ({{ selectedUsers.length }}/20 项)</span>
              </div>
              <div class="user-list selected">
                <div 
                  v-for="user in selectedUsers" 
                  :key="user.username"
                  class="user-item selected"
                  @click="removeUser(user)"
                  title="点击移除用户"
                >
                  <span>{{ user.username }}</span>
                  <el-icon class="remove-icon"><Close /></el-icon>
                </div>
                <div v-if="selectedUsers.length === 0" class="empty-state">
                  已分配执行人 (0 项)
                </div>
              </div>
            </div>
          </div>
        </el-card>

        <!-- 分配任务按钮 -->
        <div class="assignment-controls">
          <el-button 
            type="primary" 
            size="large"
            :disabled="!selectedTask || selectedUsers.length === 0"
            @click="handleAssignTasks"
            style="width: 100%;"
          >
            分配任务
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Check, ArrowRight, ArrowLeft, Document, InfoFilled, Close } from '@element-plus/icons-vue'
import { getTasks, createTaskAssignment } from '@/api/task'
import { getUserList } from '@/api/user'
import type { Task } from '@/types/task'
import type { User } from '@/types/user'

const loading = ref(false)
const userLoading = ref(false)

// 数据
const availableTasks = ref<Task[]>([])
const availableUsers = ref<User[]>([])
const selectedTask = ref<Task | null>(null)
const selectedUsers = ref<User[]>([])
const checkedAvailableUsers = ref<string[]>([])
const checkedSelectedUsers = ref<string[]>([])

// 工具函数
const getStatusType = (status: string) => {
  switch (status) {
    case '已完成':
      return 'success'
    case '进行中':
      return 'warning'
    case '已暂停':
      return 'danger'
    case '未分配':
      return 'info'
    default:
      return ''
  }
}

const formatDate = (dateString: string) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 方法
const loadAvailableTasks = async () => {
  loading.value = true
  try {
    const response = await getTasks()
    // 过滤掉已完成的任务，只显示可分配的任务
    availableTasks.value = response.data?.filter(task => 
      task.status !== '已完成' && task.status !== '已取消'
    ) || []
  } catch (error: any) {
    const errorMsg = error?.response?.data?.detail || error?.message || '加载可用任务失败'
    ElMessage.error(errorMsg)
    console.error('加载任务失败:', error)
  } finally {
    loading.value = false
  }
}

const loadAvailableUsers = async () => {
  userLoading.value = true
  try {
    // 使用用户列表API，过滤活跃用户
    const response = await getUserList({ limit: 100 })
    availableUsers.value = response.data?.filter(user => user.status === 'active') || []
  } catch (error) {
    ElMessage.error('加载可用用户失败')
    console.error('加载用户失败:', error)
  } finally {
    userLoading.value = false
  }
}

const handleTaskSelection = (currentRow: Task | null) => {
  selectedTask.value = currentRow
}

const toggleUser = (user: User, type: 'available' | 'selected') => {
  if (type === 'available') {
    const index = checkedAvailableUsers.value.indexOf(user.username)
    if (index > -1) {
      checkedAvailableUsers.value.splice(index, 1)
    } else {
      checkedAvailableUsers.value.push(user.username)
    }
  } else {
    const index = checkedSelectedUsers.value.indexOf(user.username)
    if (index > -1) {
      checkedSelectedUsers.value.splice(index, 1)
    } else {
      checkedSelectedUsers.value.push(user.username)
    }
  }
}

const addSelectedUsers = () => {
  checkedAvailableUsers.value.forEach(username => {
    const user = availableUsers.value.find(u => u.username === username)
    if (user && !selectedUsers.value.find(u => u.username === username)) {
      selectedUsers.value.push(user)
    }
  })
  checkedAvailableUsers.value = []
}

const removeSelectedUsers = () => {
  checkedSelectedUsers.value.forEach(username => {
    const index = selectedUsers.value.findIndex(u => u.username === username)
    if (index > -1) {
      selectedUsers.value.splice(index, 1)
    }
  })
  checkedSelectedUsers.value = []
}

const removeUser = (user: User) => {
  const index = selectedUsers.value.findIndex(u => u.username === user.username)
  if (index > -1) {
    selectedUsers.value.splice(index, 1)
  }
}

const handleAssignTasks = async () => {
  if (!selectedTask.value) {
    ElMessage.warning('请选择要分配的任务')
    return
  }
  
  if (selectedUsers.value.length === 0) {
    ElMessage.warning('请选择执行人')
    return
  }

  try {
    await ElMessageBox.confirm(
      `确定要将任务 "${selectedTask.value.name}" 分配给 ${selectedUsers.value.length} 个执行人吗？`,
      '确认分配',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )

    // 创建任务分配
    for (const user of selectedUsers.value) {
      await createTaskAssignment({
        task_id: selectedTask.value.id,
        user_id: user.id,
        username: user.username,
        status: '进行中',
        progress: 0,
        performance_score: 0,
        comments: ''
      })
    }

    ElMessage.success(`成功为 ${selectedUsers.value.length} 个用户分配任务`)
    // 清空选择状态
    selectedTask.value = null
    selectedUsers.value = []
    checkedAvailableUsers.value = []
    checkedSelectedUsers.value = []
    // 重新加载任务列表以更新状态
    await loadAvailableTasks()
  } catch (error: any) {
    if (error?.message !== 'cancel') {
      const errorMsg = error?.response?.data?.detail || error?.message || '任务分配失败'
      ElMessage.error(errorMsg)
      console.error('分配任务失败:', error)
    }
  }
}

// 组件挂载时加载数据
onMounted(() => {
  loadAvailableTasks()
  loadAvailableUsers()
})
</script>

<style scoped lang="scss">
.task-assignment {
  padding: 0;
  background: transparent;
  height: 100%;

  .assignment-layout {
    display: flex;
    gap: 12px;
    height: 100%;
    padding: 12px;

    .left-panel {
      width: 60%;
      display: flex;
      flex-direction: column;
      gap: 12px;

      .task-card {
        flex: 1;
        
        .card-header {
          display: flex;
          align-items: center;
          font-weight: 500;
          font-size: 16px;
        }

        .task-list {
          height: 100%;
        }
      }

      .task-detail-card {
        flex: 0 0 320px;

        .card-header {
          display: flex;
          align-items: center;
          gap: 8px;
          font-weight: 500;
          font-size: 16px;
        }

        .task-detail {
          height: 280px;
          overflow-y: auto;
          
          &::-webkit-scrollbar {
            width: 6px;
          }
          
          &::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 3px;
          }
          
          &::-webkit-scrollbar-thumb {
            background: #c1c1c1;
            border-radius: 3px;
            
            &:hover {
              background: #a8a8a8;
            }
          }
          
          .detail-content {
            .detail-grid {
              display: grid;
              grid-template-columns: 1fr 1fr;
              gap: 12px;

              .detail-item {
                &.detail-description {
                  grid-column: 1 / -1;
                }

                .detail-label {
                  display: block;
                  font-size: 11px;
                  color: #909399;
                  font-weight: 500;
                  margin-bottom: 6px;
                  text-transform: uppercase;
                  letter-spacing: 0.5px;
                }

                .detail-value {
                  font-size: 13px;
                  color: #303133;
                  line-height: 1.4;
                  word-break: break-all;
                  background: #f8f9fa;
                  padding: 6px 10px;
                  border-radius: 4px;
                  border-left: 3px solid #409eff;
                  min-height: 20px;
                  display: flex;
                  align-items: center;
                }
              }
            }
          }

          .placeholder {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            color: #909399;
            padding: 30px 0;
            background: #f9f9f9;
            border-radius: 8px;
            font-size: 14px;
            gap: 8px;

            .el-icon {
              font-size: 24px;
              color: #c0c4cc;
            }
          }
        }
      }
    }

    .right-panel {
      width: 40%;
      display: flex;
      flex-direction: column;
      gap: 12px;

      .user-selection-card {
        flex: 1;

        .card-header {
          display: flex;
          align-items: center;
          font-weight: 500;
          font-size: 16px;
        }

        .user-selection {
          display: flex;
          align-items: flex-start;
          gap: 10px;
          height: 460px;

          .available-users-section,
          .selected-users-section {
            flex: 1;

            .section-header {
              display: flex;
              align-items: center;
              gap: 8px;
              margin-bottom: 10px;
              font-weight: 500;
              color: #333;
              font-size: 13px;
            }

            .user-list {
              border: 1px solid #dcdfe6;
              border-radius: 4px;
              height: 420px;
              overflow-y: auto;
              background: #fff;
              position: relative;

              &.loading {
                opacity: 0.6;
                
                &::after {
                  content: "加载中...";
                  position: absolute;
                  top: 50%;
                  left: 50%;
                  transform: translate(-50%, -50%);
                  color: #409eff;
                  font-size: 14px;
                }
              }

              .user-item {
                display: flex;
                align-items: center;
                gap: 8px;
                padding: 6px 10px;
                cursor: pointer;
                border-bottom: 1px solid #f0f0f0;
                font-size: 13px;

                &:hover {
                  background: #f5f7fa;
                }

                &.selected {
                  background: #e6f7ff;
                  border-color: #91d5ff;
                  justify-content: space-between;
                  
                  &:hover {
                    background: #fff2f0;
                    
                    .remove-icon {
                      color: #ff4d4f;
                    }
                  }
                  
                  .remove-icon {
                    color: #d9d9d9;
                    font-size: 12px;
                    transition: color 0.2s ease;
                    
                    &:hover {
                      color: #ff4d4f;
                    }
                  }
                }

                &:last-child {
                  border-bottom: none;
                }
              }

              &.selected {
                background: #f0f9ff;
              }

              .empty-state {
                text-align: center;
                color: #999;
                padding: 40px 15px;
                font-size: 13px;
              }
            }
          }

          .transfer-buttons {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            width: 50px;
            margin-top: 33px;
            height: 420px;
            padding: 0;
            
            .transfer-btn {
              width: 40px;
              height: 40px;
              border-radius: 50%;
              display: flex;
              align-items: center;
              justify-content: center;
              
              .el-icon {
                font-size: 16px;
                font-weight: bold;
              }
              
              &:hover:not(:disabled) {
                transform: scale(1.1);
                transition: transform 0.2s ease;
              }
            }
          }
        }
      }

      .assignment-controls {
        flex: 0 0 auto;
      }
    }
  }
}

:deep(.el-card) {
  border-radius: 6px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
}

:deep(.el-card__header) {
  padding: 12px 16px;
  background: #fafafa;
  border-bottom: 1px solid #ebeef5;
}

:deep(.el-card__body) {
  padding: 12px 16px;
}

:deep(.el-table .el-table__header th) {
  background: #f5f7fa;
  color: #606266;
  font-weight: 500;
  padding: 8px 0;
}

:deep(.el-table--enable-row-hover .el-table__body tr:hover > td) {
  background-color: #f5f7fa;
}

:deep(.el-table__body tr.current-row > td) {
  background-color: #ecf5ff;
}

:deep(.el-table .el-table__body td) {
  padding: 6px 0;
}

:deep(.transfer-btn.el-button--primary) {
  background-color: #409eff;
  border-color: #409eff;
  color: white;
  
  &:hover:not(:disabled) {
    background-color: #66b1ff;
    border-color: #66b1ff;
  }
  
  &:disabled {
    background-color: #a0cfff;
    border-color: #a0cfff;
    color: white;
    cursor: not-allowed;
  }
}

:deep(.transfer-btn.el-button) {
  background-color: white;
  border-color: #dcdfe6;
  color: #606266;
  
  &:hover:not(:disabled) {
    background-color: #ecf5ff;
    border-color: #409eff;
    color: #409eff;
  }
  
  &:disabled {
    background-color: #f5f7fa;
    border-color: #e4e7ed;
    color: #c0c4cc;
    cursor: not-allowed;
  }
}
</style> 