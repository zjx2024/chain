<template>
  <div class="node-risk-status">
    <el-card class="filter-card" shadow="never">
      <template #header>
        <span>节点风险检索</span>
      </template>
      <el-form :model="filterForm" inline label-width="90px" class="filter-form">
        <el-form-item label="产业链">
          <el-select
            v-model="filterForm.industryChainId"
            placeholder="请选择产业链"
            style="width: 220px"
            @change="handleIndustryChange"
            :loading="industryChainLoading"
            clearable
          >
            <el-option
              v-for="chain in industryChainOptions"
              :key="chain.id"
              :label="chain.name"
              :value="chain.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="数据期间">
          <el-select
            v-model="filterForm.dataPeriod"
            placeholder="请选择数据期间"
            style="width: 200px"
            :disabled="!filterForm.industryChainId"
            :loading="periodLoading"
            clearable
          >
            <el-option
              v-for="period in periodOptions"
              :key="period"
              :label="period"
              :value="period"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="公司">
          <el-autocomplete
            v-model="filterForm.companyName"
            placeholder="请输入公司名称"
            :fetch-suggestions="queryCompanySuggestions"
            :trigger-on-focus="false"
            clearable
            style="width: 260px"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">确定</el-button>
          <el-button @click="resetFilter">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="result-card" shadow="never">
      <template #header>
        <span>节点风险详情</span>
      </template>
      <div class="content-area" v-loading="resultLoading">
        <template v-if="riskResult">
          <div class="status-summary" v-loading="resultLoading">
            <div class="status-card" :class="riskResult.currentRisk ? 'danger' : 'safe'">
              <div class="status-title">当前风险状况</div>
              <div class="risk-visual">
                <div class="factor-legend">
                  <div
                    class="legend-item"
                    v-for="item in factorLegend"
                    :key="item.label"
                  >
                    <span class="legend-dot" :style="{ background: item.color }" />
                    <span>{{ item.label }}</span>
                  </div>
                </div>
                <div ref="currentChartRef" class="risk-chart"></div>
              </div>
            </div>
            <div class="status-card" :class="riskResult.nextPeriodRisk ? 'danger' : 'safe'">
              <div class="status-title">T+1 期风险预警</div>
              <div class="risk-visual">
                <div class="factor-legend">
                  <div
                    class="legend-item"
                    v-for="item in factorLegend"
                    :key="item.label"
                  >
                    <span class="legend-dot" :style="{ background: item.color }" />
                    <span>{{ item.label }}</span>
                  </div>
                </div>
                <div ref="nextChartRef" class="risk-chart"></div>
              </div>
            </div>
          </div>
          <div class="alert-section" v-loading="alertLoading">
            <div class="alert-header">
              <div>
                <div class="alert-title">节点风险告警信息</div>
                <div class="alert-subtitle">基于 T+1 期 18 项风险因素预警结果的智能分析</div>
              </div>
              <template v-if="riskAlert">
                <el-tag :type="alertMeta ? alertMeta.tagType : 'success'">
                  {{ alertMeta ? alertMeta.label : '低风险' }}
                </el-tag>
              </template>
            </div>
            <div v-if="riskAlert" class="alert-content">
              <div class="alert-level-desc">
                <!-- 保留占位，若需提示可在后端 remark 字段提供说明 -->
              </div>
              <div class="alert-panels">
                <div class="panel">
                  <div class="panel-title">关键风险因素</div>
                  <div class="factor-list">
                    <div
                      class="factor-item"
                      v-for="factor in riskAlert.keyFactors"
                      :key="factor.name"
                    >
                      <div class="factor-name">{{ factor.name }}</div>
                      <div class="factor-value">{{ formatFactorValue(factor.value) }}</div>
                      <div class="factor-impact">{{ factor.impact }}</div>
                    </div>
                  </div>
                </div>
                <div class="panel">
                  <div class="panel-title">风险处置建议</div>
                  <ol class="suggestions-list">
                    <li v-for="(suggest, index) in riskAlert.suggestions" :key="index">
                      {{ suggest }}
                    </li>
                  </ol>
                </div>
              </div>
            </div>
            <el-alert
              v-else-if="alertError"
              :title="alertError"
              type="warning"
              show-icon
              :closable="false"
            />
            <el-empty v-else description="暂无该公司的告警分析结果" />
          </div>
        </template>
        <el-empty
          v-else-if="hasSearched"
          description="暂无该公司在所选期间的节点风险数据"
        />
        <el-empty
          v-else
          description="请填写筛选条件后查询节点风险状态"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, nextTick, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { getIndustryChainList } from '@/api/industryChain'
