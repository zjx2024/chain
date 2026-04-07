<template>
  <div class="risk-assessment-model2-container">
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
            src="/images/models/risk-assessment/model2-architecture.png" 
            alt="HKTGNN模型流程图"
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

    <!-- 问题挑战与设计目标 -->
    <el-card class="problem-card">
      <template #header>
        <div class="card-header">
          <span>问题挑战与设计目标</span>
        </div>
      </template>
      <div class="problem-content">
        <div class="problem-section">
          <h4><el-icon><Warning /></el-icon>产业链风险评估挑战</h4>
          <div class="challenge-items">
            <div 
              v-for="challenge in modelInfo.challenges" 
              :key="challenge"
              class="challenge-item"
            >
              <el-icon class="challenge-icon"><ArrowRight /></el-icon>
              <span>{{ challenge }}</span>
            </div>
          </div>
        </div>
        
        <div class="problem-section">
          <h4><el-icon><TrendCharts /></el-icon>设计目标</h4>
          <div class="design-goals">
            <div 
              v-for="(goal, index) in modelInfo.designGoals" 
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

    <!-- 实验验证与结果 -->
    <el-card class="optimization-card">
      <template #header>
        <div class="card-header">
          <span>实验验证与结果</span>
        </div>
      </template>
      <div class="optimization-content">
        <div class="optimization-section">
          <h4>
            <el-icon><DataBoard /></el-icon>
            数据集与对比模型
          </h4>
          <p>{{ modelInfo.experiments.dataset }}</p>
          <p>{{ modelInfo.experiments.comparison }}</p>
        </div>
        
        <div class="optimization-section">
          <h4>
            <el-icon><TrendCharts /></el-icon>
            关键结果
          </h4>
          <div class="results-grid">
            <div 
              v-for="result in modelInfo.experiments.keyResults"
              :key="result"
              class="result-item"
            >
              <el-icon class="result-icon"><CircleCheck /></el-icon>
              <span>{{ result }}</span>
            </div>
          </div>
        </div>
        
        <div class="optimization-section">
          <h4>
            <el-icon><Setting /></el-icon>
            参数影响
          </h4>
          <p>{{ modelInfo.experiments.parameterImpact }}</p>
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
  MagicStick
} from '@element-plus/icons-vue'

// 图片加载错误处理
const handleImageError = (event: Event) => {
  const img = event.target as HTMLImageElement
  img.style.display = 'none'
}

