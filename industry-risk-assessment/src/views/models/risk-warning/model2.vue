<template>
  <div class="risk-warning-model2-container">
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
            src="/images/models/risk-warning/model2-architecture.png" 
            alt="HiGNNs模型架构图"
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
          <h4><el-icon><Warning /></el-icon>产业链风险建模挑战</h4>
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

    <!-- 层次图构建 -->
    <el-card class="hierarchy-card">
      <template #header>
        <div class="card-header">
          <span>层次图构建</span>
        </div>
      </template>
      <div class="hierarchy-content">
        <div class="hierarchy-overview">
          <h4><el-icon><Share /></el-icon>双层图结构</h4>
          <p>{{ modelInfo.hierarchyGraph.overview }}</p>
        </div>
        
        <div class="hierarchy-layers">
          <div 
            v-for="layer in modelInfo.hierarchyGraph.layers" 
            :key="layer.name"
            class="layer-item"
          >
            <div class="layer-header">
              <el-icon class="layer-icon" :class="layer.iconClass">
                <component :is="layer.icon" />
              </el-icon>
              <h5>{{ layer.name }}</h5>
            </div>
            <p class="layer-description">{{ layer.description }}</p>
            <div class="layer-features">
              <span 
                v-for="feature in layer.features"
                :key="feature"
                class="feature-tag"
              >
                {{ feature }}
              </span>
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
          <div v-if="component.formula" class="component-formula">
            <span class="formula-label">关键公式：</span>
            <code>{{ component.formula }}</code>
          </div>
        </div>
      </div>
    </el-card>

    <!-- 特征融合与分类 -->
    <el-card class="fusion-card">
      <template #header>
        <div class="card-header">
          <span>特征融合与分类</span>
        </div>
      </template>
      <div class="fusion-content">
                 <div class="fusion-section">
           <h4><el-icon><MagicStick /></el-icon>注意力机制融合</h4>
           <p>{{ modelInfo.featureFusion.attention.description }}</p>
         </div>
        
        <div class="fusion-section">
          <h4><el-icon><DataBoard /></el-icon>图表示学习</h4>
          <p>{{ modelInfo.featureFusion.graphLearning.description }}</p>
          <div class="learning-formula">
            <span class="formula-label">预测公式：</span>
            <code>{{ modelInfo.featureFusion.graphLearning.formula }}</code>
          </div>
        </div>
      </div>
    </el-card>

    <!-- 预警逻辑与优化目标 -->
    <el-card class="optimization-card">
      <template #header>
        <div class="card-header">
          <span>预警逻辑与优化目标</span>
        </div>
      </template>
      <div class="optimization-content">
        <div class="optimization-section">
          <h4>
            <el-icon><Bell /></el-icon>
            风险分类标准
          </h4>
          <p>{{ modelInfo.warningLogic.classification.description }}</p>
          <div class="classification-rules">
            <div 
              v-for="rule in modelInfo.warningLogic.classification.rules"
              :key="rule.condition"
              class="rule-item"
            >
              <span class="rule-condition" :class="rule.class">{{ rule.condition }}</span>
              <span class="rule-description">{{ rule.description }}</span>
            </div>
          </div>
        </div>
        
                 <div class="optimization-section">
           <h4>
             <el-icon><TrendCharts /></el-icon>
             损失函数与优化
           </h4>
           <p>{{ modelInfo.warningLogic.optimization.description }}</p>
           <div class="optimization-formula">
             <span class="formula-label">损失函数：</span>
             <code>{{ modelInfo.warningLogic.optimization.formula }}</code>
           </div>
         </div>
        
        <div class="optimization-section">
          <h4>
            <el-icon><Star /></el-icon>
            模型优势
          </h4>
          <div class="advantages-grid">
            <div 
              v-for="advantage in modelInfo.warningLogic.advantages"
              :key="advantage"
              class="advantage-item"
            >
              <el-icon class="advantage-icon"><CircleCheck /></el-icon>
              <span>{{ advantage }}</span>
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
  ArrowRight,
  Warning,
  CircleCheck,
  Bell,
  Share,
  MagicStick,
  Star,
  Platform
} from '@element-plus/icons-vue'

// 图片加载错误处理
const handleImageError = (event: Event) => {
  const img = event.target as HTMLImageElement
  img.style.display = 'none'
}