import { getDataPeriods } from '@/api/dataset'
import { getNodeRiskAlert, getNodeRiskCompanies, getNodeRiskStatus } from '@/api/nodeRisk'
import type { IndustryChain } from '@/types/dataset'
import type { NodeRiskAlert, NodeRiskDetail, RiskFactor, RiskAlertLevel } from '@/types/risk'
import * as echarts from 'echarts/core'
import { PieChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GraphicComponent
} from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'

echarts.use([PieChart, TitleComponent, TooltipComponent, LegendComponent, GraphicComponent, CanvasRenderer])

interface FilterForm {
  industryChainId: number | null
  dataPeriod: string
  companyName: string
}

const filterForm = ref<FilterForm>({
  industryChainId: null,
  dataPeriod: '',
  companyName: ''
})

const industryChainOptions = ref<IndustryChain[]>([])
const industryChainLoading = ref(false)
const periodOptions = ref<string[]>([])
const periodLoading = ref(false)

const companyOptions = ref<string[]>([])

const hasSearched = ref(false)
const resultLoading = ref(false)
const riskResult = ref<NodeRiskDetail | null>(null)
const alertLoading = ref(false)
const riskAlert = ref<NodeRiskAlert | null>(null)
const alertError = ref<string | null>(null)
const alertMeta = computed(() => {
  if (!riskAlert.value) {
    return null
  }
  return getAlertMeta(riskAlert.value.alertLevel)
})
type EChartsInstance = ReturnType<typeof echarts.init>

const currentChartRef = ref<HTMLElement | null>(null)
const nextChartRef = ref<HTMLElement | null>(null)
let currentChart: EChartsInstance | null = null
let nextChart: EChartsInstance | null = null
const resizeHandler = () => {
  currentChart?.resize()
  nextChart?.resize()
}

const ALERT_LEVEL_META: Record<RiskAlertLevel, { label: string; tagType: 'success' | 'warning' | 'danger'; desc: string }> = {
  LOW: {
    label: '低风险',
    tagType: 'success',
    desc: '指标整体健康，无需额外操作'
  },
  MEDIUM: {
    label: '中风险',
    tagType: 'warning',
    desc: '部分指标偏离正常范围，建议持续关注'
  },
  HIGH: {
    label: '有风险',
    tagType: 'danger',
    desc: '存在较高风险，请优先处置'
  }
}

const getAlertMeta = (level?: RiskAlertLevel | string) => {
  if (level && Object.prototype.hasOwnProperty.call(ALERT_LEVEL_META, level)) {
    return ALERT_LEVEL_META[level as RiskAlertLevel]
  }
  return ALERT_LEVEL_META.LOW
}

const fetchIndustryChains = async () => {
  industryChainLoading.value = true
  try {
    const { data } = await getIndustryChainList()
    industryChainOptions.value = data
  } finally {
    industryChainLoading.value = false
  }
}

const fetchPeriodsByIndustry = async (industryChainId: number) => {
  periodLoading.value = true
  try {
    const { data } = await getDataPeriods(industryChainId)
    periodOptions.value = data
  } catch (error) {
    ElMessage.error('获取数据期间失败')
  } finally {
    periodLoading.value = false
  }
}

const handleIndustryChange = (value: number | null) => {
  filterForm.value.dataPeriod = ''
  filterForm.value.companyName = ''
  periodOptions.value = []
  companyOptions.value = []
  riskResult.value = null
  riskAlert.value = null
  alertError.value = null
  hasSearched.value = false

  if (value) {
    fetchPeriodsByIndustry(value)
    fetchCompanyOptions(value)
  }
}

const fetchCompanyOptions = async (industryChainId: number) => {
  try {
    const { data } = await getNodeRiskCompanies(industryChainId)
    companyOptions.value = data || []
  } catch (error) {
    console.error('获取公司列表失败', error)
    companyOptions.value = []
    ElMessage.error('获取公司列表失败，请检查节点风险文件')
  }
}