// 模型信息配置
const modelInfo = reactive({
  title: '基于分层知识可转移图神经网络的风险评估模型',
  description: 'HKTGNN模型通过分层处理异构图网络，结合知识转移机制解决节点特征缺失问题。模型采用六模块协同设计，从数据预处理到域转移分类，实现了高效的跨域风险评估。通过同构图转换降低计算成本，利用特征补充机制提升数据稀缺场景下的模型性能。',
  
  modules: [
    {
      name: '数据预处理',
      description: '分层构建产业链网络结构，将复杂异构图转换为多个单一产品同构图，减少计算复杂度。'
    },
    {
      name: '图嵌入编码器（GEE）', 
      description: '融合节点度、类型、最短路径等拓扑特征，生成64维嵌入向量，提取网络结构信息。'
    },
    {
      name: '特征补充器（CCAFC）',
      description: '基于特征中心性计算领域异因子，通过完备节点特征补充有偏节点财务特征。'
    },
    {
      name: '消息传递模块（DCAMP）',
      description: '跨域消息传递机制，通过校准分布偏移，解决不同域间的特征差异问题。'
    },
    {
      name: '域转移分类器（DTC）',
      description: '二分类节点风险状态，并基于节点风险结果评估产业链整体风险等级。'
    },
    {
      name: '风险等级输出',
      description: '综合节点分类结果与网络结构特征，输出产业链三级风险等级评估。'
    }
  ],
  
  challenges: [
    '数据规模大、节点特征缺失（如非上市公司财务数据不全），传统GNN计算资源消耗高',
    '异构图中公司间直接关系缺失，需通过产品关联间接建模',
    '跨域数据分布差异显著，影响模型泛化能力'
  ],
  
  designGoals: [
    '分层处理异构图，转换为小规模同构图，减少计算成本',
    '利用知识转移机制，补充有偏节点特征，解决数据饥饿问题',
    '结合域自适应消息传递，提升跨域风险评估准确性'
  ],
  
  techComponents: [
    {
      title: '分层图构建与嵌入',
      details: [
        '异构图→同构图转换：通过"公司-产品-产品-公司"元路径，将异构图转换为产品同构图',
        'GEE模块特征提取：融合节点度、类型、最短路径等拓扑特征，生成64维嵌入向量'
      ]
    },
    {
      title: '特征补充与消息传递',
      details: [
        'CCAFC特征补充：基于特征中心性计算领域异因子，补充有偏节点财务特征',
        'DCAMP跨域传递：通过校准分布偏移，解决域间特征差异问题'
      ]
    },
    {
      title: '域转移分类',
      details: [
        'DTC分类器：二分类节点风险状态，处理域间分布差异',
        '风险等级评估：结合节点分类与网络特征，输出三级产业链风险等级'
      ]
    }
  ],

  riskMetrics: [
    {
      name: '节点风险分类',
      level: '二元分类',
      description: '针对产业链中的公司节点进行风险识别，区分安全和危险状态，解决特征缺失场景。',
      features: ['安全', '危险'],
      icon: CircleCheck,
      iconClass: 'blue-icon'
    },
    {
      name: '产业链风险等级',
      level: '三元分类',
      description: '基于节点风险分布和网络结构特征，评估整个产业链的系统性风险水平。',
      features: ['低风险', '中风险', '高风险'],
      icon: Warning,
      iconClass: 'orange-icon'
    },
    {
      name: '跨域适应能力',
      level: '迁移学习',
      description: '通过域自适应机制，实现不同产业领域间的知识转移和风险评估。',
      features: ['域适应', '知识转移', '泛化能力'],
      icon: Bell,
      iconClass: 'red-icon'
    }
  ],

  experiments: {
    dataset: '数据集：集成电路产业链数据（430产品节点，1732公司节点），分7:1:2训练验证测试。',
    comparison: '对比模型：MLP、GGNN、GraphSAGE、KTGNN等，指标为F1和AUC。',
    keyResults: [
      'HKTGNN在全连接图上F1=80.75%，AUC=88.37%，优于KTGNN（F1=74.47%）和传统GNN',
      '消融实验显示，分层处理和域转移机制分别提升F1约5%和3%'
    ],
    parameterImpact: 'λ=2.5时性能最佳，F1均值最高且方差最小。'
  },

  features: [
    {
      title: '分层异构图处理',
      description: '将复杂异构图分解为多个同构子图，显著降低计算复杂度',
      icon: Share,
      iconClass: 'blue-icon'
    },
    {
      title: '知识转移机制',
      description: '通过CCAFC模块实现特征补充，解决数据稀缺问题',
      icon: Connection,
      iconClass: 'green-icon'
    },
    {
      title: '域自适应消息传递',
      description: 'DCAMP机制处理跨域分布差异，提升模型泛化能力',
      icon: MagicStick,
      iconClass: 'purple-icon'
    },
    {
      title: '高效计算性能',
      description: '通过分层处理和特征优化，实现大规模网络的高效分析',
      icon: Monitor,
      iconClass: 'orange-icon'
    }
  ]
})
</script>

<style scoped lang="scss">
.risk-assessment-model2-container {
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
        
        .challenge-items {
          .challenge-item {
            display: flex;
            align-items: flex-start;
            gap: 10px;
            margin-bottom: 12px;
            
            &:last-child {
              margin-bottom: 0;
            }
            
            .challenge-icon {
              color: #f56c6c;
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
        
        .results-grid {
          .result-item {
            display: flex;
            align-items: flex-start;
            gap: 10px;
            margin-bottom: 10px;
            
            &:last-child {
              margin-bottom: 0;
            }
            
            .result-icon {
              color: #67c23a;
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
