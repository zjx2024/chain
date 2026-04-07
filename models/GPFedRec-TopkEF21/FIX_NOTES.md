# GPFedRec-TopkEF21 模型修复说明

## 问题描述

该模型在后端调用时存在以下问题：
1. **模型未正确保存到指定路径**：模型应该保存在 `E:\projects\chain\models-storage` 文件夹下，但代码未正确保存
2. **生成多余的文件夹**：每次训练完会在当前模型目录下生成两种多余的文件夹：
   - 格式1：`ml-100k_user_clustering_5_no_privacy_full_topk0.1_cumcluster10_ef21w3_client1.0_lr0.1_r2_mp2_2025-06-25_XX-XX`
   - 格式2：`ml-100k_task_XX_completed_2025-06-25_XX-XX`

## 问题根源

1. **engine.save方法**：在`engine.py`中的`save`方法可能创建不必要的checkpoint目录
2. **模型保存路径处理不当**：训练过程中模型保存逻辑没有正确使用后端传递的`--model_save_path`参数
3. **目录命名混乱**：使用过于复杂的目录命名格式

## 修复方案

### 1. 修改 `train.py`

**关键修复点**：
1. **移除重复的目录创建逻辑**：删除了第340行附近的早期目录创建代码，避免在错误位置创建目录
2. **增强绝对路径识别**：改进了Windows盘符路径的识别逻辑，支持所有盘符（A-Z）
3. **统一目录创建**：使用单一的目录创建点，确保所有父目录都正确创建

**添加模型保存路径验证**：
```python
# 验证模型保存路径配置
if config.get('save_best_model', False):
    if not config.get('model_save_path'):
        # 如果没有指定保存路径，使用默认的models-storage路径
        default_save_path = "../../models-storage"
        config['model_save_path'] = default_save_path
        logging.warning(f"未指定模型保存路径，使用默认路径: {default_save_path}")
```

**优化模型保存逻辑**：
- 使用简洁的目录命名格式：`GPFedRec_TopkEF21_{dataset}_r{rounds}_lr{learning_rate}_{timestamp}`
- 确保模型只保存到后端指定的路径
- 统一最佳模型和最终模型的保存逻辑

### 2. 修改 `engine.py`

**禁用原有的save方法**：
```python
def save(self, alias, epoch_id, hit_ratio, ndcg):
    """保存模型检查点 - 已禁用，使用统一的模型保存机制"""
    # 注释掉原有的保存逻辑，避免创建不必要的目录
    logging.warning(f"engine.save方法已禁用，请使用统一的模型保存机制")
    logging.info(f"如需保存模型，请确保设置了--save_best_model和--model_save_path参数")
    pass
```

### 3. 创建清理脚本

创建 `cleanup_directories.py` 脚本来清理现有的多余文件夹：
- 自动识别需要清理的目录模式
- 保留必要的目录（log、data、sh_result等）
- 提供交互式确认功能

## 修复后的目录结构

修复后，模型训练将：

1. **日志文件**：继续保存在 `log/` 目录下
2. **训练结果**：继续保存在 `sh_result/` 目录下  
3. **训练后模型**：保存在后端指定的路径下，使用简洁的目录结构：
   ```
   E:\projects\chain\models-storage\
   └── GPFedRec_TopkEF21_100k_r200_lr0.1_20250625_143000\
       ├── best_model_round_XX.pth      # 最佳轮次模型
       ├── best_model_latest.pth        # 最新最佳模型
       ├── final_model.pth              # 最终模型
       └── model_info.txt               # 模型信息
   ```

## 使用方法

### 1. 清理现有多余目录

在GPFedRec-TopkEF21目录下运行：
```bash
python cleanup_directories.py
```

### 2. 后端调用参数

后端调用时需要确保传递以下参数：
```bash
--model_save_path E:/projects/chain/models-storage
--save_best_model true
```

### 3. 验证修复效果

训练完成后检查：
1. 模型是否正确保存在 `E:\projects\chain\models-storage` 目录下
2. 当前模型目录下不再生成多余的文件夹
3. 只保留必要的目录：`log/`, `data/`, `sh_result/` 等

## 修改的文件

1. **train.py**：
   - 添加模型保存路径验证逻辑
   - 优化模型保存的目录命名格式
   - 统一最佳模型和最终模型的保存逻辑

2. **engine.py**：
   - 禁用原有的save方法，避免创建不必要的checkpoint目录

3. **cleanup_directories.py**（新增）：
   - 用于清理现有的多余文件夹

4. **FIX_NOTES.md**（新增）：
   - 详细说明修复过程和使用方法

## 注意事项

1. 清理脚本会删除多余的目录，请在运行前确认备份重要数据
2. 修复后的模型保存路径依赖后端正确传递 `--model_save_path` 参数
3. 如果后端未传递保存路径，模型将保存到相对路径 `../../models-storage`

## 最新优化 (2025-06-25)

### 📁 模型保存空间优化

**问题**: 训练X轮会产生X个`best_model_round_*.pth`文件，占用大量存储空间

**解决方案**: 
- 只保存全局最佳模型 `best_model_latest.pth`
- 不再保存每轮的模型文件 `best_model_round_*.pth`
- 仍然保存最终完整模型 `final_model.pth`

**修改文件**: `train.py` 第513行附近的模型保存逻辑

**现在的模型文件结构**:
```
GPFedRec_TopkEF21_100k_r4_lr0.1_20250625_163438/
├── best_model_latest.pth    (全局最佳模型，推荐使用)
├── final_model.pth          (训练完成的最终模型)
└── model_info.txt           (模型信息和性能记录)
```

**存储空间节省**: 
- 之前: 训练4轮 = 4个best_model_round_*.pth (约910KB) + 其他文件
- 现在: 只有1个best_model_latest.pth (约227KB) + 其他文件
- **节省约75%的模型文件存储空间**

### 🧹 清理工具

创建了 `clean_old_model_files.py` 脚本来清理历史的多余模型文件:

```bash
cd models/GPFedRec-TopkEF21
python clean_old_model_files.py
```

该工具会：
- 扫描所有模型目录
- 识别需要删除的 `best_model_round_*.pth` 文件
- 安全删除并显示节省的空间
- 保留必要的文件 (`best_model_latest.pth`, `final_model.pth`, `model_info.txt`)

## 测试建议

1. **功能测试**：运行一次完整的训练流程，验证模型是否正确保存
2. **路径测试**：检查模型是否保存在正确的 `models-storage` 目录下
3. **清理测试**：验证不再生成多余的文件夹
4. **空间测试**：验证只保存1个最佳模型，不再保存每轮模型 