<template>
  <div class="integrity-model1-container">
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
            src="/images/models/integrity/model1-architecture.png" 
            alt="模型架构图"
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
          <h4><el-icon><DataBoard /></el-icon>知识图谱基础</h4>
          <p>{{ modelInfo.parameters.knowledgeGraph }}</p>
        </div>
        
        <div class="parameter-section">
          <h4><el-icon><Connection /></el-icon>元路径</h4>
          <p>{{ modelInfo.parameters.metaPath }}</p>
        </div>
        
        <div class="parameter-section">
          <h4><el-icon><Share /></el-icon>隐性异构图</h4>
          <p>{{ modelInfo.parameters.implicitGraph }}</p>
          <div class="graph-image">
            <img 
              src="/images/models/integrity/model1-implicit-graph.png" 
              alt="隐性异构图示例"
              class="graph-img"
              @error="handleImageError"
            />
          </div>
        </div>
      </div>
    </el-card>

    <!-- 关键技术路径 -->
    <el-card class="tech-path-card">
      <template #header>
        <div class="card-header">
          <span>关键技术路径</span>
        </div>
      </template>
      <div class="tech-path-content">
        <div 
          v-for="(path, index) in modelInfo.techPaths" 
          :key="path.title"
          class="path-section"
        >
          <div class="path-header">
            <div class="path-number">{{ index + 1 }}</div>
            <h4>{{ path.title }}</h4>
          </div>
          <div class="path-details">
            <div 
              v-for="detail in path.details" 
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

    <!-- 优化目标与链接预测 -->
    <el-card class="optimization-card">
      <template #header>
        <div class="card-header">
          <span>优化目标与链接预测</span>
        </div>
      </template>
      <div class="optimization-content">
        <div class="optimization-section">
          <h4>
            <el-icon><TrendCharts /></el-icon>
            损失函数
          </h4>
          <p>{{ modelInfo.optimization.lossFunction.description }}</p>
          <div class="formula-box">
            <code>{{ modelInfo.optimization.lossFunction.formula }}</code>
          </div>
        </div>
        
        <div class="optimization-section">
          <h4>
            <el-icon><Connection /></el-icon>
            链接预测
          </h4>
          <p>{{ modelInfo.optimization.linkPrediction.description }}</p>
          <div class="formula-box">
            <code>{{ modelInfo.optimization.linkPrediction.formula }}</code>
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
  Share,
  TrendCharts,
  Coordinate,
  MagicStick,
  Monitor,
  ArrowRight,
  RefreshRight,
  Star,
  CircleCheck
} from '@element-plus/icons-vue'

// 图片加载错误处理
const handleImageError = (event: Event) => {
  const img = event.target as HTMLImageElement
  img.style.display = 'none'
  // 可以在这里显示占位符或错误提示
}

