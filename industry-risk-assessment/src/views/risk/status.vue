<template>
  <div class="risk-status-container">
    <!-- 顶部筛选区 -->
    <el-card class="filter-container">
      <el-form :model="filterForm" inline>
        <el-form-item label="产业链">
          <el-select 
            v-model="filterForm.industryChainId" 
            placeholder="请选择产业链" 
            style="width: 240px"
            @change="handleIndustryChainChange"
          >
            <el-option
              v-for="item in industryChainOptions"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="数据期间">
          <el-select 
            v-model="filterForm.dataPeriod" 
            placeholder="请选择数据期间" 
            style="width: 160px"
            :disabled="!filterForm.industryChainId"
          >
            <el-option
              v-for="period in periodOptions"
              :key="period"
              :label="period"
              :value="period"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="完整性评估模型">
          <el-select
            v-model="filterForm.integrityModel"
            placeholder="请选择完整性评估模型"
            style="width: 360px"
          >
            <el-option
              v-for="item in integrityModelOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="风险评估模型">
          <el-select
            v-model="filterForm.riskModel"
            placeholder="请选择风险评估模型"
            style="width: 360px"
          >
            <el-option
              v-for="item in riskModelOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="风险预警模型">
          <el-select
            v-model="filterForm.warningModel"
            placeholder="请选择风险预警模型"
            style="width: 360px"
          >
            <el-option
              v-for="item in warningModelOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item class="action-item">
          <el-button 
            type="primary" 
            @click="handleFilter"
            :disabled="!filterForm.industryChainId || !filterForm.dataPeriod || !filterForm.integrityModel || !filterForm.riskModel || !filterForm.warningModel"
          >
            评估
          </el-button>
          <el-button @click="resetFilter">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 下部内容区 -->
    <div class="content-container">
      <!-- 左侧图表 -->
      <el-card class="chart-container" v-loading="loading">
        <template #header>
          <div class="card-header text-center">
            <span>产业链关系图谱</span>
          </div>
        </template>
        <div class="chart-controls">
          <div class="legend-info">
            <div class="legend-title">节点类型:</div>
            <div class="legend-items">
              <div class="legend-item">
                <span class="legend-icon company-icon"></span>
                <span class="legend-text">公司</span>
              </div>
              <div class="legend-item">
                <span class="legend-icon product-icon"></span>
                <span class="legend-text">产品</span>
              </div>
              <div class="legend-item">
                <span class="legend-icon risk-icon"></span>
                <span class="legend-text">风险公司</span>
              </div>
            </div>
          </div>
          <el-switch 
            v-model="showLabels" 
            active-text="显示标签" 
            inactive-text="隐藏标签"
            @change="toggleLabels"
            size="small"
          />
        </div>
        <div class="chart">
          <div ref="chartRef" class="graph-canvas"></div>
          <div v-if="graphEmpty && !graphRendering" class="empty-state">
            <div class="empty-icon">⌛</div>
            <div class="empty-title">暂无可展示的关系数据</div>
            <div class="empty-desc">请确认已上传产业链数据或更换其他时间/产业链重试</div>
          </div>
          <div v-if="graphRendering" class="graph-loading-mask">
            <div class="loading-panel">
              <div class="loading-spinner"></div>
              <div class="loading-title">正在渲染关系图谱...</div>
              <div class="loading-tip">节点较多时需要几秒钟，请稍候</div>
            </div>
          </div>
        </div>
      </el-card>

      <!-- 右侧统计信息 -->
      <div class="stats-container">
        <!-- 第一张卡片：产业链信息 -->
        <el-card class="stat-card" v-loading="loading">
          <template #header>
            <div class="card-header">
              <span>产业链信息</span>
            </div>
          </template>
          <div class="stat-grid">
            <div class="stat-item">
              <div class="stat-value">{{ getProductCount() }}</div>
              <div class="stat-label">产品节点数</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ getCompanyCount() }}</div>
              <div class="stat-label">公司节点数</div>
            </div>
          </div>
        </el-card>
        
        <!-- 第二张卡片：风险概览 -->
        <el-card class="stat-card" style="margin-top: 20px;" v-loading="loading">
          <template #header>
            <div class="card-header">
              <span>风险概览</span>
            </div>
          </template>
          <div class="risk-overview">
            <div ref="riskChartRef" class="risk-chart"></div>
            <div class="risk-summary">
              <div class="summary-title">当前产业链风险情况</div>
              <div class="summary-value" :class="`level-${riskLevelClass}`">
                {{ riskLevelText }}
              </div>
              <div class="forecast-title">T+1期当前产业链风险预测</div>
              <div class="forecast-value" :class="`level-${nextRiskLevelClass}`">
                {{ nextRiskLevelText }}
              </div>
            </div>
          </div>
        </el-card>
        <el-card class="stat-card integrity-card" style="margin-top: 20px;" v-loading="loading">
          <template #header>
            <div class="card-header">
              <span>产业链完整性</span>
            </div>
          </template>
          <div class="integrity-metrics">
            <div class="metric-item">
              <div class="metric-label">产业链抵抗力得分</div>
              <div class="metric-value">{{ riskOverview.resilienceScore.toFixed(2) }}</div>
            </div>
            <div class="metric-item">
              <div class="metric-label">产业链恢复力得分</div>
              <div class="metric-value">{{ riskOverview.recoveryScore.toFixed(2) }}</div>
            </div>
            <div class="metric-item highlight">
              <div class="metric-label">产业链完整性得分</div>
              <div class="metric-value">{{ riskOverview.integrityScore.toFixed(2) }}</div>
            </div>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed, nextTick } from 'vue'
