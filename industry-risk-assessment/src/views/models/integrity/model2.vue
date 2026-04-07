<template>
  <div class="integrity-model2-container">
    <h2>{{ modelInfo.title }}</h2>
    
    <!-- 模型概述 -->
    <el-card class="overview-card">
      <template #header>
        <div class="card-header">
          <span>模型概述</span>
        </div>
      </template>
      <div class="model-intro">
        <p class="model-description">
          {{ modelInfo.description }}
        </p>
      </div>
    </el-card>

    <!-- 模型架构 -->
    <el-card class="architecture-card">
      <template #header>
        <div class="card-header">
          <span>模型架构</span>
        </div>
      </template>
      <div class="architecture-content">
        <div class="architecture-image">
          <img 
            src="/images/models/integrity/model2-architecture.png" 
            alt="模型四模块流程图"
            class="architecture-img"
            @error="handleImageError"
          />
        </div>
        
        <div class="modules-grid">
          <div 
            v-for="module in modelInfo.modules" 
            :key="module.name"
            class="module-item"
          >
            <div class="module-header">
              <el-icon><Setting /></el-icon>
              <span>{{ module.name }}</span>
            </div>
            <p class="module-description">{{ module.description }}</p>
          </div>
        </div>
      </div>
    </el-card>

    <!-- 核心参数定义 -->
    <el-card class="parameters-card">
      <template #header>
        <div class="card-header">
          <span>模型核心参数定义</span>
        </div>
      </template>
      <div class="parameters-content">
        <div class="parameter-section">
          <h4><el-icon><Connection /></el-icon>节点对与成对编码</h4>
          <p>{{ modelInfo.parameters.nodePairEncoding }}</p>
        </div>
        
        <div class="parameter-section">
          <h4><el-icon><TrendCharts /></el-icon>PPR 分数</h4>
          <p>{{ modelInfo.parameters.pprScore }}</p>
        </div>
        
        <div class="parameter-section">
          <h4><el-icon><Coordinate /></el-icon>相对位置编码（RPE）</h4>
          <p>{{ modelInfo.parameters.rpe }}</p>
        </div>
      </div>
    </el-card>

    <!-- 关键技术路径 -->
    <el-card class="tech-path-card">
      <template #header>
        <div class="card-header">
          <span>核心技术组件</span>
        </div>
      </template>
      <div class="tech-path-content">
        <div 
          v-for="(component, index) in modelInfo.techComponents" 
          :key="component.title"
          class="path-section"
        >
          <div class="path-header">
            <div class="path-number">{{ index + 1 }}</div>
            <h4>{{ component.title }}</h4>
          </div>
          <div class="path-details">
            <div 
              v-for="detail in component.details" 
              :key="detail"
              class="path-detail-item"
            >
              <el-icon class="detail-icon"><ArrowRight /></el-icon>
              <span>{{ detail }}</span>
            </div>
          </div>
        </div>
      </div>
    </el-card>

    <!-- 完整性评估指标 -->
    <el-card class="metrics-card">
      <template #header>
        <div class="card-header">
          <span>完整性评估指标</span>
        </div>
      </template>
      <div class="metrics-grid">
        <div 
          v-for="metric in modelInfo.metrics" 
          :key="metric.name"
          class="metric-item"
        >
          <div class="metric-header">
            <el-icon class="metric-icon" :class="metric.iconClass">
              <component :is="metric.icon" />
            </el-icon>
            <div class="metric-info">
              <h5>{{ metric.name }}</h5>
              <span class="metric-code">{{ metric.code }}</span>
            </div>
          </div>
          <p class="metric-description">{{ metric.description }}</p>
          <div class="metric-formula">
            <span class="formula-label">公式：</span>
            <code>{{ metric.formula }}</code>
          </div>
        </div>
      </div>
    </el-card>

    <!-- 链接预测与评估流程 -->
    <el-card class="optimization-card">
      <template #header>
        <div class="card-header">
          <span>链接预测与评估流程</span>
        </div>
      </template>
      <div class="optimization-content">
        <div class="optimization-section">
          <h4>
            <el-icon><DataBoard /></el-icon>
            得分函数
          </h4>
          <p>{{ modelInfo.prediction.scoreFunction.description }}</p>
          <div class="formula-box">
            <code>{{ modelInfo.prediction.scoreFunction.formula }}</code>
          </div>
        </div>
        
        <div class="optimization-section">
          <h4>
            <el-icon><Monitor /></el-icon>
            评估流程
          </h4>
          <p>{{ modelInfo.prediction.evaluationProcess.description }}</p>
          <div class="process-steps">
            <div 
              v-for="(step, index) in modelInfo.prediction.evaluationProcess.steps"
              :key="index"
              class="process-step"
            >
              <span class="step-number">{{ index + 1 }}</span>
              <span class="step-text">{{ step }}</span>
            </div>
          </div>
        </div>
      </div>
    </el-card>

    <!-- 技术特点 -->
    <el-card class="features-card">
      <template #header>
        <div class="card-header">
          <span>技术特点</span>
        </div>
      </template>
      <div class="features-grid">
        <div 
          v-for="feature in modelInfo.features" 
          :key="feature.title"
          class="feature-item"
        >
          <el-icon class="feature-icon" :class="feature.iconClass">
            <component :is="feature.icon" />
          </el-icon>
          <h5>{{ feature.title }}</h5>
          <p>{{ feature.description }}</p>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import { 
  Setting, 
  DataBoard, 
  Connection, 
  TrendCharts,
  Coordinate,
  Monitor,
  ArrowRight,
  RefreshRight,
  Star,
  CircleCheck,
  Share,
  MagicStick
} from '@element-plus/icons-vue'

