<template>
  <div class="models-container">
    <h2>模型管理</h2>
    
    <!-- 搜索栏 -->
    <el-card class="search-card">
      <el-row :gutter="20">
        <el-col :span="8">
          <el-input
            v-model="searchKeyword"
            placeholder="搜索模型名称、数据集或优化器..."
            :prefix-icon="SearchIcon"
            clearable
            @keyup.enter="handleSearch"
            @clear="handleSearch"
          />
        </el-col>
        <el-col :span="4">
          <el-button type="primary" @click="handleSearch" :loading="tableLoading">
            搜索
          </el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-col>
      </el-row>
    </el-card>
    
    <!-- 已完成训练的模型列表 -->
    <el-card class="models-card">
      <template #header>
        <div class="card-header">
          <span>训练完成的模型列表</span>
          <el-button type="success" size="small" @click="handleRefresh" :loading="tableLoading">
            刷新
          </el-button>
        </div>
      </template>
      
      <el-table :data="completedModels" style="width: 100%" v-loading="tableLoading">
        <el-table-column prop="id" label="序号" width="80" align="center"></el-table-column>
        <el-table-column prop="datasetName" label="数据集" width="150" show-overflow-tooltip></el-table-column>
        <el-table-column prop="trainedModelName" label="模型名称" min-width="350" show-overflow-tooltip></el-table-column>
        <el-table-column prop="optimizerName" label="优化器" width="100"></el-table-column>
        <el-table-column prop="trainingEpochs" label="训练轮次" width="100" align="center"></el-table-column>
        <el-table-column prop="learningRate" label="学习率" width="100" align="center">
          <template #default="scope">
            {{ scope.row.learningRate ? Number(scope.row.learningRate).toFixed(4) : '-' }}
          </template>
        </el-table-column>
        <el-table-column label="状态" width="80" align="center">
          <template #default="scope">
            <el-tag :type="getStatusTag(scope.row.status).type" size="small">
              {{ getStatusTag(scope.row.status).label }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="创建时间" width="180">
          <template #default="scope">
            {{ formatTime(scope.row.createTime) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" align="center" fixed="right">
          <template #default="scope">
            <div class="action-buttons">
              <el-button type="primary" size="small" @click="handleView(scope.row)">
                查看详情
              </el-button>
              <el-button 
                type="danger" 
                size="small" 
                @click="handleDelete(scope.row)"
                :loading="deleteLoading[scope.row.id]"
                :disabled="scope.row.status === 'DELETED'"
              >
                删除
              </el-button>
              <!--
              <el-button 
                type="warning" 
                size="small" 
                @click="handleTest(scope.row)"
                :disabled="scope.row.status !== 'ACTIVE'"
              >
                测试
              </el-button>
              -->
            </div>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 空状态 -->
      <el-empty 
        v-if="!tableLoading && completedModels.length === 0"
        :image-size="120"
        description="暂无训练完成的模型"
      >
        <template #image>
          <el-icon size="120" color="#e6e8eb">
            <DocumentIcon />
          </el-icon>
        </template>
        <el-button type="primary" @click="handleRefresh">
          刷新列表
        </el-button>
      </el-empty>
      
      <!-- 分页 -->
      <div v-if="total > 0" class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          background
        />
      </div>
    </el-card>

    <!-- 模型详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      :title="`模型详情 - ${currentModel?.trainedModelName || ''}`"
      width="80%"
      :close-on-click-modal="false"
    >
      <div v-if="currentModel" class="model-detail">
        <!-- 基本信息 -->
        <el-card class="detail-card">
          <template #header>
            <span class="detail-title">基本信息</span>
          </template>
          <el-row :gutter="20">
            <el-col :span="8">
              <div class="detail-item">
                <span class="label">模型名称：</span>
                <span class="value">{{ currentModel.trainedModelName }}</span>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="detail-item">
                <span class="label">数据集：</span>
                <span class="value">{{ currentModel.datasetName }}</span>
              </div>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="8">
              <div class="detail-item">
                <span class="label">优化器：</span>
                <span class="value">{{ currentModel.optimizerName }}</span>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="detail-item">
                <span class="label">训练轮次：</span>
                <span class="value">{{ currentModel.trainingEpochs }}</span>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="detail-item">
                <span class="label">学习率：</span>
                <span class="value">{{ currentModel.learningRate ? Number(currentModel.learningRate).toFixed(4) : '-' }}</span>
              </div>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="8">
              <div class="detail-item">
                <span class="label">状态：</span>
                <el-tag :type="getStatusTag(currentModel.status).type" size="small">
                  {{ getStatusTag(currentModel.status).label }}
                </el-tag>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="detail-item">
                <span class="label">创建时间：</span>
                <span class="value">{{ formatTime(currentModel.createTime) }}</span>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="detail-item">
                <span class="label">更新时间：</span>
                <span class="value">{{ formatTime(currentModel.updateTime) }}</span>
              </div>
            </el-col>
          </el-row>
        </el-card>

        <!-- 训练过程展示（MetaPath2vec/完整性评估显示评估文本，其它模型显示图片） -->
        <el-card class="detail-card">
          <template #header>
            <span class="detail-title">
              {{ usesMetricsText(currentModel) ? '评估结果' : '训练过程图片' }}
            </span>
          </template>
          <div v-if="usesMetricsText(currentModel)" class="plots-container">
            <div class="metrics-text" v-if="currentModel.description && currentModel.description.trim()">
              <pre>{{ currentModel.description }}</pre>
            </div>
            <div v-else class="no-plots">
              <el-icon><PictureFilled /></el-icon>
              <span>未捕获评估结果</span>
            </div>
          </div>
          <div v-else v-loading="plotsLoading" class="plots-container">
            <div v-if="plotsError" class="error-message">
              <el-icon><WarningFilled /></el-icon>
              <span>{{ plotsError }}</span>
            </div>
            <div v-else-if="trainingPlots.length === 0 && !plotsLoading" class="no-plots">
              <el-icon><PictureFilled /></el-icon>
              <span>该模型未保存过程数据</span>
            </div>
            <div v-else class="plots-grid">
              <div v-for="plot in trainingPlots" :key="plot.filename" class="plot-item">
                <div class="plot-title">{{ plot.displayName }}</div>
                <div class="plot-image-container">
                  <el-image
                    :src="plot.blobUrl || plot.url"
                    :alt="plot.displayName"
                    fit="contain"
                    :preview-src-list="trainingPlots.map(p => p.blobUrl || p.url)"
                    :initial-index="trainingPlots.findIndex(p => p.filename === plot.filename)"
                    class="plot-image"
                    lazy
                  >
                    <template #error>
                      <div class="image-error">
                        <el-icon><PictureFilled /></el-icon>
                        <span>加载失败</span>
                      </div>
                    </template>
                  </el-image>
                </div>
              </div>
            </div>
          </div>
        </el-card>
      </div>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="detailDialogVisible = false">关闭</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search as SearchIcon, Document as DocumentIcon, WarningFilled, PictureFilled } from '@element-plus/icons-vue'
import { getActiveTrainedModels, deleteTrainedModel, getTrainingPlots, getTrainingPlotBlob, getTrainedModelById, type TrainedModel, type PageQuery, type TrainingPlot } from '@/api/trainedModel'

// 加载状态
const tableLoading = ref(false)
const deleteLoading = reactive<Record<number, boolean>>({})
const plotsLoading = ref(false)

// 搜索关键词
const searchKeyword = ref('')

// 分页数据
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 已完成训练的模型数据
const completedModels = ref<TrainedModel[]>([])

// 详情对话框相关
const detailDialogVisible = ref(false)
const currentModel = ref<TrainedModel | null>(null)
const trainingPlots = ref<TrainingPlot[]>([])
const plotsError = ref('')

const isMetaPathModel = (model: TrainedModel | null) => {
  if (!model) return false
  return Boolean(model.description && model.description.includes('准确率'))
}

const isIntegrityEvaluationModel = (model: TrainedModel | null) => {
  if (!model) return false
  return model.taskTypeCode === 'INTEGRITY_ASSESSMENT'
}

const usesMetricsText = (model: TrainedModel | null) => {
  return isMetaPathModel(model) || isIntegrityEvaluationModel(model)
}

const shouldLoadTrainingPlots = (model: TrainedModel | null) => {
  if (!model) return false
  return !usesMetricsText(model)
}

// 搜索功能
const handleSearch = () => {
  currentPage.value = 1 // 重置到第一页
  loadModels()
}

// 重置搜索
const handleReset = () => {
  searchKeyword.value = ''
  currentPage.value = 1
  loadModels()
}

// 刷新数据
const handleRefresh = () => {
  loadModels()
}

// 查看模型详情
const handleView = async (row: TrainedModel) => {
  detailDialogVisible.value = true
  
  try {
    // 重新获取详情，确保拿到 description 等完整字段
    const { data } = await getTrainedModelById(row.id)
    currentModel.value = data
  } catch (e) {
    currentModel.value = row
  }
  
  // 部分模型不加载图片
  if (!shouldLoadTrainingPlots(currentModel.value)) {
    plotsLoading.value = false
    trainingPlots.value = []
    plotsError.value = ''
    return
  }
  
  // 加载训练过程图片
  await loadTrainingPlots(currentModel.value!.id)
}

// 加载训练过程图片
const loadTrainingPlots = async (modelId: number) => {
  try {
    plotsLoading.value = true
    plotsError.value = ''
    trainingPlots.value = []
    
    const { data } = await getTrainingPlots(modelId)
    
    // 为每个图片获取blob URL（带认证）
    const plotsWithBlobUrls = []
    for (const plot of data) {
      try {
        const blobUrl = await getTrainingPlotBlob(modelId, plot.filename)
        plotsWithBlobUrls.push({ ...plot, blobUrl })
      } catch (error) {
        console.error(`获取图片 ${plot.filename} 失败:`, error)
        plotsWithBlobUrls.push(plot)
      }
    }
    
    trainingPlots.value = plotsWithBlobUrls
    
  } catch (error: any) {
    console.error('获取训练图片失败:', error)
    if (error.response?.status === 404) {
      plotsError.value = '该模型未保存过程数据'
    } else {
      plotsError.value = '获取训练图片失败'
    }
  } finally {
    plotsLoading.value = false
  }
}

// 删除模型
const handleDelete = async (row: TrainedModel) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除模型 "${row.trainedModelName}" 吗？此操作不可恢复！`, 
      '删除确认', 
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning',
        dangerouslyUseHTMLString: false
      }
    )
    
    // 设置删除加载状态
    deleteLoading[row.id] = true
    
    try {
      await deleteTrainedModel(row.id)
      ElMessage.success('删除成功！')
      
      // 重新加载数据
      await loadModels()
    } catch (deleteError) {
      console.error('删除模型失败:', deleteError)
      ElMessage.error('删除失败，请稍后重试')
    } finally {
      deleteLoading[row.id] = false
    }
    
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('删除操作失败:', error)
    }
    // 用户取消操作时不显示消息
  }
}

// const handleTest = (row: TrainedModel) => {
//   ElMessage.info(`测试模型: ${row.trainedModelName}`)
//   // 这里可以跳转到模型测试页面
// }

// 分页处理
const handleSizeChange = (val: number) => {
  pageSize.value = val
  currentPage.value = 1 // 重置到第一页
  loadModels()
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
  loadModels()
}

// 加载模型数据
const loadModels = async () => {
  try {
    tableLoading.value = true
    
    const params: PageQuery = {
      current: currentPage.value,
      size: pageSize.value
    }
    
    // 如果有搜索关键词，添加到参数中
    if (searchKeyword.value.trim()) {
      params.keyword = searchKeyword.value.trim()
    }
    
    const { data } = await getActiveTrainedModels(params)
    completedModels.value = data.records
    total.value = data.total
    
    console.log('获取训练完成模型列表:', data)
  } catch (error) {
    console.error('获取模型数据失败:', error)
    ElMessage.error('获取模型数据失败')
  } finally {
    tableLoading.value = false
  }
}

// 格式化时间
const formatTime = (timeString: string) => {
  if (!timeString) return '-'
  const date = new Date(timeString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

// 获取状态标签样式
const getStatusTag = (status: string) => {
  switch (status) {
    case 'ACTIVE':
      return { label: '可用', type: 'success' }
    case 'ARCHIVED':
      return { label: '已归档', type: 'warning' }
    case 'DELETED':
      return { label: '已删除', type: 'danger' }
    default:
      return { label: '未知', type: 'info' }
  }
}

// 清理blob URL
const cleanupBlobUrls = () => {
  trainingPlots.value.forEach(plot => {
    if (plot.blobUrl) {
      URL.revokeObjectURL(plot.blobUrl)
    }
  })
}

onMounted(() => {
  loadModels()
})

onUnmounted(() => {
  cleanupBlobUrls()
})
</script>

<style scoped lang="scss">
.models-container {
  h2 {
    margin-bottom: 20px;
    color: #303133;
  }
  
  .search-card {
    margin-bottom: 20px;
    
    .el-row {
      display: flex;
      align-items: center;
    }
  }
  
  .models-card {
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      
      span {
        font-size: 16px;
        font-weight: 500;
        color: #303133;
      }
    }
    
    .pagination-container {
      display: flex;
      justify-content: center;
      margin-top: 20px;
    }
  }
  
  .action-buttons {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    flex-wrap: wrap;
    
    .el-button {
      margin: 0;
      flex-shrink: 0;
      min-width: 60px;
      
      &.is-disabled {
        opacity: 0.5;
      }
    }
  }
  
  // 模型详情对话框样式
  .model-detail {
    .detail-card {
      margin-bottom: 20px;
      
      &:last-child {
        margin-bottom: 0;
      }
      
      .detail-title {
        font-size: 16px;
        font-weight: 500;
        color: #303133;
      }
      
      .detail-item {
        display: flex;
        align-items: center;
        margin-bottom: 12px;
        
        .label {
          font-weight: 500;
          color: #606266;
          min-width: 80px;
        }
        
        .value {
          color: #303133;
          word-break: break-all;
        }
      }
    }
    
    .plots-container {
      min-height: 200px;
      
      .error-message, .no-plots {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 200px;
        color: #909399;
        
        .el-icon {
          font-size: 48px;
          margin-bottom: 12px;
        }
        
        span {
          font-size: 14px;
        }
      }
      
      .plots-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 20px;
        
        .plot-item {
          border: 1px solid #e4e7ed;
          border-radius: 8px;
          overflow: hidden;
          
          .plot-title {
            padding: 12px 16px;
            background-color: #f5f7fa;
            font-weight: 500;
            color: #303133;
            text-align: center;
            border-bottom: 1px solid #e4e7ed;
          }
          
          .plot-image-container {
            padding: 16px;
            
            .plot-image {
              width: 100%;
              height: 250px;
              border-radius: 4px;
              
              .image-error {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100%;
                color: #c0c4cc;
                
                .el-icon {
                  font-size: 48px;
                  margin-bottom: 8px;
                }
                
                span {
                  font-size: 14px;
                }
              }
            }
          }
        }
      }
    }
  }
  
  :deep(.el-table) {
    .el-button {
      vertical-align: middle;
      display: inline-flex;
      align-items: center;
      justify-content: center;
    }
    
    .el-table__cell {
      vertical-align: middle;
    }
    
    .el-tag {
      margin: 0;
    }
  }
  
  // 分页组件样式
  :deep(.el-pagination) {
    .el-pagination__sizes,
    .el-pagination__total,
    .el-pagination__jump {
      color: #606266;
    }
    
    .el-pager li {
      &.is-active {
        color: #409eff;
        background-color: #f0f9ff;
      }
    }
  }
  
  // 对话框样式
  :deep(.el-dialog) {
    .el-dialog__header {
      padding: 20px 20px 10px;
      border-bottom: 1px solid #e4e7ed;
      
      .el-dialog__title {
        font-size: 18px;
        font-weight: 600;
        color: #303133;
      }
    }
    
    .el-dialog__body {
      padding: 20px;
      max-height: 70vh;
      overflow-y: auto;
    }
    
    .el-dialog__footer {
      padding: 10px 20px 20px;
      border-top: 1px solid #e4e7ed;
    }
  }
  
  // 响应式设计
  @media (max-width: 1200px) {
    .action-buttons {
      gap: 4px;
      
      .el-button {
        min-width: 50px;
        font-size: 12px;
        padding: 4px 8px;
      }
    }
    
    .plots-grid {
      grid-template-columns: 1fr;
    }
  }
  
  @media (max-width: 768px) {
    :deep(.el-dialog) {
      width: 95% !important;
      margin: 0 auto;
    }
    
    .model-detail {
      .detail-item {
        flex-direction: column;
        align-items: flex-start;
        
        .label {
          min-width: auto;
          margin-bottom: 4px;
        }
      }
    }
  }
}
</style> 
