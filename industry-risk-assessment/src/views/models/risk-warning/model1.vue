<template>
  <div class="risk-warning-model1-container">
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
        <div class="architecture-flow">
          <div class="flow-description">
            <h4>模型流程架构</h4>
            <p>{{ modelInfo.architectureFlow }}</p>
          </div>
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
          <h4><el-icon><Warning /></el-icon>产业链风险预警挑战</h4>
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

    <!-- 指标体系构建 -->
    <el-card class="indicators-card">
      <template #header>
        <div class="card-header">
          <span>指标体系构建</span>
        </div>
      </template>
      <div class="indicators-content">
        <div class="indicators-overview">
          <h4><el-icon><DataBoard /></el-icon>指标体系结构</h4>
          <p>{{ modelInfo.indicators.overview }}</p>
        </div>
        
        <div class="indicators-grid">
          <div 
            v-for="indicator in modelInfo.indicators.primaryIndicators" 
            :key="indicator.name"
            class="indicator-item"
          >
            <div class="indicator-header">
              <el-icon class="indicator-icon" :class="indicator.iconClass">
                <component :is="indicator.icon" />
              </el-icon>
              <h5>{{ indicator.name }}</h5>
            </div>
            <p class="indicator-description">{{ indicator.description }}</p>
            <div class="indicator-details">
              <span 
                v-for="detail in indicator.details"
                :key="detail"
                class="detail-tag"
              >
                {{ detail }}
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

    <!-- 风险预警等级 -->
    <el-card class="metrics-card">
      <template #header>
        <div class="card-header">
          <span>风险预警等级</span>
        </div>
      </template>
      <div class="metrics-grid">
        <div 
          v-for="level in modelInfo.warningLevels" 
          :key="level.name"
          class="metric-item"
        >
          <div class="metric-header">
            <el-icon class="metric-icon" :class="level.iconClass">
              <component :is="level.icon" />
            </el-icon>
            <div class="metric-info">
              <h5>{{ level.name }}</h5>
              <span class="metric-code" :class="level.codeClass">{{ level.range }}</span>
            </div>
          </div>
          <p class="metric-description">{{ level.description }}</p>
          <div class="metric-features">
            <span 
              v-for="feature in level.features"
              :key="feature"
              class="feature-tag"
            >
              {{ feature }}
            </span>
          </div>
        </div>
      </div>
    </el-card>

    <!-- 模型优势与结果 -->
    <el-card class="optimization-card">
      <template #header>
        <div class="card-header">
          <span>模型优势与结果</span>
        </div>
      </template>
      <div class="optimization-content">
        <div class="optimization-section">
          <h4>
            <el-icon><Star /></el-icon>
            模型优势
          </h4>
          <div class="advantages-grid">
            <div 
              v-for="advantage in modelInfo.advantages"
              :key="advantage"
              class="advantage-item"
            >
              <el-icon class="advantage-icon"><CircleCheck /></el-icon>
              <span>{{ advantage }}</span>
            </div>
          </div>
        </div>
        
        <div class="optimization-section">
          <h4>
            <el-icon><TrendCharts /></el-icon>
            预警逻辑与结果解读
          </h4>
          <p>{{ modelInfo.warningLogic.description }}</p>
          <div class="warning-logic">
            <div 
              v-for="logic in modelInfo.warningLogic.classification"
              :key="logic.range"
              class="logic-item"
            >
              <span class="logic-range" :class="logic.class">{{ logic.range }}</span>
              <span class="logic-description">{{ logic.description }}</span>
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
  TrendCharts,
  Monitor,
  ArrowRight,
  Warning,
  CircleCheck,
  Bell,
  MagicStick,
  Coordinate,
  Star,
  CreditCard,
  OfficeBuilding,
  Platform
} from '@element-plus/icons-vue'

