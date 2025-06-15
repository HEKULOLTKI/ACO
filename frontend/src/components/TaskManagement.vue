<template>
  <div>
    <!-- 创建任务弹窗 -->
    <el-dialog
      v-model="createTaskVisible"
      title="创建任务"
      width="600px"
      @close="resetCreateForm"
    >
      <el-form
        ref="createFormRef"
        :model="createForm"
        :rules="createRules"
        label-width="100px"
      >
        <el-form-item label="任务名称" prop="name">
          <el-input
            v-model="createForm.name"
            placeholder="请输入任务名称"
            clearable
          />
        </el-form-item>
        <el-form-item label="任务类型" prop="type">
          <el-select
            v-model="createForm.type"
            placeholder="请选择任务类型"
            style="width: 100%"
          >
            <el-option label="网络搭建任务" value="网络搭建任务" />
            <el-option label="系统构建任务" value="系统构建任务" />
            <el-option label="运维监管任务" value="运维监管任务" />
            <el-option label="日志安全任务" value="日志安全任务" />
          </el-select>
        </el-form-item>
        <el-form-item label="任务阶段" prop="phase">
          <el-select
            v-model="createForm.phase"
            placeholder="请选择任务阶段"
            style="width: 100%"
          >
            <el-option label="检测阶段" value="检测阶段" />
            <el-option label="优化阶段" value="优化阶段" />
            <el-option label="配置阶段" value="配置阶段" />
            <el-option label="维护阶段" value="维护阶段" />
            <el-option label="测试阶段" value="测试阶段" />
            <el-option label="监控阶段" value="监控阶段" />
          </el-select>
        </el-form-item>
        <el-form-item label="任务描述" prop="description">
          <el-input
            v-model="createForm.description"
            type="textarea"
            :rows="4"
            placeholder="请输入任务描述"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="createTaskVisible = false">取消</el-button>
          <el-button
            type="primary"
            :loading="createLoading"
            @click="handleCreateSubmit"
          >
            创建
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 任务下发弹窗 -->
    <el-dialog
      v-model="assignTaskVisible"
      title="任务下发"
      width="700px"
      @close="resetAssignForm"
    >
      <div class="assign-task-content">
        <div class="task-selection">
          <h4>选择任务</h4>
          <el-table
            ref="taskTableRef"
            :data="unassignedTasks"
            @selection-change="handleTaskSelection"
            style="width: 100%; margin-bottom: 20px"
            max-height="300px"
          >
            <el-table-column type="selection" width="55" />
            <el-table-column prop="id" label="任务ID" width="80" />
            <el-table-column prop="name" label="任务名称" />
            <el-table-column prop="type" label="任务类型" width="120" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="scope">
                <el-tag type="info">{{ scope.row.status }}</el-tag>
              </template>
            </el-table-column>
          </el-table>
        </div>

        <div class="user-assignment" v-if="selectedTasks.length > 0">
          <h4>分配用户</h4>
          <el-form
            ref="assignFormRef"
            :model="assignForm"
            :rules="assignRules"
            label-width="100px"
          >
            <el-form-item label="选择用户" prop="username">
              <el-select
                v-model="assignForm.username"
                placeholder="请选择用户"
                style="width: 100%"
                @change="handleUserChange"
              >
                <el-option
                  v-for="user in userList"
                  :key="user.id"
                  :label="`${user.username} (${user.role})`"
                  :value="user.username"
                  :data-user-id="user.id"
                />
              </el-select>
            </el-form-item>
            <el-form-item label="备注说明" prop="comments">
              <el-input
                v-model="assignForm.comments"
                type="textarea"
                :rows="3"
                placeholder="请输入分配说明"
              />
            </el-form-item>
          </el-form>
        </div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="assignTaskVisible = false">取消</el-button>
          <el-button
            type="primary"
            :loading="assignLoading"
            :disabled="selectedTasks.length === 0 || !assignForm.username"
            @click="handleAssignSubmit"
          >
            下发任务
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 进度管理弹窗 -->
    <el-dialog
      v-model="progressVisible"
      title="进度管理"
      width="900px"
    >
      <div class="progress-management">
        <el-table
          :data="assignmentList"
          style="width: 100%"
        >
          <el-table-column prop="id" label="分配ID" width="80" />
          <el-table-column prop="task_id" label="任务ID" width="80" />
          <el-table-column label="任务信息" width="200">
            <template #default="scope">
              <div>
                <div class="task-name">{{ getTaskName(scope.row.task_id) }}</div>
                <div class="task-type">{{ getTaskType(scope.row.task_id) }}</div>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="username" label="执行用户" width="120" />
          <el-table-column label="进度" width="200">
            <template #default="scope">
              <div class="progress-container">
                <el-progress
                  :percentage="scope.row.progress"
                  :color="getProgressColor(scope.row.progress)"
                />
                <span class="progress-text">{{ scope.row.progress }}%</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态" width="100">
            <template #default="scope">
              <el-tag :type="getStatusTagType(scope.row.status)">
                {{ scope.row.status }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" fixed="right" width="120">
            <template #default="scope">
              <el-button
                link
                type="primary"
                size="small"
                @click="handleEditProgress(scope.row)"
              >
                编辑
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="progressVisible = false">关闭</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 编辑进度弹窗 -->
    <el-dialog
      v-model="editProgressVisible"
      title="编辑任务进度"
      width="500px"
    >
      <el-form
        ref="progressFormRef"
        :model="progressForm"
        :rules="progressRules"
        label-width="100px"
      >
        <el-form-item label="当前进度" prop="progress">
          <el-slider
            v-model="progressForm.progress"
            :step="5"
            show-input
            :max="100"
            style="margin-right: 20px"
          />
        </el-form-item>
        <el-form-item label="任务状态" prop="status">
          <el-select
            v-model="progressForm.status"
            placeholder="请选择状态"
            style="width: 100%"
          >
            <el-option label="进行中" value="进行中" />
            <el-option label="已完成" value="已完成" />
            <el-option label="已暂停" value="已暂停" />
            <el-option label="已取消" value="已取消" />
          </el-select>
        </el-form-item>
        <el-form-item label="性能评分" prop="performance_score">
          <el-input-number
            v-model="progressForm.performance_score"
            :min="0"
            :max="100"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="备注" prop="comments">
          <el-input
            v-model="progressForm.comments"
            type="textarea"
            :rows="3"
            placeholder="请输入备注信息"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="editProgressVisible = false">取消</el-button>
          <el-button
            type="primary"
            :loading="progressLoading"
            @click="handleProgressSubmit"
          >
            保存
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import {
  createTask,
  getTasks,
  createTaskAssignment,
  getTaskAssignments,
  updateTaskAssignment,
  type Task,
  type TaskAssignment
} from '@/api/task'
import { getUsers, type User } from '@/api/user'

// 弹窗显示状态
const createTaskVisible = ref(false)
const assignTaskVisible = ref(false)
const progressVisible = ref(false)
const editProgressVisible = ref(false)

// 加载状态
const createLoading = ref(false)
const assignLoading = ref(false)
const progressLoading = ref(false)

// 表单引用
const createFormRef = ref<FormInstance>()
const assignFormRef = ref<FormInstance>()
const progressFormRef = ref<FormInstance>()

// 数据
const unassignedTasks = ref<Task[]>([])
const assignmentList = ref<TaskAssignment[]>([])
const userList = ref<User[]>([])
const selectedTasks = ref<Task[]>([])
const currentEditAssignment = ref<TaskAssignment | null>(null)

// 创建任务表单
const createForm = reactive({
  name: '',
  type: '',
  phase: '',
  description: ''
})

// 任务分配表单
const assignForm = reactive({
  username: '',
  user_id: null as number | null,
  comments: ''
})

// 进度编辑表单
const progressForm = reactive({
  progress: 0,
  status: '',
  performance_score: 0,
  comments: ''
})

// 表单验证规则
const createRules: FormRules = {
  name: [{ required: true, message: '请输入任务名称', trigger: 'blur' }],
  type: [{ required: true, message: '请选择任务类型', trigger: 'change' }],
  phase: [{ required: true, message: '请选择任务阶段', trigger: 'change' }],
  description: [{ required: true, message: '请输入任务描述', trigger: 'blur' }]
}

const assignRules: FormRules = {
  username: [{ required: true, message: '请选择用户', trigger: 'change' }]
}

const progressRules: FormRules = {
  progress: [{ required: true, message: '请设置进度', trigger: 'blur' }],
  status: [{ required: true, message: '请选择状态', trigger: 'change' }]
}

// 计算属性
const taskMap = computed(() => {
  const map = new Map()
  unassignedTasks.value.forEach(task => {
    map.set(task.id, task)
  })
  return map
})

// 暴露的方法
const showCreateTask = () => {
  createTaskVisible.value = true
}

const showAssignTask = async () => {
  await loadUnassignedTasks()
  await loadUsers()
  assignTaskVisible.value = true
}

const showProgressManagement = async () => {
  await loadAssignments()
  await loadUnassignedTasks() // 为了获取任务信息
  progressVisible.value = true
}

// 加载数据的方法
const loadUnassignedTasks = async () => {
  try {
    const response = await getTasks({ status: '未分配' })
    unassignedTasks.value = response.data
  } catch (error) {
    console.error('加载未分配任务失败:', error)
  }
}

const loadUsers = async () => {
  try {
    const response = await getUsers()
    userList.value = response.data
  } catch (error) {
    console.error('加载用户列表失败:', error)
  }
}

const loadAssignments = async () => {
  try {
    const response = await getTaskAssignments()
    assignmentList.value = response.data
  } catch (error) {
    console.error('加载任务分配失败:', error)
  }
}

// 事件处理
const handleTaskSelection = (selection: Task[]) => {
  selectedTasks.value = selection
}

const handleUserChange = (username: string) => {
  const user = userList.value.find(u => u.username === username)
  if (user) {
    assignForm.user_id = user.id
  }
}

const handleCreateSubmit = async () => {
  if (!createFormRef.value) return

  await createFormRef.value.validate(async (valid) => {
    if (valid) {
      createLoading.value = true
      try {
        await createTask(createForm)
        ElMessage.success('任务创建成功')
        createTaskVisible.value = false
        emit('refresh')
      } catch (error) {
        ElMessage.error('任务创建失败')
      } finally {
        createLoading.value = false
      }
    }
  })
}

const handleAssignSubmit = async () => {
  if (!assignFormRef.value) return

  await assignFormRef.value.validate(async (valid) => {
    if (valid) {
      assignLoading.value = true
      try {
        // 为每个选中的任务创建分配
        for (const task of selectedTasks.value) {
          await createTaskAssignment({
            task_id: task.id,
            user_id: assignForm.user_id!,
            username: assignForm.username,
            status: '进行中',
            progress: 0,
            performance_score: 0,
            comments: assignForm.comments
          })
        }
        ElMessage.success(`成功下发 ${selectedTasks.value.length} 个任务`)
        assignTaskVisible.value = false
        emit('refresh')
      } catch (error) {
        ElMessage.error('任务下发失败')
      } finally {
        assignLoading.value = false
      }
    }
  })
}

const handleEditProgress = (assignment: TaskAssignment) => {
  currentEditAssignment.value = assignment
  progressForm.progress = assignment.progress
  progressForm.status = assignment.status
  progressForm.performance_score = assignment.performance_score
  progressForm.comments = assignment.comments || ''
  editProgressVisible.value = true
}

const handleProgressSubmit = async () => {
  if (!progressFormRef.value || !currentEditAssignment.value) return

  await progressFormRef.value.validate(async (valid) => {
    if (valid) {
      progressLoading.value = true
      try {
        await updateTaskAssignment(currentEditAssignment.value!.id, {
          progress: progressForm.progress,
          status: progressForm.status,
          performance_score: progressForm.performance_score,
          comments: progressForm.comments
        })
        ElMessage.success('进度更新成功')
        editProgressVisible.value = false
        await loadAssignments()
        emit('refresh')
      } catch (error) {
        ElMessage.error('进度更新失败')
      } finally {
        progressLoading.value = false
      }
    }
  })
}

// 重置表单
const resetCreateForm = () => {
  Object.assign(createForm, {
    name: '',
    type: '',
    phase: '',
    description: ''
  })
  createFormRef.value?.resetFields()
}

const resetAssignForm = () => {
  Object.assign(assignForm, {
    username: '',
    user_id: null,
    comments: ''
  })
  selectedTasks.value = []
  assignFormRef.value?.resetFields()
}

// 工具方法
const getTaskName = (taskId: number) => {
  const task = taskMap.value.get(taskId)
  return task?.name || '未知任务'
}

const getTaskType = (taskId: number) => {
  const task = taskMap.value.get(taskId)
  return task?.type || '未知类型'
}

const getProgressColor = (progress: number) => {
  if (progress < 30) return '#f56c6c'
  if (progress < 70) return '#e6a23c'
  return '#67c23a'
}

const getStatusTagType = (status: string) => {
  const typeMap: Record<string, string> = {
    '进行中': 'primary',
    '已完成': 'success',
    '已暂停': 'warning',
    '已取消': 'danger'
  }
  return typeMap[status] || 'info'
}

// 事件发射
const emit = defineEmits<{
  refresh: []
}>()

// 暴露方法给父组件
defineExpose({
  showCreateTask,
  showAssignTask,
  showProgressManagement
})
</script>

<style scoped lang="scss">
.assign-task-content {
  .task-selection {
    margin-bottom: 20px;
    
    h4 {
      margin: 0 0 15px 0;
      color: #303133;
      font-size: 16px;
    }
  }

  .user-assignment {
    border-top: 1px solid #ebeef5;
    padding-top: 20px;
    
    h4 {
      margin: 0 0 15px 0;
      color: #303133;
      font-size: 16px;
    }
  }
}

.progress-management {
  .task-name {
    font-weight: 500;
    color: #303133;
    margin-bottom: 4px;
  }
  
  .task-type {
    font-size: 12px;
    color: #909399;
  }

  .progress-container {
    display: flex;
    align-items: center;
    gap: 10px;
    
    .el-progress {
      flex: 1;
    }
    
    .progress-text {
      font-size: 12px;
      color: #606266;
      min-width: 35px;
    }
  }
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style> 