import * as echarts from 'echarts'
import { ElMessage } from 'element-plus'

import { getIndustryChainList } from '@/api/industryChain'
import { getDataPeriods } from '@/api/dataset'
import type { IndustryChain } from '@/types/dataset'
import { getIndustryChainGraph, getRiskOverview, type RiskOverview } from '@/api/riskStatus'
import type { GraphData, GraphNode } from '@/types/graph'

type GraphLayoutPoint = {
  x: number
  y: number
}

// 筛选表单数据
const filterForm = ref({
  industryChainId: null as number | null,
  dataPeriod: '',
  integrityModel: '',
  riskModel: '',
  warningModel: ''
})

// 产业链选项
const industryChainOptions = ref<IndustryChain[]>([])
// 数据期间选项
const periodOptions = ref<string[]>([])
const integrityModelOptions = [
  {
    value: 'link-prediction-integrity',
    label: '基于链接预测的产业链完整性评估模型'
  },
  {
    value: 'graph-attention-message-passing-integrity',
    label: '基于图注意力机制和消息传递网络的产业链完整性评估模型'
  },
  {
    value: 'heterogeneous-attention-embedding-integrity',
    label: '融合注意力机制的多边异质网络结构嵌入模型'
  }
]
const riskModelOptions = [
  {
    value: 'han-risk',
    label: '基于邻居采样和图注意力机制的风险评估模型'
  },
  {
    value: 'hier-transfer-gnn-risk',
    label: '基于分层知识可转移图神经网络的风险评估模型'
  },
  {
    value: 'topology-attention-pooling-risk',
    label: '融合图拓扑特征与注意力池化的产业链风险评估模型'
  },
  {
    value: 'graph-fusion-attribute-completion-risk',
    label: '结合图融合和属性补全的产业链风险评估模型'
  }
]
const warningModelOptions = [
  {
    value: 'pca-cnn-warning',
    label: '基于PCA-CNN的产业链风险预警模型'
  },
  {
    value: 'hier-gnn-lstm-warning',
    label: '结合层次图神经网络和LSTM的产业链风险预警模型'
  }
]

// 加载状态
const loading = ref(false)

// 显示控制
const showLabels = ref(false)