// 模型信息配置
const modelInfo = reactive({
  title: '基于PCA-CNN的产业链风险预警模型',
  description: '本模型结合主成分分析（PCA）和卷积神经网络（CNN），构建高效的产业链风险预警系统。通过建立多维指标体系，利用PCA进行特征降维，再采用CNN进行非线性风险模式识别，实现对产业链风险的准确预警和分级管理。',
  
  architectureFlow: '模型采用"指标构建→PCA降维→CNN预警"的三阶段流程：首先构建包含4个一级指标和29个三级指标的综合风险评估体系，然后通过PCA将高维指标压缩为8个主成分，最后利用CNN的卷积、池化和全连接层实现风险等级的智能分类预警。',
  
  modules: [
    {
      name: '指标体系构建',
      description: '设计4个一级指标（融资企业资格、运行环境、核心企业资质、产业链运营）和29个三级指标，构建全面的风险评估框架。'
    },
    {
      name: 'PCA降维处理', 
      description: '将29个指标通过主成分分析降维为8个主成分，解释76.57%的总方差，有效减少数据冗余。'
    },
    {
      name: 'CNN预警模型',
      description: '输入PCA主成分特征，通过卷积层、池化层和全连接层进行特征提取和风险等级分类预测。'
    }
  ],
  
  challenges: [
    '风险因素复杂（宏观经济、产业链内部、外部环境），指标维度高（29个三级指标），存在数据冗余与相关性',
    '传统方法难以处理高维数据与非线性特征，需要高效的降维与特征提取技术',
    '产业链风险具有动态性和突发性，需要实时准确的预警机制'
  ],
  
  designGoals: [
    '构建多维度风险指标体系，融合财务与非财务指标',
    '利用PCA降维，提取关键风险特征，降低计算复杂度',
    '基于CNN构建预警模型，捕捉非线性风险模式，提升预警准确率'
  ],
  
  indicators: {
    overview: '构建包含4个一级指标和29个三级指标的综合风险评估体系，涵盖融资能力、运营环境、企业资质和产业链协调等多个维度。',
    primaryIndicators: [
      {
        name: '融资企业资格',
        description: '评估企业融资能力和财务健康状况，包含16个财务指标。',
        details: ['资产收益率', '流动比率', '债务比率', '现金流量'],
        icon: CreditCard,
        iconClass: 'blue-icon'
      },
      {
        name: '运行环境',
        description: '分析宏观经济和行业前景对产业链的影响。',
        details: ['宏观经济指标', '行业景气度', '政策环境', '市场需求'],
        icon: TrendCharts,
        iconClass: 'green-icon'
      },
      {
        name: '核心企业资质',
        description: '评估产业链核心企业的实力和稳定性。',
        details: ['盈利能力', '创新能力', '市场地位', '治理结构'],
        icon: OfficeBuilding,
        iconClass: 'purple-icon'
      },
      {
        name: '产业链运营',
        description: '衡量产业链整体协调性和运营效率。',
        details: ['供应链稳定性', '信息共享程度', '协作效率', '风险传导'],
        icon: Platform,
        iconClass: 'orange-icon'
      }
    ]
  },
  
  techComponents: [
    {
      title: 'PCA降维过程',
      details: [
        '数据预处理：标准化数据，KMO检验值0.82（适合因子分析），Bartlett球度检验显著',
        '主成分提取：8个主成分（特征值>1），累计方差贡献率76.57%，如F1（核心企业盈利能力）、F2（运营安全因素）等'
      ],
      formula: 'F = Σ(αᵢ×贡献率ᵢ/0.765) × Fᵢ'
    },
    {
      title: 'CNN模型架构',
      details: [
        '输入层：8个主成分特征，转换为适合CNN的张量形式',
        '卷积层：使用卷积核提取局部特征，公式：Xⱼˡ = f(Σᵢ∈Pⱼ Xᵢ·Kᵢⱼˡ + bⱼˡ)'
      ],
      formula: 'Xⱼˡ = f(Σᵢ∈Pⱼ Xᵢ·Kᵢⱼˡ + bⱼˡ)'
    },
    {
      title: 'CNN网络结构',
      details: [
        '池化层：2×2窗口maxpooling降维，保留关键特征',
        '全连接层：两层全连接，ReLU激活，输出风险等级（安全/较安全/警惕/危险）'
      ]
    }
  ],

  warningLevels: [
    {
      name: '安全等级',
      range: 'F > 1',
      description: '产业链运行稳定，各项指标表现良好，风险程度较低。',
      features: ['低风险', '稳定运行', '健康发展'],
      icon: CircleCheck,
      iconClass: 'green-icon',
      codeClass: 'safe-code'
    },
    {
      name: '较安全等级',
      range: '0 < F < 1',
      description: '产业链整体平稳，存在轻微风险因素，需要持续关注。',
      features: ['较低风险', '轻微波动', '可控状态'],
      icon: Monitor,
      iconClass: 'blue-icon',
      codeClass: 'relatively-safe-code'
    },
    {
      name: '警惕等级',
      range: '-1 < F < 0',
      description: '产业链出现一定风险信号，需要采取预防措施。',
      features: ['较高风险', '需要关注', '预防措施'],
      icon: Warning,
      iconClass: 'orange-icon',
      codeClass: 'caution-code'
    },
    {
      name: '危险等级',
      range: 'F < -1',
      description: '产业链面临较大风险，需要立即采取应对措施。',
      features: ['高风险', '紧急状态', '立即应对'],
      icon: Bell,
      iconClass: 'red-icon',
      codeClass: 'danger-code'
    }
  ],

  advantages: [
    'PCA减少维度，避免"维度灾难"，CNN捕捉非线性关系，比传统线性模型更准确',
    '融合财务与非财务指标，覆盖产业链多环节风险，预警及时性与可信度高'
  ],

  warningLogic: {
    description: '模型基于PCA主成分综合得分F进行风险等级划分，通过CNN优化分类边界：',
    classification: [
      { range: 'F > 1', description: '低风险（安全）', class: 'safe' },
      { range: '0 < F < 1', description: '较低风险（较安全）', class: 'relatively-safe' },
      { range: '-1 < F < 0', description: '较高风险（警惕）', class: 'caution' },
      { range: 'F < -1', description: '高风险（危险）', class: 'danger' }
    ]
  },

  features: [
    {
      title: 'PCA降维技术',
      description: '高效的主成分分析，将29维指标降至8维，保留76.57%信息',
      icon: Coordinate,
      iconClass: 'blue-icon'
    },
    {
      title: 'CNN深度学习',
      description: '卷积神经网络捕捉非线性风险模式，提升预警准确性',
      icon: MagicStick,
      iconClass: 'green-icon'
    },
    {
      title: '多维指标体系',
      description: '融合财务与非财务指标，全面覆盖产业链风险因素',
      icon: DataBoard,
      iconClass: 'purple-icon'
    },
    {
      title: '智能风险预警',
      description: '四级风险等级分类，实现精准的风险预警和管理',
      icon: Bell,
      iconClass: 'orange-icon'
    }
  ]
})
</script>

