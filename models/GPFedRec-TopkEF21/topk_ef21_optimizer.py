"""
Top-k稀疏化与EF21错误反馈优化器
GPFedRec-TopkEF21专用Top-k+EF21智能压缩优化器
"""
import torch
import numpy as np
import logging
from typing import Dict, Any, Tuple, Optional

class TopKEF21Optimizer:
    """Top-k稀疏化与EF21错误反馈优化器"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        # use_topk_ef21固定为True（项目专用功能）
        self.topk_ratio = config.get('topk_ratio', 0.1)
        self.ef21_warmup_rounds = config.get('ef21_warmup_rounds', 3)
        self.disable_ef21 = config.get('disable_ef21', False)
        # GPFedRec-TopkEF21专用全物品嵌入模式，使用固定Top-k比例
        
        # EF21状态存储
        self.error_feedback = {}  # 每个用户的错误反馈
        self.last_compressed = {}  # 上次压缩的梯度
        self.compression_stats = {}  # 压缩统计信息
        
        # 使用固定Top-k比例，无需性能监控
        
        # Top-k+EF21优化器（固定启用）
        logging.info(f"✅ Top-k+EF21优化器已启用")
        logging.info(f"  - 初始Top-k比例: {self.topk_ratio*100:.1f}%")
        if self.disable_ef21:
            logging.info("  - EF21错误反馈: ❌ 已禁用")
        else:
            logging.info(f"  - EF21预热轮数: {self.ef21_warmup_rounds}")
        logging.info(f"  - 固定Top-k比例: {self.topk_ratio*100:.1f}%")
    
    # 自适应Top-k功能已移除，使用固定Top-k比例
    
    def compress_gradients(self, gradients: Dict[str, torch.Tensor], user_id: int, round_id: int) -> Dict[str, Any]:
        """
        对梯度进行Top-k稀疏化压缩
        注意：这里的输入是已经经过物品级稀疏化的梯度（只包含用户交互的物品）
        """
        # Top-k+EF21压缩（固定启用）
        
        compressed_gradients = {}
        
        # 使用固定Top-k比例
        current_ratio = self.topk_ratio
        
        for param_name, grad_tensor in gradients.items():
            if param_name == 'embedding_item.weight':
                # 对物品嵌入梯度进行Top-k压缩，返回真正的稀疏表示
                topk_result = self._topk_compress_embeddings(
                    grad_tensor, current_ratio, user_id, param_name, round_id
                )
                
                # 使用新的稀疏格式
                compressed_gradients['embedding_item.weight'] = topk_result['compressed_embeddings']
                compressed_gradients['topk_indices'] = topk_result['topk_indices']
                compressed_gradients['original_shape'] = topk_result['original_shape']
                compressed_gradients['compression_info'] = {
                    'compression_ratio': topk_result['compression_ratio'],
                    'communication_reduction': topk_result['communication_reduction']
                }
            else:
                # 其他参数直接复制（或可以选择性压缩）
                compressed_gradients[param_name] = grad_tensor.clone()
        
        return compressed_gradients
    
    def _prepare_ef21_target(self, embeddings: torch.Tensor, user_id: int, 
                           param_name: str, use_ef21: bool) -> torch.Tensor:
        """
        准备EF21目标向量
        """
        # 首次初始化
        if param_name not in self.error_feedback[user_id]:
            self.error_feedback[user_id][param_name] = torch.zeros_like(embeddings)
            self.last_compressed[user_id][param_name] = torch.zeros_like(embeddings)
            return embeddings  # 首次使用普通压缩
        
        # 检查尺寸是否匹配
        last_shape = self.last_compressed[user_id][param_name].shape
        current_shape = embeddings.shape
        
        if last_shape == current_shape:
            # 尺寸匹配，正常使用EF21
            if use_ef21:
                return embeddings - self.last_compressed[user_id][param_name]
            else:
                return embeddings
        else:
            # 尺寸不匹配，重新初始化（主要用于稀疏模式下的动态物品数量变化）
            self.error_feedback[user_id][param_name] = torch.zeros_like(embeddings)
            self.last_compressed[user_id][param_name] = torch.zeros_like(embeddings)
            return embeddings
    
    def _topk_compress_embeddings(self, embeddings: torch.Tensor, k_ratio: float, 
                                 user_id: int, param_name: str, round_id: int) -> Dict[str, Any]:
        """
        对嵌入矩阵进行Top-k压缩，真正减少通信开销
        
        核心设计原则：
        1. Top-k比例永远基于本地全部嵌入数量计算（包括零梯度嵌入）
        2. EF21计算只针对有更新的嵌入进行，跳过零梯度嵌入以节省计算
        
        Args:
            embeddings: 形状为 [num_items, embedding_dim] 的嵌入矩阵
            k_ratio: Top-k比例（相对于全部嵌入）
            user_id: 用户ID
            param_name: 参数名称
            round_id: 轮次ID
        Returns:
            Dict包含压缩后的嵌入、索引和统计信息
        """
        # 是否使用EF21（考虑禁用标志和预热期）
        use_ef21 = not self.disable_ef21 and round_id >= self.ef21_warmup_rounds
        
        # 初始化EF21状态
        if user_id not in self.error_feedback:
            self.error_feedback[user_id] = {}
            self.last_compressed[user_id] = {}
        
        # 🔥 新增：智能梯度过滤，只对有意义的梯度进行EF21计算
        # 计算每个嵌入向量的L2范数，识别有意义的梯度
        embedding_norms = torch.norm(embeddings, dim=1)
        meaningful_threshold = 1e-6  # 梯度阈值，低于此值认为是零梯度
        meaningful_mask = embedding_norms > meaningful_threshold
        meaningful_indices = torch.where(meaningful_mask)[0]
        
        # 统计有意义的梯度数量
        total_items = embeddings.shape[0]
        meaningful_items = meaningful_indices.numel()
        zero_gradient_items = total_items - meaningful_items
        
        if meaningful_items == 0:
            # 所有梯度都为零，直接返回空结果
            logging.warning(f"用户{user_id}第{round_id}轮: 所有嵌入梯度为零，跳过压缩")
            return {
                'compressed_embeddings': torch.empty(0, embeddings.shape[1]),
                'topk_indices': [],
                'original_shape': embeddings.shape,
                'compression_ratio': 0.0,
                'communication_reduction': 1.0,
                'zero_gradient_items': zero_gradient_items,
                'meaningful_items': meaningful_items
            }
        
        # 🎯 关键优化：只对有意义的梯度进行EF21处理
        if use_ef21 and meaningful_items < total_items:
            # 部分梯度为零的情况，只对有意义的部分进行EF21
            target_for_compression = self._prepare_ef21_target_selective(
                embeddings, meaningful_indices, user_id, param_name, use_ef21
            )
        else:
            # 全部梯度有意义或不使用EF21的情况
            target_for_compression = self._prepare_ef21_target(
                embeddings, user_id, param_name, use_ef21
            )
        
        # 🎯 核心改进：Top-k比例永远基于全部嵌入，但EF21只针对有更新的嵌入
        # 1. 计算基于全部嵌入的Top-k数量
        k = max(1, int(total_items * k_ratio))  # 永远基于总嵌入数计算
        
        # 2. 计算所有嵌入的重要性分数（包括零梯度嵌入）
        # 对于零梯度的嵌入，重要性分数为0，但仍然参与Top-k选择
        importance_scores = torch.norm(target_for_compression, dim=1)
        
        # 3. 🔥 改进：优先选择有意义梯度，避免上传零梯度嵌入
        if meaningful_items >= k:
            # 有意义梯度足够，从中选择Top-k
            meaningful_importance_scores = importance_scores[meaningful_indices]
            _, topk_indices_in_meaningful = torch.topk(meaningful_importance_scores, k)
            topk_indices = meaningful_indices[topk_indices_in_meaningful]
        else:
            # 有意义梯度不足，选择所有有意义梯度，不补充零梯度嵌入
            topk_indices = meaningful_indices
            logging.info(f"用户{user_id}第{round_id}轮: 交互嵌入{meaningful_items}个 < Top-k目标{k}个，仅上传交互嵌入")
        
        # 4. 统计Top-k中有意义梯度的数量（用于EF21优化统计）
        if len(topk_indices) > 0:
            topk_meaningful_mask = meaningful_mask[topk_indices]
            topk_meaningful_count = topk_meaningful_mask.sum().item()
            topk_zero_gradient_count = len(topk_indices) - topk_meaningful_count
        else:
            topk_meaningful_count = 0
            topk_zero_gradient_count = 0
        
        # 创建稀疏掩码
        mask = torch.zeros_like(importance_scores, dtype=torch.bool)
        if len(topk_indices) > 0:
            mask[topk_indices] = True
        
        # 应用压缩
        compressed_target = torch.zeros_like(target_for_compression)
        compressed_target[mask] = target_for_compression[mask]
        
        # 计算压缩后的梯度
        if use_ef21:
            # EF21: g^{t+1} = g^t + C(∇f - g^t)
            if param_name in self.last_compressed[user_id]:
                compressed_gradient = self.last_compressed[user_id][param_name] + compressed_target
            else:
                compressed_gradient = compressed_target
            
            # 🔥 优化：只更新有意义梯度的错误反馈
            if meaningful_items < total_items:
                self._update_ef21_state_selective(
                    target_for_compression, compressed_target, meaningful_indices,
                    user_id, param_name
                )
            else:
                # 全部更新（传统方式）
                compression_error = target_for_compression - compressed_target
                self.error_feedback[user_id][param_name] = compression_error
            
            # 更新上次压缩的梯度
            self.last_compressed[user_id][param_name] = compressed_gradient.clone()
        else:
            # 普通压缩：直接使用压缩后的梯度
            compressed_gradient = compressed_target
            self.last_compressed[user_id][param_name] = compressed_gradient.clone()
        
        # 🔥 关键改进：只返回Top-k选中的嵌入，真正减少通信开销
        if len(topk_indices) > 0:
            topk_embeddings = compressed_gradient[topk_indices]  # 只取Top-k的嵌入
            topk_indices_list = topk_indices.cpu().tolist()     # 转换为列表
        else:
            topk_embeddings = torch.empty(0, embeddings.shape[1])
            topk_indices_list = []
        
        # 记录压缩统计（基于全部嵌入的Top-k选择）
        selected_k = len(topk_indices)  # 实际选择的Top-k数量
        compression_ratio = selected_k / total_items if total_items > 0 else 0.0
        actual_communication_reduction = 1 - (selected_k / total_items) if total_items > 0 else 1.0
        
        if user_id not in self.compression_stats:
            self.compression_stats[user_id] = []
        self.compression_stats[user_id].append({
            'round': round_id,
            'compression_ratio': compression_ratio,
            'actual_communication_reduction': actual_communication_reduction,
            'original_items': total_items,
            'compressed_items': selected_k,  # 实际选择的Top-k数量
            'target_k': k,  # 目标k值（永远基于总数计算）
            'meaningful_items': meaningful_items,  # 全部有意义梯度数量
            'zero_gradient_items': zero_gradient_items,  # 全部零梯度数量
            'topk_meaningful_items': topk_meaningful_count,  # Top-k中有意义梯度数量
            'topk_zero_gradient_items': topk_zero_gradient_count,  # Top-k中零梯度数量
            'ef21_computation_saved': topk_zero_gradient_count if use_ef21 else 0,  # EF21计算节省（Top-k中的零梯度）
            'original_norm': torch.norm(embeddings).item(),
            'compressed_norm': torch.norm(topk_embeddings).item() if len(topk_embeddings) > 0 else 0.0,
            'use_ef21': use_ef21
        })
        
        # 返回真正的稀疏表示
        return {
            'compressed_embeddings': topk_embeddings,      # 只包含Top-k的嵌入
            'topk_indices': topk_indices_list,             # Top-k的索引
            'original_shape': embeddings.shape,            # 原始形状信息
            'compression_ratio': compression_ratio,         # 压缩比例
            'communication_reduction': actual_communication_reduction,  # 通信减少比例
            'zero_gradient_items': zero_gradient_items,    # 零梯度物品数量
            'meaningful_items': meaningful_items,          # 有意义梯度物品数量
            'ef21_computation_saved': zero_gradient_items if use_ef21 else 0  # EF21计算节省量
        }
    
    def _prepare_ef21_target_selective(self, embeddings: torch.Tensor, meaningful_indices: torch.Tensor,
                                     user_id: int, param_name: str, use_ef21: bool) -> torch.Tensor:
        """
        选择性准备EF21目标向量，只处理有意义的梯度
        """
        # 首次初始化
        if param_name not in self.error_feedback[user_id]:
            self.error_feedback[user_id][param_name] = torch.zeros_like(embeddings)
            self.last_compressed[user_id][param_name] = torch.zeros_like(embeddings)
            return embeddings  # 首次使用普通压缩
        
        if use_ef21:
            # 只对有意义的梯度应用EF21
            target = embeddings.clone()
            target[meaningful_indices] = (embeddings[meaningful_indices] - 
                                        self.last_compressed[user_id][param_name][meaningful_indices])
            return target
        else:
            return embeddings
    
    def _update_ef21_state_selective(self, target_for_compression: torch.Tensor, 
                                   compressed_target: torch.Tensor, meaningful_indices: torch.Tensor,
                                   user_id: int, param_name: str):
        """
        选择性更新EF21状态，只更新有意义梯度的错误反馈
        """
        if param_name not in self.error_feedback[user_id]:
            self.error_feedback[user_id][param_name] = torch.zeros_like(target_for_compression)
        
        # 只更新有意义梯度的错误反馈
        compression_error = target_for_compression - compressed_target
        self.error_feedback[user_id][param_name][meaningful_indices] = compression_error[meaningful_indices]
        # 零梯度部分的错误反馈保持为0（不更新）
    
    def get_compression_stats(self, user_id: int) -> Dict[str, Any]:
        """获取用户的压缩统计信息"""
        if user_id not in self.compression_stats:
            return {}
        
        stats = self.compression_stats[user_id]
        if not stats:
            return {}
        
        latest_stats = stats[-1]
        avg_compression_ratio = np.mean([s['compression_ratio'] for s in stats])
        
        return {
            'total_rounds': len(stats),
            'latest_compression_ratio': latest_stats['compression_ratio'],
            'avg_compression_ratio': avg_compression_ratio,
            'current_topk_ratio': self.topk_ratio,
            'ef21_active': latest_stats['use_ef21']
        }
    
    def log_compression_summary(self, round_id: int):
        """记录压缩总结信息（包含EF21计算优化统计）"""
        if not self.compression_stats:
            return
        
        # 计算全局统计
        all_ratios = []
        all_communication_reductions = []
        ef21_active_count = 0
        total_original_items = 0
        total_compressed_items = 0
        total_meaningful_items = 0
        total_zero_gradient_items = 0
        total_ef21_computation_saved = 0
        
        for user_stats in self.compression_stats.values():
            if user_stats:
                latest = user_stats[-1]
                all_ratios.append(latest['compression_ratio'])
                if 'actual_communication_reduction' in latest:
                    all_communication_reductions.append(latest['actual_communication_reduction'])
                if 'original_items' in latest and 'compressed_items' in latest:
                    total_original_items += latest['original_items']
                    total_compressed_items += latest['compressed_items']
                if 'meaningful_items' in latest:
                    total_meaningful_items += latest['meaningful_items']
                if 'zero_gradient_items' in latest:
                    total_zero_gradient_items += latest['zero_gradient_items']
                if 'ef21_computation_saved' in latest:
                    total_ef21_computation_saved += latest['ef21_computation_saved']
                if latest['use_ef21']:
                    ef21_active_count += 1
        
        if all_ratios:
            avg_ratio = np.mean(all_ratios)
            total_users = len(self.compression_stats)
            
            # 计算目标k值统计
            total_target_k = 0
            for user_stats in self.compression_stats.values():
                if user_stats:
                    latest = user_stats[-1]
                    if 'target_k' in latest:
                        total_target_k += latest['target_k']
            
            logging.info(f"🎯 第{round_id}轮 Top-k+EF21智能压缩:")
            logging.info(f"  - Top-k比例: {self.topk_ratio*100:.1f}% (基于全部嵌入)")
            logging.info(f"  - 目标选择数量: {total_target_k:,}")
            logging.info(f"  - 实际选择数量: {total_compressed_items:,}")
            logging.info(f"  - 稀疏嵌入压缩: {total_original_items:,} → {total_compressed_items:,}")
            
            # 零梯度优化统计
            if total_zero_gradient_items > 0:
                zero_gradient_ratio = total_zero_gradient_items / total_original_items * 100
                logging.info(f"  - 全部零梯度嵌入: {total_zero_gradient_items:,} ({zero_gradient_ratio:.1f}%)")
                logging.info(f"  - 全部有意义梯度: {total_meaningful_items:,}")
                
                if total_ef21_computation_saved > 0:
                    computation_saving_ratio = total_ef21_computation_saved / total_compressed_items * 100 if total_compressed_items > 0 else 0
                    logging.info(f"  - Top-k中零梯度(EF21节省): {total_ef21_computation_saved:,} ({computation_saving_ratio:.1f}%)")
            
            if all_communication_reductions:
                avg_communication_reduction = np.mean(all_communication_reductions)
                logging.info(f"  - 通信减少: {avg_communication_reduction*100:.2f}%")
            
            logging.info(f"  - EF21激活用户: {ef21_active_count}/{total_users}") 