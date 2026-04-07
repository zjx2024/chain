<template>
  <div class="risk-assessment-model1-container">
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
            src="/images/models/risk-assessment/model1-architecture.png" 
            alt="GANS模型总体架构"
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

    <!-- 问题定义与设计目标 -->
    <el-card class="problem-card">
      <template #header>
        <div class="card-header">
          <span>问题定义与设计目标</span>
        </div>
      </template>
      <div class="problem-content">
        <div class="problem-section">
          <h4><el-icon><DataBoard /></el-icon>产业链风险评估定义</h4>
          <p>{{ modelInfo.problemDefinition.riskDefinition }}</p>
          <div class="risk-labels">
            <div class="label-item">
              <span class="label-type">节点风险标签：</span>
              <span class="label-content">二元（安全/危险）</span>
            </div>
            <div class="label-item">
              <span class="label-type">产业链风险标签：</span>
              <span class="label-content">三元（低/中/高风险）</span>
            </div>
          </div>
        </div>
        
        <div class="problem-section">
          <h4><el-icon><TrendCharts /></el-icon>设计目标</h4>
          <div class="design-goals">
            <div 
              v-for="(goal, index) in modelInfo.problemDefinition.designGoals" 
              :key="index"
              class="goal-item"
            >
              <span class="goal-number">{{ index + 1 }}</span>
              <span class="goal-text">{{ goal }}</span>
            </div>
          </div>
        </div>
      </div>
    </el-card>

    <!-- 核心技术组件 -->
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

    <!-- 风险评估指标 -->
    <el-card class="metrics-card">
      <template #header>
        <div class="card-header">
          <span>风险评估指标</span>
        </div>
      </template>
      <div class="metrics-grid">
        <div 
          v-for="metric in modelInfo.riskMetrics" 
          :key="metric.name"
          class="metric-item"
        >
          <div class="metric-header">
            <el-icon class="metric-icon" :class="metric.iconClass">
              <component :is="metric.icon" />
            </el-icon>
            <div class="metric-info">
              <h5>{{ metric.name }}</h5>
              <span class="metric-code">{{ metric.level }}</span>
            </div>
          </div>
          <p class="metric-description">{{ metric.description }}</p>
          <div class="metric-features">
            <span 
              v-for="feature in metric.features"
              :key="feature"
              class="feature-tag"
            >
              {{ feature }}
            </span>
          </div>
        </div>
      </div>
    </el-card>

    <!-- 算法流程与优化 -->
    <el-card class="optimization-card">
      <template #header>
        <div class="card-header">
          <span>算法流程与优化</span>
        </div>
      </template>
      <div class="optimization-content">
        <div class="optimization-section">
          <h4>
            <el-icon><Monitor /></el-icon>
            损失函数
          </h4>
          <p>{{ modelInfo.algorithm.lossFunction.description }}</p>
          <div class="loss-functions">
            <div class="loss-item">
              <span class="loss-label">节点风险：</span>
              <code>{{ modelInfo.algorithm.lossFunction.nodeLoss }}</code>
            </div>
            <div class="loss-item">
              <span class="loss-label">产业链风险：</span>
              <code>{{ modelInfo.algorithm.lossFunction.chainLoss }}</code>
            </div>
          </div>
        </div>
        
        <div class="optimization-section">
          <h4>
            <el-icon><Connection /></el-icon>
            关键算法步骤
          </h4>
          <div class="algorithm-steps">
            <div 
              v-for="(step, index) in modelInfo.algorithm.keySteps"
              :key="index"
              class="algorithm-step"
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
  Monitor,
  ArrowRight,
  Warning,
  CircleCheck,
  Bell,
  Share,
  MagicStick,
  Coordinate
} from '@element-plus/icons-vue'

// 图片加载错误处理
const handleImageError = (event: Event) => {
  const img = event.target as HTMLImageElement
  img.style.display = 'none'
}

