#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GPFedRec-TopkEF21 主入口脚本
专门用于Top-k+EF21稀疏上传策略的联邦推荐系统

使用方法:
    python main.py --config topk_no_privacy
    python main.py --config topk_differential_privacy --num_round 400
    python main.py --list-configs  # 查看所有可用配置
"""

import argparse
import sys
import os
from config import (
    get_experiment_config, 
    print_available_configs, 
    EXPERIMENT_CONFIGS,
    DEFAULT_CONFIG
)

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='GPFedRec-TopkEF21: 基于Top-k+EF21的联邦推荐系统',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python main.py --config topk_no_privacy
  python main.py --config topk_differential_privacy --num_round 400
  python main.py --list-configs
        """
    )
    
    parser.add_argument('--config', type=str, 
                       choices=list(EXPERIMENT_CONFIGS.keys()),
                       help='实验配置名称')
    
    parser.add_argument('--list-configs', action='store_true',
                       help='列出所有可用的实验配置')
    
    # 允许覆盖配置参数
    parser.add_argument('--dataset', type=str, default=None,
                       help='数据集名称 (默认: 100k)')
    parser.add_argument('--num_round', type=int, default=None,
                       help='训练轮数 (默认: 200)')
    parser.add_argument('--clients_sample_ratio', type=float, default=None,
                       help='客户端采样比例 (默认: 1.0)')
    parser.add_argument('--lr', type=float, default=None,
                       help='学习率 (默认: 0.1)')
    parser.add_argument('--topk_ratio', type=float, default=None,
                       help='Top-k压缩比例 (默认: 0.1)')
    parser.add_argument('--ef21_weight', type=int, default=None,
                       help='EF21权重参数 (默认: 3)')
    parser.add_argument('--n_clusters', type=int, default=None,
                       help='聚类数量 (默认: 5)')
    parser.add_argument('--privacy_method', type=str, default=None,
                       choices=['none', 'differential_privacy'],
                       help='隐私保护方法：无保护或差分隐私')
    parser.add_argument('--dp', type=float, default=None,
                       help='差分隐私参数')
    
    return parser.parse_args()

def build_train_command(config):
    """构建训练命令"""
    cmd_parts = ['python', 'train.py']
    
    # 添加所有配置参数
    for key, value in config.items():
        if key == 'experiment_name':
            continue  # 跳过实验名称
        
        if isinstance(value, bool):
            cmd_parts.append(f'--{key}')
            cmd_parts.append(str(value))
        else:
            cmd_parts.append(f'--{key}')
            cmd_parts.append(str(value))
    
    return cmd_parts

def main():
    args = parse_args()
    
    # 显示可用配置
    if args.list_configs:
        print_available_configs()
        return
    
    # 检查是否指定了配置
    if not args.config:
        print("❌ 错误: 请指定实验配置 (使用 --config 参数)")
        print("💡 提示: 使用 --list-configs 查看所有可用配置")
        sys.exit(1)
    
    # 获取基础配置
    try:
        config = get_experiment_config(args.config)
    except ValueError as e:
        print(f"❌ 错误: {e}")
        print("💡 提示: 使用 --list-configs 查看所有可用配置")
        sys.exit(1)
    
    # 覆盖命令行参数
    override_params = {}
    for param in ['dataset', 'num_round', 'clients_sample_ratio', 'lr', 
                  'topk_ratio', 'ef21_weight', 'n_clusters', 'privacy_method',
                  'dp']:
        value = getattr(args, param)
        if value is not None:
            override_params[param] = value
    
    # 应用覆盖参数
    config.update(override_params)
    
    # 显示实验信息
    print("🎯 GPFedRec-TopkEF21 实验启动!")
    print(f"📊 实验配置: {config.get('experiment_name', args.config)}")
    print(f"🔧 核心参数:")
    print(f"   - 数据集: {config['dataset']}")
    print(f"   - 训练轮数: {config['num_round']}")
    print(f"   - 客户端比例: {config['clients_sample_ratio']}")
    print(f"   - Top-k比例: {config['topk_ratio']}")
    print(f"   - EF21权重: {config['ef21_weight']}")
    print(f"   - 隐私方法: {config['privacy_method']}")
    print(f"   - 聚合策略: clustering_then_graph (固定启用)")
    print()
    
    # 构建并执行训练命令
    cmd_parts = build_train_command(config)
    
    print("🚀 执行命令:")
    print(" ".join(cmd_parts))
    print()
    
    # 执行训练
    os.system(" ".join(cmd_parts))

if __name__ == "__main__":
    main() 