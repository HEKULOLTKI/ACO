<template>
  <div class="dashboard">
    <!-- 统计卡片网格 -->
    <div class="stats-grid">
      <!-- 当前在线设备 -->
      <div class="stat-card stat-card-1">
        <div class="stat-icon">
          <img src="@/assets/icon/组 3589.png" alt="在线设备" />
        </div>
        <div class="stat-info">
          <div class="stat-number">3台</div>
          <div class="stat-label">当前在线设备</div>
        </div>
      </div>

      <!-- 活跃用户数 -->
      <div class="stat-card stat-card-2">
        <div class="stat-icon">
          <img src="@/assets/icon/组 3590.png" alt="活跃用户" />
        </div>
        <div class="stat-info">
          <div class="stat-number">20人</div>
          <div class="stat-label">活跃用户数</div>
        </div>
      </div>

      <!-- 处理任务数 -->
      <div class="stat-card stat-card-3">
        <div class="stat-icon">
          <img src="@/assets/icon/组 3591.png" alt="处理任务" />
        </div>
        <div class="stat-info">
          <div class="stat-number">{{ deviceStats.online_devices }}台</div>
          <div class="stat-label">在线设备数</div>
        </div>
      </div>

      <!-- 系统运行状态 -->
      <div class="stat-card stat-card-4">
        <div class="stat-icon">
          <img src="@/assets/icon/组 3592.png" alt="运行状态" />
        </div>
        <div class="stat-info">
          <div class="stat-number">运行中</div>
          <div class="stat-label">系统运行状态</div>
        </div>
      </div>

      <!-- 备份磁盘占用 -->
      <div class="stat-card stat-card-5">
        <div class="stat-icon">
          <img src="@/assets/icon/组 3593.png" alt="磁盘占用" />
        </div>
        <div class="stat-info">
          <div class="stat-number">694MB</div>
          <div class="stat-label">备份磁盘占用</div>
        </div>
      </div>

      <!-- 告警数量 -->
      <div class="stat-card stat-card-6">
        <div class="stat-icon">
          <img src="@/assets/icon/组 3594.png" alt="告警数量" />
        </div>
        <div class="stat-info">
          <div class="stat-number">5条</div>
          <div class="stat-label">告警数量</div>
        </div>
      </div>
    </div>

    <!-- 图表区域 -->
    <div class="charts-section">
      <!-- 系统综合对比图 -->
      <div class="chart-card system-chart">
        <div class="chart-header">
          <h3 class="chart-title">
            <img src="@/assets/icon/组 3000.png" alt="系统监控" class="chart-icon-img" />
            系统资源实时监控
          </h3>
        </div>
        <div class="chart-content">
          <div class="chart-legend">
            <div class="legend-items">
              <span class="legend-item">
                <span class="legend-dot cpu"></span>
                CPU 使用率
              </span>
              <span class="legend-item">
                <span class="legend-dot memory"></span>
                内存使用率
              </span>
              <span class="legend-item">
                <span class="legend-dot disk"></span>
                磁盘使用率
              </span>
            </div>
            <span class="legend-realtime-value">
              <span class="realtime-time">{{ realtimeInfo.time }}</span>
              <span class="realtime-value">{{ realtimeInfo.value }}%</span>
            </span>
          </div>
          <div ref="systemChart" class="chart-container"></div>
        </div>
      </div>

      <!-- 告警信息和设备告警区域 -->
      <div class="alert-section">
        <!-- 告警信息 -->
        <div class="alert-card">
          <div class="alert-header">
            <h3 class="alert-title">
              <img src="@/assets/icon/组 3000.png" alt="告警信息" class="alert-icon-img" />
              告警信息
            </h3>
          </div>
          <div class="alert-content">
            <div class="alert-charts">
              <!-- 告警状态统计 -->
              <div class="alert-chart-item">
                <div class="chart-selector">
                  <select v-model="alertStatusType" @change="updateAlertStatusChart">
                    <option value="status">告警状态</option>
                    <option value="level">告警等级</option>
                    <option value="type">告警类型</option>
                  </select>
                </div>
                <div ref="alertStatusChart" class="alert-pie-chart"></div>
                <div class="alert-chart-label">告警状态统计</div>
              </div>
              <!-- 告警级别统计 -->
              <div class="alert-chart-item">
                <div class="chart-selector">
                  <select v-model="alertLevelType" @change="updateAlertLevelChart">
                    <option value="level">告警级别</option>
                    <option value="region">区域分布</option>
                    <option value="time">时段分布</option>
                  </select>
                </div>
                <div ref="alertLevelChart" class="alert-pie-chart"></div>
                <div class="alert-chart-label">告警级别统计</div>
              </div>
            </div>
            <!-- 图例 -->
            <div class="alert-legends">
              <div class="legend-row">
                <div class="legend-item">
                  <span class="legend-dot" style="background: #ff7875;"></span>
                  CPU告警
                </div>
                <div class="legend-percentage">42%</div>
              </div>
              <div class="legend-row">
                <div class="legend-item">
                  <span class="legend-dot" style="background: #ffa940;"></span>
                  内存告警
                </div>
                <div class="legend-percentage">42%</div>
              </div>
              <div class="legend-row">
                <div class="legend-item">
                  <span class="legend-dot" style="background: #52c41a;"></span>
                  磁盘告警
                </div>
                <div class="legend-percentage">42%</div>
              </div>
            </div>
          </div>
        </div>

        <!-- 设备告警 -->
        <div class="device-alert-card">
          <div class="device-alert-header">
            <h3 class="device-alert-title">
              <img src="@/assets/icon/组 3000.png" alt="设备告警" class="device-alert-icon-img" />
              设备告警
            </h3>
          </div>
          <div class="device-alert-content">
            <div class="device-alert-list">
              <div v-for="(alert, index) in systemAlertData" :key="index" class="device-alert-item">
                <div class="alert-type-header">
                  <span class="alert-type-badge">{{ alert.type }}</span>
                  <span class="alert-category-badge">{{ alert.category }}</span>
                  <span class="alert-phase-badge" :class="getAlertLevelClass(alert.phase)">{{ alert.phase }}</span>
                </div>
                <div class="alert-details">
                  <div class="alert-detail-line">{{ alert.detail1 }}</div>
                  <div class="alert-detail-line">{{ alert.detail2 }}</div>
                  <div class="alert-detail-line">{{ alert.detail3 }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 设备信息表格 -->
    <div class="device-table-section">
      <div class="table-card">
        <div class="table-header">
          <h3 class="table-title">
            <img src="@/assets/icon/设备.png" alt="设备列表" class="table-icon-img" />
            设备列表
          </h3>
          <div class="table-actions">
            <button class="action-btn create-btn" @click="handleCreateDevice">
              <img src="@/assets/icon/添加.png" alt="添加设备" class="btn-icon-img" />
              添加设备
            </button>
            <button class="action-btn download-btn" @click="handleManageDevice">
              <img src="@/assets/icon/设备.png" alt="设备管理" class="btn-icon-img" />
              设备管理
            </button>
            <button class="action-btn progress-btn" @click="handleMonitorDevice">
              <img src="@/assets/icon/系统参数.png" alt="设备监控" class="btn-icon-img" />
              设备监控
            </button>
            <button class="action-btn import-btn" @click="handleRefreshData">
              <img src="@/assets/icon/upload.png" alt="刷新数据" class="btn-icon-img" />
              刷新数据
            </button>
          </div>
        </div>
        <div class="table-content">
          <div v-if="deviceLoading" class="loading-container">
            <div class="loading-text">加载中...</div>
          </div>
          <table v-else class="device-table">
            <thead>
              <tr>
                <th>设备ID</th>
                <th>设备名称</th>
                <th>设备类型</th>
                <th>IP地址</th>
                <th>位置</th>
                <th>状态</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="device in deviceList" :key="device.id">
                <td>{{ device.id }}</td>
                <td>{{ device.name }}</td>
                <td>{{ device.type || '-' }}</td>
                <td>{{ device.ip || '-' }}</td>
                <td>{{ device.location || '-' }}</td>
                <td>
                  <span :class="['status-tag', getDeviceStatusClass(device.status)]">
                    {{ getDeviceStatusText(device.status) }}
                  </span>
                </td>
              </tr>
              <tr v-if="deviceList.length === 0">
                <td colspan="6" style="text-align: center; color: #999; padding: 40px;">
                  暂无设备数据
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>


  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import { getDevices } from '@/api/device'
import type { Device, DeviceStatistics } from '@/types/device'
import { ElMessage } from 'element-plus'

interface DeviceInfo {
  id: number
  type1: string
  type2: string
  phase: string
  description: string
  role: string
  status: string
}



const systemChart = ref<HTMLElement>()
const deviceChart = ref<HTMLElement>()
const alertStatusChart = ref<HTMLElement>()
const alertLevelChart = ref<HTMLElement>()
// 实时数据
const realtimeData = ref({
  cpu: [18, 20, 22, 19, 21, 20, 23, 18, 19, 21, 20],
  memory: [38, 40, 42, 39, 41, 40, 43, 38, 39, 41, 40],
  disk: [62, 64, 66, 63, 65, 64, 67, 62, 63, 65, 64]
})

// 实时信息显示
const realtimeInfo = ref({
  time: '18:35:12',
  value: 64
})

let chartInstance: any = null
let animationTimer: any = null

// 告警图表选择器状态
const alertStatusType = ref('status')
const alertLevelType = ref('level')

// 生成时间标签
const generateTimeLabels = () => {
  const labels = []
  const now = new Date()
  
  for (let i = 10; i >= 0; i--) {
    const time = new Date(now.getTime() - i * 10000) // 每10秒一个点
    const timeStr = time.toTimeString().slice(0, 8)
    labels.push(timeStr)
  }
  
  return labels
}

// 设备列表数据 - 使用后端API
const deviceList = ref<Device[]>([])
const deviceStats = ref<DeviceStatistics>({
  total_devices: 0,
  online_devices: 0,
  offline_devices: 0,
  type_statistics: {}
})
const deviceLoading = ref(false)

// 系统告警数据
const systemAlertData = ref([
  {
    type: '风扇异常',
    category: '硬件告警',
    phase: '严重告警',
    detail1: '服务器节点1 - 风扇转速异常 (2100RPM)',
    detail2: '温度传感器显示: 78°C | 超过安全阈值',
    detail3: '建议立即检查风扇运行状态或更换'
  },
  {
    type: '电源异常',
    category: '硬件告警',
    phase: '警告',
    detail1: '服务器节点2 - 电源模块功率异常 (85%)',
    detail2: '电压不稳定: 11.2V | 标准值: 12V±5%',
    detail3: '建议检查电源线路或更换电源模块'
  }
])



// 加载设备数据
const loadDeviceData = async () => {
  if (deviceLoading.value) return
  
  deviceLoading.value = true
  try {
    // 获取设备列表
    const devicesResponse = await getDevices({ limit: 10 })
    deviceList.value = devicesResponse.data.devices
    
    // 计算本地设备统计（不调用统计接口）
    const onlineDevices = deviceList.value.filter(device => device.status === 'online').length
    const offlineDevices = deviceList.value.filter(device => device.status === 'offline').length
    const maintenanceDevices = deviceList.value.filter(device => device.status === 'maintenance').length
    
    // 统计设备类型
    const typeStats: { [key: string]: number } = {}
    deviceList.value.forEach(device => {
      if (device.type) {
        typeStats[device.type] = (typeStats[device.type] || 0) + 1
      }
    })
    
    deviceStats.value = {
      total_devices: deviceList.value.length,
      online_devices: onlineDevices,
      offline_devices: offlineDevices + maintenanceDevices,
      type_statistics: typeStats
    }
    
  } catch (error) {
    console.error('加载设备数据失败:', error)
    // 如果是网络错误或者无法连接后端，使用默认数据
    deviceList.value = [
      {
        id: 1,
        name: '服务器-01',
        type: 'server',
        ip: '192.168.1.100',
        status: 'online',
        location: '机房A-01'
      },
      {
        id: 2,
        name: '服务器-02',
        type: 'server',
        ip: '192.168.1.101',
        status: 'offline',
        location: '机房A-02'
      },
      {
        id: 3,
        name: '工作站-01',
        type: 'workstation',
        ip: '192.168.1.200',
        status: 'online',
        location: '办公室-203'
      }
    ]
    deviceStats.value = {
      total_devices: 3,
      online_devices: 2,
      offline_devices: 1,
      type_statistics: {
        'server': 2,
        'workstation': 1
      }
    }
    ElMessage.warning('使用演示数据，请确保后端服务正常运行')
  } finally {
    deviceLoading.value = false
  }
}

// 设备操作处理函数
const handleCreateDevice = () => {
  // 跳转到设备管理页面
  ElMessage.info('跳转到设备管理页面创建设备')
}

const handleManageDevice = () => {
  // 跳转到设备管理页面
  ElMessage.info('跳转到设备管理页面')
}

const handleMonitorDevice = () => {
  // 设备监控功能
  ElMessage.info('设备监控功能')
}

const handleRefreshData = () => {
  loadDeviceData()
  ElMessage.success('数据刷新成功')
}



const getDeviceStatusClass = (status: string) => {
  const statusMap: { [key: string]: string } = {
    'online': 'status-online',
    'offline': 'status-offline',
    'maintenance': 'status-maintenance'
  }
  return statusMap[status] || 'status-default'
}

const getDeviceStatusText = (status: string) => {
  const textMap: { [key: string]: string } = {
    'online': '在线',
    'offline': '离线',
    'maintenance': '维护中'
  }
  return textMap[status] || status
}

// 根据告警级别返回对应的CSS类
const getAlertLevelClass = (level: string) => {
  const levelMap: { [key: string]: string } = {
    '严重告警': 'alert-critical',
    '警告': 'alert-warning',
    '一般告警': 'alert-normal'
  }
  return levelMap[level] || 'alert-normal'
}

const initSystemChart = () => {
  if (!systemChart.value) return
  
  chartInstance = echarts.init(systemChart.value)
  
  // 生成时间标签
  const timeLabels = generateTimeLabels()
  
  const option = {
    grid: {
      top: 40,
      left: 60,
      right: 40,
      bottom: 40
    },
    xAxis: {
      type: 'category',
      data: timeLabels,
      axisLine: {
        lineStyle: { color: '#E5E7EB' }
      },
      axisTick: { show: false },
      axisLabel: {
        color: '#6B7280',
        fontSize: 11,
        interval: 2
      }
    },
    yAxis: {
      type: 'value',
      min: 0,
      max: 100,
      interval: 20,
      axisLine: { show: false },
      axisTick: { show: false },
      splitLine: {
        lineStyle: { color: '#F3F4F6', type: 'dashed' }
      },
      axisLabel: {
        color: '#6B7280',
        fontSize: 11,
        formatter: '{value}%'
      }
    },
        series: [
      {
        name: 'CPU使用率',
        type: 'line',
        smooth: true,
        lineStyle: { 
          color: '#10B981', 
          width: 3 
        },
        itemStyle: { 
          color: '#10B981',
          borderColor: '#10B981',
          borderWidth: 2
        },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(16, 185, 129, 0.2)' },
              { offset: 1, color: 'rgba(16, 185, 129, 0.02)' }
            ]
          }
        },
        data: realtimeData.value.cpu,
        animationDuration: 1000,
        animationEasing: 'cubicOut'
      },
      {
        name: '内存使用率',
        type: 'line',
        smooth: true,
        lineStyle: { 
          color: '#3B82F6', 
          width: 3 
        },
        itemStyle: { 
          color: '#3B82F6',
          borderColor: '#3B82F6',
          borderWidth: 2
        },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(59, 130, 246, 0.2)' },
              { offset: 1, color: 'rgba(59, 130, 246, 0.02)' }
            ]
          }
        },
        data: realtimeData.value.memory,
        animationDuration: 1000,
        animationEasing: 'cubicOut'
      },
      {
        name: '磁盘使用率',
        type: 'line',
        smooth: true,
        lineStyle: { 
          color: '#8B5CF6', 
          width: 3 
        },
        itemStyle: { 
          color: '#8B5CF6',
          borderColor: '#8B5CF6',
          borderWidth: 2
        },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(139, 92, 246, 0.2)' },
              { offset: 1, color: 'rgba(139, 92, 246, 0.02)' }
            ]
          }
        },
        data: realtimeData.value.disk,
        animationDuration: 1000,
        animationEasing: 'cubicOut',
        markPoint: {
          data: [{
            coord: [timeLabels.length - 1, realtimeData.value.disk[realtimeData.value.disk.length - 1]],
            itemStyle: {
              color: '#8B5CF6',
              borderColor: '#ffffff',
              borderWidth: 2
            },
            label: {
              show: true,
              position: 'top',
              formatter: (params: any) => {
                return `${realtimeInfo.value.time}\n${realtimeInfo.value.value}`
              },
              backgroundColor: 'rgba(255, 255, 255, 0.9)',
              borderColor: '#8B5CF6',
              borderWidth: 1,
              borderRadius: 4,
              padding: [4, 8],
              fontSize: 11,
              color: '#374151'
            }
          }]
        },

      }
    ]
  }
  chartInstance.setOption(option)
  
  // 启动实时更新
  startRealtimeUpdate()
}

