<template>
  <div class="risk-model-container">
    <h2>模型训练</h2>
    
    <!-- 算法训练参数选择 -->
    <el-card class="parameter-card">
      <template #header>
        <div class="card-header">
          <span>算法训练参数选择</span>
        </div>
      </template>
      
      <el-form :model="trainForm" ref="trainFormRef" label-width="80px" class="train-form">
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="数据集" prop="datasetId" :rules="[{ required: true, message: '请选择数据集', trigger: 'change' }]">
              <el-select v-model="trainForm.datasetId" placeholder="请选择数据集" style="width: 100%" @change="handleDatasetChange" :loading="datasetsLoading">
                <el-option 
                  v-for="dataset in availableDatasets" 
                  :key="dataset.id" 
                  :label="dataset.name" 
                  :value="dataset.id"
                >
                  <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span>{{ dataset.name }}</span>
                    <div style="display: flex; align-items: center; gap: 8px;">
                      <el-tag 
                        :type="getDatasetTypeTag(dataset.typeCode).type" 
                        size="small"
                        effect="plain"
                      >
                        {{ getDatasetTypeTag(dataset.typeCode).label }}
                      </el-tag>
                      <span style="color: #8492a6; font-size: 13px">{{ dataset.dataPeriod }}</span>
                    </div>
                  </div>
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="日期(季)" prop="dataPeriod">
              <el-select v-model="trainForm.dataPeriod" placeholder="请选择日期" style="width: 100%" :disabled="!selectedDataset">
                <el-option 
                  v-for="period in availablePeriods" 
                  :key="period" 
                  :label="period" 
                  :value="period">
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="任务类型" prop="taskTypeId" :rules="[{ required: true, message: '请选择任务类型', trigger: 'change' }]">
              <el-select v-model="trainForm.taskTypeId" placeholder="请选择任务类型" style="width: 100%" @change="handleTaskTypeChange" :loading="taskTypesLoading">
                <el-option 
                  v-for="taskType in availableTaskTypes" 
                  :key="taskType.id" 
                  :label="taskType.name" 
                  :value="taskType.id">
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="模型" prop="modelId" :rules="[{ required: true, message: '请选择模型', trigger: 'change' }]">
              <el-select v-model="trainForm.modelId" placeholder="请选择模型" style="width: 100%" @change="handleModelChange" :loading="modelsLoading" :disabled="!trainForm.taskTypeId">
                <el-option 
                  v-for="model in availableModels" 
                  :key="model.id" 
                  :label="model.description" 
                  :value="model.id">
                  <span>{{ model.description }}</span>
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="训练轮次" prop="epochs" :rules="[{ required: true, message: '请输入训练轮次', trigger: 'blur' }]">
              <el-input v-model="trainForm.epochs" placeholder="请输入epoch"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="优化器" prop="optimizerId" :rules="[{ required: true, message: '请选择优化器', trigger: 'change' }]">
              <el-select v-model="trainForm.optimizerId" placeholder="请选择优化器" style="width: 100%" @change="handleOptimizerChange" :loading="optimizersLoading" :disabled="!trainForm.modelId">
                <el-option 
                  v-for="optimizer in availableOptimizers" 
                  :key="optimizer.optimizerId" 
                  :label="optimizer.optimizerName" 
                  :value="optimizer.optimizerId">
                  <span>{{ optimizer.optimizerName }}</span>
                  <span style="float: right; color: #8492a6; font-size: 13px">默认: {{ optimizer.defaultLr }}</span>
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="学习率" prop="learningRate">
              <el-input 
                v-model="trainForm.learningRate" 
                placeholder="可选，不输入将使用默认学习率"
                clearable>
                <template #suffix>
                  <el-tooltip 
                    effect="dark" 
                    content="不输入学习率时，系统将使用选中优化器的默认学习率" 
                    placement="top">
                    <el-icon><InfoFilled /></el-icon>
                  </el-tooltip>
                </template>
              </el-input>
              <div v-if="selectedOptimizer && currentLearningRate" class="lr-hint">
                <span class="hint-text">
                  {{ trainForm.learningRate ? '自定义学习率' : '将使用默认学习率' }}: {{ currentLearningRate }}
                </span>
              </div>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row>
          <el-col :span="24" class="button-group">
            <el-button type="primary" @click="handleTrain" :loading="trainLoading">确认并开始</el-button>
            <el-button @click="resetForm">重置</el-button>
          </el-col>
        </el-row>
      </el-form>
    </el-card>
    
    <!-- 训练进度表格 -->
    <el-card class="progress-card">
      <template #header>
        <div class="card-header">
          <span>训练进度</span>
        </div>
      </template>
      
      <el-table :data="trainingProgress" style="width: 100%" v-loading="tableLoading">
        <el-table-column prop="id" label="序号" min-width="80" align="center"></el-table-column>
        <el-table-column prop="datasetName" label="数据集" min-width="120"></el-table-column>
        <el-table-column prop="taskName" label="模型名称" min-width="200"></el-table-column>
        <el-table-column prop="taskTypeName" label="任务类型" min-width="100"></el-table-column>
        <el-table-column prop="startTime" label="训练时间" min-width="160"></el-table-column>
        <el-table-column prop="currentEpoch" label="当前训练轮次" min-width="130" align="center">
          <template #default="scope">
            <span v-if="scope.row.modelName === 'MetaPath2vec'">—</span>
            <span v-else-if="scope.row.status === 'RUNNING'" class="training-progress">
              {{ scope.row.currentEpoch }}/{{ scope.row.totalEpochs }}
            </span>
            <span v-else-if="scope.row.status === 'COMPLETED'" class="completed-progress">
              {{ scope.row.totalEpochs }}/{{ scope.row.totalEpochs }}
            </span>
            <span v-else>{{ scope.row.currentEpoch || 0 }}/{{ scope.row.totalEpochs }}</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" min-width="100" align="center">
          <template #default="scope">
            <el-button 
              type="danger" 
              size="small" 
              @click="handleTerminate(scope.row)"
              v-if="scope.row.status === 'RUNNING'"
            >
              终止
            </el-button>
            <el-tag v-else-if="scope.row.status === 'COMPLETED'" type="success">已完成</el-tag>
            <el-tag v-else-if="scope.row.status === 'TERMINATED'" type="warning">已终止</el-tag>
            <el-tag v-else-if="scope.row.status === 'FAILED'" type="danger">失败</el-tag>
            <el-tag v-else-if="scope.row.status === 'PENDING'" type="info">待启动</el-tag>
          </template>
        </el-table-column>
      </el-table>
      
      <div v-if="trainingProgress.length === 0" class="empty-state">
        <el-empty description="暂无训练任务"></el-empty>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, onUnmounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { InfoFilled } from '@element-plus/icons-vue'