// 图表数据
const graphData = ref<GraphData>({
  nodes: [],
  links: [],
  categories: [
    { name: '产品' },
    { name: '公司' }
  ]
})
const graphDataCache = new Map<number, GraphData>()
const graphLayoutCache = new Map<number, Record<string, GraphLayoutPoint>>()
const adjacencyMap = ref<Record<string, string[]>>({})
const nodeLookup = ref<Record<string, GraphNode>>({})
const nodeAliasMap = ref<Record<string, string>>({})
const chartRef = ref<HTMLElement>()
let chart: echarts.ECharts | null = null
const graphRendering = ref(false)
const graphEmpty = ref(false)
let graphEventsBound = false
let graphFinishedBound = false

const ensureChartInstance = () => {
  if (!chart && chartRef.value) {
    chart = echarts.init(chartRef.value)
  }
}

// 风险概览数据
const riskOverview = ref<RiskOverview>({
  riskCompanyCount: 0,
  totalCompanyCount: 0,
  riskCompanies: [],
  normalCompanies: [],
  riskLevel: '待评估',
  resilienceScore: 0,
  recoveryScore: 0,
  integrityScore: 0,
  nextPeriodLabel: 'T+1期',
  nextPeriodRiskCompanyCount: 0,
  nextPeriodRiskLevel: '待评估'
})

const riskLevelText = computed(() => riskOverview.value.riskLevel || '待评估')

const mapRiskLevelClass = (level?: string) => {
  switch (level) {
    case '高风险':
      return 'high'
    case '中风险':
      return 'medium'
    case '低风险':
      return 'low'
    default:
      return 'pending'
  }
}

const riskLevelClass = computed(() => mapRiskLevelClass(riskOverview.value.riskLevel))
const nextRiskLevelText = computed(() => riskOverview.value.nextPeriodRiskLevel || '待评估')
const nextRiskLevelClass = computed(() => mapRiskLevelClass(riskOverview.value.nextPeriodRiskLevel))

const riskCompanySet = computed(() => {
  const ids = riskOverview.value.riskCompanies || []
  return new Set(ids.map(id => `C${id}`))
})

const isRiskCompanyNode = (node: GraphNode) => {
  if (node.category !== '公司') return false
  return riskCompanySet.value.has(node.id || '')
}

const resolveCanonicalKey = (key?: string) => {
  if (!key) return ''
  return nodeAliasMap.value[key] || key
}

const getConnectedNodes = (primaryKey?: string, fallbackKey?: string) => {
  const connected = new Set<string>()
  const addConnections = (key?: string) => {
    if (!key) return
    const canonical = resolveCanonicalKey(key)
    const neighbors = adjacencyMap.value[canonical]
    if (neighbors) {
      neighbors.forEach(n => connected.add(n))
    }
  }
  addConnections(primaryKey)
  addConnections(fallbackKey)
  return Array.from(connected)
    .map(key => nodeLookup.value[key])
    .filter((node): node is GraphNode => Boolean(node))
}

const buildGraphCaches = () => {
  const adjacency: Record<string, Set<string>> = {}
  const lookup: Record<string, GraphNode> = {}
  const alias: Record<string, string> = {}

  graphData.value.nodes.forEach(node => {
    const canonicalKey = node.id || node.name
    if (!canonicalKey) return
    lookup[canonicalKey] = node
    alias[canonicalKey] = canonicalKey
    if (node.id) {
      alias[node.id] = canonicalKey
    }
    if (node.name) {
      alias[node.name] = canonicalKey
    }
    if (!adjacency[canonicalKey]) {
      adjacency[canonicalKey] = new Set()
    }
  })

  graphData.value.links.forEach(link => {
    const sourceKey = alias[link.source] || link.source
    const targetKey = alias[link.target] || link.target
    if (!sourceKey || !targetKey) return

    if (!adjacency[sourceKey]) {
      adjacency[sourceKey] = new Set()
    }
    if (!adjacency[targetKey]) {
      adjacency[targetKey] = new Set()
    }

    adjacency[sourceKey].add(targetKey)
    adjacency[targetKey].add(sourceKey)
  })

  adjacencyMap.value = Object.fromEntries(
    Object.entries(adjacency).map(([key, set]) => [key, Array.from(set)])
  )
  nodeLookup.value = lookup
  nodeAliasMap.value = alias
}