const queryCompanySuggestions = (queryString: string, cb: (results: { value: string }[]) => void) => {
  const results = !queryString
    ? companyOptions.value
    : companyOptions.value.filter(name =>
        name.toLowerCase().includes(queryString.toLowerCase())
      )
  cb(results.map(value => ({ value })))
}

const handleSearch = async () => {
  if (!filterForm.value.industryChainId || !filterForm.value.dataPeriod) {
    ElMessage.warning('请选择产业链和数据期间')
    return
  }
  if (!filterForm.value.companyName) {
    ElMessage.warning('请输入公司名称')
    return
  }

  resultLoading.value = true
  hasSearched.value = true
  const startTime = Date.now()
  try {
    const { data } = await getNodeRiskStatus({
      industryChainId: filterForm.value.industryChainId,
      dataPeriod: filterForm.value.dataPeriod,
      companyName: filterForm.value.companyName
    })
    const elapsed = Date.now() - startTime
    const minDuration = 2000
    if (elapsed < minDuration) {
      await new Promise(resolve => setTimeout(resolve, minDuration - elapsed))
    }
    riskResult.value = data
    await fetchRiskAlert()
  } catch (error: any) {
    console.error('获取节点风险状态失败', error)
    riskResult.value = null
    riskAlert.value = null
    alertError.value = null
    if (error.response?.data?.message) {
      ElMessage.error(error.response.data.message)
    } else {
      ElMessage.error('获取节点风险状态失败')
    }
  } finally {
    resultLoading.value = false
  }
}

const resetFilter = () => {
  filterForm.value = {
    industryChainId: null,
    dataPeriod: '',
    companyName: ''
  }
  periodOptions.value = []
  companyOptions.value = []
  riskResult.value = null
  riskAlert.value = null
  alertError.value = null
  hasSearched.value = false
}

const fetchRiskAlert = async () => {
  if (!filterForm.value.industryChainId || !filterForm.value.dataPeriod || !filterForm.value.companyName) {
    return
  }
  alertLoading.value = true
  alertError.value = null
  try {
    const { data } = await getNodeRiskAlert({
      industryChainId: filterForm.value.industryChainId,
      dataPeriod: filterForm.value.dataPeriod,
      companyName: filterForm.value.companyName
    })
    riskAlert.value = data
  } catch (error: any) {
    console.error('获取节点风险告警失败', error)
    riskAlert.value = null
    alertError.value = error.response?.data?.message || '获取节点风险告警失败'
  } finally {
    alertLoading.value = false
  }
}

const COLOR_MAP = {
  red: '#F56C6C',
  yellow: '#FFD666',
  green: '#2FB850',
  neutral: '#d9d9d9'
} as const

const factorLegend = [
  { color: COLOR_MAP.red, label: '隐患' },
  { color: COLOR_MAP.yellow, label: '注意' },
  { color: COLOR_MAP.green, label: '健康' }
]

type FactorSegment = {
  value: number
  name: string
  displayValue: number | null
  itemStyle: { color: string }
}

const formatFactorValue = (value: number | null | undefined) => {
  if (value === null || value === undefined || Number.isNaN(value)) {
    return '--'
  }
  return Number(value).toFixed(2)
}