// 图片加载错误处理
const handleImageError = (event: Event) => {
  const img = event.target as HTMLImageElement
  img.style.display = 'none'
}

// 模型信息配置
const modelInfo = reactive({
  title: '基于图注意力与消息传递网络的产业链完整性评估模型',
  description: '本模型结合图注意力机制与消息传递网络，通过四模块协同设计实现产业链完整性的精准评估。模型采用图神经网络提取节点特征，利用PPR分数筛选关键节点，结合相对位置编码生成成对关系特征，最终实现高效的链接预测和完整性评估。',
  
  modules: [
    {
      name: '节点特征编码',
      description: '采用图卷积网络（GCN）提取包含邻居信息的节点特征，通过邻接矩阵归一化和图卷积操作捕获局部结构信息。'
    },
    {
      name: '候选节点筛选', 
      description: '基于个性化PageRank（PPR）分数筛选对目标链接重要的节点，包括共同邻居、1跳邻居和多跳邻居。'
    },
    {
      name: '成对编码生成',
      description: '结合图注意力机制与相对位置编码（RPE），通过注意力权重计算生成节点对的关系特征向量。'
    },
    {
      name: '评估模块',
      description: '基于成对编码预测链接存在概率，并通过预测链接全图计算RT/RL指标，输出完整性得分IT。'
    }
  ],
  
  parameters: {
    nodePairEncoding: '节点对(u,v)分为直接/间接相连，成对编码通过MLP网络捕捉节点间的关系特征，融合节点特征与边特征信息。',
    pprScore: '基于随机游走计算节点相对重要性，通过迭代传播方式衡量节点间的结构关联强度，用于候选节点筛选。',
    rpe: '利用PPR分数参数化节点与目标链接的相对位置关系，通过MLP网络编码位置信息，避免节点顺序敏感性问题。'
  },
  
  techComponents: [
    {
      title: '节点特征提取（GCN）',
      details: [
        '通过邻接矩阵归一化处理，确保特征传播的稳定性',
        '多层图卷积操作捕获不同尺度的邻域结构信息'
      ]
    },
    {
      title: '候选节点筛选',
      details: [
        '基于PPR分数阈值筛选对目标链接重要的候选节点',
        '包括共同邻居、1跳邻居和多跳邻居等多类型节点筛选'
      ]
    },
    {
      title: '成对编码与注意力机制',
      details: [
        '通过GATv2注意力机制计算动态权重，融合节点特征与位置编码',
        '聚合多种邻居信息生成节点对的关系特征表示'
      ]
    }
  ],

  metrics: [
    {
      name: '抵抗能力',
      code: 'RT',
      description: '企业连接密度指标，通过计算企业间连接数量评估产业链结构稳定性。连接密度越高，产业链抵御外部冲击的能力越强。',
      formula: 'RT = ∑zᵢⱼ/n （zᵢⱼ为邻接矩阵元素）',
      icon: CircleCheck,
      iconClass: 'red-icon'
    },
    {
      name: '恢复能力',
      code: 'RL',
      description: '潜在关系发现能力，评估产业链识别和利用隐藏连接的潜力。比值越高说明信息透明度越好，恢复能力越强。',
      formula: 'RL = |R|/(|R| + |R\'|)',
      icon: RefreshRight,
      iconClass: 'blue-icon'
    },
    {
      name: '完整性得分',
      code: 'IT',
      description: '综合评估指标，通过抵抗能力和恢复能力的均值计算。该指标全面反映产业链的健康程度和稳健性水平。',
      formula: 'IT = (RT + RL)/2，得分越高完整性越强',
      icon: Star,
      iconClass: 'gold-icon'
    }
  ],

  prediction: {
    scoreFunction: {
      description: '结合节点对特征与邻域结构信息，通过MLP计算链接存在概率',
      formula: 'p(a,b) = σ(MLP(hₐ ⊙ hᵦ || s(a,b) || N^CN || N^1 || N^-1))'
    },
    evaluationProcess: {
      description: '预测链接→全图计算→输出IT评估流程',
      steps: [
        '对候选节点对计算链接概率',
        '基于概率阈值确定预测链接',
        '在增强图上计算RT和RL指标',
        '输出综合完整性得分IT'
      ]
    }
  },

  features: [
    {
      title: '图注意力机制',
      description: '动态聚合邻居信息，自适应学习节点重要性权重',
      icon: Setting,
      iconClass: 'blue-icon'
    },
    {
      title: '消息传递网络',
      description: '高效的图神经网络框架，支持多层信息传播',
      icon: Share,
      iconClass: 'green-icon'
    },
    {
      title: 'PPR候选筛选',
      description: '基于随机游走的智能节点筛选，提升计算效率',
      icon: TrendCharts,
      iconClass: 'purple-icon'
    },
    {
      title: '相对位置编码',
      description: '避免节点顺序敏感性，增强模型泛化能力',
      icon: MagicStick,
      iconClass: 'orange-icon'
    }
  ]
})
</script>

