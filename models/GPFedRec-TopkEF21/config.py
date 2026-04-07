# -*- coding: utf-8 -*-
"""
GPFedRec-TopkEF21 配置文件
专门用于Top-k+EF21稀疏上传策略的联邦推荐系统配置
"""

# ===== 默认配置 =====
DEFAULT_CONFIG = {
    # 基础参数
    'dataset': '100k',
    'num_round': 200,
    'clients_sample_ratio': 1.0,
    'lr': 0.1,
    
    # Top-k+EF21 核心参数（固定启用）
    'topk_ratio': 0.1,
    'ef21_weight': 3,
    'ef21_warmup_rounds': 5,
    
    # 聚合策略（固定为聚类后图聚合）
    'n_clusters': 5,
    'adaptive_reg': 'user',
    
    # 隐私保护
    'privacy_method': 'none',
    'dp': 1e-6,
    
    # 模型参数
    'embedding_dim': 64,
    'hidden_dim': 128,
    'dropout': 0.1,
}

# ===== 实验配置模板 =====
EXPERIMENT_CONFIGS = {
    # 无隐私保护实验
    'topk_no_privacy': {
        **DEFAULT_CONFIG,
        'privacy_method': 'none',
        'experiment_name': 'Top-k+EF21无隐私保护实验'
    },
    
    # 差分隐私实验（轻量级）
    'topk_lightweight_dp': {
        **DEFAULT_CONFIG,
        'privacy_method': 'differential_privacy',
        'dp': 1e-8,  # 更轻量的差分隐私
        'experiment_name': 'Top-k+EF21轻量差分隐私实验'
    },
    
    # 差分隐私实验
    'topk_differential_privacy': {
        **DEFAULT_CONFIG,
        'privacy_method': 'differential_privacy',
        'dp': 1e-6,
        'experiment_name': 'Top-k+EF21差分隐私实验'
    },
    
    # 强化差分隐私实验
    'topk_strong_dp': {
        **DEFAULT_CONFIG,
        'privacy_method': 'differential_privacy',
        'dp': 1e-5,  # 更强的差分隐私
        'experiment_name': 'Top-k+EF21强化差分隐私实验'
    },
    
    # 高压缩比实验
    'topk_high_compression': {
        **DEFAULT_CONFIG,
        'topk_ratio': 0.05,  # 更高的压缩比
        'ef21_weight': 5,
        'experiment_name': 'Top-k+EF21高压缩比实验'
    },
    
    # 中等压缩比实验
    'topk_medium_compression': {
        **DEFAULT_CONFIG,
        'topk_ratio': 0.15,  # 中等压缩比
        'ef21_weight': 4,
        'experiment_name': 'Top-k+EF21中等压缩比实验'
    },
}

# ===== Top-k+EF21 专用配置 =====
TOPK_EF21_CONFIG = {
    # 压缩相关
    'compression_threshold': 1e-6,  # 梯度阈值
    
    # EF21相关
    'ef21_momentum': 0.9,           # EF21动量
    'error_feedback_decay': 0.99,   # 错误反馈衰减
    'compression_warmup': 5,        # 压缩预热轮数
    
    # 统计相关
    'log_compression_stats': True,  # 记录压缩统计
    'stats_interval': 10,           # 统计间隔
    'save_compression_history': True,  # 保存压缩历史
}

# ===== 隐私保护配置 =====
PRIVACY_CONFIGS = {
    'none': {
        'description': '无隐私保护',
        'params': {}
    },
    'differential_privacy': {
        'description': '差分隐私保护',
        'params': {
            'dp': 1e-6,
            'noise_multiplier': 1.0,
            'clipping_bound': 1.0
        }
    }
}

# ===== 聚合策略配置（固定为聚类后图聚合）=====
CLUSTERING_GRAPH_CONFIG = {
    'description': '聚类+图引导聚合',
    'params': {
        'n_clusters': 5,
        'clustering_method': 'kmeans',
        'graph_regularization': True,
        'adaptive_reg': 'user'
    }
}

def get_experiment_config(experiment_name):
    """获取实验配置"""
    if experiment_name in EXPERIMENT_CONFIGS:
        return EXPERIMENT_CONFIGS[experiment_name].copy()
    else:
        raise ValueError(f"未知的实验配置: {experiment_name}")

def get_privacy_config(privacy_method):
    """获取隐私保护配置"""
    if privacy_method in PRIVACY_CONFIGS:
        return PRIVACY_CONFIGS[privacy_method].copy()
    else:
        raise ValueError(f"未知的隐私保护方法: {privacy_method}")

def get_clustering_graph_config():
    """获取聚类后图聚合配置（固定策略）"""
    return CLUSTERING_GRAPH_CONFIG.copy()

def print_available_configs():
    """打印所有可用配置"""
    print("🎯 GPFedRec-TopkEF21 可用配置:")
    print("\n📊 实验配置:")
    for name, config in EXPERIMENT_CONFIGS.items():
        print(f"  - {name}: {config['experiment_name']}")
    
    print("\n🔒 隐私保护方法:")
    for name, config in PRIVACY_CONFIGS.items():
        print(f"  - {name}: {config['description']}")
    
    print("\n🔄 聚合策略:")
    print(f"  - clustering_then_graph: {CLUSTERING_GRAPH_CONFIG['description']} (固定启用)")

if __name__ == "__main__":
    print_available_configs() 