const createGraphDataset = () => {
  const currentIndustryChainId = filterForm.value.industryChainId
  const layoutPositions = currentIndustryChainId ? graphLayoutCache.get(currentIndustryChainId) : undefined
  const nodes = graphData.value.nodes.map(node => {
    const canonicalId = node.id || node.name
    const isCompany = node.category === '公司'
    const riskFlag = isRiskCompanyNode(node)
    const color = riskFlag ? '#F56C6C' : (isCompany ? '#409EFF' : '#67C23A')
    const baseSize = node.symbolSize || (isCompany ? 16 : 10)
    const size = riskFlag ? baseSize * 1.3 : baseSize
    const position = canonicalId ? layoutPositions?.[canonicalId] : undefined
    return {
      id: canonicalId,
      name: node.name,
      category: node.category,
      symbol: isCompany ? 'circle' : 'rect',
      symbolSize: size,
      value: node.value,
      itemStyle: {
        color
      },
      label: {
        show: showLabels.value,
        color: '#1f2d3d',
        formatter: node.name,
        fontSize: 11
      },
      x: position?.x,
      y: position?.y,
      fixed: Boolean(position),
      data: {
        ...node,
        riskFlag
      } as any
    }
  })

  const edges = graphData.value.links
    .map(link => {
      const sourceKey = resolveCanonicalKey(link.source)
      const targetKey = resolveCanonicalKey(link.target)
      if (!sourceKey || !targetKey) return null
      return {
        source: sourceKey,
        target: targetKey,
        lineStyle: {
          opacity: 0.2
        },
        data: link as any
      }
    })
    .filter((edge): edge is NonNullable<typeof edge> => Boolean(edge))

  graphEmpty.value = nodes.length === 0
  return { nodes, edges }
}

// 获取产业链列表
const fetchIndustryChains = async () => {
  try {
    const { data } = await getIndustryChainList()
    industryChainOptions.value = data
  } catch (error) {
    console.error('获取产业链列表失败:', error)
    ElMessage.error('获取产业链列表失败')
  }
}

// 获取数据期间列表
const fetchDataPeriods = async (industryChainId: number) => {
  try {
    const { data } = await getDataPeriods(industryChainId)
    periodOptions.value = data
  } catch (error) {
    console.error('获取数据期间列表失败:', error)
    ElMessage.error('获取数据期间列表失败')
  }
}

// 处理产业链选择变化
const handleIndustryChainChange = async (value: number) => {
  filterForm.value.dataPeriod = ''
  periodOptions.value = []
  
  if (value) {
    await fetchDataPeriods(value)
  }
}

// 获取图谱数据
const fetchGraphData = async (forceRefresh = false, renderAfterLoad = true) => {
  const industryChainId = filterForm.value.industryChainId
  if (!industryChainId) {
    ElMessage.warning('请选择产业链')
    return
  }

  const cachedGraphData = !forceRefresh ? graphDataCache.get(industryChainId) : undefined
  if (cachedGraphData) {
    graphData.value = cachedGraphData
    buildGraphCaches()
    if (renderAfterLoad) {
      await renderGraph()
    }
    return
  }

  loading.value = true
  try {
    const res = await getIndustryChainGraph(industryChainId)
    graphData.value = res.data
    graphDataCache.set(industryChainId, res.data)
    graphLayoutCache.delete(industryChainId)
    buildGraphCaches()
    if (renderAfterLoad) {
      await renderGraph()
    }
  } catch (error) {
    console.error('获取图谱数据失败', error)
    ElMessage.error('获取图谱数据失败')
  } finally {
    loading.value = false
  }
}

// 获取风险概览数据
const fetchRiskOverview = async (renderGraphAfterLoad = true) => {
  if (!filterForm.value.industryChainId || !filterForm.value.dataPeriod) {
    return
  }
  
  loading.value = true
  try {
    const res = await getRiskOverview(
      filterForm.value.industryChainId, 
      filterForm.value.dataPeriod
    )
    riskOverview.value = res.data
    initRiskChart()
    if (chart && renderGraphAfterLoad) {
      await renderGraph()
    }
  } catch (error: any) {
    console.error('获取风险概览数据失败', error)
    // 提供更具体的错误信息
    if (error.response?.data?.message) {
      ElMessage.error(`获取风险概览数据失败: ${error.response.data.message}`)
    } else {
      ElMessage.error('获取风险概览数据失败，请确保已上传特征标签数据')
    }
  } finally {
    loading.value = false
  }
}