<style scoped lang="scss">
.integrity-model2-container {
  .card-header {
    font-size: 16px;
    font-weight: 600;
    color: #303133;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .overview-card {
    margin-bottom: 20px;
    
    .model-intro {
      .model-description {
        font-size: 14px;
        line-height: 1.8;
        color: #606266;
        margin: 0;
        text-align: justify;
      }
    }
  }

  .architecture-card {
    margin-bottom: 20px;
    
    .architecture-content {
      .architecture-image {
        margin-bottom: 30px;
        text-align: center;
        
        .architecture-img {
          max-width: 100%;
          height: auto;
          border-radius: 8px;
          box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
        }
        
        .diagram-caption {
          margin-top: 12px;
          color: #909399;
          font-size: 14px;
          font-style: italic;
        }
      }
      
      .modules-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 20px;
        
        .module-item {
          border: 1px solid #e4e7ed;
          border-radius: 8px;
          padding: 20px;
          background-color: #fafbfc;
          transition: all 0.3s ease;
          
          &:hover {
            border-color: #409eff;
            box-shadow: 0 2px 12px 0 rgba(64, 158, 255, 0.1);
          }
          
          .module-header {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 12px;
            font-weight: 600;
            color: #303133;
            
            .el-icon {
              color: #409eff;
            }
          }
          
          .module-description {
            font-size: 13px;
            line-height: 1.6;
            color: #606266;
            margin: 0;
          }
        }
      }
    }
  }

  .parameters-card {
    margin-bottom: 20px;
    
    .parameters-content {
      .parameter-section {
        margin-bottom: 25px;
        
        &:last-child {
          margin-bottom: 0;
        }
        
        h4 {
          display: flex;
          align-items: center;
          gap: 8px;
          margin: 0 0 12px 0;
          font-size: 15px;
          font-weight: 600;
          color: #303133;
          
          .el-icon {
            color: #67c23a;
          }
        }
        
        p {
          font-size: 14px;
          line-height: 1.7;
          color: #606266;
          margin: 0 0 15px 0;
          text-align: justify;
        }
      }
    }
  }

  .tech-path-card {
    margin-bottom: 20px;
    
    .tech-path-content {
      .path-section {
        margin-bottom: 25px;
        
        &:last-child {
          margin-bottom: 0;
        }
        
        .path-header {
          display: flex;
          align-items: center;
          gap: 15px;
          margin-bottom: 15px;
          
          .path-number {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background: linear-gradient(135deg, #409eff, #66b1ff);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 600;
            font-size: 14px;
            flex-shrink: 0;
          }
          
          h4 {
            margin: 0;
            font-size: 16px;
            font-weight: 600;
            color: #303133;
          }
        }
        
        .path-details {
          padding-left: 47px;
          
          .path-detail-item {
            display: flex;
            align-items: flex-start;
            gap: 10px;
            margin-bottom: 8px;
            
            &:last-child {
              margin-bottom: 0;
            }
            
            .detail-icon {
              color: #409eff;
              margin-top: 2px;
              flex-shrink: 0;
            }
            
            span {
              font-size: 14px;
              line-height: 1.6;
              color: #606266;
            }
          }
        }
      }
    }
  }

  .metrics-card {
    margin-bottom: 20px;
    
    .metrics-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 20px;
      
      .metric-item {
        border: 1px solid #e4e7ed;
        border-radius: 8px;
        padding: 20px;
        background: #fafbfc;
        transition: all 0.3s ease;
        
        &:hover {
          border-color: #409eff;
          box-shadow: 0 2px 12px 0 rgba(64, 158, 255, 0.1);
        }
        
        .metric-header {
          display: flex;
          align-items: center;
          gap: 12px;
          margin-bottom: 12px;
          
          .metric-icon {
            font-size: 24px;
            
            &.red-icon { color: #f56c6c; }
            &.blue-icon { color: #409eff; }
            &.gold-icon { color: #e6a23c; }
          }
          
          .metric-info {
            h5 {
              margin: 0 0 4px 0;
              font-size: 16px;
              font-weight: 600;
              color: #303133;
            }
            
            .metric-code {
              background: #e1f3d8;
              color: #67c23a;
              padding: 2px 8px;
              border-radius: 4px;
              font-size: 12px;
              font-weight: 600;
            }
          }
        }
        
        .metric-description {
          font-size: 13px;
          line-height: 1.6;
          color: #606266;
          margin: 0 0 15px 0;
        }
        
        .metric-formula {
          display: flex;
          align-items: center;
          gap: 8px;
          flex-wrap: wrap;
          
          .formula-label {
            font-size: 13px;
            color: #909399;
            font-weight: 500;
          }
          
          code {
            background: #f4f4f5;
            border: 1px solid #e9e9eb;
            border-radius: 4px;
            padding: 4px 8px;
            font-size: 13px;
            color: #e6a23c;
            font-family: 'Courier New', monospace;
          }
        }
      }
    }
  }

  .optimization-card {
    margin-bottom: 20px;
    
    .optimization-content {
      .optimization-section {
        margin-bottom: 25px;
        
        &:last-child {
          margin-bottom: 0;
        }
        
        h4 {
          display: flex;
          align-items: center;
          gap: 8px;
          margin: 0 0 12px 0;
          font-size: 16px;
          font-weight: 600;
          color: #303133;
          
          .el-icon {
            color: #409eff;
          }
        }
        
        p {
          font-size: 14px;
          line-height: 1.7;
          color: #606266;
          margin: 0 0 12px 0;
        }
        
        .formula-box {
          background: #f8f9fa;
          border: 1px solid #e9ecef;
          border-radius: 6px;
          padding: 12px 16px;
          display: flex;
          align-items: center;
          gap: 10px;
          
          code {
            background: #fff;
            border: 1px solid #dee2e6;
            border-radius: 4px;
            padding: 6px 12px;
            font-size: 14px;
            color: #495057;
            font-family: 'Courier New', monospace;
            font-weight: 500;
          }
        }
        
        .process-steps {
          .process-step {
            display: flex;
            align-items: center;
            margin-bottom: 12px;
            
            &:last-child {
              margin-bottom: 0;
            }
            
            .step-number {
              width: 24px;
              height: 24px;
              background: #409EFF;
              color: white;
              border-radius: 50%;
              display: flex;
              align-items: center;
              justify-content: center;
              font-size: 12px;
              font-weight: bold;
              margin-right: 12px;
              flex-shrink: 0;
            }
            
            .step-text {
              color: #606266;
              line-height: 1.6;
              font-size: 14px;
            }
          }
        }
      }
    }
  }

  .features-card {
    .features-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 20px;
      
      .feature-item {
        text-align: center;
        padding: 20px;
        border-radius: 8px;
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        border: 1px solid #f0f0f0;
        transition: all 0.3s ease;
        
        &:hover {
          transform: translateY(-2px);
          box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.1);
        }
        
        .feature-icon {
          font-size: 32px;
          margin-bottom: 15px;
          
          &.blue-icon { color: #409eff; }
          &.green-icon { color: #67c23a; }
          &.purple-icon { color: #9c27b0; }
          &.orange-icon { color: #ff9800; }
        }
        
        h5 {
          margin: 0 0 10px 0;
          font-size: 16px;
          font-weight: 600;
          color: #303133;
        }
        
        p {
          margin: 0;
          font-size: 13px;
          line-height: 1.5;
          color: #606266;
        }
      }
    }
  }

  // 响应式设计
  @media (max-width: 768px) {
    .modules-grid,
    .features-grid {
      grid-template-columns: 1fr;
    }
  }
}
</style> 