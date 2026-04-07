# GPFedRec-TopkEF21: 基于Top-k+EF21的联邦推荐系统

## 🎯 项目简介

GPFedRec-TopkEF21 是一个专门实现 **Top-k+EF21 稀疏上传策略** 的联邦推荐系统。该项目从 GPFedRec-improved 分离出来，专注于智能稀疏通信优化，采用全物品嵌入模式进行Top-k+EF21压缩。

## 🚀 核心特性

### 📊 Top-k+EF21 稀疏上传策略
- **智能Top-k选择**：基于梯度重要性进行Top-k压缩
- **EF21错误反馈**：通过错误累积提升压缩效果
- **自适应压缩比**：根据性能动态调整Top-k比例
- **零梯度优化**：跳过零梯度嵌入的EF21计算

### 🔧 核心设计原则
1. **Top-k比例永远基于本地全部嵌入数量计算**
2. **EF21计算只针对有更新的嵌入进行**
3. **优先上传有意义梯度，避免零梯度嵌入传输**
4. **支持多种聚合策略（聚类+图引导）**

## 📁 项目结构

```
GPFedRec-TopkEF21/
├── topk_ef21_optimizer.py          # Top-k+EF21核心优化器
├── improved_clustering_aggregation.py  # 改进的聚合策略
├── train.py                         # 主训练脚本
├── engine.py                        # 联邦学习引擎
├── data.py                          # 数据处理
├── utils.py                         # 工具函数
├── metrics.py                       # 评估指标
├── mlp.py                          # MLP模型
├── run_topk_ef21_clustering_experiment.py  # 实验运行脚本
└── data/                           # 数据目录
    └── 100k/
        └── ratings.dat
```

## 🎛️ 关键参数

### Top-k+EF21 相关参数
- `--use_topk_ef21`: 启用Top-k+EF21优化器
- `--topk_ratio`: Top-k压缩比例 (默认: 0.1)
- `--ef21_weight`: EF21权重参数 (默认: 3)
- `--ef21_warmup_rounds`: EF21预热轮数

### 聚合策略参数
- 聚合方法: `clustering_then_graph` (固定启用)
- `--n_clusters`: 聚类数量 (默认: 5)
- `--adaptive_reg`: 自适应正则化策略

### 隐私保护参数
- `--privacy_method`: 隐私保护方法 (`none`, `differential_privacy`)
- `--dp`: 差分隐私参数

## 🚀 快速开始

### 基础实验
```bash
python train.py \
    --dataset 100k \
    --num_round 200 \
    --clients_sample_ratio 1.0 \
    --lr 0.1 \
    --use_topk_ef21 True \
    --topk_ratio 0.1 \
    --ef21_weight 3 \
    # 聚合方法固定为clustering_then_graph \
    --n_clusters 5 \
    --privacy_method none
```

### 带差分隐私保护的实验
```bash
python train.py \
    --dataset 100k \
    --num_round 200 \
    --clients_sample_ratio 1.0 \
    --lr 0.1 \
    --use_topk_ef21 True \
    --topk_ratio 0.1 \
    --ef21_weight 3 \
    # 聚合方法固定为clustering_then_graph \
    --n_clusters 5 \
    --privacy_method differential_privacy \
    --dp 1e-6
```

### 使用实验脚本
```bash
python run_topk_ef21_clustering_experiment.py topk_differential_privacy
```

## 📊 实验配置

项目支持多种实验配置：

| 配置名称 | 描述 | 隐私保护 |
|----------|------|----------|
| `topk_no_privacy` | 无隐私保护的Top-k+EF21 | ❌ |
| `topk_lightweight_dp` | 轻量差分隐私保护 | 🔊 |
| `topk_differential_privacy` | 标准差分隐私保护 | 🔊 |
| `topk_strong_dp` | 强化差分隐私保护 | 🔊 |

## 🔄 与其他版本的区别

| 特性 | GPFedRec (原版) | GPFedRec-improved | GPFedRec-TopkEF21 |
|------|-----------------|-------------------|-------------------|
| **稀疏上传** | 多种策略混合 | 多种策略混合 | **专注Top-k+EF21** |
| **压缩算法** | 简单稀疏化 | 多种压缩方法 | **智能Top-k+EF21** |
| **聚合策略** | 基础聚合 | 改进聚合 | **聚类+图引导** |
| **隐私保护** | 无 | 多种方案 | **差分隐私保护** |
| **项目定位** | 基础版本 | 实验平台 | **专业Top-k+EF21** |