// 处理筛选
const handleFilter = async () => {
  if (!filterForm.value.industryChainId || !filterForm.value.dataPeriod || !filterForm.value.integrityModel || !filterForm.value.riskModel || !filterForm.value.warningModel) {
    ElMessage.warning('请完整选择产业链、数据期间、完整性评估模型、风险评估模型和风险预警模型')
    return
  }
  
  // 图谱与期间无关，风险状态与期间有关；统一在数据就绪后只渲染一次图谱
  await fetchGraphData(false, false)
  await fetchRiskOverview(false)
  await renderGraph()
}

// 重置筛选
const resetFilter = () => {
  filterForm.value = {
    industryChainId: null,
    dataPeriod: '',
    integrityModel: '',
    riskModel: '',
    warningModel: ''
  }
  periodOptions.value = []
  graphData.value = {
    nodes: [],
    links: [],
    categories: [
      { name: '产品' },
      { name: '公司' }
    ]
  }
  adjacencyMap.value = {}
  nodeLookup.value = {}
  nodeAliasMap.value = {}
  graphEmpty.value = true
  renderGraph()
}

// 图表相关
const riskChartRef = ref<HTMLElement>()
const riskChartInstance = ref<echarts.ECharts | null>(null)

// 初始化风险饼图
const initRiskChart = () => {
  if (!riskChartRef.value) return
  riskChartInstance.value?.dispose()
  const riskChart = echarts.init(riskChartRef.value)
  
  // 计算风险比例（如需在图例或其他处显示可再次启用）
  
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      show: false
    },
    series: [
          {
            name: '企业风险状态',
            type: 'pie',
            radius: '75%',
            center: ['50%', '40%'],
            data: [
              { 
                value: riskOverview.value.riskCompanyCount, 
                name: '风险公司',
                itemStyle: { color: '#F56C6C' }
              },
              { 
                value: riskOverview.value.totalCompanyCount - riskOverview.value.riskCompanyCount, 
                name: '正常企业',
                itemStyle: { color: '#67C23A' }
              }
            ],
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            },
            label: {
              show: false,
              formatter: '{b}: {c} ({d}%)'
            },
            itemStyle: {
              borderRadius: 4
            }
          }
    ]
  }
  
  riskChart.setOption(option)
  
  // 保存图表实例以便后续更新
  riskChartInstance.value = riskChart
}

const resolveNodeByRef = (ref?: string) => {
  if (!ref) return undefined
  return nodeLookup.value[resolveCanonicalKey(ref)]
}

const captureGraphLayout = () => {
  const industryChainId = filterForm.value.industryChainId
  if (!chart || !industryChainId) return

  const option = chart.getOption() as any
  const seriesData = option?.series?.[0]?.data
  if (!Array.isArray(seriesData) || !seriesData.length) return

  const positions: Record<string, GraphLayoutPoint> = {}
  seriesData.forEach((node: any) => {
    const key = node?.id || node?.name
    if (!key) return
    const x = Number(node?.x)
    const y = Number(node?.y)
    if (Number.isFinite(x) && Number.isFinite(y)) {
      positions[key] = { x, y }
    }
  })

  if (Object.keys(positions).length > 0) {
    graphLayoutCache.set(industryChainId, positions)
  }
}