// 生成随机数据
const generateCpuData = (baseValue: number) => {
  return Math.max(15, Math.min(25, baseValue + (Math.random() - 0.5) * 6))
}

const generateMemoryData = (baseValue: number) => {
  return Math.max(35, Math.min(45, baseValue + (Math.random() - 0.5) * 8))
}

const generateDiskData = (baseValue: number) => {
  return Math.max(60, Math.min(68, baseValue + (Math.random() - 0.5) * 6))
}

// 实时更新数据
const updateChartData = () => {
  if (!chartInstance) return
  
  // 移除第一个数据点，添加新的数据点
  realtimeData.value.cpu.shift()
  realtimeData.value.memory.shift()
  realtimeData.value.disk.shift()
  
  // 生成新的随机数据
  const lastCpuValue = realtimeData.value.cpu[realtimeData.value.cpu.length - 1]
  const lastMemoryValue = realtimeData.value.memory[realtimeData.value.memory.length - 1]
  const lastDiskValue = realtimeData.value.disk[realtimeData.value.disk.length - 1]
  
  const newCpuValue = generateCpuData(lastCpuValue)
  const newMemoryValue = generateMemoryData(lastMemoryValue)
  const newDiskValue = generateDiskData(lastDiskValue)
  
  realtimeData.value.cpu.push(newCpuValue)
  realtimeData.value.memory.push(newMemoryValue)
  realtimeData.value.disk.push(newDiskValue)
  
  // 更新实时信息显示（以磁盘数据为主）
  const now = new Date()
  realtimeInfo.value.time = now.toTimeString().slice(0, 8)
  realtimeInfo.value.value = Math.round(newDiskValue * 100) / 100
  
  // 更新时间标签
  const timeLabels = generateTimeLabels()
  
  // 更新图表
  chartInstance.setOption({
    xAxis: {
      data: timeLabels
    },
    series: [
      { data: realtimeData.value.cpu },
      { data: realtimeData.value.memory },
      {
        data: realtimeData.value.disk,
        markPoint: {
          data: [{
            coord: [timeLabels.length - 1, newDiskValue],
            itemStyle: {
              color: '#8B5CF6',
              borderColor: '#ffffff',
              borderWidth: 2
            },
            label: {
              show: true,
              position: 'top',
              formatter: () => {
                return `${realtimeInfo.value.time}\n${realtimeInfo.value.value}%`
              },
              backgroundColor: 'rgba(255, 255, 255, 0.9)',
              borderColor: '#8B5CF6',
              borderWidth: 1,
              borderRadius: 4,
              padding: [4, 8],
              fontSize: 11,
              color: '#374151'
            }
          }]
        }
      }
    ]
  })
}