// 模型信息配置
const modelInfo = reactive({
  title: '基于层次图神经网络和LSTM的产业链风险预警模型',
  description: 'HiGNNs模型创新性地结合层次图神经网络与LSTM自编码器，构建双层图结构来表达产业链的复杂关系。通过投资子图和产业链图的层次设计，模型能够同时捕捉密集的投资关系和稀疏的上下游关系，利用LSTM处理财务时序特征，GIN网络提取投资图结构特征，最终通过注意力机制实现多源特征融合和精准风险预警。',
  
  modules: [
    {
      name: '层次图构建',
      description: '构建双层图结构：第一层为投资子图（密集连接），第二层为产业链图（稀疏连接），通过中心节点关联两层。'
    },
    {
      name: '财务特征提取', 
      description: 'LSTM自编码器处理多季度财务数据，压缩三维时序特征为固定长度向量，捕捉财务指标的动态变化。'
    },
    {
      name: '投资特征提取',
      description: 'GIN模型结合位置编码、度编码、类型编码和最短路径编码，提取投资图的丰富结构特征。'
    },
    {
      name: '风险评估预警',
      description: '注意力机制动态融合财务与投资特征，通过图表示学习进行二分类风险预警，输出风险概率。'
    }
  ],
  
  challenges: [
    '数据多层级：包含产业链上下游关系（稀疏）和投资关系（密集），传统单层图难以表达复杂的网络结构',
    '财务数据时序性：多季度指标需要捕捉动态变化，投资关系需要结构特征提取',
    '特征异构性：财务特征与投资特征具有不同的维度和语义，需要有效的融合机制'
  ],
  
  designGoals: [
    '构建"产业链-投资"层次图，融合上下游与投资关系',
    '利用LSTM自编码器提取财务时序特征，GNN捕捉投资图结构',
    '基于注意力机制融合多源特征，实现风险二分类预警'
  ],
  
  hierarchyGraph: {
    overview: '模型采用双层图结构设计，有效解决了产业链网络中关系密度差异大的问题，通过层次化建模实现了复杂网络关系的精准表达。',
    layers: [
      {
        name: '投资子图（第一层）',
        description: '以上市公司为中心节点，包含投资人/投资公司，边为投资关系，具有高密度、高连通性特点。',
        features: ['密集投资网络', '人工编码特征', '位置/度/类型编码', '最短路径信息'],
        icon: Connection,
        iconClass: 'blue-icon'
      },
      {
        name: '产业链图（第二层）',
        description: '公司为节点，边为产品/服务交易关系，节点属性包含财务与投资特征，连接相对稀疏。',
        features: ['上下游关系', '产品交易网络', '财务特征融合', '稀疏连接结构'],
        icon: Platform,
        iconClass: 'green-icon'
      }
    ]
  },
  
     techComponents: [
     {
       title: 'LSTM自编码器',
       details: [
         '输入：三维财务时序数据（企业数×季度数×指标维度）',
         '编码器：LSTM压缩时序数据为固定维度状态，捕捉时序依赖关系'
       ]
     },
     {
       title: '投资特征提取',
       details: [
         '节点编码：拉普拉斯新矩阵特征值分解解决节点K列',
         '度编码：入度/出度归一化，反映投资活跃度'
       ]
     },
     {
       title: 'GIN模型特征聚合',
       details: [
         '类型编码：one-hot维度表示节点类型（上市/非上市/自然人等）',
         '最短路径编码：节点对最短路径归一化，反映结构邻近相似性'
       ],
       formula: 'h(l+1) = f((1+ε)·h(l) + Σ h(l))'
     },
     {
       title: '特征融合与分类',
       details: [
         '注意力机制：计算财务特征f_f和投资特征f_i权重',
         '图表示学习：聚合邻居特征输入全连接层，sigmoid激活输出风险概率'
       ]
     }
   ],

     featureFusion: {
     attention: {
       description: '采用注意力机制动态计算财务与投资特征的融合权重，根据不同企业的特点自适应调整特征重要性。通过权重归一化实现多源特征的有效融合。'
     },
     graphLearning: {
       description: '聚合邻居特征输入全连接层，通过sigmoid激活函数输出风险概率，实现端到端的风险预警。',
       formula: 'p = sigmoid(W · hv + b)'
     }
   },

  warningLogic: {
    classification: {
      description: '模型采用二分类策略，基于概率阈值判定风险状态，为产业链风险管理提供及时预警。',
      rules: [
        { condition: '概率 > 0.5', description: '判定为风险状态（标签1）', class: 'high-risk' },
        { condition: '概率 ≤ 0.5', description: '反之为无风险（标签0）', class: 'low-risk' }
      ]
    },
         optimization: {
       description: '采用多任务学习框架，同时优化财务自编码重建和风险分类任务。使用均方误差损失重建财务特征，二元交叉熵损失进行风险分类。',
       formula: 'L = -Σᵢ(yᵢ log pᵢ + (1-yᵢ) log(1-pᵢ))'
     },
    advantages: [
      '层次图结构同时捕捉产业链全关系和投资密集关系',
      'LSTM自编码器自动提取财务时序特征，避免人工特征工程',
      '注意力机制动态融合多源特征，提升风险识别准确率'
    ]
  },

  features: [
    {
      title: '层次图建模',
      description: '双层图结构精确表达产业链复杂网络关系',
      icon: Share,
      iconClass: 'blue-icon'
    },
    {
      title: 'LSTM时序建模',
      description: '自编码器捕捉财务数据的时间序列特征',
      icon: TrendCharts,
      iconClass: 'green-icon'
    },
    {
      title: '注意力特征融合',
      description: '动态加权融合财务与投资特征，增强表达能力',
      icon: MagicStick,
      iconClass: 'purple-icon'
    },
    {
      title: '智能风险预警',
      description: '端到端学习框架，实现精准的二分类风险预警',
      icon: Bell,
      iconClass: 'orange-icon'
    }
  ]
})
</script>