const buildGraphOption = (): echarts.EChartsOption => {
  const { nodes, edges } = createGraphDataset()
  const currentIndustryChainId = filterForm.value.industryChainId
  const currentLayoutCache = currentIndustryChainId ? graphLayoutCache.get(currentIndustryChainId) : undefined
  const useStoredLayout = Boolean(currentLayoutCache && Object.keys(currentLayoutCache).length > 0)
  graphEmpty.value = nodes.length === 0

  return {
    animation: false,
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(0,0,0,0.85)',
      borderWidth: 0,
      textStyle: {
        color: '#fff'
      },
      formatter: (params: any) => {
        if (params.dataType === 'node') {
          const nodeData = params.data
          const nodeId = nodeData.id || nodeData.name
          const connections = getConnectedNodes(nodeId, nodeData.name) || []
          const connectionInfo = connections.length > 0
            ? `<div style="margin-top: 10px; border-top: 1px solid rgba(255,255,255,0.2); padding-top: 6px;">
                <div style="font-size: 12px; color: #ccc; margin-bottom: 4px;">相关连接 (${connections.length}个)</div>
                ${connections.slice(0, 4).map((conn: GraphNode) => `<div style="font-size: 12px; color: #fff;">• ${conn.category}: ${conn.name}</div>`).join('')}
                ${connections.length > 4 ? `<div style="font-size: 12px; color: #999;">... 还有${connections.length - 4}个节点</div>` : ''}
               </div>`
            : ''
          return `
            <div style="max-width: 300px;">
              <div style="font-weight: 600; margin-bottom: 4px;">${nodeData.category}</div>
              <div style="font-size: 16px; font-weight: bold;">${nodeData.name}</div>
              ${nodeData.data?.riskLevel ? `<div style="margin-top: 4px; color: ${getRiskColor(nodeData.data.riskLevel)};">风险等级: ${nodeData.data.riskLevel}</div>` : ''}
              ${connectionInfo}
            </div>
          `
        }

        if (params.dataType === 'edge') {
          const sourceNode = resolveNodeByRef(params.data.source)
          const targetNode = resolveNodeByRef(params.data.target)
          return `
            <div style="max-width: 260px;">
              <div style="font-weight: 600; margin-bottom: 6px;">连接关系</div>
              <div style="font-size: 12px; color: #ccc;">${sourceNode?.category || '节点'} → ${targetNode?.category || '节点'}</div>
              <div style="font-size: 14px; color: #fff; margin-top: 4px;">${sourceNode?.name || params.data.source} → ${targetNode?.name || params.data.target}</div>
            </div>
          `
        }
        return ''
      }
    },
    series: [
      {
        type: 'graph',
        layout: useStoredLayout ? 'none' : 'force',
        data: nodes,
        links: edges,
        categories: [
          { name: '公司' },
          { name: '产品' }
        ],
        roam: true,
        edgeSymbol: ['none', 'arrow'],
        edgeSymbolSize: [0, 8],
        focusNodeAdjacency: true,
        force: useStoredLayout ? undefined : {
          repulsion: 260,
          gravity: 0.02,
          edgeLength: [80, 160],
          friction: 0.6,
          layoutAnimation: false
        },
        lineStyle: {
          color: '#bfc5d1',
          width: 1,
          opacity: 0.35
        },
        emphasis: {
          focus: 'adjacency',
          label: {
            show: true
          },
          lineStyle: {
            width: 3,
            color: '#111',
            opacity: 0.9
          }
        },
        blur: {
          label: {
            show: false
          },
          lineStyle: {
            width: 0.4,
            opacity: 0.05
          }
        }
      }
    ]
  }
}

const renderGraph = async () => {
  graphRendering.value = true
  await nextTick()
  ensureChartInstance()
  if (!chart) {
    graphRendering.value = false
    return
  }

  try {
    const option = buildGraphOption()
    chart.setOption(option, true)
    chart.resize()

    if (!graphEventsBound) {
      chart.on('mouseover', params => {
        if (params.seriesType === 'graph') {
          chart?.dispatchAction({
            type: 'focusNodeAdjacency',
            seriesIndex: params.seriesIndex ?? 0,
            dataIndex: params.dataIndex
          })
        }
      })
      chart.on('mouseout', params => {
        if (params.seriesType === 'graph') {
          chart?.dispatchAction({
            type: 'unfocusNodeAdjacency'
          })
        }
      })
      graphEventsBound = true
    }

    if (!graphFinishedBound) {
      chart.on('finished', () => {
        captureGraphLayout()
      })
      graphFinishedBound = true
    }
  } catch (error) {
    console.error('渲染图谱失败', error)
    graphEmpty.value = true
  } finally {
    graphRendering.value = false
  }
}

