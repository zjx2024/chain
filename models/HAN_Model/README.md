# HAN Model - 基于邻居采样和图注意力机制的风险评估模型

## 模型简介
HAN (Hierarchical Attention Network) 是一个基于邻居采样和图注意力机制的异构图神经网络模型，专门用于产业链风险评估。

## 核心特性
- **邻居采样机制**: 使用SAGEConv进行高效的邻居节点采样
- **语义注意力**: 通过SemanticAttention模块聚合多元路径信息
- **边丢弃正则化**: 支持DropEdge机制防止过拟合
- **多元路径学习**: 支持异构图中的多种元路径组合

## 文件说明
- `model.py`: HAN模型的核心实现，包含HANLayer和HAN主类
- `main.py`: 模型训练和评估的主程序
- `utils.py`: 数据处理和图构建的工具函数

## 模型架构
```
输入: 异构图 + 节点特征
  ↓
HANLayer (多个元路径的SAGEConv + SemanticAttention)
  ↓
分类层 (Linear)
  ↓
输出: 风险预测结果
```

## 数据集路径
- 特征数据：通过 `--feat-file` 参数指定
- 图数据：根据特征文件自动选择
  - 集成电路数据集 → `graph/Inte_Graph.pt`
  - 电子信息数据集 → `graph/Electric.pt`

## 使用方法

### 基本使用
```bash
python main.py
```

### 使用命令行参数
```bash
# 指定特征文件路径
python main.py --feat-file /path/to/your/feature_file.xlsx

# 指定训练轮次
python main.py --epochs 1000

# 指定学习率
python main.py --lr 0.01

# 组合使用多个参数
python main.py --feat-file /path/to/data.xlsx --epochs 500 --lr 0.005
```

### 命令行参数说明
- `--feat-file`: 特征文件路径 (默认: `../datasets/Electric/Electric_2022Q2.xlsx`)
- `--epochs`: 训练轮次 (默认: 800)
- `--lr`: 学习率 (默认: 0.001)
- `--seed`: 随机种子 (默认: 1)
- `--log-dir`: 日志保存目录 (默认: `results`)

### 图数据自动选择机制
模型会根据特征文件名自动选择对应的图数据：
- 文件名包含"集成电路"或"Inte" → 使用 `graph/Inte_Graph.pt`
- 文件名包含"电子信息"或"Electric" → 使用 `graph/Electric.pt`
- 无法识别时 → 默认使用 `graph/Electric.pt`

### 模型保存
训练完成后，模型会自动保存到 `../models-storage/` 目录中，保存格式为：
```
../models-storage/HAN_Model_{数据集名称}_epochs{训练轮次}_lr{学习率}_{时间戳}/
├── Best_f1_model.pth      # 最佳F1分数模型
├── Best_acc_model.pth     # 最佳准确率模型
├── Best_auc_model.pth     # 最佳AUC模型
├── model_info.txt         # 模型训练信息
├── acc.txt                # 训练准确率记录
├── f12.txt                # 训练F1分数记录
├── auc.txt                # 训练AUC记录
├── training_plots/        # 训练过程图表
│   ├── training_curves_improved_{时间戳}.png
│   ├── test_curves_improved_{时间戳}.png
│   └── train_vs_test_comparison_improved_{时间戳}.png
└── IndustryChain_{时间戳}/ # 日志目录
```

例如：`../models-storage/HAN_Model_Electric_2022Q2_epochs800_lr0.001_20250102_143025/`

## 主要参数
- `meta_paths`: 元路径定义，如[["cp","pc"],["cp","pp","pc"]]
- `hidden_size`: 隐藏层维度，默认128
- `num_heads`: 注意力头数，默认[12]
- `dropout`: 丢弃率，默认0.4

## 输出结果

模型训练完成后会生成以下输出：

1. **模型权重文件**：
   - `modeldata/Best_acc_model.pth` - 最佳准确率模型
   - `modeldata/Best_f1_model.pth` - 最佳F1分数模型  
   - `modeldata/Best_auc_model.pth` - 最佳AUC模型

2. **训练过程可视化图片**：
   - `training_plots/training_curves_improved_*.png` - 优化版训练集准确率、F1分数、AUC变化曲线
   - `training_plots/test_curves_improved_*.png` - 优化版测试集准确率、F1分数、AUC变化曲线
   - `training_plots/train_vs_test_comparison_improved_*.png` - 优化版训练集vs测试集性能对比图

3. **控制台输出**：
   - 每个epoch的训练和验证指标
   - 最佳模型的最终测试结果 