import { getDatasetList, getIndustryChains, getDataPeriods } from '@/api/dataset'
import { getTaskTypes, getModelsByTaskType, getOptimizersByModel, startModelTraining, getRunningTasks, terminateTask, type ModelTrainingRequest, type TrainingTask } from '@/api/modelTraining'
import type { Dataset, IndustryChain } from '@/types/dataset'
import type { TaskType, Model, OptimizerWithLr } from '@/api/modelTraining'

// 表单数据
const trainForm = reactive({
  datasetId: null as number | null,
  dataPeriod: '',
  taskTypeId: null as number | null,
  modelId: null as number | null,
  optimizerId: null as number | null,
  epochs: '',
  learningRate: ''
})

// 表单引用
const trainFormRef = ref()

// 加载状态
const trainLoading = ref(false)
const tableLoading = ref(false)
const datasetsLoading = ref(false)
const taskTypesLoading = ref(false)
const modelsLoading = ref(false)
const optimizersLoading = ref(false)

// 后端数据
const availableDatasets = ref<Dataset[]>([])
const industryChains = ref<IndustryChain[]>([])
const availablePeriods = ref<string[]>([])
const availableTaskTypes = ref<TaskType[]>([])
const availableModels = ref<Model[]>([])
const availableOptimizers = ref<OptimizerWithLr[]>([])

// 选中的数据集信息
const selectedDataset = computed(() => {
  return availableDatasets.value.find(d => d.id === trainForm.datasetId)
})

// 选中的任务类型信息
const selectedTaskType = computed(() => {
  return availableTaskTypes.value.find(t => t.id === trainForm.taskTypeId)
})

// 选中的模型信息
const selectedModel = computed(() => {
  return availableModels.value.find(m => m.id === trainForm.modelId)
})

// 选中的优化器信息
const selectedOptimizer = computed(() => {
  return availableOptimizers.value.find(o => o.optimizerId === trainForm.optimizerId)
})

// 当前使用的学习率（用户输入的或默认的）
const currentLearningRate = computed(() => {
  return trainForm.learningRate || (selectedOptimizer.value?.defaultLr?.toString() || '')
})

// 训练进度数据
const trainingProgress = ref<TrainingTask[]>([])

// 定时器
let epochTimer: number | null = null

// 获取数据集类型标签
const getDatasetTypeTag = (typeCode: string) => {
  switch (typeCode) {
    case 'FEATURE_LABEL':
      return { label: '特征标签', type: 'primary' }
    case 'TRAIN_TEST':
      return { label: '训练测试', type: 'success' }
    case 'INDUSTRY_RELATION':
      return { label: '产业链关系', type: 'warning' }
    default:
      return { label: '未知类型', type: 'info' }
  }
}

