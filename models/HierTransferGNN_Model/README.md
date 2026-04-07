# HierTransferGNN Model - 基于分层知识可转移图神经网络的风险评估模型

## 模型简介
HierTransferGNN 是一个基于分层知识可转移图神经网络的风险评估模型，通过预训练的知识嵌入和分层异构图卷积网络来实现跨领域的风险评估。

## 核心特性
- **分层异构图卷积**: 使用HeteroRGCNLayer处理多种节点和边类型
- **知识可转移性**: 通过MetaPath2vec预训练获得可转移的节点嵌入
- **门控特征融合**: CompanyFeatureFusion模块融合财务特征和预训练嵌入
- **全局池化**: 支持多种图级别的池化策略（mean、max、sum）

## 文件说明
- `model_pure.py`: 核心模型实现，包含RiskEvaluationModel主类
- `main_pure.py`: 完整的训练和评估流程
- `PreTrain.py`: MetaPath2vec预训练模块
- `data_read.py`: 异构图数据读取和预处理
- `utils.py`: 工具函数和辅助方法

## 模型架构
```
输入: 异构图 + 公司财务特征
  ↓
MetaPath2vec预训练 (公司和产品嵌入)
  ↓
CompanyFeatureFusion (门控融合财务特征和预训练嵌入)
  ↓
HeteroRGCNLayer (分层异构图卷积)
  ↓
GlobalPooling (图级别池化)
  ↓
分类器 (Linear + ReLU + Linear)
  ↓
输出: 风险评估结果
```

## 数据集路径
- 数据文件：`../datasets/Inte/Graph_generate.xlsx`

## 使用方法
```bash
python main_pure.py
```

## 主要参数
- `company_feat_dim`: 公司特征维度，默认18
- `embed_dim`: 嵌入维度，默认64
- `hidden_dim`: 隐藏层维度，默认128
- `num_layers`: RGCN层数，默认2
- `pool_type`: 池化类型，默认"mean"

## 预训练阶段
- 使用MetaPath2vec在异构图上预训练节点嵌入
- 支持多种元路径：company-cp-product、product-pc-company等
- 预训练模型可在不同数据集间迁移

## 特色功能
- **知识迁移**: 预训练的嵌入可在不同产业链数据间共享
- **分层学习**: 多层RGCN捕获不同层次的图结构信息
- **特征融合**: 智能融合结构化财务特征和图嵌入特征

## 输出结果

模型训练完成后会生成以下输出：

1. **训练指标文件**：
   - `acc_4.txt` - 验证集准确率变化记录
   - `f1_4.txt` - 验证集F1分数变化记录
   - `auc_4.txt` - 验证集AUC值变化记录
   - `epoch_4.txt` - 对应的训练轮数记录

2. **模型权重文件**：
   - `model_save/Checkpoint_mean_*auc_model.pth` - 最佳AUC模型权重

3. **预训练嵌入**：
   - `embeddings_save/` - MetaPath2vec预训练嵌入文件

4. **训练过程可视化图片**：
   - `training_plots/validation_curves_improved_*.png` - 优化版验证集AUC、准确率、F1分数变化曲线
   - `training_plots/training_loss_improved_*.png` - 优化版训练损失变化曲线
   - `training_plots/performance_comparison_improved_*.png` - 优化版综合性能对比图

5. **控制台输出**：
   - 训练过程中的损失和指标变化
   - 最终测试集性能评估结果
   - 图级风险预测结果 