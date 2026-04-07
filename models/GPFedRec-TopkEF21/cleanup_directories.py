#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GPFedRec-TopkEF21 目录清理脚本
用于清理训练过程中生成的多余目录
"""

import os
import shutil
import re
from datetime import datetime

def cleanup_directories():
    """清理当前目录下的多余文件夹"""
    current_dir = os.getcwd()
    print(f"当前目录: {current_dir}")
    
    # 需要清理的目录模式
    patterns_to_clean = [
        # 以日志文件名命名的长目录
        r'^ml-100k_user_clustering_\d+_.*_\d{4}-\d{2}-\d{2}_\d{2}-\d{2}$',
        # task_completed格式的目录
        r'^ml-100k_task_\d+_completed_\d{4}-\d{2}-\d{2}_\d{2}-\d{2}$',
        # checkpoints目录
        r'^checkpoints$'
    ]
    
    # 需要保留的目录
    keep_dirs = {
        'log',           # 日志目录
        'data',          # 数据目录
        'sh_result',     # 结果目录
        '__pycache__',   # Python缓存（可选保留）
        '.idea',         # IDE配置（可选保留）
    }
    
    # 扫描当前目录
    items = os.listdir(current_dir)
    dirs_to_clean = []
    
    for item in items:
        item_path = os.path.join(current_dir, item)
        
        # 只处理目录
        if os.path.isdir(item_path):
            # 检查是否在保留列表中
            if item in keep_dirs:
                print(f"保留目录: {item}")
                continue
            
            # 检查是否匹配需要清理的模式
            should_clean = False
            for pattern in patterns_to_clean:
                if re.match(pattern, item):
                    should_clean = True
                    break
            
            if should_clean:
                dirs_to_clean.append(item)
    
    # 显示将要清理的目录
    if dirs_to_clean:
        print(f"\n发现 {len(dirs_to_clean)} 个需要清理的目录:")
        for i, dir_name in enumerate(dirs_to_clean, 1):
            print(f"  {i}. {dir_name}")
        
        # 询问用户是否确认清理
        response = input(f"\n是否确认清理这些目录? (y/N): ").strip().lower()
        
        if response in ['y', 'yes']:
            print("\n开始清理...")
            cleaned_count = 0
            
            for dir_name in dirs_to_clean:
                try:
                    dir_path = os.path.join(current_dir, dir_name)
                    shutil.rmtree(dir_path)
                    print(f"✅ 已删除: {dir_name}")
                    cleaned_count += 1
                except Exception as e:
                    print(f"❌ 删除失败 {dir_name}: {e}")
            
            print(f"\n清理完成! 共删除 {cleaned_count}/{len(dirs_to_clean)} 个目录")
        else:
            print("清理操作已取消")
    else:
        print("\n没有发现需要清理的目录")

def show_directory_summary():
    """显示目录摘要信息"""
    current_dir = os.getcwd()
    items = os.listdir(current_dir)
    
    print("\n📁 当前目录内容摘要:")
    print("=" * 50)
    
    dirs = []
    files = []
    
    for item in items:
        item_path = os.path.join(current_dir, item)
        if os.path.isdir(item_path):
            dirs.append(item)
        else:
            files.append(item)
    
    print(f"目录数量: {len(dirs)}")
    if dirs:
        for d in sorted(dirs):
            print(f"  📁 {d}")
    
    print(f"\n文件数量: {len(files)}")
    if files:
        for f in sorted(files):
            print(f"  📄 {f}")

if __name__ == "__main__":
    print("GPFedRec-TopkEF21 目录清理工具")
    print("=" * 50)
    
    # 显示当前目录状态
    show_directory_summary()
    
    # 执行清理
    cleanup_directories()
    
    # 显示清理后的状态
    print("\n" + "=" * 50)
    print("清理后的目录状态:")
    show_directory_summary() 