// 获取训练相关数据集列表（特征与标签数据、训练测试数据）
const fetchDatasets = async () => {
  try {
    datasetsLoading.value = true
    
    // 并行获取多种类型的数据集
    const [featureLabelData, trainTestData] = await Promise.all([
      getDatasetList({
        pageNum: 1,
        pageSize: 1000,
        typeCode: 'FEATURE_LABEL'
      }),
      getDatasetList({
        pageNum: 1,
        pageSize: 1000,
        typeCode: 'TRAIN_TEST'
      })
    ])
    
    // 合并两种类型的数据集
    const allDatasets = [
      ...featureLabelData.data.records,
      ...trainTestData.data.records
    ]
    
    // 按创建时间降序排序，最新的在前面
    availableDatasets.value = allDatasets.sort((a, b) => 
      new Date(b.createTime).getTime() - new Date(a.createTime).getTime()
    )
    
    console.log('获取数据集列表:', availableDatasets.value)
  } catch (error) {
    console.error('获取数据集列表失败:', error)
    ElMessage.error('获取数据集列表失败')
  } finally {
    datasetsLoading.value = false
  }
}

// 获取产业链列表
const fetchIndustryChains = async () => {
  try {
    const { data } = await getIndustryChains()
    industryChains.value = data
    console.log('获取产业链列表:', industryChains.value)
  } catch (error) {
    console.error('获取产业链列表失败:', error)
    ElMessage.error('获取产业链列表失败')
  }
}

// 获取指定产业链的数据期间列表
const fetchDataPeriods = async (industryChainId: number) => {
  try {
    const { data } = await getDataPeriods(industryChainId)
    availablePeriods.value = data
    console.log('获取数据期间列表:', availablePeriods.value)
  } catch (error) {
    console.error('获取数据期间列表失败:', error)
    ElMessage.error('获取数据期间列表失败')
  }
}

// 获取任务类型列表
const fetchTaskTypes = async () => {
  try {
    taskTypesLoading.value = true
    const { data } = await getTaskTypes()
    // 过滤掉测试任务类型
    availableTaskTypes.value = (data || []).filter((t: any) => t?.code !== 'TEST_TASK' && t?.name !== '测试训练任务')
    console.log('获取任务类型列表:', availableTaskTypes.value)
  } catch (error) {
    console.error('获取任务类型列表失败:', error)
    ElMessage.error('获取任务类型列表失败')
  } finally {
    taskTypesLoading.value = false
  }
}

// 获取指定任务类型的模型列表
const fetchModelsByTaskType = async (taskTypeId: number) => {
  try {
    modelsLoading.value = true
    const { data } = await getModelsByTaskType(taskTypeId)
    availableModels.value = data
    console.log('获取模型列表:', availableModels.value)
  } catch (error) {
    console.error('获取模型列表失败:', error)
    ElMessage.error('获取模型列表失败')
  } finally {
    modelsLoading.value = false
  }
}

// 获取指定模型的优化器列表
const fetchOptimizersByModel = async (modelId: number) => {
  try {
    optimizersLoading.value = true
    const { data } = await getOptimizersByModel(modelId)
    availableOptimizers.value = data
    console.log('获取优化器列表:', availableOptimizers.value)
  } catch (error) {
    console.error('获取优化器列表失败:', error)
    ElMessage.error('获取优化器列表失败')
  } finally {
    optimizersLoading.value = false
  }
}

// 处理数据集选择变化
const handleDatasetChange = async (datasetId: number) => {
  const dataset = availableDatasets.value.find(d => d.id === datasetId)
  if (dataset) {
    trainForm.dataPeriod = dataset.dataPeriod
    await fetchDataPeriods(dataset.industryChainId)
  }
}

// 处理任务类型选择变化
const handleTaskTypeChange = async (taskTypeId: number) => {
  // 清空下级选项
  trainForm.modelId = null
  trainForm.optimizerId = null
  trainForm.learningRate = ''
  availableModels.value = []
  availableOptimizers.value = []
  
  // 获取对应的模型列表
  if (taskTypeId) {
    await fetchModelsByTaskType(taskTypeId)
  }
}

// 处理模型选择变化
const handleModelChange = async (modelId: number) => {
  // 清空下级选项
  trainForm.optimizerId = null
  trainForm.learningRate = ''
  availableOptimizers.value = []
  
  // 获取对应的优化器列表
  if (modelId) {
    await fetchOptimizersByModel(modelId)
  }
}

// 处理优化器选择变化
const handleOptimizerChange = (optimizerId: number) => {
  const optimizer = availableOptimizers.value.find(o => o.optimizerId === optimizerId)
  if (optimizer) {
    // 只有当学习率为空时才自动填充默认学习率
    if (!trainForm.learningRate) {
      trainForm.learningRate = optimizer.defaultLr.toString()
    }
  }
}