const applyLabelVisibility = () => {
  if (!chart) return
  renderGraph()
}

// 获取风险等级颜色
const getRiskColor = (riskLevel: string) => {
  switch (riskLevel) {
    case 'HIGH': return '#F56C6C'
    case 'MEDIUM': return '#E6A23C' 
    case 'LOW': return '#67C23A'
    default: return '#909399'
  }
}



// 切换标签显示
const toggleLabels = () => {
  applyLabelVisibility()
}

// 监听窗口大小变化
const handleResize = () => {
  chart?.resize()
  riskChartInstance.value?.resize()
}

// 获取产品节点数量
const getProductCount = () => {
  return graphData.value.nodes.filter(node => node.category === '产品').length || 0
}

// 获取公司节点数量
const getCompanyCount = () => {
  return graphData.value.nodes.filter(node => node.category === '公司').length || 0
}

// 组件挂载时初始化
onMounted(async () => {
  await fetchIndustryChains()
  // 不再在这里初始化风险图表，而是在获取数据后初始化
  window.addEventListener('resize', handleResize)
})

// 组件卸载时清理
onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  chart?.dispose()
  chart = null
  graphEventsBound = false
  graphFinishedBound = false
  riskChartInstance.value?.dispose()
})
</script>

<style scoped lang="scss">
.risk-status-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 20px;
  
  .filter-container {
    margin-bottom: 20px;
    padding-top: 16px;

    :deep(.el-form) {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: center;
      gap: 8px 12px;
    }

    :deep(.el-form-item) {
      margin-bottom: 0;
    }

    :deep(.action-item) {
      margin-left: 8px;
    }
  }
  
  .content-container {
    flex: 1;
    display: flex;
    gap: 20px;
    min-height: 0; // 修复 flex 布局下的滚动问题
    
    .chart-container {
      flex: 1;
      
      .chart-controls {
        margin-bottom: 12px;
        padding: 12px 16px;
        background: #f8f9fa;
        border-radius: 8px;
        border: 1px solid #e9ecef;
        display: flex;
        justify-content: space-between;
        align-items: center;
        
        .legend-info {
          display: flex;
          align-items: center;
          gap: 12px;
          
          .legend-title {
            font-size: 14px;
            font-weight: 600;
            color: #333;
          }
          
          .legend-items {
            display: flex;
            gap: 16px;
            
            .legend-item {
              display: flex;
              align-items: center;
              gap: 6px;
              
                .legend-icon {
                  width: 16px;
                  height: 16px;
                  border-radius: 50%;
                  border: 2px solid #fff;
                  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                  
                  &.company-icon {
                    background: #409EFF;
                    border-radius: 50%;
                  }
                  
                  &.product-icon {
                    background: #67C23A;
                    border-radius: 2px;
                  }

                  &.risk-icon {
                    background: #F56C6C;
                    border-radius: 50%;
                  }
                }
              
              .legend-text {
                font-size: 12px;
                font-weight: 500;
                color: #666;
              }
            }
          }
        }
        
        .el-switch {
          .el-switch__label {
            font-size: 12px;
            color: #666;
          }
        }
      }
      

      
      .chart {
        height: 620px;
        border: 2px solid #f0f0f0;
        border-radius: 8px;
        box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.08);
        background: linear-gradient(135deg, #fafbfc 0%, #ffffff 100%);
        position: relative;
        overflow: hidden;
        
        &:hover {
          border-color: #409eff;
          box-shadow: 0 6px 30px 0 rgba(64, 158, 255, 0.15);
        }
        
        // 添加图表背景网格效果
        &::before {
          content: '';
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background-image: 
            linear-gradient(rgba(0,0,0,.02) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0,0,0,.02) 1px, transparent 1px);
          background-size: 20px 20px;
          pointer-events: none;
          z-index: 0;
        }

        .graph-canvas {
          position: relative;
          width: 100%;
          height: 100%;
          z-index: 1;
        }

        .empty-state {
          position: absolute;
          inset: 0;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          gap: 10px;
          color: #909399;
          text-align: center;
          z-index: 2;

          .empty-icon {
            font-size: 40px;
          }

          .empty-title {
            font-size: 16px;
            font-weight: 600;
            color: #606266;
          }

          .empty-desc {
            font-size: 13px;
            max-width: 60%;
            color: #a0a4ac;
          }
        }

        .graph-loading-mask {
          position: absolute;
          inset: 0;
          background: rgba(255, 255, 255, 0.92);
          display: flex;
          align-items: center;
          justify-content: center;
          z-index: 3;

          .loading-panel {
            width: 320px;
            padding: 20px;
            border-radius: 12px;
            background: #fff;
            box-shadow: 0 15px 35px rgba(15, 23, 42, 0.15);
            text-align: center;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 12px;

            .loading-spinner {
              width: 36px;
              height: 36px;
              border: 3px solid #e5e7eb;
              border-top-color: #409eff;
              border-radius: 50%;
              animation: spin 0.8s linear infinite;
            }

            .loading-title {
              font-size: 16px;
              font-weight: 600;
              color: #1f2d3d;
            }

            .loading-tip {
              font-size: 13px;
              color: #909399;
            }
          }
        }

        @keyframes spin {
          to {
            transform: rotate(360deg);
          }
        }

      }
      
      // 移除标题下方的分割线
      :deep(.el-card__header) {
        border-bottom: none;
      }
    }
    
    .stats-container {
      width: 300px;
      
      .stat-card {
        .card-header {
          font-weight: bold;
        }
        
        .risk-overview {
          display: flex;
          flex-direction: column;
          gap: 12px;
          
          .risk-chart {
            height: 200px;
          }

          .risk-summary {
            display: flex;
            flex-direction: column;
            gap: 6px;
            background: #f6f9fc;
            border-radius: 8px;
            padding: 12px 16px;

            .summary-title {
              font-size: 14px;
              color: #666;
            }

            .summary-value {
              font-size: 20px;
              font-weight: 600;

              &.level-high {
                color: #f56c6c;
              }

              &.level-medium {
                color: #e6a23c;
              }

              &.level-low {
                color: #67c23a;
              }

              &.level-pending {
                color: #909399;
              }
            }

            .forecast-title {
              margin-top: 10px;
              font-size: 13px;
              color: #8c8c8c;
            }

            .forecast-value {
              font-size: 18px;
              font-weight: 600;

              &.level-high {
                color: #f56c6c;
              }

              &.level-medium {
                color: #e6a23c;
              }

              &.level-low {
                color: #67c23a;
              }

              &.level-pending {
                color: #909399;
              }
            }
          }
        }
        
        .stat-grid {
          display: grid;
          grid-template-columns: repeat(2, 1fr);
          gap: 20px;
          
          .stat-item {
            text-align: center;
            
            .stat-value {
              font-size: 24px;
              font-weight: bold;
              color: #409EFF;
            }
            
            .stat-label {
              margin-top: 8px;
              color: #666;
            }
          }
        }

        .integrity-metrics {
          display: flex;
          flex-direction: column;
          gap: 4px;

          .metric-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 2px 0 2px;
            border-bottom: 1px dashed #e5e7eb;

            &:first-child {
              padding-top: 0;
            }

            &:last-child {
              border-bottom: none;
            }

            &.highlight {
              .metric-value {
                color: #1f8ef1;
              }
            }

            .metric-label {
              color: #606266;
              font-size: 13px;
            }

            .metric-value {
              font-size: 16px;
              font-weight: bold;
              color: #303133;
            }
          }
        }
        
        // 移除标题下方的分割线
        :deep(.el-card__header) {
          border-bottom: none;
          padding-bottom: 4px;
        }
      }
    }
  }
  
  .text-center {
    text-align: center;
    font-size: 24px;
    margin-bottom: -20px;
  }
}
</style> 