// 模型信息配置
const modelInfo = reactive({
  title: '基于链接预测的产业链完整性评估模型',
  description: '本模型基于链接预测技术，通过构建产业链异构图谱，实现对产业链完整性的量化评估。模型采用多模块协同工作的架构设计，能够有效识别产业链中的潜在风险点和薄弱环节。',
  
  modules: [
    {
      name: '路径编码模块',
      description: '通过随机游走生成路径，编码隐藏语义嵌入，捕获节点间的深层关联关系。'
    },
    {
      name: '语义编码模块', 
      description: '从节点主嵌入中提取类型相关语义信息，增强模型对不同实体类型的理解能力。'
    },
    {
      name: '上下文调节模块',
      description: '基于路径语义区分不同上下文节点的异构信息，提高模型的泛化能力。'
    },
    {
      name: '完整性评估模块',
      description: '聚合嵌入后预测链接，量化产业链完整性，输出可解释的评估结果。'
    }
  ],
  
  parameters: {
    knowledgeGraph: '以三元组（实体 - 关系 - 实体）构建产业链异构图，包含节点类型（企业、产品等）和关系类型（生产、供应等），为模型提供结构化的知识表示基础。',
    metaPath: '如"产品 - 供应商 - 产品（PSP）"，捕捉节点间复合语义关系，不同路径对应不同产业链逻辑（如合作/竞争），是模型理解产业链复杂关系的关键。',
    implicitGraph: '节点和关系类型缺失的产业链网络，需通过特征推理隐藏语义。模型能够在信息不完整的情况下，推断出潜在的产业链结构和关系。'
  },
  
  techPaths: [
    {
      title: '基于随机游走的路径编码',
      details: [
        '从目标节点出发采样多条路径，截断为不同长度以捕捉多尺度语义',
        '路径编码器通过节点嵌入均值生成路径语义向量'
      ]
    },
    {
      title: '表示学习的语义编码',
      details: [
        '主嵌入（捕捉结构信息）+ 语义嵌入（提炼隐藏类型语义）',
        '通过全连接层实现语义特征提取'
      ]
    },
    {
      title: '节点上下文聚合',
      details: [
        '基于路径语义调节上下文节点信息，通过缩放向量 γ 和移位向量 β 差异化处理',
        '加权聚合短路径优先，生成目标节点主嵌入'
      ]
    }
  ],

  metrics: [
    {
      name: '产业链抵抗能力度量',
      code: 'RT(C)',
      description: '衡量产业链在面对外部冲击时的结构稳定性。其中 zᵢⱼ 表示企业i与企业j之间的连接关系（存在连接为1，不存在为0），n 表示产业链中企业总数。该指标计算所有企业对之间连接数的总和，再除以企业总数得到平均连接密度。连接密度越高，表明产业链内部联系越紧密，在面对供应链中断等外部冲击时的抵抗能力越强。',
      formula: 'RT(C) = (Σᵢ₌₀ⁿ⁻¹ Σⱼ₌₀ⁿ⁻¹ zᵢⱼ) / n',
      icon: CircleCheck,
      iconClass: 'red-icon'
    },
    {
      name: '产业链恢复能力度量',
      code: 'RL(C)',
      description: '评估产业链信息透明度和潜在关系发现能力。针对产业链C = (Z,R)，R 表示已知的显性关系集合，R\' = {rₘ₊₁, rₘ₊₂, ⋯, rₘ₊ₖ} 表示企业间可能存在的隐性关系集合。该指标计算已知关系数量与总关系数量（已知关系+潜在关系）的比值。比值越高说明产业链的信息透明度越好，隐藏关系越少，在遭受冲击后的恢复能力越强。',
      formula: 'RL(C) = R / (|R| + |R\'|)',
      icon: RefreshRight,
      iconClass: 'blue-icon'
    },
    {
      name: '产业链的完整性得分',
      code: 'IT(C)',
      description: '综合评估产业链的整体稳健性，通过抵抗能力和恢复能力的算术平均值计算得出。该指标既考虑了产业链的结构稳定性（抵抗能力），又考虑了信息透明度（恢复能力），能够全面反映产业链的完整性水平。分值越高表明产业链越健康稳定，既能有效抵御外部冲击，又具备良好的自我修复能力。',
      formula: 'IT(C) = (RT(C) + RL(C)) / 2',
      icon: Star,
      iconClass: 'gold-icon'
    }
  ],

  optimization: {
    lossFunction: {
      description: '采用平移误差损失和正则化惩罚项的组合，确保模型训练的稳定性和泛化能力',
      formula: 'L = L1 + L2'
    },
    linkPrediction: {
      description: '通过编码器生成节点对语义嵌入，评估隐藏关系存在概率，实现链接预测功能',
      formula: 'P(link) = σ(encoder(u, v))'
    }
  },

  features: [
    {
      title: '多模块协同',
      description: '四个核心模块协同工作，实现端到端的完整性评估',
      icon: TrendCharts,
      iconClass: 'blue-icon'
    },
    {
      title: '异构图建模',
      description: '支持多类型节点和关系的复杂产业链结构建模',
      icon: Coordinate,
      iconClass: 'green-icon'
    },
    {
      title: '语义增强',
      description: '通过元路径捕获深层语义，提升模型理解能力',
      icon: MagicStick,
      iconClass: 'purple-icon'
    },
    {
      title: '可解释性',
      description: '提供清晰的评估过程和结果解释，增强模型可信度',
      icon: Monitor,
      iconClass: 'orange-icon'
    }
  ]
})
</script>

<style scoped lang="scss">
.integrity-model1-container {
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
        
        .image-placeholder {
          border: 2px dashed #dcdfe6;
          border-radius: 8px;
          padding: 40px;
          background-color: #fafafa;
          color: #909399;
          
          .el-icon {
            margin-bottom: 10px;
            color: #c0c4cc;
          }
          
          p {
            margin: 5px 0;
            font-size: 14px;
            
            &.image-note {
              font-size: 12px;
              color: #c0c4cc;
            }
          }
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
        
        .graph-image {
          text-align: center;
          
          .graph-img {
            max-width: 100%;
            height: auto;
            border-radius: 6px;
            border: 1px solid #e4e7ed;
          }
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
          
          .formula-ref {
            font-size: 12px;
            color: #c0c4cc;
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
          
          .formula-ref {
            font-size: 12px;
            color: #6c757d;
            margin-left: auto;
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
