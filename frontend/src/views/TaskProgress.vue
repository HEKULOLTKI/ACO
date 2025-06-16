<template>
  <div class="task-progress">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>{{ authStore.isAdmin ? '全部任务进度' : '我的任务进度' }}</span>
        </div>
      </template>

      <!-- 搜索栏 -->
      <div class="search-bar">
        <el-form :model="searchForm" inline>
          <el-form-item label="任务名称">
            <el-input 
              v-model="searchForm.taskName" 
              placeholder="请输入任务名称"
              clearable
            />
          </el-form-item>
          <el-form-item label="执行角色">
            <el-input 
              v-model="searchForm.username" 
              placeholder="请输入执行角色"
              clearable
            />
          </el-form-item>
          <el-form-item label="状态">
            <el-select v-model="searchForm.status" placeholder="选择状态" clearable>
              <el-option label="进行中" value="进行中" />
              <el-option label="已完成" value="已完成" />
              <el-option label="未下发" value="未下发" />
            </el-select>
          </el-form-item>
          <el-form-item label="时间范围">
            <el-date-picker
              v-model="searchForm.dateRange"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
            />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">
              <el-icon><Search /></el-icon>
              搜索
            </el-button>
            <el-button @click="handleReset">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <!-- 统计卡片 -->
      <div class="stats-cards">
        <el-row :gutter="20">
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-content">
                <div class="stat-value">{{ stats.total }}</div>
                <div class="stat-label">总任务数</div>
              </div>
              <el-icon class="stat-icon total"><Document /></el-icon>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-content">
                <div class="stat-value">{{ stats.inProgress }}</div>
                <div class="stat-label">进行中</div>
              </div>
              <el-icon class="stat-icon progress"><Clock /></el-icon>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-content">
                <div class="stat-value">{{ stats.completed }}</div>
                <div class="stat-label">已完成</div>
              </div>
              <el-icon class="stat-icon completed"><CircleCheck /></el-icon>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-content">
                <div class="stat-value">{{ stats.avgProgress }}%</div>
                <div class="stat-label">平均进度</div>
              </div>
              <el-icon class="stat-icon avg"><TrendCharts /></el-icon>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 图表区域 -->
      <div class="charts-section">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-card>
              <template #header>
                <span>任务状态分布</span>
              </template>
              <div ref="statusChartRef" class="chart-container"></div>
            </el-card>
          </el-col>
          <el-col :span="12">
            <el-card>
              <template #header>
                <span>任务进度趋势</span>
              </template>
              <div ref="progressChartRef" class="chart-container"></div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 任务进度表格 -->
      <div class="progress-table">
        <el-table :data="progressList" v-loading="loading" style="width: 100%">
          <el-table-column prop="id" label="ID" width="60" />
          <el-table-column prop="task_name" label="任务名称" min-width="150" />
          <el-table-column prop="task_type" label="任务类型" width="120" />
          <el-table-column prop="username" label="执行角色" width="100" />
          <el-table-column prop="status" label="状态" width="100">
            <template #default="scope">
              <el-tag :type="getStatusType(scope.row.status)">
                {{ scope.row.status }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="progress" label="进度" width="150">
            <template #default="scope">
              <el-progress 
                :percentage="scope.row.progress" 
                :status="scope.row.progress === 100 ? 'success' : (scope.row.status === '未下发' ? 'exception' : '')"
                :stroke-width="8"
              />
            </template>
          </el-table-column>
          <el-table-column prop="performance_score" label="绩效评分" width="120">
            <template #default="scope">
              <el-rate 
                v-model="scope.row.performance_score" 
                :max="5" 
                disabled 
                show-score
                text-color="#ff9900"
              />
            </template>
          </el-table-column>
          <el-table-column prop="assigned_at" label="分配时间" width="150" />
          <el-table-column prop="last_update" label="最后更新" width="150" />
          <el-table-column prop="comments" label="备注" min-width="120" show-overflow-tooltip />
          <el-table-column label="操作" width="180" fixed="right">
            <template #default="scope">
              <el-button size="small" type="primary" @click="handleViewDetail(scope.row)">
                查看详情
              </el-button>
              <el-button size="small" type="success" @click="handleProgressManagementTable(scope.row)">
                进度管理
              </el-button>
            </template>
          </el-table-column>
        </el-table>

        <!-- 分页 -->
        <div class="pagination">
          <el-pagination
            v-model:current-page="pagination.currentPage"
            v-model:page-size="pagination.pageSize"
            :page-sizes="[10, 20, 50, 100]"
            :total="pagination.total"
            layout="sizes, prev, pager, next, jumper, total"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </div>
      </div>
    </el-card>

    <!-- 任务详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="任务进度管理"
      width="800px"
      :close-on-click-modal="false"
    >
      <div v-if="currentTask" class="task-detail-container">
        <!-- 任务基本信息 -->
        <div class="task-header">
          <div class="task-number">
            <span class="label">任务名称:</span>
            <span class="value">{{ currentTask.task_name }}</span>
          </div>
        </div>

        <!-- 任务描述 -->
        <div class="task-description">
          <label>任务描述</label>
          <el-input 
            v-model="currentTask.task_description"
            type="textarea"
            :rows="3"
            disabled
            placeholder="任务描述"
          />
        </div>

        <!-- 进度信息 -->
        <div class="progress-section">
          <div class="progress-item">
            <span class="progress-label">总体进度</span>
            <div class="progress-bar">
              <el-progress 
                :percentage="currentTask.progress" 
                :color="getProgressColor(currentTask.progress)"
                :stroke-width="20"
              />
              <span class="progress-text">进度{{ currentTask.progress }}%</span>
              <span class="performance-text">平均绩效: {{ Math.round(currentTask.performance_score * 920) }}万</span>
            </div>
          </div>
        </div>

        <!-- 任务详情表格 -->
        <div class="task-details-table">
          <div class="table-header">
            <div class="header-cell">任务ID</div>
            <div class="header-cell">任务类型</div>
            <div class="header-cell">任务状态</div>
            <div class="header-cell">阶段任务</div>
            <div class="header-cell">任务描述</div>
            <div class="header-cell">执行角色</div>
          </div>
          <div class="table-body">
            <div class="table-row">
              <div class="table-cell">{{ currentTask.task_id }}</div>
              <div class="table-cell">{{ currentTask.task_type }}</div>
              <div class="table-cell">
                <el-tag :type="getStatusType(currentTask.status)">
                  {{ currentTask.status }}
                </el-tag>
              </div>
              <div class="table-cell">执行阶段</div>
              <div class="table-cell">{{ currentTask.task_name }}</div>
              <div class="table-cell">
                <div class="role-card">
                  <span class="role-name">{{ currentTask.username }}</span>
                  <span class="role-type">系统分析师</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 绩效评分明细表格 -->
        <div class="performance-details-section">
          <h3 class="section-title">绩效评分明细</h3>
          <div class="performance-details-table">
            <div class="table-header">
              <div class="header-cell">序号</div>
              <div class="header-cell">任务名称</div>
              <div class="header-cell">任务明细</div>
              <div class="header-cell">测评点</div>
              <div class="header-cell">得分依据</div>
            </div>
            <div class="table-body">
              <div class="table-row" v-for="detail in performanceDetails" :key="detail.id">
                <div class="table-cell">{{ detail.sequence }}</div>
                <div class="table-cell">{{ detail.task_name }}</div>
                <div class="table-cell">{{ detail.task_detail }}</div>
                <div class="table-cell">{{ detail.evaluation_point }}</div>
                <div class="table-cell">{{ detail.score_basis }}</div>
              </div>
            </div>
          </div>
        </div>
              </div>
      </el-dialog>

    <!-- 进度管理对话框 -->
    <el-dialog
      v-model="progressManagementDialogVisible"
      title="进度管理"
      width="600px"
    >
      <el-form
        ref="progressManagementFormRef"
        :model="progressManagementForm"
        :rules="progressManagementRules"
        label-width="100px"
      >
        <el-form-item label="任务名称">
          <el-input v-model="progressManagementForm.task_name" disabled />
        </el-form-item>
        <el-form-item label="执行角色">
          <el-input v-model="progressManagementForm.username" disabled />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="progressManagementForm.status" placeholder="选择状态">
            <el-option label="进行中" value="进行中" />
            <el-option label="已完成" value="已完成" />
            <el-option label="未下发" value="未下发" />
          </el-select>
        </el-form-item>
        <el-form-item label="进度" prop="progress">
          <el-slider 
            v-model="progressManagementForm.progress" 
            :max="100" 
            show-input 
            :format-tooltip="(val: number) => `${val}%`"
          />
        </el-form-item>
        <el-form-item label="绩效评分" prop="performance_score">
          <el-rate v-model="progressManagementForm.performance_score" :max="5" show-text />
        </el-form-item>
        <el-form-item label="备注说明" prop="comments">
          <el-input 
            v-model="progressManagementForm.comments" 
            type="textarea"
            :rows="4"
            placeholder="请输入更新说明" 
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="progressManagementDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleProgressManagementSubmit">
            确定更新
          </el-button>
        </span>
      </template>
    </el-dialog>
    </div>
  </template>

<script setup lang="ts">
import { ref, reactive, onMounted, nextTick } from 'vue'
import { ElMessage, type FormInstance } from 'element-plus'
import { 
  Search, 
  Document, 
  Clock, 
  CircleCheck, 
  TrendCharts 
} from '@element-plus/icons-vue'
import * as echarts from 'echarts'
import { getMyTasks, getMyTaskStats, getTaskAssignments, updateTaskAssignment } from '@/api/task'
import { getTaskAssignmentStats } from '@/api/taskAssignment'
import { updateTaskProgress } from '@/api/taskProgress'
import { useAuthStore } from '@/store/modules/auth'

interface TaskProgress {
  id: number
  task_id: number
  task_name: string
  task_description: string
  task_type: string
  username: string
  status: string
  progress: number
  performance_score: number
  comments: string
  assigned_at: string
  last_update: string
}

interface Stats {
  total: number
  inProgress: number
  completed: number
  avgProgress: number
}

interface PerformanceDetail {
  id: number
  sequence: string
  task_name: string
  task_detail: string
  evaluation_point: string
  completion_rate: number
  score_basis: string
  performance_score: number
}

const authStore = useAuthStore()
const loading = ref(false)
const detailDialogVisible = ref(false)
const progressManagementDialogVisible = ref(false)
const progressManagementFormRef = ref<FormInstance>()
const statusChartRef = ref<HTMLElement>()
const progressChartRef = ref<HTMLElement>()

const searchForm = reactive({
  taskName: '',
  username: '',
  status: '',
  dateRange: [] as string[]
})

const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 0
})

