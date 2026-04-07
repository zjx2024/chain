<template>
  <div class="dashboard-container">
    <div class="page-header">
      <h2 class="page-title">课题三指标成果总览</h2>
      <!-- <p class="page-subtitle">展示系统集成的课题三各项指标成果，包括数据集和模型两大核心内容</p> -->
    </div>

    <!-- 数据集部分 -->
    <el-card class="section-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <el-icon class="header-icon"><DataLine /></el-icon>
          <span class="card-title">数据集</span>
          <el-tag type="success" class="header-tag">2条产业链</el-tag>
        </div>
      </template>
      
      <div class="dataset-section">
        <el-table :data="datasetData" border style="width: 100%" class="dataset-table">
          <el-table-column prop="metric" label="指标" width="200" align="center">
            <template #default="{ row }">
              <span class="metric-label">{{ row.metric }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="integratedCircuit" label="集成电路" align="center">
            <template #default="{ row }">
              <span class="data-value">{{ row.integratedCircuit }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="electronicInfo" label="电子信息" align="center">
            <template #default="{ row }">
              <span class="data-value">{{ row.electronicInfo }}</span>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>

    <!-- 模型部分 -->
    <el-card class="section-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <el-icon class="header-icon"><Box /></el-icon>
          <span class="card-title">模型</span>
          <el-tag type="primary" class="header-tag">9个模型</el-tag>
        </div>
      </template>

      <div class="models-section">
        <!-- 完整性评估模型 -->
        <div class="model-category">
          <div class="category-header">
            <h3 class="category-title">
              <el-icon class="category-icon"><CircleCheck /></el-icon>
              完整性评估模型
            </h3>
            <div class="category-badges">
              <el-tag type="success" size="small">指标1.1</el-tag>
              <el-tag type="info" size="small">目标: 2个</el-tag>
              <el-tag type="warning" size="small">完成: 3个</el-tag>
              <el-tag type="success" size="small">超额完成</el-tag>
            </div>
          </div>
          <div class="category-description">
            基于生产网络结构和网络节点的产业链完整性评估模型
          </div>
          <div class="model-list">
            <div 
              v-for="(model, index) in integrityModels" 
              :key="index"
              class="model-item"
            >
              <div class="model-number">{{ index + 1 }}</div>
              <div class="model-name">{{ model.name }}</div>
            </div>
          </div>
        </div>

        <!-- 风险评估模型 -->
        <div class="model-category">
          <div class="category-header">
            <h3 class="category-title">
              <el-icon class="category-icon"><Warning /></el-icon>
              风险评估模型
            </h3>
            <div class="category-badges">
              <el-tag type="success" size="small">指标1.2</el-tag>
              <el-tag type="info" size="small">目标: 2个</el-tag>
              <el-tag type="warning" size="small">完成: 4个</el-tag>
              <el-tag type="success" size="small">超额完成</el-tag>
            </div>
          </div>
          <div class="category-description">
            基于状态转移矩阵的产业链风险评估模型
          </div>
          <div class="model-list">
            <div 
              v-for="(model, index) in riskAssessmentModels" 
              :key="index"
              class="model-item"
            >
              <div class="model-number">{{ index + 1 }}</div>
              <div class="model-name">{{ model.name }}</div>
            </div>
          </div>
        </div>

        <!-- 风险预警模型 -->
        <div class="model-category">
          <div class="category-header">
            <h3 class="category-title">
              <el-icon class="category-icon"><Bell /></el-icon>
              风险预警模型
            </h3>
            <div class="category-badges">
              <el-tag type="success" size="small">指标1.3</el-tag>
              <el-tag type="info" size="small">目标: 2个</el-tag>
              <el-tag type="warning" size="small">完成: 2个</el-tag>
              <el-tag type="success" size="small">已完成</el-tag>
            </div>
          </div>
          <div class="category-description">
            基于产业链状态矩阵方法的风险预警模型
          </div>
          <div class="model-list">
            <div 
              v-for="(model, index) in riskWarningModels" 
              :key="index"
              class="model-item"
            >
              <div class="model-number">{{ index + 1 }}</div>
              <div class="model-name">{{ model.name }}</div>
            </div>
          </div>
        </div>
      </div>
    </el-card>

    <!-- 统计摘要 -->
    <el-row :gutter="20" class="summary-row">
      <el-col :span="6">
        <el-card class="summary-card" shadow="hover">
          <div class="summary-content">
            <div class="summary-icon integrity">
              <el-icon><CircleCheck /></el-icon>
            </div>
            <div class="summary-info">
              <div class="summary-value">3</div>
              <div class="summary-label">完整性评估模型</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="summary-card" shadow="hover">
          <div class="summary-content">
            <div class="summary-icon risk-assessment">
              <el-icon><Warning /></el-icon>
            </div>
            <div class="summary-info">
              <div class="summary-value">4</div>
              <div class="summary-label">风险评估模型</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="summary-card" shadow="hover">
          <div class="summary-content">
            <div class="summary-icon risk-warning">
              <el-icon><Bell /></el-icon>
            </div>
            <div class="summary-info">
              <div class="summary-value">2</div>
              <div class="summary-label">风险预警模型</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="summary-card" shadow="hover">
          <div class="summary-content">
            <div class="summary-icon total">
              <el-icon><Trophy /></el-icon>
            </div>
            <div class="summary-info">
              <div class="summary-value">9</div>
              <div class="summary-label">模型总数</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { DataLine, Box, CircleCheck, Warning, Bell, Trophy } from '@element-plus/icons-vue'

// 数据集数据
const datasetData = ref([
  { metric: '公司节点 (个)', integratedCircuit: '1793', electronicInfo: '2405' },
  { metric: '产品节点 (个)', integratedCircuit: '423', electronicInfo: '910' },
  { metric: '风险因素 (项)', integratedCircuit: '18', electronicInfo: '18' },
  { metric: '产品-产品链接', integratedCircuit: '1880', electronicInfo: '2075' },
  { metric: '产品-公司链接', integratedCircuit: '3915', electronicInfo: '4141' },
  { metric: '产业链时间跨度 (季度)', integratedCircuit: '23', electronicInfo: '23' }
])

// 完整性评估模型
const integrityModels = ref([
  { name: '基于链接预测的产业链完整性评估模型' },
  { name: '融合注意力机制的多边异质嵌入与完整性评估模型' },
  { name: '基于图注意力机制和消息传递网络的产业链完整性评估模型' }
])

// 风险评估模型
const riskAssessmentModels = ref([
  { name: '基于邻居采样和图注意力机制的风险评估模型' },
  { name: '基于分层知识可转移图神经网络的风险评估模型' },
  { name: '融合图拓扑特征与注意力池化的产业链风险评估模型' },
  { name: '结合图融合和属性补全的产业链风险评估模型' }
])

// 风险预警模型
const riskWarningModels = ref([
  { name: '基于PCA-CNN的产业链风险预警模型' },
  { name: '结合层次图神经网络和LSTM的产业链风险预警模型' }
])
</script>

<style scoped lang="scss">
.dashboard-container {
  padding: 0;
  
  .page-header {
    margin-bottom: 24px;
    
    .page-title {
      font-size: 28px;
      font-weight: 600;
      color: #303133;
      margin: 0 0 8px 0;
    }
    
    .page-subtitle {
      font-size: 14px;
      color: #909399;
      margin: 0;
    }
  }
  
  .section-card {
    margin-bottom: 24px;
    
    .card-header {
      display: flex;
      align-items: center;
      gap: 12px;
      
      .header-icon {
        font-size: 20px;
        color: #409eff;
      }
      
      .card-title {
        font-size: 18px;
        font-weight: 600;
        color: #303133;
        flex: 1;
      }
      
      .header-tag {
        margin-left: auto;
      }
    }
  }
  
  .dataset-section {
    .dataset-table {
      margin-top: 16px;
      
      .metric-label {
        font-weight: 500;
        color: #606266;
      }
      
      .data-value {
        font-size: 16px;
        font-weight: 600;
        color: #303133;
      }
    }
  }
  
  .models-section {
    .model-category {
      margin-bottom: 32px;
      
      &:last-child {
        margin-bottom: 0;
      }
      
      .category-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 12px;
        flex-wrap: wrap;
        gap: 12px;
        
        .category-title {
          display: flex;
          align-items: center;
          gap: 8px;
          font-size: 18px;
          font-weight: 600;
          color: #303133;
          margin: 0;
          
          .category-icon {
            font-size: 20px;
            color: #409eff;
          }
        }
        
        .category-badges {
          display: flex;
          gap: 8px;
          flex-wrap: wrap;
        }
      }
      
      .category-description {
        font-size: 14px;
        color: #909399;
        margin-bottom: 16px;
        padding-left: 28px;
      }
      
      .model-list {
        display: flex;
        flex-direction: column;
        gap: 12px;
        
        .model-item {
          display: flex;
          align-items: center;
          padding: 16px 20px;
          background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%);
          border-radius: 8px;
          border-left: 4px solid #409eff;
          transition: all 0.3s ease;
          
          &:hover {
            transform: translateX(4px);
            box-shadow: 0 2px 12px rgba(64, 158, 255, 0.1);
          }
          
          .model-number {
            width: 32px;
            height: 32px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #409eff 0%, #66b1ff 100%);
            color: #fff;
            border-radius: 50%;
            font-weight: 600;
            font-size: 14px;
            margin-right: 16px;
            flex-shrink: 0;
          }
          
          .model-name {
            font-size: 15px;
            color: #606266;
            line-height: 1.5;
            flex: 1;
          }
        }
      }
    }
  }
  
  .summary-row {
    margin-top: 24px;
    
    .summary-card {
      height: 100%;
      
      .summary-content {
        display: flex;
        align-items: center;
        gap: 16px;
        
        .summary-icon {
          width: 56px;
          height: 56px;
          display: flex;
          align-items: center;
          justify-content: center;
          border-radius: 12px;
          font-size: 28px;
          
          &.integrity {
            background: linear-gradient(135deg, #67c23a 0%, #85ce61 100%);
            color: #fff;
          }
          
          &.risk-assessment {
            background: linear-gradient(135deg, #e6a23c 0%, #ebb563 100%);
            color: #fff;
          }
          
          &.risk-warning {
            background: linear-gradient(135deg, #f56c6c 0%, #f78989 100%);
            color: #fff;
          }
          
          &.total {
            background: linear-gradient(135deg, #409eff 0%, #66b1ff 100%);
            color: #fff;
          }
        }
        
        .summary-info {
          flex: 1;
          
          .summary-value {
            font-size: 32px;
            font-weight: 700;
            color: #303133;
            line-height: 1;
            margin-bottom: 8px;
          }
          
          .summary-label {
            font-size: 14px;
            color: #909399;
          }
        }
      }
    }
  }
}
</style> 