## 📈 性能特点

### 通信效率
- **压缩比**: 90%+ 通信减少 (Top-k=0.1)
- **智能选择**: 只上传重要梯度
- **零梯度优化**: 跳过无效计算

### 模型性能
- **EF21增强**: 错误反馈提升收敛
- **自适应调整**: 动态优化压缩比
- **聚合优化**: 聚类+图引导聚合

## 🛠️ 开发说明

### 核心模块
1. **TopKEF21Optimizer**: Top-k+EF21压缩核心
2. **ImprovedClusteringAggregation**: 智能聚合策略
3. **FedEngine**: 联邦学习引擎

### 扩展方向
- [ ] 更多压缩算法集成
- [ ] 高级聚合策略
- [ ] 更强隐私保护机制
- [ ] 异构环境适配

## 📊 日志和结果

- **训练日志**: `log/` 目录
- **实验结果**: `sh_result/` 目录
- **压缩统计**: 内置详细统计信息

---

**注意**: 此项目专门用于Top-k+EF21稀疏上传策略的研究和实验，采用全物品嵌入模式，确保实验结果的清晰性和可比较性。

# 隐私保护真稀疏GPFedRec

基于GPFedRec的改进联邦推荐算法，集成了真稀疏通信、聚类图聚合、自适应正则化和隐私保护等创新技术。

## 🚀 核心改进

### 1. 真稀疏参数上传
- **通信效率提升**: 减少75-80%的通信量
- **稀疏率**: 20% (仅上传用户交互的物品嵌入)
- **零向量填充**: 非交互物品使用零向量

### 2. 聚类后图聚合  
- **聚类数量**: 5-10个用户簇
- **图聚合**: 在簇内进行消息传递
- **零向量敏感性**: 解决传统图聚合的零向量问题

### 3. 用户自适应正则化
- **策略**: 根据用户交互数量调整正则化系数
- **范围**: reg_min=0.1, reg_max=2.0
- **效果**: 平衡个性化学习和全局知识

### 4. 隐私保护机制
- **虚假物品填充**: 50%的隐私保护比例
- **自适应策略**: proportional填充策略
- **隐私与性能**: 在保护隐私的同时维持推荐性能

## 📊 实验结果对比

| 算法 | Hit Ratio@10 | NDCG@10 | 提升率 |
|------|-------------|---------|--------|
| 原始GPFedRec | 0.6416 | 0.3996 | - |
| **改进GPFedRec** | **0.6744** | **0.3824** | **HR: +5.11%** |

### 性能分析
- ✅ **Hit Ratio提升**: +5.11% (0.6416 → 0.6744)
- ⚠️ **NDCG略降**: -4.31% (0.3996 → 0.3824)
- 🔒 **隐私保护**: 45.6%的虚假物品填充
- 📡 **通信效率**: 减少约80%的参数传输

## 🏃‍♂️ 快速开始

### 环境要求
```bash
Python 3.8+
PyTorch 1.8+
pandas, numpy, scikit-learn
```

### 基础训练
```bash
# 标准150轮训练
python train.py --dataset 100k --num_round 150 --lr 0.1

# 快速测试 (10轮)
python train.py --dataset 100k --num_round 10 --lr 0.1
```

### 自定义参数
```bash
python train.py --dataset 100k --num_round 150 --lr 0.1 \
    --adaptive_reg user \
    --privacy_method differential_privacy \
    # GPFedRec-TopkEF21专用全物品嵌入模式 \
    # 聚合方法固定为clustering_then_graph \
    --n_clusters 5 \
    --dp 1e-6
```

## 📁 项目结构

```
GPFedRec-opt_version/
├── train.py                                    # 主训练脚本
├── engine.py                                   # 改进算法引擎
├── mlp.py                                      # MLP模型定义
├── data.py                                     # 数据处理
├── utils.py                                    # 工具函数 (包含改进功能)
├── metrics.py                                  # 评估指标
├── improved_clustering_aggregation.py          # 聚类聚合算法
├── data/100k/ratings.dat                      # MovieLens-100K数据
├── sh_result/                                  # 实验结果
└── log/                                        # 训练日志
```

