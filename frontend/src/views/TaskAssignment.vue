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
              <div class="header-left">
                <span>🔖 任务下发列表</span>
                <el-tag v-if="filteredTasks.length > 0" type="info" size="small">
                  {{ filteredTasks.length }} 个任务
                </el-tag>
              </div>
              <!-- 角色选择器 -->
              <div class="role-selector">
                <el-select
                  v-model="selectedRole"
                  placeholder="选择角色任务"
                  clearable
                  @change="handleRoleChange"
                  style="width: 180px"
                  size="small"
                >
                  <el-option label="全部任务" value="" />
                  <el-option label="网络规划设计师" value="网络规划设计师" />
                  <el-option label="系统架构设计师" value="系统架构设计师" />
                  <el-option label="系统规划与管理师" value="系统规划与管理师" />
                  <el-option label="系统分析师" value="系统分析师" />
                </el-select>
              </div>
            </div>
          </template>
          
          <div class="task-list">
            <el-table 
              :data="filteredTasks" 
              v-loading="loading"
              @selection-change="handleTaskSelectionChange"
              @current-change="handleCurrentTaskChange"
              highlight-current-row
              height="450"
              style="width: 100%"
              size="small"
            >
              <el-table-column type="selection" width="45" />
              <el-table-column prop="id" label="ID" width="60" />
              <el-table-column prop="name" label="任务名称" min-width="140" show-overflow-tooltip />
              <el-table-column prop="type" label="类型" width="100" />
              <el-table-column prop="phase" label="阶段" width="100" />
              <el-table-column prop="role_binding" label="执行角色" width="120" show-overflow-tooltip />
            </el-table>
            
            <!-- 批量操作提示 -->
            <div v-if="selectedTasks.length > 0" class="batch-info">
              <el-icon><InfoFilled /></el-icon>
              <span>已选择 {{ selectedTasks.length }} 个任务</span>
              <el-button type="text" @click="clearTaskSelection" size="small">清空选择</el-button>
            </div>
          </div>
        </el-card>

        <!-- 任务详情 -->
        <el-card shadow="never" class="task-detail-card">
          <template #header>
            <div class="card-header">
              <el-icon><Document /></el-icon>
              <span>任务详情</span>
              <el-tag v-if="currentTask" type="success" size="small">
                {{ currentTask.name }}
              </el-tag>
            </div>
          </template>
          
          <div class="task-detail">
            <div v-if="currentTask" class="detail-content">
              <div class="detail-grid">
                <div class="detail-item">
                  <label class="detail-label">任务ID</label>
                  <div class="detail-value">{{ currentTask.id }}</div>
                </div>
                <div class="detail-item">
                  <label class="detail-label">任务名称</label>
                  <div class="detail-value">{{ currentTask.name }}</div>
                </div>
                <div class="detail-item">
                  <label class="detail-label">任务类型</label>
                  <div class="detail-value">{{ currentTask.type || '未指定' }}</div>
                </div>
                <div class="detail-item">
                  <label class="detail-label">阶段任务</label>
                  <div class="detail-value">{{ currentTask.phase || '未指定' }}</div>
                </div>
                <div class="detail-item">
                  <label class="detail-label">执行角色</label>
                  <div class="detail-value">{{ currentTask.role_binding || '未指定' }}</div>
                </div>
                <div class="detail-item">
                  <label class="detail-label">任务状态</label>
                  <div class="detail-value">
                    <el-tag :type="getStatusType(currentTask.status)" size="small">
                      {{ currentTask.status || '未分配' }}
                    </el-tag>
                  </div>
                </div>
                <div class="detail-item">
                  <label class="detail-label">创建时间</label>
                  <div class="detail-value">{{ formatDate(currentTask.create_time) }}</div>
                </div>
                <div class="detail-item">
                  <label class="detail-label">更新时间</label>
                  <div class="detail-value">{{ formatDate(currentTask.update_time) || '未更新' }}</div>
                </div>
                <div class="detail-item detail-description">
                  <label class="detail-label">任务描述</label>
                  <div class="detail-value description-content">
                    {{ currentTask.description || '对生产环境进行全面的安全漏洞扫描，包括操作系统、应用程序和网络设备。此任务需要使用专业的安全扫描工具，对目标系统进行深度检测，识别潜在的安全风险和漏洞，并生成详细的安全评估报告。' }}
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="placeholder">
              <el-icon><InfoFilled /></el-icon>
              <span>点击任务查看详情</span>
              <p class="placeholder-tip">选择左侧任务列表中的任务，<br>即可在此处查看详细信息</p>
            </div>
          </div>
        </el-card>
      </div>

      <!-- 右侧：执行角色选择区域 -->
      <div class="right-panel">
        <!-- 选择执行角色 -->
        <el-card shadow="never" class="user-selection-card">
          <template #header>
            <div class="card-header">
              <div class="header-left">
                <span>👥 选择执行角色</span>
                <el-tag type="warning" size="small">
                  {{ availableUsers.length }} 个可用角色
                </el-tag>
              </div>
              <el-tag v-if="selectedUsers.length > 0" type="success" size="small">
                已选 {{ selectedUsers.length }} 个
              </el-tag>
            </div>
          </template>

          <div class="user-selection">
            <!-- 可选执行角色（上方） -->
            <div class="available-users-section">
              <div class="section-header">
                <span>可选执行角色</span>
                <el-button 
                  v-if="checkedAvailableUsers.length > 0"
                  type="primary" 
                  size="small"
                  @click="addSelectedUsers"
                >
                  添加选中 ({{ checkedAvailableUsers.length }})
                </el-button>
              </div>
              <div class="user-list available" :class="{ loading: userLoading }">
                <div 
                  v-for="user in availableUsers" 
                  :key="user.username"
                  class="user-item"
                  @click="toggleUser(user, 'available')"
                >
                  <el-checkbox :model-value="checkedAvailableUsers.includes(user.username)" />
                  <div class="user-card-inline">
                    <div class="user-display">{{ user.username }}</div>
                    <div class="user-role">{{ user.role }}</div>
                  </div>
                </div>
                <div v-if="availableUsers.length === 0 && !userLoading" class="empty-state">
                  暂无可选用户
                </div>
              </div>
            </div>

            <!-- 已选执行角色（下方） -->
            <div class="selected-users-section">
              <div class="section-header">
                <div class="header-left">
                  <el-icon><Check /></el-icon>
                  <span>已选执行角色</span>
                </div>
                <el-button 
                  v-if="selectedUsers.length > 0"
                  type="danger" 
                  size="small"
                  plain
                  @click="clearSelectedUsers"
                >
                  清空全部
                </el-button>
              </div>
              <div class="user-list selected">
                <div 
                  v-for="user in selectedUsers" 
                  :key="user.username"
                  class="user-item selected"
                  @click="removeUser(user)"
                  title="点击移除用户"
                >
                  <div class="user-card-inline">
                    <div class="user-display">{{ user.username }}</div>
                    <div class="user-role">{{ user.role }}</div>
                  </div>
                  <el-icon class="remove-icon"><Close /></el-icon>
                </div>
                <div v-if="selectedUsers.length === 0" class="empty-state">
                  点击上方用户进行选择
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
            :disabled="selectedTasks.length === 0 || selectedUsers.length === 0"
            @click="handleAssignTasks"
            style="width: 100%;"
          >
            <el-icon><Check /></el-icon>
            分配任务 ({{ selectedTasks.length }} 个任务 → {{ selectedUsers.length }} 个角色)
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
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
const selectedTasks = ref<Task[]>([]) // 多选的任务列表
const currentTask = ref<Task | null>(null) // 当前查看详情的任务
const selectedUsers = ref<User[]>([])
const checkedAvailableUsers = ref<string[]>([])
const checkedSelectedUsers = ref<string[]>([])
const selectedRole = ref<string>('')