const progressManagementForm = reactive({
  id: 0,
  task_name: '',
  username: '',
  status: '',
  progress: 0,
  performance_score: 0,
  comments: ''
})

const progressList = ref<TaskProgress[]>([])
const currentTask = ref<TaskProgress | null>(null)
const stats = ref<Stats>({
  total: 0,
  inProgress: 0,
  completed: 0,
  avgProgress: 0
})

const performanceDetails = ref<PerformanceDetail[]>([])

const progressManagementRules = {
  status: [
    { required: true, message: '请选择状态', trigger: 'change' }
  ],
  progress: [
    { required: true, message: '请设置进度', trigger: 'blur' },
    { type: 'number', min: 0, max: 100, message: '进度范围为0-100', trigger: 'blur' }
  ],
  performance_score: [
    { required: true, message: '请设置绩效评分', trigger: 'change' },
    { type: 'number', min: 0, max: 5, message: '绩效评分范围为0-5', trigger: 'change' }
  ]
}

const getStatusType = (status: string) => {
  switch (status) {
    case '已完成':
      return 'success'
    case '进行中':
      return 'warning'
    case '未下发':
      return 'danger'
    default:
      return ''
  }
}

const getProgressColor = (percentage: number) => {
  if (percentage < 30) {
    return '#f56c6c'
  } else if (percentage < 70) {
    return '#e6a23c'
  } else {
    return '#67c23a'
  }
}