## 🔧 主要参数说明

### 模型参数
- `--latent_dim`: 嵌入维度 (默认: 32)
- `--layers`: MLP层结构 (默认: [64,32,16,8])
- `--lr`: 学习率 (默认: 0.1)

### 联邦学习参数
- `--num_round`: 训练轮数 (默认: 150)
- `--clients_sample_ratio`: 客户端采样比例 (默认: 1.0)
- `--local_epoch`: 本地训练轮数 (默认: 1)

### 改进算法参数
- `--adaptive_reg`: 正则化策略 ['none', 'user'] (默认: 'user')
- GPFedRec-TopkEF21专用全物品嵌入模式（无需配置）
- 聚合方法: `clustering_then_graph` (固定启用)
- `--privacy_protection`: 启用隐私保护 (默认: True)
- `--n_clusters`: 聚类数量 (默认: 5)

## 📈 实验记录

### 最新实验 (2025-06-02)
- **数据集**: MovieLens-100K
- **训练轮数**: 150轮
- **最佳结果**: HR@10=0.6744, NDCG@10=0.3824
- **最佳轮次**: 第131轮

## 🎯 核心创新点

1. **真稀疏联邦学习**: 首次在联邦推荐中实现真正的稀疏参数传输
2. **聚类图聚合**: 解决零向量对图聚合的负面影响
3. **自适应正则化**: 根据用户特征动态调整正则化强度
4. **隐私保护机制**: 虚假物品填充提供额外的隐私保障

## 📚 技术特点

- **通信高效**: 真稀疏上传减少通信开销
- **性能提升**: 在保持隐私的同时提升推荐性能
- **鲁棒性强**: 聚类聚合增强算法稳定性
- **隐私友好**: 多层隐私保护机制

---

**开发者**: 郑嘉兴  
**联系方式**: 2024021015@stu.cdut.edu.cn 
**项目日期**: 2025年6月

# GPFedRec-improved

改进版GPFedRec联邦推荐系统，集成Top-k稀疏化与EF21错误反馈优化。

## 主要改进

1. **Top-k稀疏化**: 对梯度进行Top-k压缩，减少通信开销
2. **EF21错误反馈**: 补偿压缩误差，提升收敛性
3. **自适应Top-k**: 根据性能动态调整压缩比例
4. **隐私保护**: 支持差分隐私、微分隐私等多种隐私保护机制

## 使用方法

### 稀疏物品嵌入模式（默认）
先进行物品级稀疏化，再进行Top-k+EF21压缩：
```bash
python train.py --use_topk_ef21 True --topk_ratio 0.1 --ef21_warmup_rounds 3 --privacy_method differential_privacy --dp 1e-06 --clients_sample_ratio 1.0 --lr 0.1 --num_round 50 --mp_layers 2
```

### 全物品嵌入模式
关闭稀疏上传，直接对完整物品嵌入进行Top-k+EF21压缩：
```bash
python train.py --use_topk_ef21 True --topk_ratio 0.1 --ef21_warmup_rounds 3 --privacy_method differential_privacy --dp 1e-06 --clients_sample_ratio 1.0 --lr 0.1 --num_round 50 --mp_layers 2
```

## 参数说明

- GPFedRec-TopkEF21专用全物品嵌入模式（自动启用）
  - `True`: 稀疏物品嵌入模式，先物品级稀疏化再Top-k压缩
  - `False`: 全物品嵌入模式，直接对完整物品嵌入进行Top-k压缩
- `--use_topk_ef21`: 是否启用Top-k+EF21优化
- `--topk_ratio`: Top-k比例（0.1表示保留10%的梯度）
- `--ef21_warmup_rounds`: EF21预热轮数
- `--adaptive_topk`: 是否启用自适应Top-k调整

## 模式对比

| 模式 | 通信开销 | 理论收敛性 | 实现复杂度 |
|------|----------|------------|------------|
| 稀疏物品嵌入 | 98.8%减少 | 良好 | 中等 |
| 全物品嵌入 | ~90%减少 | 最佳 | 简单 |