const getFactorColor = (index: number, rawValue: number | null | undefined) => {
  if (rawValue === null || rawValue === undefined || Number.isNaN(rawValue)) {
    return COLOR_MAP.neutral
  }
  const value = rawValue
  switch (index) {
    case 0:
      if (value < 2) return COLOR_MAP.red
      if (value < 8) return COLOR_MAP.yellow
      return COLOR_MAP.green
    case 1:
    case 2:
      if (value < 0) return COLOR_MAP.red
      if (value < 8) return COLOR_MAP.yellow
      return COLOR_MAP.green
    case 3:
      if (value >= 20 && value <= 60) return COLOR_MAP.green
      if (value <= 75) return COLOR_MAP.yellow
      return COLOR_MAP.red
    case 4:
      if (value < 1) return COLOR_MAP.red
      if (value < 1.5) return COLOR_MAP.yellow
      return COLOR_MAP.green
    case 5:
      if (value < 0.6) return COLOR_MAP.red
      if (value < 1.0) return COLOR_MAP.yellow
      return COLOR_MAP.green
    case 6:
      if (value < 0.15) return COLOR_MAP.red
      if (value < 0.35) return COLOR_MAP.yellow
      return COLOR_MAP.green
    case 7:
      if (value <= 0.7) return COLOR_MAP.green
      if (value <= 1.2) return COLOR_MAP.yellow
      return COLOR_MAP.red
    case 8:
      if (value < 0) return COLOR_MAP.red
      if (value < 0.2) return COLOR_MAP.yellow
      return COLOR_MAP.green
    case 9:
      if (value < 1.5) return COLOR_MAP.red
      if (value < 3.0) return COLOR_MAP.yellow
      return COLOR_MAP.green
    case 10:
      if (value < 2) return COLOR_MAP.red
      if (value < 5) return COLOR_MAP.yellow
      return COLOR_MAP.green
    case 11:
      if (value < 0.7) return COLOR_MAP.red
      if (value < 1.1) return COLOR_MAP.yellow
      return COLOR_MAP.green
    case 12:
      if (value < 30) return COLOR_MAP.red
      if (value < 80) return COLOR_MAP.yellow
      return COLOR_MAP.green
    case 13:
      if (value < 0.3) return COLOR_MAP.red
      if (value < 0.6) return COLOR_MAP.yellow
      return COLOR_MAP.green
    case 14:
      if (value < 0) return COLOR_MAP.red
      if (value < 5) return COLOR_MAP.yellow
      return COLOR_MAP.green
    case 15:
      if (value < 0) return COLOR_MAP.red
      if (value < 8) return COLOR_MAP.yellow
      return COLOR_MAP.green
    case 16:
      if (value < 0) return COLOR_MAP.red
      if (value < 8) return COLOR_MAP.yellow
      return COLOR_MAP.green
    case 17:
      if (value < 0) return COLOR_MAP.red
      if (value < 5) return COLOR_MAP.yellow
      return COLOR_MAP.green
    default:
      return COLOR_MAP.neutral
  }
}

const buildFactorSegments = (factors?: RiskFactor[]): FactorSegment[] => {
  if (!factors || factors.length === 0) {
    return [
      {
        value: 1,
        name: '暂无数据',
        displayValue: null,
        itemStyle: { color: COLOR_MAP.neutral }
      }
    ]
  }
  return factors.map(factor => ({
    value: 1,
    name: factor.name,
    displayValue: factor.value ?? null,
    itemStyle: { color: getFactorColor(factor.index, factor.value) }
  }))
}

const buildChartOption = (factors: RiskFactor[] | undefined, isRisk: boolean, label: string) => {
  const segments = buildFactorSegments(factors)
  return {
    tooltip: {
      trigger: 'item',
      formatter: (params: any) => {
        return `${params.data.name}<br/>指标值：${formatFactorValue(params.data.displayValue)}`
      }
    },
    animationDuration: 800,
    series: [
      {
        name: 'risk',
        type: 'pie',
        radius: ['70%', '90%'],
        avoidLabelOverlap: true,
        label: { show: false },
        itemStyle: { borderRadius: 6, borderWidth: 2, borderColor: '#fff' },
        data: segments
      }
    ],
    graphic: [
      {
        type: 'text',
        left: 'center',
        top: 'center',
        z: 10,
        silent: true,
        style: {
          text: label,
          textAlign: 'center',
          fill: isRisk ? '#D4380D' : '#237804',
          fontSize: 20,
          fontWeight: 600
        }
      }
    ]
  }
}

const renderCharts = () => {
  if (!riskResult.value) {
    disposeCharts()
    return
  }
  nextTick(() => {
    if (currentChartRef.value && !currentChart) {
      currentChart = echarts.init(currentChartRef.value)
    }
    if (currentChart) {
      currentChart.setOption(
        buildChartOption(
          riskResult.value!.currentFactors,
          riskResult.value!.currentRisk,
          riskResult.value!.currentRisk ? '风险' : '安全'
        ),
        true
      )
    }
    if (nextChartRef.value && !nextChart) {
      nextChart = echarts.init(nextChartRef.value)
    }
    if (nextChart) {
      nextChart.setOption(
        buildChartOption(
          riskResult.value!.nextPeriodFactors,
          riskResult.value!.nextPeriodRisk,
          riskResult.value!.nextPeriodRisk ? '风险' : '安全'
        ),
        true
      )
    }
  })
}