// 启动实时更新
const startRealtimeUpdate = () => {
  animationTimer = setInterval(() => {
    updateChartData()
  }, 2000) // 每2秒更新一次
}

// 停止实时更新
const stopRealtimeUpdate = () => {
  if (animationTimer) {
    clearInterval(animationTimer)
    animationTimer = null
  }
}

// 初始化告警状态图表
const initAlertStatusChart = () => {
  if (!alertStatusChart.value) return
  
  const chart = echarts.init(alertStatusChart.value)
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    series: [
      {
        name: '告警状态',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: '14',
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: false
        },
        data: [
          { 
            value: 42, 
            name: '异常告警',
            itemStyle: { color: '#6366f1' }
          },
          { 
            value: 58, 
            name: '正常告警',
            itemStyle: { color: '#10b981' }
          }
        ]
      }
    ]
  }
  chart.setOption(option)
}

// 初始化告警级别图表
const initAlertLevelChart = () => {
  if (!alertLevelChart.value) return
  
  const chart = echarts.init(alertLevelChart.value)
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    series: [
      {
        name: '告警级别',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: '14',
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: false
        },
        data: [
          { 
            value: 42, 
            name: 'CPU告警',
            itemStyle: { color: '#ff7875' }
          },
          { 
            value: 42, 
            name: '内存告警',
            itemStyle: { color: '#ffa940' }
          },
          { 
            value: 16, 
            name: '磁盘告警',
            itemStyle: { color: '#52c41a' }
          }
        ]
      }
    ]
  }
  chart.setOption(option)
}

