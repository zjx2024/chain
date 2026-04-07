import request from '@/utils/request'

// 训练后模型接口
export interface TrainedModel {
  id: number
  trainedModelName: string
  originalModelName?: string
  trainingTaskId: number
  taskTypeId?: number
  taskTypeCode?: string
  taskTypeName?: string
  modelSavePath: string
  logFileName: string
  trainingEpochs: number
  learningRate?: number
  bestEpoch?: number
  modelSize?: number
  trainingDuration?: number
  datasetName: string
  optimizerName: string
  status: string
  description?: string
  createTime: string
  updateTime: string
}

// 训练图片接口
export interface TrainingPlot {
  filename: string
  displayName: string
  url: string
  blobUrl?: string
}

// 分页查询接口
export interface PageQuery {
  current: number
  size: number
  keyword?: string
}

// 分页响应接口
export interface PageResult<T> {
  records: T[]
  total: number
  current: number
  size: number
  pages: number
}

// 分页获取可用的训练后模型
export const getActiveTrainedModels = (params: PageQuery) => {
  return request.get<PageResult<TrainedModel>>('/api/trained-models', { params })
}

// 获取所有可用的训练后模型（不分页）
export const getAllActiveTrainedModels = () => {
  return request.get<TrainedModel[]>('/api/trained-models/all')
}

// 根据ID获取训练后模型详情
export const getTrainedModelById = (id: number) => {
  return request.get<TrainedModel>(`/api/trained-models/${id}`)
}

// 获取训练过程图片列表
export const getTrainingPlots = (id: number) => {
  return request.get<TrainingPlot[]>(`/api/trained-models/${id}/training-plots`)
}

// 获取训练过程图片URL
export const getTrainingPlotUrl = (id: number, filename: string) => {
  return `/api/trained-models/${id}/training-plots/${filename}`
}

// 获取训练过程图片blob数据
export const getTrainingPlotBlob = async (id: number, filename: string): Promise<string> => {
  try {
    const response = await request.get(`/api/trained-models/${id}/training-plots/${filename}`, {
      responseType: 'blob'
    })
    
    // 创建blob URL
    const blob = response.data
    return URL.createObjectURL(blob)
  } catch (error: any) {
    console.error('获取图片blob失败:', error)
    throw error
  }
}

// 根据训练任务ID获取训练后模型
export const getTrainedModelByTaskId = (taskId: number) => {
  return request.get<TrainedModel>(`/api/trained-models/by-training-task/${taskId}`)
}

// 根据模型名称获取训练后模型
export const getTrainedModelByName = (modelName: string) => {
  return request.get<TrainedModel>(`/api/trained-models/by-name/${encodeURIComponent(modelName)}`)
}

// 归档模型
export const archiveTrainedModel = (id: number) => {
  return request.put<string>(`/api/trained-models/${id}/archive`)
}

// 删除模型
export const deleteTrainedModel = (id: number) => {
  return request.delete<string>(`/api/trained-models/${id}`)
}

// 模型测试相关接口

// 模型测试请求接口
export interface ModelTestRequest {
  trainedModelId?: number
  trainedModelName?: string
  testDatasetId?: number
  testDatasetPath?: string
  testBatchSize?: number
  device?: string
  saveResults?: boolean
  outputPath?: string
}

// 模型测试结果接口
export interface ModelTestResult {
  testTime: string
  trainedModelName: string
  testDatasetName: string
  hr10?: number
  ndcg10?: number
  testLoss?: number
  performanceComparison?: {
    hrRelativeChange?: number
    ndcgRelativeChange?: number
    hrDifference?: number
    ndcgDifference?: number
    trainingBestHr?: number
    trainingBestNdcg?: number
  }
  resultFilePath?: string
  status: string
  errorMessage?: string
  additionalInfo?: Record<string, any>
}

// 测试训练后模型
export const testTrainedModel = (testRequest: ModelTestRequest) => {
  return request.post<ModelTestResult>('/api/trained-models/test', testRequest)
}

// 异步测试训练后模型
export const testTrainedModelAsync = (testRequest: ModelTestRequest) => {
  return request.post<string>('/api/trained-models/test-async', testRequest)
}

// 验证测试环境
export const validateTestEnvironment = () => {
  return request.get<boolean>('/api/trained-models/test/validate-environment')
} 