const getTaskDescription = (taskType?: string, taskName?: string) => {
  // 根据任务类型和任务名称生成描述
  if (taskName?.includes('网络架构')) {
    return '设计企业网络拓扑结构和配置方案，确保网络架构的安全性和可扩展性'
  } else if (taskName?.includes('服务器') || taskName?.includes('环境')) {
    return '搭建生产环境服务器和应用系统，配置负载均衡和高可用架构'
  } else if (taskName?.includes('监控') || taskName?.includes('配置')) {
    return '配置系统监控和告警机制，建立完善的运维监控体系'
  } else if (taskName?.includes('安全') || taskName?.includes('审计')) {
    return '分析系统日志并识别安全威胁，建立安全审计机制'
  } else if (taskType?.includes('网络')) {
    return '将全网设备接入INC进行统一管理，构建区域控制，并下发安全配置'
  } else if (taskType?.includes('系统')) {
    return '配置和优化系统架构，确保系统性能和稳定性'
  } else if (taskType?.includes('安全')) {
    return '实施安全防护措施，建立完善的安全防护体系'
  } else {
    return '执行相关技术任务，确保项目目标的顺利完成'
  }
}

const loadProgressData = async () => {
  loading.value = true
  try {
    let tasksResponse
    
    // 根据用户角色决定调用哪个API
    if (authStore.isAdmin) {
      // 管理员获取所有任务分配
      tasksResponse = await getTaskAssignments({
        status: searchForm.status || undefined,
        skip: (pagination.currentPage - 1) * pagination.pageSize,
        limit: pagination.pageSize
      })
    } else {
      // 普通用户获取个人任务
      tasksResponse = await getMyTasks({
        status: searchForm.status || undefined
      })
    }
    
    // 直接使用后端返回的数据，无需复杂映射
    progressList.value = tasksResponse.data?.map(item => ({
      id: item.id,
      task_id: item.task_id,
      task_name: item.task_name || `任务 ${item.task_id}`,
      task_description: getTaskDescription(item.task_type, item.task_name),
      task_type: item.task_type || '未知类型',
      username: item.username,
      status: item.status,
      progress: item.progress,
      performance_score: item.performance_score,
      comments: item.comments || '',
      assigned_at: item.assigned_at,
      last_update: item.last_update
    })) || []
    
    // 如果是普通用户，直接使用数据长度作为总数
    // 如果是管理员，需要单独获取总数（这里简化处理）
    pagination.total = progressList.value.length
    
    // 计算统计数据
    calculateStats()
    
    // 获取统计数据
    try {
      if (authStore.isAdmin) {
        // 管理员获取全部任务分配统计
        const statsResponse = await getTaskAssignmentStats()
        if (statsResponse.data) {
          stats.value = {
            total: statsResponse.data.total_assignments,
            inProgress: statsResponse.data.in_progress,
            completed: statsResponse.data.completed,
            avgProgress: Math.round(statsResponse.data.avg_progress || 0)
          }
        }
      } else {
        // 普通用户获取个人任务统计
        const statsResponse = await getMyTaskStats()
        if (statsResponse.data) {
          stats.value = {
            total: statsResponse.data.total_tasks,
            inProgress: statsResponse.data.in_progress_tasks,
            completed: statsResponse.data.completed_tasks,
            avgProgress: Math.round((statsResponse.data.average_score || 0) * 20) // 转换为百分比
          }
        }
      }
    } catch (statsError) {
      console.warn('获取统计数据失败:', statsError)
      // 如果统计API失败，使用计算的统计数据
    }
  } catch (error) {
    ElMessage.error('加载任务进度数据失败')
    console.error('加载任务进度失败:', error)
  } finally {
    loading.value = false
  }
}