// 更新告警状态图表
const updateAlertStatusChart = () => {
  initAlertStatusChart()
}

// 更新告警级别图表
const updateAlertLevelChart = () => {
  initAlertLevelChart()
}

onMounted(async () => {
  await nextTick()
  initSystemChart()
  initAlertStatusChart()
  initAlertLevelChart()
  loadDeviceData()
})

// 组件卸载时清理定时器
onUnmounted(() => {
  stopRealtimeUpdate()
  if (chartInstance) {
    chartInstance.dispose()
    chartInstance = null
  }
})
</script>

<style scoped lang="scss">
.dashboard {
  padding: 24px;
  background: #f8fafc;
  min-height: 100vh;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 16px;
  margin-bottom: 24px;

  .stat-card {
    background: white;
    border-radius: 8px;
    padding: 20px;
    display: flex;
    align-items: center;
    gap: 12px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    position: relative;
    overflow: hidden;

    &::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 4px;
    }

    &.stat-card-1::before {
      background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }

    &.stat-card-2::before {
      background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
    }

    &.stat-card-3::before {
      background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
    }

    &.stat-card-4::before {
      background: linear-gradient(90deg, #43e97b 0%, #38f9d7 100%);
    }

    &.stat-card-5::before {
      background: linear-gradient(90deg, #fa709a 0%, #fee140 100%);
    }

    &.stat-card-6::before {
      background: linear-gradient(90deg, #a8edea 0%, #fed6e3 100%);
    }

    .stat-icon {
      width: 40px;
      height: 40px;
      display: flex;
      align-items: center;
      justify-content: center;

      img {
        width: 32px;
        height: 32px;
      }
    }

    .stat-info {
      flex: 1;

      .stat-number {
        font-size: 18px;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 4px;
      }

      .stat-label {
        font-size: 12px;
        color: #6b7280;
      }
    }
  }
}

.charts-section {
  margin-bottom: 24px;

  .system-chart {
    margin-bottom: 16px;
    position: relative;
    
    &::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 3px;
      background: linear-gradient(90deg, #10B981, #3B82F6, #06B6D4);
      border-radius: 8px 8px 0 0;
      animation: monitoring-pulse 3s ease-in-out infinite;
    }
    
    .chart-title {
      position: relative;
      
      &::after {
        content: '●';
        color: #10B981;
        margin-left: 8px;
        animation: blink 2s ease-in-out infinite;
      }
    }
  }

  .alert-section {
    display: flex;
    gap: 16px;

    .alert-card {
      flex: 1;
      background: white;
      border-radius: 8px;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);

      .alert-header {
        padding: 16px 20px;
        border-bottom: 1px solid #e5e7eb;
        display: flex;
        justify-content: space-between;
        align-items: center;

        .alert-title {
          font-size: 16px;
          font-weight: 600;
          color: #1f2937;
          margin: 0;
          display: flex;
          align-items: center;
          gap: 8px;

          .alert-icon {
            font-size: 14px;
          }
          
          .alert-icon-img {
            width: 16px;
            height: 16px;
            object-fit: contain;
          }
        }
      }

      .alert-content {
        padding: 20px;

        .alert-charts {
          display: flex;
          gap: 16px;
          margin-bottom: 16px;

          .alert-chart-item {
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;

            .chart-selector {
              margin-bottom: 12px;
              
              select {
                padding: 4px 8px;
                border: 1px solid #d1d5db;
                border-radius: 4px;
                font-size: 12px;
                color: #374151;
                background: white;
                cursor: pointer;
                
                &:focus {
                  outline: none;
                  border-color: #3b82f6;
                }
              }
            }

            .alert-pie-chart {
              width: 100%;
              height: 160px;
              margin-bottom: 16px;
            }

            .alert-chart-label {
              font-size: 12px;
              color: #6b7280;
            }
          }
        }

                 .alert-legends {
           display: flex;
           flex-direction: column;
           gap: 8px;
           margin-top: 16px;

           .legend-row {
             display: flex;
             justify-content: space-between;
             align-items: center;
             
             .legend-item {
               display: flex;
               align-items: center;
               gap: 6px;
               font-size: 12px;
               color: #6b7280;
               
               .legend-dot {
                 width: 8px;
                 height: 8px;
                 border-radius: 50%;
               }
             }
             
             .legend-percentage {
               color: #6b7280;
               font-size: 12px;
               font-weight: 500;
             }
           }
         }
       }
     }

    .device-alert-card {
      flex: 1;
      background: white;
      border-radius: 8px;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);

      .device-alert-header {
        padding: 16px 20px;
        border-bottom: 1px solid #e5e7eb;
        display: flex;
        justify-content: space-between;
        align-items: center;

        .device-alert-title {
          font-size: 16px;
          font-weight: 600;
          color: #1f2937;
          margin: 0;
          display: flex;
          align-items: center;
          gap: 8px;

          .device-alert-icon {
            font-size: 14px;
          }
          
          .device-alert-icon-img {
            width: 16px;
            height: 16px;
            object-fit: contain;
          }
        }
      }

             .device-alert-content {
         padding: 20px;

         .device-alert-list {
           display: flex;
           flex-direction: column;
           gap: 12px;

           .device-alert-item {
             background: #f8fafc;
             border-radius: 8px;
             padding: 16px;
             border-left: 4px solid #3b82f6;
             transition: all 0.3s ease;
             
             &:hover {
               background: #f1f5f9;
               transform: translateX(2px);
             }
             
                           .alert-type-header {
                display: flex;
                gap: 8px;
                margin-bottom: 12px;
                
                .alert-type-badge {
                  background: #3b82f6;
                  color: white;
                  padding: 4px 8px;
                  border-radius: 4px;
                  font-size: 10px;
                  font-weight: 500;
                }
                
                .alert-category-badge {
                  background: #6366f1;
                  color: white;
                  padding: 4px 8px;
                  border-radius: 4px;
                  font-size: 10px;
                  font-weight: 500;
                }
                
                .alert-phase-badge {
                  padding: 4px 8px;
                  border-radius: 4px;
                  font-size: 10px;
                  font-weight: 500;
                  color: white;
                  
                  &.alert-critical {
                    background: #ef4444;
                    animation: pulse 2s infinite;
                  }
                  
                  &.alert-warning {
                    background: #f59e0b;
                  }
                  
                  &.alert-normal {
                    background: #10b981;
                  }
                }
              }

                           .alert-details {
                display: flex;
                flex-direction: column;
                gap: 6px;
                
                .alert-detail-line {
                  font-size: 12px;
                  color: #374151;
                  line-height: 1.5;
                  padding: 2px 0;
                  
                  &:first-child {
                    font-weight: 600;
                    color: #1f2937;
                    font-size: 13px;
                  }
                  
                  &:nth-child(2) {
                    color: #6b7280;
                    font-family: 'Courier New', monospace;
                  }
                  
                  &:last-child {
                    color: #059669;
                    font-style: italic;
                  }
                }
              }
           }
         }
      }
    }
     }
 }