const disposeCharts = () => {
  currentChart?.dispose()
  currentChart = null
  nextChart?.dispose()
  nextChart = null
}

onMounted(() => {
  fetchIndustryChains()
  window.addEventListener('resize', resizeHandler)
})

onUnmounted(() => {
  disposeCharts()
  window.removeEventListener('resize', resizeHandler)
})

watch(riskResult, () => {
  if (riskResult.value) {
    renderCharts()
  } else {
    disposeCharts()
  }
})
</script>

<style scoped lang="scss">
.node-risk-status {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;

  .filter-card,
  .result-card {
    border-radius: 12px;
  }

  .filter-form {
    display: flex;
    flex-wrap: wrap;
    gap: 12px 32px;
    align-items: flex-end;
  }

  .content-area {
    min-height: 320px;
    display: flex;
    align-items: stretch;
    justify-content: center;
    flex-direction: column;

    .status-summary {
      width: 100%;
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 20px;

      .status-card {
        border-radius: 12px;
        padding: 24px;
        box-shadow: inset 0 0 0 1px #ebeef5;
        display: flex;
        flex-direction: column;
        gap: 12px;

        &.safe {
          background: #f6ffed;
          color: #389e0d;
        }

        &.danger {
          background: #fff1f0;
          color: #d4380d;
        }

        .status-title {
          font-size: 16px;
          font-weight: 600;
        }

        .status-value {
          font-size: 32px;
          font-weight: bold;
        }

        .status-desc {
          font-size: 13px;
          color: #666;
        }

        .risk-visual {
          display: flex;
          justify-content: center;
          align-items: center;
          margin-top: 12px;
          min-height: 180px;
          position: relative;

          .factor-legend {
            position: absolute;
            top: 8px;
            right: 8px;
            display: flex;
            gap: 12px;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 8px;
            padding: 6px 10px;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
            font-size: 12px;

            .legend-item {
              display: flex;
              align-items: center;
              gap: 4px;

              .legend-dot {
                width: 10px;
                height: 10px;
                border-radius: 50%;
              }
            }
          }
        }

        .risk-chart {
          width: 180px;
          height: 180px;
        }
      }
    }
    .alert-section {
      margin-top: 24px;
      border-radius: 12px;
      padding: 20px;
      background: #fafafa;
      border: 1px solid #f0f0f0;
      display: flex;
      flex-direction: column;
      gap: 16px;

      .alert-header {
        display: flex;
        justify-content: space-between;
        align-items: center;

        .alert-title {
          font-size: 16px;
          font-weight: 600;
        }

        .alert-subtitle {
          font-size: 12px;
          color: #909399;
          margin-top: 4px;
        }
      }

      .alert-content {
        display: flex;
        flex-direction: column;
        gap: 16px;

        .alert-level-desc {
          display: flex;
          flex-direction: column;
          gap: 8px;
          font-size: 13px;
          color: #666;

          .level-meta {
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
            color: #909399;
          }

          .level-remark {
            color: #409eff;
          }
        }

        .alert-panels {
          display: flex;
          flex-wrap: wrap;
          gap: 18px;

          .panel {
            flex: 1;
            min-width: 280px;
            background: #fff;
            border-radius: 10px;
            padding: 16px 20px;
            box-shadow: inset 0 0 0 1px #f1f1f1;
            display: flex;
            flex-direction: column;
            gap: 12px;

            .panel-title {
              font-size: 16px;
              font-weight: 600;
            }

            .factor-list {
              display: flex;
              flex-direction: column;
              gap: 10px;
            }

            .factor-item {
              padding: 10px 12px;
              border-radius: 10px;
              background: #f8f8f8;
              box-shadow: inset 0 0 0 1px #f1f1f1;

              .factor-name {
                font-size: 14px;
                color: #303133;
                font-weight: 600;
              }

              .factor-value {
                font-size: 20px;
                font-weight: bold;
                margin: 4px 0;
                color: #303133;
              }

              .factor-impact {
                font-size: 13px;
                color: #606266;
              }
            }

            .suggestions-list {
              padding-left: 20px;
              margin: 0;
              display: flex;
              flex-direction: column;
              gap: 10px;
              font-size: 15px;
              color: #40454d;
            }
          }

        }
      }
    }
  }
}
</style>