const calculateStats = () => {
  const total = progressList.value.length
  const inProgress = progressList.value.filter(item => item.status === '进行中').length
  const completed = progressList.value.filter(item => item.status === '已完成').length
  const avgProgress = total > 0 
    ? Math.round(progressList.value.reduce((sum, item) => sum + item.progress, 0) / total)
    : 0
  
  stats.value = {
    total,
    inProgress,
    completed,
    avgProgress
  }
}

const initCharts = () => {
  nextTick(() => {
    // 状态分布饼图
    if (statusChartRef.value) {
      const statusChart = echarts.init(statusChartRef.value)
      const statusData = [
        { value: stats.value.inProgress, name: '进行中' },
        { value: stats.value.completed, name: '已完成' },
        { value: progressList.value.filter(item => item.status === '未下发').length, name: '未下发' }
      ]
      
      statusChart.setOption({
        tooltip: {
          trigger: 'item'
        },
        legend: {
          orient: 'vertical',
          left: 'left'
        },
        series: [
          {
            name: '任务状态',
            type: 'pie',
            radius: '50%',
            data: statusData,
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      })
    }
    
    // 进度趋势图
    if (progressChartRef.value) {
      const progressChart = echarts.init(progressChartRef.value)
      const progressData = progressList.value.map(item => ({
        name: item.task_name,
        value: item.progress
      }))
      
      progressChart.setOption({
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: progressData.map(item => item.name),
          axisLabel: {
            rotate: 45,
            interval: 0
          }
        },
        yAxis: {
          type: 'value',
          max: 100,
          axisLabel: {
            formatter: '{value}%'
          }
        },
        series: [
          {
            name: '进度',
            type: 'bar',
            data: progressData.map(item => item.value),
            itemStyle: {
              color: function(params: any) {
                const colorList = ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de']
                return colorList[params.dataIndex % colorList.length]
              }
            }
          }
        ]
      })
    }
  })
}

const handleSearch = () => {
  pagination.currentPage = 1
  loadProgressData()
}

const handleReset = () => {
  searchForm.taskName = ''
  searchForm.username = ''
  searchForm.status = ''
  searchForm.dateRange = []
  pagination.currentPage = 1
  loadProgressData()
}



const handleViewDetail = (row: TaskProgress) => {
  currentTask.value = row
  loadPerformanceDetails(row.id)
  detailDialogVisible.value = true
}

const handleProgressManagement = () => {
  // 进度管理功能，可以跳转到进度管理页面或弹出管理对话框
  ElMessage.info('进度管理功能开发中...')
  // 这里可以添加具体的进度管理逻辑
  // 例如：router.push('/progress-management')
}

const handleProgressManagementTable = (row: TaskProgress) => {
  // 表格中的进度管理功能
  progressManagementDialogVisible.value = true
  Object.assign(progressManagementForm, {
    id: row.id,
    task_name: row.task_name,
    username: row.username,
    status: row.status,
    progress: row.progress,
    performance_score: row.performance_score,
    comments: row.comments
  })
}

const handleProgressManagementSubmit = async () => {
  if (!progressManagementFormRef.value) return
  
  try {
    await progressManagementFormRef.value.validate()
    
    // 根据用户角色选择合适的API
    if (authStore.isAdmin) {
      await updateTaskAssignment(progressManagementForm.id, {
        status: progressManagementForm.status,
        progress: progressManagementForm.progress,
        performance_score: progressManagementForm.performance_score,
        comments: progressManagementForm.comments
      })
    } else {
      await updateTaskProgress(progressManagementForm.id, {
        status: progressManagementForm.status,
        progress: progressManagementForm.progress,
        performance_score: progressManagementForm.performance_score,
        comments: progressManagementForm.comments
      })
    }
    
    ElMessage.success('进度更新成功')
    progressManagementDialogVisible.value = false
    loadProgressData()
  } catch (error: any) {
    ElMessage.error('更新失败')
    console.error('更新任务进度失败:', error)
  }
}

const loadPerformanceDetails = (taskId: number) => {
  // 这里是模拟数据，实际应该从后端API获取
  // 根据不同任务类型生成相应的绩效评分明细
  performanceDetails.value = [
    {
      id: 1,
      sequence: '1.1',
      task_name: '用户流量访问测试',
      task_detail: '测试用户访问系统的流量情况，监控并发访问性能',
      evaluation_point: '访问流量监控',
      completion_rate: 100,
      score_basis: '成功监控到用户访问流量，并发处理能力达标',
      performance_score: 15
    },
    {
      id: 2,
      sequence: '1.2',
      task_name: '系统性能测试',
      task_detail: '测试系统在高负载下的性能表现，包括响应时间和吞吐量',
      evaluation_point: '性能指标监控',
      completion_rate: 95,
      score_basis: '系统响应时间符合要求，吞吐量达到预期指标',
      performance_score: 12
    },
    {
      id: 3,
      sequence: '2.1',
      task_name: '安全漏洞扫描',
      task_detail: '对系统进行全面的安全漏洞扫描，包括SQL注入、XSS等',
      evaluation_point: '漏洞检测',
      completion_rate: 100,
      score_basis: '发现并修复所有高危漏洞，安全评估通过',
      performance_score: 20
    },
    {
      id: 4,
      sequence: '2.2',
      task_name: '权限管理测试',
      task_detail: '测试系统的权限控制机制，验证角色权限分配',
      evaluation_point: '权限验证',
      completion_rate: 98,
      score_basis: '权限控制机制运行正常，访问控制有效',
      performance_score: 18
    },
    {
      id: 5,
      sequence: '3.1',
      task_name: '数据备份恢复测试',
      task_detail: '测试系统数据备份和恢复机制的有效性',
      evaluation_point: '备份恢复验证',
      completion_rate: 92,
      score_basis: '备份恢复流程完整，数据完整性验证通过',
      performance_score: 16
    },
    {
      id: 6,
      sequence: '3.2',
      task_name: '日志审计配置',
      task_detail: '配置系统日志审计功能，确保操作可追溯',
      evaluation_point: '审计日志',
      completion_rate: 100,
      score_basis: '日志记录完整，审计功能正常运行',
      performance_score: 14
    },
    {
      id: 7,
      sequence: '4.1',
      task_name: '网络安全配置',
      task_detail: '配置防火墙规则，设置网络访问控制策略',
      evaluation_point: '网络安全',
      completion_rate: 96,
      score_basis: '防火墙规则配置正确，网络隔离有效',
      performance_score: 17
    },
    {
      id: 8,
      sequence: '4.2',
      task_name: '入侵检测部署',
      task_detail: '部署入侵检测系统，实现实时安全监控',
      evaluation_point: '入侵检测',
      completion_rate: 88,
      score_basis: '入侵检测系统正常运行，告警机制有效',
      performance_score: 13
    }
  ]
}

const handleSizeChange = (val: number) => {
  pagination.pageSize = val
  pagination.currentPage = 1
  loadProgressData()
}

const handleCurrentChange = (val: number) => {
  pagination.currentPage = val
  loadProgressData()
}

onMounted(() => {
  loadProgressData().then(() => {
    initCharts()
  })
})
</script>

<style scoped lang="scss">
.task-progress {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .search-bar {
    margin-bottom: 20px;
    padding: 20px;
    background: #f5f5f5;
    border-radius: 4px;
  }

  .stats-cards {
    margin-bottom: 20px;

    .stat-card {
      position: relative;
      overflow: hidden;

      .stat-content {
        .stat-value {
          font-size: 32px;
          font-weight: bold;
          color: #333;
          margin-bottom: 8px;
        }

        .stat-label {
          font-size: 14px;
          color: #666;
        }
      }

      .stat-icon {
        position: absolute;
        right: 20px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 48px;
        opacity: 0.3;

        &.total {
          color: #409eff;
        }

        &.progress {
          color: #e6a23c;
        }

        &.completed {
          color: #67c23a;
        }

        &.avg {
          color: #f56c6c;
        }
      }
    }
  }

  .charts-section {
    margin-bottom: 20px;

    .chart-container {
      height: 300px;
    }
  }

  .progress-table {
    .pagination {
      margin-top: 20px;
      text-align: right;
    }
  }

  .task-detail {
    .el-descriptions {
      margin-top: 20px;
    }
  }
}

.task-detail-container {
  padding: 20px;
  
  .task-header {
    margin-bottom: 20px;
    padding: 15px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 8px;
    
    .task-number {
      font-size: 18px;
      .label {
        font-weight: bold;
      }
      .value {
        margin-left: 10px;
      }
    }
  }

  .task-description {
    margin-bottom: 20px;
    padding: 15px;
    background: #f8f9fa;
    border-radius: 8px;
    
    label {
      display: block;
      margin-bottom: 8px;
      font-weight: 500;
      color: #333;
    }
    
    .description-detail {
      margin-top: 10px;
      padding: 12px;
      background: white;
      border-radius: 4px;
      color: #666;
      font-size: 14px;
      line-height: 1.6;
      border-left: 4px solid #409eff;
    }
  }

  .progress-section {
    margin-bottom: 20px;
    padding: 15px;
    background: #f8f9fa;
    border-radius: 8px;
    
    .progress-item {
      .progress-label {
        display: block;
        margin-bottom: 10px;
        font-weight: 500;
        color: #333;
      }
      
      .progress-bar {
        display: flex;
        align-items: center;
        gap: 15px;
        
        .el-progress {
          flex: 1;
        }
        
        .progress-text {
          font-weight: bold;
          color: #409eff;
          min-width: 80px;
        }
        
        .performance-text {
          font-weight: bold;
          color: #67c23a;
          min-width: 120px;
        }
      }
    }
  }

  .task-details-table {
    margin-bottom: 20px;
    border: 1px solid #e4e7ed;
    border-radius: 8px;
    overflow: hidden;
    
    .table-header {
      display: flex;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      
      .header-cell {
        flex: 1;
        padding: 12px;
        font-weight: bold;
        text-align: center;
        border-right: 1px solid rgba(255, 255, 255, 0.2);
        
        &:last-child {
          border-right: none;
        }
      }
    }
    
    .table-body {
      .table-row {
        display: flex;
        background: white;
        
        .table-cell {
          flex: 1;
          padding: 12px;
          text-align: center;
          border-right: 1px solid #e4e7ed;
          
          &:last-child {
            border-right: none;
          }
          
          .role-card {
            display: inline-flex;
            flex-direction: column;
            align-items: center;
            padding: 8px 12px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 6px;
            
            .role-name {
              font-weight: bold;
              margin-bottom: 2px;
            }
            
            .role-type {
              font-size: 12px;
              opacity: 0.9;
            }
          }
        }
      }
    }
  }

  .performance-details-section {
    margin-bottom: 20px;
    
    .section-title {
      margin-bottom: 15px;
      font-size: 16px;
      font-weight: bold;
      color: #333;
      border-left: 4px solid #409eff;
      padding-left: 10px;
    }
  }

  .performance-details-table {
    margin-bottom: 20px;
    border: 1px solid #e4e7ed;
    border-radius: 8px;
    overflow: hidden;
    
    .table-header {
      display: flex;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      
      .header-cell {
        flex: 1;
        padding: 12px;
        font-weight: bold;
        text-align: center;
        border-right: 1px solid rgba(255, 255, 255, 0.2);
        font-size: 14px;
        
        &:last-child {
          border-right: none;
        }
      }
    }
    
    .table-body {
      .table-row {
        display: flex;
        background: white;
        border-bottom: 1px solid #e4e7ed;
        
        &:last-child {
          border-bottom: none;
        }
        
        &:hover {
          background: #f5f7fa;
        }
        
        .table-cell {
          flex: 1;
          padding: 12px;
          text-align: center;
          border-right: 1px solid #e4e7ed;
          font-size: 13px;
          
          &:last-child {
            border-right: none;
          }
          
          .completion-text {
            display: block;
            margin-top: 4px;
            font-size: 12px;
            color: #666;
          }
          
          .score-value {
            font-weight: bold;
            font-size: 16px;
            color: #67c23a;
            background: linear-gradient(135deg, #67c23a, #85ce61);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
          }
        }
      }
    }
  }

  .performance-summary {
    display: flex;
    justify-content: space-around;
    padding: 20px;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    border-radius: 8px;
    margin-top: 15px;
    
    .summary-item {
      text-align: center;
      
      .summary-label {
        display: block;
        font-size: 14px;
        color: #666;
        margin-bottom: 5px;
      }
      
      .summary-value {
        font-size: 18px;
        font-weight: bold;
        color: #333;
        
        &.highlight {
          font-size: 22px;
          color: #67c23a;
          text-shadow: 0 2px 4px rgba(103, 194, 58, 0.3);
        }
      }
    }
  }

  .bottom-actions {
    margin-top: 30px;
    text-align: center;
    padding: 20px;
    background: #f8f9fa;
    border-radius: 8px;
    
    .el-button {
      margin: 0 10px;
      min-width: 120px;
    }
  }
}
</style> 