<style scoped lang="scss">
.risk-warning-model1-container {
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
      .architecture-flow {
        margin-bottom: 30px;
        padding: 20px;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 8px;
        border-left: 4px solid #409eff;
        
        h4 {
          margin: 0 0 12px 0;
          color: #303133;
          font-size: 16px;
          font-weight: 600;
        }
        
        p {
          margin: 0;
          font-size: 14px;
          line-height: 1.7;
          color: #606266;
          text-align: justify;
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

  .indicators-card {
    margin-bottom: 20px;
    
    .indicators-content {
      .indicators-overview {
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
      
      .indicators-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 20px;
        
        .indicator-item {
          border: 1px solid #e4e7ed;
          border-radius: 8px;
          padding: 20px;
          background: #fafbfc;
          transition: all 0.3s ease;
          
          &:hover {
            border-color: #409eff;
            box-shadow: 0 2px 12px 0 rgba(64, 158, 255, 0.1);
          }
          
          .indicator-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 12px;
            
            .indicator-icon {
              font-size: 24px;
              
              &.blue-icon { color: #409eff; }
              &.green-icon { color: #67c23a; }
              &.purple-icon { color: #9c27b0; }
              &.orange-icon { color: #ff9800; }
            }
            
            h5 {
              margin: 0;
              font-size: 16px;
              font-weight: 600;
              color: #303133;
            }
          }
          
          .indicator-description {
            font-size: 13px;
            line-height: 1.6;
            color: #606266;
            margin: 0 0 15px 0;
          }
          
          .indicator-details {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            
            .detail-tag {
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
            
            &.green-icon { color: #67c23a; }
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
              padding: 2px 8px;
              border-radius: 4px;
              font-size: 12px;
              font-weight: 600;
              
              &.safe-code { background: #e1f3d8; color: #67c23a; }
              &.relatively-safe-code { background: #ecf5ff; color: #409eff; }
              &.caution-code { background: #fdf6ec; color: #e6a23c; }
              &.danger-code { background: #fef0f0; color: #f56c6c; }
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
        
        .warning-logic {
          .logic-item {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 10px;
            
            &:last-child {
              margin-bottom: 0;
            }
            
            .logic-range {
              min-width: 80px;
              padding: 4px 8px;
              border-radius: 4px;
              font-size: 12px;
              font-weight: 600;
              text-align: center;
              
              &.safe { background: #e1f3d8; color: #67c23a; }
              &.relatively-safe { background: #ecf5ff; color: #409eff; }
              &.caution { background: #fdf6ec; color: #e6a23c; }
              &.danger { background: #fef0f0; color: #f56c6c; }
            }
            
            .logic-description {
              font-size: 14px;
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
    .indicators-grid {
      grid-template-columns: 1fr;
    }
  }
}
</style> 