// 开始训练
const handleTrain = async () => {
  if (!trainFormRef.value) return
  
  try {
    await trainFormRef.value.validate()
    trainLoading.value = true
    
    // 构建训练请求
    const dataset = selectedDataset.value
    const taskType = selectedTaskType.value
    const model = selectedModel.value
    const optimizer = selectedOptimizer.value
    
    if (!dataset || !taskType || !model || !optimizer) {
      ElMessage.error('请完整填写训练参数')
      trainLoading.value = false
      return
    }
    
    // 如果用户没有输入学习率，使用默认学习率
    const learningRate = trainForm.learningRate ? parseFloat(trainForm.learningRate) : undefined
    
    const trainingRequest: ModelTrainingRequest = {
      datasetId: trainForm.datasetId!,
      dataPeriod: trainForm.dataPeriod,
      taskTypeId: trainForm.taskTypeId!,
      modelId: trainForm.modelId!,
      optimizerId: trainForm.optimizerId!,
      epochs: parseInt(trainForm.epochs),
      learningRate: learningRate,
      clientsSampleRatio: 1.0, // 默认值
      topkRatio: 0.1, // 默认值
      nClusters: 5, // 默认值
      privacyMethod: 'none', // 默认值
      dp: 1e-6 // 默认值
    }
    
    try {
      // 启动训练
      await startModelTraining(trainingRequest)
      ElMessage.success('模型训练已启动！')
      await fetchTrainingTasks()
      resetForm()
    } catch (error) {
      console.error('训练启动失败:', error)
      ElMessage.error('训练启动失败，请检查服务器连接')
    } finally {
      trainLoading.value = false
    }
  } catch (error) {
    console.log('表单验证失败:', error)
    trainLoading.value = false
  }
}

// 获取训练任务列表
const fetchTrainingTasks = async () => {
  try {
    tableLoading.value = true
    const { data } = await getRunningTasks() // 获取正在运行的训练任务
    trainingProgress.value = data
  } catch (error) {
    console.error('获取训练任务列表失败:', error)
    ElMessage.error('获取训练任务列表失败')
  } finally {
    tableLoading.value = false
  }
}

// 终止训练
const handleTerminate = async (row: TrainingTask) => {
  try {
    await ElMessageBox.confirm(`确定要终止模型 "${row.taskName}" 的训练吗？此操作不可逆，终止后将彻底删除此次训练及其进度。`, '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await terminateTask(row.id)
    ElMessage.success('训练已终止！')
    
    // 刷新训练任务列表
    await fetchTrainingTasks()
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('终止训练失败:', error)
      ElMessage.error('终止训练失败')
    } else {
      ElMessage.info('已取消终止')
    }
  }
}

// 重置表单
const resetForm = () => {
  if (!trainFormRef.value) return
  trainFormRef.value.resetFields()
  availablePeriods.value = []
  availableModels.value = []
  availableOptimizers.value = []
}

onMounted(async () => {
  // 并行获取基础数据
  await Promise.all([
    fetchDatasets(),
    fetchIndustryChains(),
    fetchTaskTypes(),
    fetchTrainingTasks() // 获取训练任务列表
  ])
  
  // 启动定时器（每30秒刷新一次训练任务列表）
  epochTimer = setInterval(fetchTrainingTasks, 30000)
})

onUnmounted(() => {
  if (epochTimer) {
    clearInterval(epochTimer)
  }
})
</script>

<style scoped lang="scss">
.risk-model-container {
  h2 {
    margin-bottom: 20px;
    color: #303133;
  }
  
  .parameter-card {
    margin-bottom: 20px;
    
    .card-header {
      font-weight: 600;
      color: #303133;
    }
    
    .train-form {
      .button-group {
        text-align: center;
        margin-top: 20px;
        
        .el-button {
          margin: 0 10px;
          min-width: 80px;
        }
      }
    }
  }
  
  .progress-card {
    .card-header {
      font-weight: 600;
      color: #303133;
    }
    
    .empty-state {
      padding: 40px 0;
    }
    
    .training-progress {
      color: #409eff;
      font-weight: 600;
      animation: pulse 2s infinite;
    }
    
    .completed-progress {
      color: #67c23a;
      font-weight: 600;
    }
  }
  
  .lr-hint {
    margin-top: 4px;
    
    .hint-text {
      font-size: 12px;
      color: #909399;
      line-height: 1.2;
    }
  }
  
  :deep(.el-form-item__label) {
    font-weight: 500;
  }
  
  :deep(.el-card__header) {
    background-color: #f8f9fa;
    border-bottom: 1px solid #e9ecef;
  }
  
  :deep(.el-table) {
    .el-button {
      margin: 0 2px;
    }
  }
}

@keyframes pulse {
  0% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
  100% {
    opacity: 1;
  }
}
</style> 