<style scoped lang="scss">
.risk-warning-model2-container {
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

  .hierarchy-card {
    margin-bottom: 20px;
    
    .hierarchy-content {
      .hierarchy-overview {
        margin-bottom: 25px;
        
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
          margin: 0;
          text-align: justify;
        }
      }
      
      .hierarchy-layers {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
        gap: 20px;
        
        .layer-item {
          border: 1px solid #e4e7ed;
          border-radius: 8px;
          padding: 20px;
          background: #fafbfc;
          transition: all 0.3s ease;
          
          &:hover {
            border-color: #409eff;
            box-shadow: 0 2px 12px 0 rgba(64, 158, 255, 0.1);
          }
          
          .layer-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 12px;
            
            .layer-icon {
              font-size: 24px;
              
              &.blue-icon { color: #409eff; }
              &.green-icon { color: #67c23a; }
            }
            
            h5 {
              margin: 0;
              font-size: 16px;
              font-weight: 600;
              color: #303133;
            }
          }
          
          .layer-description {
            font-size: 13px;
            line-height: 1.6;
            color: #606266;
            margin: 0 0 15px 0;
          }
          
          .layer-features {
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
          margin-bottom: 12px;
          
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
        
        .component-formula {
          padding-left: 47px;
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

  .fusion-card {
    margin-bottom: 20px;
    
    .fusion-content {
      .fusion-section {
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
          margin: 0 0 15px 0;
        }
        
        .attention-formulas {
          .formula-item {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 8px;
            flex-wrap: wrap;
            
            &:last-child {
              margin-bottom: 0;
            }
            
            .formula-label {
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
        
        .learning-formula {
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
        
        .classification-rules {
          .rule-item {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 10px;
            
            &:last-child {
              margin-bottom: 0;
            }
            
            .rule-condition {
              min-width: 100px;
              padding: 4px 8px;
              border-radius: 4px;
              font-size: 12px;
              font-weight: 600;
              text-align: center;
              
              &.high-risk { background: #fef0f0; color: #f56c6c; }
              &.low-risk { background: #e1f3d8; color: #67c23a; }
            }
            
            .rule-description {
              font-size: 14px;
              color: #606266;
            }
          }
        }
        
                 .optimization-formula {
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
        
        .advantages-grid {
          .advantage-item {
            display: flex;
            align-items: flex-start;
            gap: 10px;
            margin-bottom: 10px;
            
            &:last-child {
              margin-bottom: 0;
            }
            
            .advantage-icon {
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
    .features-grid,
    .hierarchy-layers {
      grid-template-columns: 1fr;
    }
  }
}
</style> 