// 模型信息配置
const modelInfo = reactive({
  title: '基于邻居采样和图注意力机制的风险评估模型',
  description: '本模型通过异质图建模产业链网络，结合邻居采样和图注意力机制实现多层级风险评估。模型采用四模块协同设计，从异质图构建到节点风险分类，再到产业链风险等级评估，实现了从微观节点到宏观网络的全方位风险识别与预警。',
  
  modules: [
    {
      name: '异质图构建',
      description: '融合产品-公司关系与财务属性信息，构建包含多类型节点和边关系的异质图网络结构。'
    },
    {
      name: '公司图生成', 
      description: '基于元路径和投融资关系，构建刻画供应、竞争、投资关系的公司关联图谱。'
    },
    {
      name: '节点风险评估',
      description: '采用邻域采样和图注意力机制，实现公司节点的二元风险分类（安全/危险）。'
    },
    {
      name: '产业链风险评估',
      description: '融合节点风险结果与网络结构特征，评估产业链整体的三级风险等级。'
    }
  ],
  
  problemDefinition: {
    riskDefinition: '通过异质图建模产业链网络，节点包含公司（财务/结构特征）和产品，边类型涵盖公司-产品、产品-公司、产品-产品关系。模型能够识别网络中的风险传播路径和关键风险节点。',
    designGoals: [
      '构建异质图与风险指标体系，提取节点特征与连接关系',
      '转换公司关联图，刻画供应、竞争、投融资关系',
      '结合邻域采样与注意力机制，实现节点与产业链风险评估'
    ]
  },
  
  techComponents: [
    {
      title: '异质图与公司图生成',
      details: [
        '通过元路径构建公司间的供应、竞争、投资关系图谱',
        '基于股权持有、共同投资、相同投资人等关系构建投融资关系图'
      ]
    },
    {
      title: '节点风险评估（GANS）',
      details: [
        '邻域采样：定义采样邻域，通过均值聚合逐层融合邻居特征',
        '关系级注意力：为三种关系图分配权重，加权融合节点嵌入'
      ]
    },
    {
      title: '产业链风险评估',
      details: [
        '结构特征提取：节点度转换为嵌入，获取网络结构特征',
        '图池化聚合：拼接风险嵌入与结构特征，通过全连接层输出三级风险等级'
      ]
    }
  ],

  riskMetrics: [
    {
      name: '节点风险分类',
      level: '二元分类',
      description: '针对产业链中的公司节点进行风险识别，判断其财务状况和经营风险水平。',
      features: ['安全', '危险'],
      icon: CircleCheck,
      iconClass: 'blue-icon'
    },
    {
      name: '产业链风险等级',
      level: '三元分类',
      description: '评估整个产业链网络的系统性风险，考虑风险传播和网络稳定性。',
      features: ['低风险', '中风险', '高风险'],
      icon: Warning,
      iconClass: 'orange-icon'
    },
    {
      name: '风险传播路径',
      level: '网络分析',
      description: '识别产业链中的关键风险传播路径和薄弱环节，提供预警机制。',
      features: ['路径识别', '影响评估', '预警提示'],
      icon: Bell,
      iconClass: 'red-icon'
    }
  ],

  algorithm: {
    lossFunction: {
      description: '采用多任务学习框架，同时优化节点风险分类和产业链风险等级评估',
      nodeLoss: 'L₁ = -∑(yᵥ₍ᵢ₎ log ŷᵥ₍ᵢ₎ + (1-yᵥ₍ᵢ₎) log(1-ŷᵥ₍ᵢ₎))',
      chainLoss: 'L₂ = -∑(t log t̂) (t为真实风险等级)'
    },
    keySteps: [
      '异质图转换为公司关系图，提取多源特征',
      '邻域采样与多层聚合，生成节点嵌入',
      '关系级注意力融合多图特征，分类节点风险',
      '结合节点结构特征，池化评估产业链风险'
    ]
  },

  features: [
    {
      title: '异质图建模',
      description: '多类型节点和边关系建模，全面刻画产业链网络',
      icon: Share,
      iconClass: 'blue-icon'
    },
    {
      title: '邻居采样机制',
      description: '高效的图采样策略，处理大规模网络结构',
      icon: Coordinate,
      iconClass: 'green-icon'
    },
    {
      title: '图注意力机制',
      description: '自适应关系权重学习，增强模型表达能力',
      icon: MagicStick,
      iconClass: 'purple-icon'
    },
    {
      title: '多层级风险评估',
      description: '从节点到网络的分层风险评估体系',
      icon: TrendCharts,
      iconClass: 'orange-icon'
    }
  ]
})
</script>

<style scoped lang="scss">
.risk-assessment-model1-container {
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

  .problem-card {
    margin-bottom: 20px;
    
    .problem-content {
      .problem-section {
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
        
        .risk-labels {
          display: flex;
          gap: 20px;
          flex-wrap: wrap;
          
          .label-item {
            .label-type {
              font-weight: 600;
              color: #303133;
            }
            
            .label-content {
              color: #409eff;
              background: #ecf5ff;
              padding: 2px 8px;
              border-radius: 4px;
              font-size: 12px;
            }
          }
        }
        
        .design-goals {
          .goal-item {
            display: flex;
            align-items: center;
            margin-bottom: 12px;
            
            &:last-child {
              margin-bottom: 0;
            }
            
            .goal-number {
              width: 24px;
              height: 24px;
              background: #67c23a;
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
            
            .goal-text {
              color: #606266;
              line-height: 1.6;
              font-size: 14px;
            }
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
            
            &.blue-icon { color: #409eff; }
            &.orange-icon { color: #e6a23c; }
            &.red-icon { color: #f56c6c; }
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
        
        .metric-features {
          display: flex;
          gap: 8px;
          flex-wrap: wrap;
          
          .feature-tag {
            background: #f0f2f5;
            color: #606266;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            border: 1px solid #e4e7ed;
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
        
        .loss-functions {
          .loss-item {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 8px;
            
            &:last-child {
              margin-bottom: 0;
            }
            
            .loss-label {
              font-size: 13px;
              color: #909399;
              font-weight: 500;
              min-width: 80px;
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
        
        .algorithm-steps {
          .algorithm-step {
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