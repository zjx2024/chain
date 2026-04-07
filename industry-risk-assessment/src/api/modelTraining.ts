import request from '@/utils/request'

// 任务类型接口
export interface TaskType {
  id: number
  code: string
  name: string
  description?: string
  createTime: string
  updateTime: string
}

// 模型接口
export interface Model {
  id: number
  code: string
  name: string
  description?: string
  modelPath?: string
  createTime: string
  updateTime: string
}

// 优化器接口（带默认学习率）
export interface OptimizerWithLr {
  id: number
  modelId: number
  optimizerId: number
  defaultLr: number
  createTime: string
  modelName: string
  optimizerName: string
}

// 获取所有任务类型
export function getTaskTypes() {
  return request<TaskType[]>({
    url: '/api/model-training/task-types',
    method: 'get'
  })
}

// 根据任务类型ID获取可用模型列表
export function getModelsByTaskType(taskTypeId: number) {
  return request<Model[]>({
    url: `/api/model-training/models/${taskTypeId}`,
    method: 'get'
  })
}

// 根据模型ID获取可用优化器列表（带默认学习率）
export function getOptimizersByModel(modelId: number) {
  return request<OptimizerWithLr[]>({
    url: `/api/model-training/optimizers/${modelId}`,
    method: 'get'
  })
}

// 根据模型ID获取模型详情
export function getModelById(modelId: number) {
  return request<Model>({
    url: `/api/model-training/model/${modelId}`,
    method: 'get'
  })
}

// 更新模型文件路径
export function updateModelPath(modelId: number, modelPath: string) {
  return request({
    url: `/api/model-training/model/${modelId}/path`,
    method: 'put',
    data: modelPath,
    headers: {
      'Content-Type': 'text/plain'
    }
  })
}

// 检查模型文件是否存在
export function checkModelFileExists(modelId: number) {
  return request<boolean>({
    url: `/api/model-training/model/${modelId}/exists`,
    method: 'get'
  })
}

// 获取模型的完整文件系统路径
export function getModelFullPath(modelId: number) {
  return request<string>({
    url: `/api/model-training/model/${modelId}/fullpath`,
    method: 'get'
  })
}

// 模型训练请求接口
export interface ModelTrainingRequest {
  datasetId: number
  dataPeriod: string
  taskTypeId: number
  modelId: number
  optimizerId: number
  epochs: number
  learningRate?: number
  clientsSampleRatio?: number
  topkRatio?: number
  nClusters?: number
  privacyMethod?: string
  dp?: number
}

// 训练任务接口
export interface TrainingTask {
  id: number
  taskName: string
  datasetName: string
  dataPeriod: string
  taskTypeName: string
  modelName: string
  optimizerName: string
  learningRate?: number
  totalEpochs: number
  currentEpoch: number
  status: string
  startTime?: string
  endTime?: string
  createTime: string
  updateTime: string
}

// 启动模型训练
export function startModelTraining(trainingRequest: ModelTrainingRequest) {
  return request<TrainingTask>({
    url: '/api/model-training/start',
    method: 'post',
    data: trainingRequest
  })
}



// 获取正在运行的训练任务列表
export function getRunningTasks() {
  return request<TrainingTask[]>({
    url: '/api/model-training/tasks/running',
    method: 'get'
  })
}

// 获取最近的训练任务列表
export function getRecentTasks(limit = 10) {
  return request<TrainingTask[]>({
    url: '/api/model-training/tasks/recent',
    method: 'get',
    params: { limit }
  })
}

// 终止训练任务
export function terminateTask(taskId: number) {
  return request<string>({
    url: `/api/model-training/tasks/${taskId}/terminate`,
    method: 'post'
  })
} 