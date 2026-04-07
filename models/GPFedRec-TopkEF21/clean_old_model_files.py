#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理多余的历史模型文件
只保留：
- best_model_latest.pth (全局最佳模型)
- final_model.pth (最终完整模型)
- model_info.txt (模型信息)

删除：
- best_model_round_*.pth (每轮的模型文件)
"""

import os
import glob
import logging
from pathlib import Path

def clean_model_directory(model_dir):
    """清理指定目录下的多余模型文件"""
    if not os.path.exists(model_dir):
        print(f"目录不存在: {model_dir}")
        return
    
    print(f"正在清理目录: {model_dir}")
    
    # 查找所有 best_model_round_*.pth 文件
    round_model_pattern = os.path.join(model_dir, "best_model_round_*.pth")
    round_model_files = glob.glob(round_model_pattern)
    
    if not round_model_files:
        print("  ✅ 没有找到需要删除的 best_model_round_*.pth 文件")
        return
    
    print(f"  📁 找到 {len(round_model_files)} 个轮次模型文件:")
    for file_path in round_model_files:
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path) / 1024  # KB
        print(f"    - {file_name} ({file_size:.1f} KB)")
    
    # 询问用户确认
    confirm = input(f"  ❓ 确定要删除这 {len(round_model_files)} 个文件吗？(y/N): ")
    if confirm.lower() != 'y':
        print("  ❌ 取消删除操作")
        return
    
    # 删除文件
    deleted_count = 0
    total_size = 0
    for file_path in round_model_files:
        try:
            file_size = os.path.getsize(file_path)
            os.remove(file_path)
            deleted_count += 1
            total_size += file_size
            print(f"    ✅ 已删除: {os.path.basename(file_path)}")
        except Exception as e:
            print(f"    ❌ 删除失败: {os.path.basename(file_path)} - {e}")
    
    print(f"  🎉 清理完成! 删除了 {deleted_count} 个文件，节省空间 {total_size/1024:.1f} KB")
    
    # 显示保留的文件
    print("  📋 保留的文件:")
    for keep_file in ['best_model_latest.pth', 'final_model.pth', 'model_info.txt']:
        keep_path = os.path.join(model_dir, keep_file)
        if os.path.exists(keep_path):
            file_size = os.path.getsize(keep_path) / 1024  # KB
            print(f"    ✅ {keep_file} ({file_size:.1f} KB)")
        else:
            print(f"    ⚪ {keep_file} (不存在)")

def main():
    """主函数"""
    print("=" * 60)
    print("🧹 GPFedRec-TopkEF21 模型文件清理工具")
    print("=" * 60)
    print("此工具将删除历史的 best_model_round_*.pth 文件")
    print("只保留全局最佳模型和最终模型文件")
    print()
    
    # 查找 models-storage 目录下的所有模型目录
    models_storage_path = "../../models-storage"
    if not os.path.exists(models_storage_path):
        print(f"❌ models-storage 目录不存在: {models_storage_path}")
        return
    
    # 查找所有 GPFedRec 模型目录
    model_dirs = []
    for item in os.listdir(models_storage_path):
        item_path = os.path.join(models_storage_path, item)
        if os.path.isdir(item_path) and item.startswith('GPFedRec'):
            model_dirs.append(item_path)
    
    if not model_dirs:
        print("❌ 没有找到任何 GPFedRec 模型目录")
        return
    
    print(f"📁 找到 {len(model_dirs)} 个模型目录:")
    for i, model_dir in enumerate(model_dirs, 1):
        dir_name = os.path.basename(model_dir)
        print(f"  {i}. {dir_name}")
    
    print()
    choice = input("选择操作: (a)全部清理 / (数字)清理指定目录 / (q)退出: ")
    
    if choice.lower() == 'q':
        print("👋 退出程序")
        return
    elif choice.lower() == 'a':
        print("🚀 开始清理所有目录...")
        for model_dir in model_dirs:
            print()
            clean_model_directory(model_dir)
    elif choice.isdigit():
        index = int(choice) - 1
        if 0 <= index < len(model_dirs):
            print(f"🚀 开始清理目录: {os.path.basename(model_dirs[index])}")
            clean_model_directory(model_dirs[index])
        else:
            print("❌ 无效的目录编号")
    else:
        print("❌ 无效的选择")
    
    print()
    print("=" * 60)
    print("✅ 清理工具执行完成!")
    print("=" * 60)

if __name__ == "__main__":
    main() 