// 根据角色过滤任务
const filteredTasks = computed(() => {
  if (!selectedRole.value) {
    return availableTasks.value
  }
  return availableTasks.value.filter(task => 
    task.role_binding === selectedRole.value
  )
})

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
    // 只显示未分配的任务
    availableTasks.value = response.data?.filter(task => 
      task.status === '未分配' || !task.status
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
    // 使用用户列表API，过滤活跃用户，排除admin用户
    const response = await getUserList({ limit: 100 })
    availableUsers.value = response.data?.filter(user => 
      user.status === 'active' && user.username !== 'admin'
    ) || []
  } catch (error) {
    ElMessage.error('加载可用用户失败')
    console.error('加载用户失败:', error)
  } finally {
    userLoading.value = false
  }
}

// 处理多选任务变化
const handleTaskSelectionChange = (selection: Task[]) => {
  selectedTasks.value = selection
}

// 处理当前任务变化（用于显示详情）
const handleCurrentTaskChange = (currentRow: Task | null) => {
  currentTask.value = currentRow
}

// 清空任务选择
const clearTaskSelection = () => {
  selectedTasks.value = []
  currentTask.value = null
}

// 清空已选用户
const clearSelectedUsers = () => {
  selectedUsers.value = []
}

const handleRoleChange = () => {
  // 当角色改变时，清除当前选择
  selectedTasks.value = []
  currentTask.value = null
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
  if (selectedTasks.value.length === 0) {
    ElMessage.warning('请选择要分配的任务')
    return
  }
  
  if (selectedUsers.value.length === 0) {
    ElMessage.warning('请选择执行角色')
    return
  }

  const taskNames = selectedTasks.value.map(task => task.name).join('、')
  const totalAssignments = selectedTasks.value.length * selectedUsers.value.length

  try {
    await ElMessageBox.confirm(
      `确定要将 ${selectedTasks.value.length} 个任务 (${taskNames}) 分配给 ${selectedUsers.value.length} 个执行角色吗？\n总共将创建 ${totalAssignments} 个任务分配。`,
      '确认批量分配',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )

    // 批量创建任务分配
    let successCount = 0
    let errorCount = 0
    
    for (const task of selectedTasks.value) {
      for (const user of selectedUsers.value) {
        try {
          await createTaskAssignment({
            task_id: task.id,
            user_id: user.id,
            username: user.username,
            status: '进行中',
            progress: 0,
            performance_score: 0,
            comments: ''
          })
          successCount++
        } catch (error) {
          console.error(`分配任务 ${task.name} 给用户 ${user.username} 失败:`, error)
          errorCount++
        }
      }
    }

    if (successCount > 0) {
      ElMessage.success(`成功创建 ${successCount} 个任务分配${errorCount > 0 ? `，失败 ${errorCount} 个` : ''}`)
    }
    
    if (errorCount > 0 && successCount === 0) {
      ElMessage.error(`任务分配失败，共 ${errorCount} 个分配失败`)
    }

    // 清空选择状态
    selectedTasks.value = []
    currentTask.value = null
    selectedUsers.value = []
    checkedAvailableUsers.value = []
    checkedSelectedUsers.value = []
    
    // 重新加载任务列表以更新状态
    await loadAvailableTasks()
  } catch (error: any) {
    if (error?.message !== 'cancel') {
      const errorMsg = error?.response?.data?.detail || error?.message || '批量任务分配失败'
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

  .assignment-layout {
    display: flex;
    gap: 12px;
    padding: 8px;

    .left-panel {
      width: 60%;
      display: flex;
      flex-direction: column;
      gap: 12px;

      .task-card {
        flex: 2;
        
        .card-header {
          display: flex;
          align-items: center;
          justify-content: space-between;
          font-weight: 500;
          font-size: 16px;

          .header-left {
            display: flex;
            align-items: center;
            gap: 8px;
          }

          .role-selector {
            display: flex;
            align-items: center;
            gap: 8px;
          }
        }

        .task-list {
          height: 100%;
          position: relative;

          .batch-info {
            position: absolute;
            bottom: 8px;
            left: 8px;
            right: 8px;
            background: #e6f3ff;
            border: 1px solid #66b3ff;
            border-radius: 4px;
            padding: 6px 12px;
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 14px;
            color: #0066cc;
            z-index: 10;

            .el-icon {
              font-size: 16px;
            }

            .el-button--text {
              padding: 0;
              margin-left: auto;
              color: #0066cc;
              font-size: 14px;
            }
          }
        }
      }

      .task-detail-card {
        flex: 1;

        .card-header {
          display: flex;
          align-items: center;
          gap: 8px;
          font-weight: 500;
          font-size: 16px;
        }

        .task-detail {
          height: 280px; // 设置固定合理高度
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
              grid-template-columns: 1fr;
              gap: 16px;

              .detail-item {
                &.detail-description {
                  grid-column: 1 / -1;
                }

                .detail-label {
                  display: block;
                  font-size: 12px;
                  color: #909399;
                  font-weight: 600;
                  margin-bottom: 6px;
                  text-transform: uppercase;
                  letter-spacing: 0.5px;
                }

                .detail-value {
                  font-size: 14px;
                  color: #303133;
                  line-height: 1.4;
                  word-break: break-all;
                  background: #f8f9fa;
                  padding: 8px 12px;
                  border-radius: 6px;
                  border-left: 4px solid #0066cc;
                  min-height: 24px;
                  display: flex;
                  align-items: center;

                  &.description-content {
                    align-items: flex-start;
                    padding: 12px;
                    line-height: 1.6;
                    white-space: pre-wrap;
                    word-break: break-word;
                    max-height: 120px;
                    overflow-y: auto;
                    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                    border-left: 4px solid #17a2b8;
                  }

                  .el-tag {
                    margin: 0;
                    font-weight: 600;
                  }
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
            padding: 40px 0;
            background: #f9f9f9;
            border-radius: 8px;
            font-size: 14px;
            gap: 8px;

            .el-icon {
              font-size: 24px;
              color: #c0c4cc;
            }

            .placeholder-tip {
              margin: 8px 0 0 0;
              color: #bbb;
              font-size: 12px;
              text-align: center;
              line-height: 1.4;
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
        flex: 1; // 占满剩余空间，与左侧高度一致

        .card-header {
          display: flex;
          align-items: center;
          justify-content: space-between;
          font-weight: 500;
          font-size: 16px;

          .header-left {
            display: flex;
            align-items: center;
            gap: 8px;
          }
        }

        .user-selection {
          display: flex;
          flex-direction: column;
          gap: 12px;
          height: 100%;

          .available-users-section,
          .selected-users-section {
            flex: 1;

            .section-header {
              display: flex;
              align-items: center;
              justify-content: space-between;
              margin-bottom: 8px;
              font-weight: 500;
              color: #333;
              font-size: 14px;

              .header-left {
                display: flex;
                align-items: center;
                gap: 6px;
              }
            }

            .user-list {
              border: 1px solid #dcdfe6;
              border-radius: 4px;
              flex: 1; // 使用flex布局自动分配高度
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
                padding: 8px 10px;
                cursor: pointer;
                border-bottom: 1px solid #f0f0f0;
                font-size: 14px;
                min-height: 50px;

                &:hover {
                  background: #f5f7fa;
                }

                .user-card-inline {
                  flex: 1;
                  background: linear-gradient(135deg, #e6f3ff 0%, #b3d9ff 100%);
                  border-radius: 6px;
                  padding: 10px 14px;
                  color: #0066cc;
                  box-shadow: 0 1px 4px rgba(179, 217, 255, 0.3);
                  display: flex;
                  flex-direction: row;
                  align-items: center;
                  justify-content: space-between;
                  border: 1px solid #cce7ff;
                  gap: 8px;
                  
                  .user-display {
                    font-weight: 600;
                    font-size: 16px;
                    line-height: 1.2;
                    white-space: nowrap;
                    overflow: hidden;
                    text-overflow: ellipsis;
                    flex: 1;
                  }

                  .user-role {
                    font-size: 14px;
                    font-weight: 500;
                    opacity: 0.9;
                    white-space: nowrap;
                    overflow: hidden;
                    text-overflow: ellipsis;
                    flex-shrink: 0;
                    background: rgba(255, 255, 255, 0.7);
                    padding: 2px 8px;
                    border-radius: 12px;
                    font-style: italic;
                  }
                }

                &.selected {
                  background: #f0f8ff;
                  border-color: #66b3ff;
                  justify-content: space-between;
                  
                  .user-card-inline {
                    background: linear-gradient(135deg, #cce7ff 0%, #99ccff 100%);
                    border: 1px solid #80bfff;
                    color: #003d7a;
                  }
                  
                  &:hover {
                    background: #fff2f0;
                    
                    .remove-icon {
                      color: #ff4d4f;
                    }
                  }
                  
                  .remove-icon {
                    color: #d9d9d9;
                    font-size: 14px;
                    transition: color 0.2s ease;
                    flex-shrink: 0;
                    
                    &:hover {
                      color: #ff4d4f;
                    }
                  }
                }

                &:last-child {
                  border-bottom: none;
                }
              }

              .empty-state {
                text-align: center;
                color: #999;
                padding: 30px 15px;
                font-size: 13px;
              }
            }
          }

          .selected-users-section {
            .user-list {
              background: #f8f9fa;
              border-color: #e8f4f8;
            }
          }
        }
      }

      .assignment-controls {
        flex: 0 0 auto;

        .el-button {
          height: 48px;
          font-size: 16px;
          font-weight: 600;
          
          .el-icon {
            margin-right: 6px;
          }
        }
      }
    }
  }

  // 响应式设计
  @media (max-width: 1200px) {
    .assignment-layout {
      .left-panel {
        width: 58%;
      }
      
      .right-panel {
        width: 42%;
      }
    }
  }

  @media (max-width: 992px) {
    .assignment-layout {
      flex-direction: column;
      
      .left-panel,
      .right-panel {
        width: 100%;
      }

      .right-panel {
        .user-selection-card {
          // 移动端保持flex布局，不设置固定高度
        }
        
        .user-selection {
          .user-list {
            min-height: 200px; // 设置最小高度确保可用性
          }
        }
      }
    }
  }
}

:deep(.el-card) {
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border: 1px solid #e8eaec;
}

:deep(.el-card__header) {
  padding: 12px 16px;
  background: linear-gradient(135deg, #fafbfc 0%, #f1f3f5 100%);
  border-bottom: 1px solid #e8eaec;
}

:deep(.el-card__body) {
  padding: 12px 16px;
}

:deep(.el-table .el-table__header th) {
  background: #f8f9fa;
  color: #495057;
  font-weight: 600;
  padding: 8px 0;
  font-size: 13px;
}

:deep(.el-table--enable-row-hover .el-table__body tr:hover > td) {
  background-color: #f8f9fa;
}

:deep(.el-table__body tr.current-row > td) {
  background-color: #e3f2fd;
}

:deep(.el-table .el-table__body td) {
  padding: 6px 0;
  font-size: 13px;
}

:deep(.el-table--small .el-table__cell) {
  padding: 4px 0;
}

:deep(.el-tag) {
  border-radius: 12px;
  font-size: 11px;
  height: 20px;
  line-height: 18px;
  padding: 0 8px;
}

:deep(.el-button--small) {
  height: 28px;
  padding: 5px 10px;
  font-size: 12px;
}
</style> 