.chart-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);

  .chart-header {
    padding: 16px 20px;
    border-bottom: 1px solid #e5e7eb;

    .chart-title {
      font-size: 16px;
      font-weight: 600;
      color: #1f2937;
      margin: 0;
      display: flex;
      align-items: center;
      gap: 8px;

      .chart-icon {
        font-size: 14px;
      }
      
      .chart-icon-img {
        width: 16px;
        height: 16px;
        object-fit: contain;
      }
    }
  }

  .chart-content {
    padding: 20px;
  }

  .chart-legend {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;

    .legend-items {
      display: flex;
      gap: 24px;
      
      .legend-item {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 12px;
        color: #6b7280;

        .legend-dot {
          width: 8px;
          height: 8px;
          border-radius: 50%;

          &.cpu { background: #10B981; }
          &.memory { background: #3B82F6; }
          &.disk { background: #8B5CF6; }
        }
      }
    }
    
    .legend-realtime-value {
      display: flex;
      flex-direction: column;
      align-items: flex-end;
      gap: 2px;
      
      .realtime-time {
        font-size: 11px;
        color: #6b7280;
        font-weight: 500;
      }
      
      .realtime-value {
        font-size: 16px;
        font-weight: 700;
        color: #8B5CF6;
      }
    }
  }

  .chart-container {
    height: 200px;
  }

  .pie-chart {
    height: 180px;
    margin-bottom: 16px;
  }
}
 
 .device-table-section {
  .table-card {
    background: white;
    border-radius: 8px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);

    .table-header {
      padding: 16px 20px;
      border-bottom: 1px solid #e5e7eb;
      display: flex;
      justify-content: space-between;
      align-items: center;

      .table-title {
        font-size: 16px;
        font-weight: 600;
        color: #1f2937;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 8px;

        .table-icon {
          font-size: 14px;
        }
        
        .table-icon-img {
          width: 16px;
          height: 16px;
          object-fit: contain;
        }
      }

      .table-actions {
        display: flex;
        gap: 8px;

        .action-btn {
          display: flex;
          align-items: center;
          gap: 4px;
          padding: 6px 12px;
          border-radius: 4px;
          border: none;
          font-size: 12px;
          cursor: pointer;
          transition: all 0.2s;

          .btn-icon {
            font-size: 12px;
          }
          
          .btn-icon-img {
            width: 12px;
            height: 12px;
            object-fit: contain;
            filter: brightness(0) invert(1);
          }

          &.create-btn {
            background: #10b981;
            color: white;

            &:hover {
              background: #059669;
            }
          }

          &.download-btn {
            background: #3b82f6;
            color: white;

            &:hover {
              background: #2563eb;
            }
          }

          &.progress-btn {
            background: #f59e0b;
            color: white;

            &:hover {
              background: #d97706;
            }
          }

          &.import-btn {
            background: #8b5cf6;
            color: white;

            &:hover {
              background: #7c3aed;
            }
          }
        }
      }
    }

    .table-content {
      overflow-x: auto;

      .loading-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 60px 20px;

        .loading-text {
          color: #6b7280;
          font-size: 14px;
        }
      }

      .device-table {
        width: 100%;
        border-collapse: collapse;

        th {
          background: #f9fafb;
          padding: 12px 16px;
          text-align: left;
          font-size: 12px;
          font-weight: 600;
          color: #374151;
          border-bottom: 1px solid #e5e7eb;
          white-space: nowrap;
        }

        td {
          padding: 12px 16px;
          font-size: 12px;
          color: #6b7280;
          border-bottom: 1px solid #f3f4f6;
          white-space: nowrap;
        }

        .status-tag {
          padding: 2px 8px;
          border-radius: 12px;
          font-size: 11px;
          font-weight: 500;

          &.status-online {
            background: #ecfdf5;
            color: #059669;
          }

          &.status-offline {
            background: #fef2f2;
            color: #dc2626;
          }

          &.status-maintenance {
            background: #fef3c7;
            color: #d97706;
          }

          &.status-default {
            background: #f3f4f6;
            color: #6b7280;
          }
        }
      }
    }
  }
}

// 响应式设计
@media (max-width: 1400px) {
  .stats-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 1024px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .alert-section {
    flex-direction: column;
  }
}

@media (max-width: 768px) {
  .dashboard {
    padding: 16px;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .table-header {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }
  
  .alert-section {
    flex-direction: column;
  }
}

// 实时监控动画
@keyframes monitoring-pulse {
  0%, 100% {
    opacity: 0.6;
    transform: scaleX(1);
  }
  50% {
    opacity: 1;
    transform: scaleX(1.02);
  }
}

@keyframes blink {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.3;
  }
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.7;
    transform: scale(1.1);
  }
}

@keyframes criticalPulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
    box-shadow: 0 0 0 3px rgba(255, 255, 255, 1), 0 0 0 0 rgba(239, 68, 68, 0.7);
  }
  50% {
    opacity: 0.9;
    transform: scale(1.05);
    box-shadow: 0 0 0 3px rgba(255, 255, 255, 1), 0 0 0 8px rgba(239, 68, 68, 0);
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
  }
  33% {
    transform: translateY(-10px) rotate(1deg);
  }
  66% {
    transform: translateY(5px) rotate(-1deg);
  }
}
</style> 