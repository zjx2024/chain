#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GPFedRec-TopkEF21 路径处理修复验证脚本
用于测试修复后的绝对路径处理逻辑
"""

import os
import sys

def test_path_processing():
    """测试路径处理逻辑"""
    print("=" * 60)
    print("GPFedRec-TopkEF21 路径处理修复验证")
    print("=" * 60)
    
    # 测试用例
    test_paths = [
        "E:/projects/chain/models-storage",
        "e:/projects/chain/models-storage", 
        "E:\\projects\\chain\\models-storage",
        "../../models-storage",
        "/absolute/unix/path",
        "relative/path",
        "C:/Windows/System32",
        "D:/Data/Models"
    ]
    
    print(f"当前工作目录: {os.getcwd()}")
    print(f"脚本所在目录: {os.path.dirname(os.path.abspath(__file__))}")
    print()
    
    for i, test_path in enumerate(test_paths, 1):
        print(f"测试 {i}: {test_path}")
        
        # 模拟train.py中的路径处理逻辑
        model_save_path = test_path
        
        # 标准化路径分隔符
        model_save_path = model_save_path.replace('\\', '/')
        print(f"  标准化分隔符: {model_save_path}")
        
        # 检查是否为绝对路径
        is_abs_before = os.path.isabs(model_save_path)
        print(f"  原始识别为绝对路径: {is_abs_before}")
        
        if not is_abs_before:
            # 检查Windows盘符
            if model_save_path.lower().startswith(('a:/', 'b:/', 'c:/', 'd:/', 'e:/', 'f:/', 'g:/', 'h:/', 'i:/', 'j:/', 'k:/', 'l:/', 'm:/', 'n:/', 'o:/', 'p:/', 'q:/', 'r:/', 's:/', 't:/', 'u:/', 'v:/', 'w:/', 'x:/', 'y:/', 'z:/')):
                model_save_path = os.path.normpath(model_save_path)
                print(f"  Windows绝对路径处理: {model_save_path}")
            else:
                model_save_path = os.path.abspath(model_save_path)
                print(f"  转换为绝对路径: {model_save_path}")
        
        # 最终标准化
        model_save_path = os.path.normpath(model_save_path)
        print(f"  最终路径: {model_save_path}")
        
        # 验证最终结果
        final_is_abs = os.path.isabs(model_save_path)
        print(f"  最终是否为绝对路径: {final_is_abs}")
        
        # 检查是否在当前工作目录下
        current_dir = os.path.abspath(os.getcwd())
        is_under_current = model_save_path.startswith(current_dir)
        print(f"  是否在当前工作目录下: {is_under_current}")
        
        print("-" * 40)
    
    print("测试完成！")
    print("\n预期结果:")
    print("- 所有路径应该被正确识别为绝对路径")
    print("- E:/projects/chain/models-storage 类型的路径不应该在当前工作目录下")
    print("- 相对路径会被转换为基于当前工作目录的绝对路径")

def test_directory_creation():
    """测试目录创建逻辑"""
    print("\n" + "=" * 60)
    print("目录创建测试")
    print("=" * 60)
    
    test_base_paths = [
        "E:/projects/chain/models-storage",
        "../../models-storage"
    ]
    
    for base_path in test_base_paths:
        print(f"\n测试基础路径: {base_path}")
        
        # 模拟完整的目录处理
        model_save_path = base_path.replace('\\', '/')
        
        if not os.path.isabs(model_save_path):
            if model_save_path.lower().startswith(('a:/', 'b:/', 'c:/', 'd:/', 'e:/', 'f:/', 'g:/', 'h:/', 'i:/', 'j:/', 'k:/', 'l:/', 'm:/', 'n:/', 'o:/', 'p:/', 'q:/', 'r:/', 's:/', 't:/', 'u:/', 'v:/', 'w:/', 'x:/', 'y:/', 'z:/')):
                model_save_path = os.path.normpath(model_save_path)
            else:
                model_save_path = os.path.abspath(model_save_path)
        
        model_save_path = os.path.normpath(model_save_path)
        
        if os.path.splitext(model_save_path)[1]:
            save_dir = os.path.dirname(model_save_path)
        else:
            save_dir = model_save_path
        
        # 模拟创建子目录
        model_dir_name = "GPFedRec_TopkEF21_100k_r1_lr0.1_20250625_TEST"
        full_model_dir = os.path.join(save_dir, model_dir_name)
        
        print(f"  处理后的基础路径: {save_dir}")
        print(f"  完整模型目录: {full_model_dir}")
        print(f"  是否为绝对路径: {os.path.isabs(full_model_dir)}")
        print(f"  与当前目录的关系: {'在当前目录下' if full_model_dir.startswith(os.path.abspath(os.getcwd())) else '不在当前目录下'}")

if __name__ == "__main__":
    test_path_processing()
    test_directory_creation() 