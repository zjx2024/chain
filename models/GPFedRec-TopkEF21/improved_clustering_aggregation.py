#!/usr/bin/env python3
"""
改进的聚类聚合方法：解决稀疏上传导致的图聚合问题
基于用户交互模式进行聚类，然后在聚类内和聚类间进行分层聚合
"""

import copy
import logging
import numpy as np
import torch
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics.pairwise import cosine_similarity

# 尝试导入图聚合工具，确保必须可用
try:
    from utils import construct_user_relation_graph_via_item, select_topk_neighboehood, MP_on_graph
    GRAPH_UTILS_AVAILABLE = True
except ImportError:
    raise ImportError("图聚合工具必须可用，GPFedRec-TopkEF21项目专门用于Top-k+EF21算法")

# 设置日志格式
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class UserClusteringAggregator:
    """用户聚类聚合器 - 专为Top-k+EF21算法设计"""
    
    def __init__(self, n_clusters=5, min_cluster_size=2):
        self.n_clusters = n_clusters
        self.min_cluster_size = min_cluster_size
        self.user_clusters = {}
        self.last_clustering_round = -1
        self.clustering_update_frequency = 10
        
        # Top-k+EF21专用：用户累积交互历史
        self.user_cumulative_interactions = {}
        
    def update_user_interactions_from_topk(self, round_user_params, round_id):
        """从Top-k参数中更新用户累积交互历史"""
        for user, params in round_user_params.items():
            if 'item_indices' in params:
                # Top-k稀疏模式：记录Top-k选择的物品
                topk_indices = params['item_indices']
                if isinstance(topk_indices, torch.Tensor):
                    topk_indices = topk_indices.cpu().numpy()
                
                if user not in self.user_cumulative_interactions:
                    self.user_cumulative_interactions[user] = set()
                
                self.user_cumulative_interactions[user].update(topk_indices)
            else:
                # 全物品模式：记录所有非零嵌入的物品
                embedding = params['embedding_item.weight']
                nonzero_indices = torch.nonzero(torch.sum(torch.abs(embedding), dim=1) > 1e-8).flatten()
                
                if user not in self.user_cumulative_interactions:
                    self.user_cumulative_interactions[user] = set()
                
                if len(nonzero_indices) > 0:
                    self.user_cumulative_interactions[user].update(nonzero_indices.cpu().numpy())
        
        logging.debug(f"第{round_id}轮累积交互更新完成，总用户数: {len(self.user_cumulative_interactions)}")

    def compute_cumulative_interaction_similarity(self, selected_users=None):
        """基于累积交互历史计算用户相似性"""
        if selected_users is None:
            users = list(self.user_cumulative_interactions.keys())
        else:
            users = [u for u in selected_users if u in self.user_cumulative_interactions]
        
        if len(users) < 2:
            return np.eye(len(users)), users
        
        # 构建累积交互矩阵
        all_items = set()
        for user in users:
            all_items.update(self.user_cumulative_interactions[user])
        all_items = sorted(list(all_items))
        
        if len(all_items) == 0:
            return np.eye(len(users)), users
        
        # 创建用户-物品交互矩阵
        interaction_matrix = np.zeros((len(users), len(all_items)))
        for i, user in enumerate(users):
            user_items = self.user_cumulative_interactions[user]
            for j, item in enumerate(all_items):
                if item in user_items:
                    interaction_matrix[i, j] = 1
        
        # 计算余弦相似性
        similarity_matrix = cosine_similarity(interaction_matrix)
        
        return similarity_matrix, users

    def should_update_clustering(self, round_id):
        """判断是否需要更新聚类"""
        if self.last_clustering_round == -1:
            return True
        return (round_id - self.last_clustering_round) >= self.clustering_update_frequency

    def cluster_users_by_cumulative_interaction(self, participating_users, round_id):
        """基于累积交互历史进行用户聚类"""
        if not self.should_update_clustering(round_id):
            logging.debug(f"第{round_id}轮跳过聚类更新，使用上次聚类结果")
            return
        
        # 计算相似性矩阵
        similarity_matrix, ordered_users = self.compute_cumulative_interaction_similarity(participating_users)
        
        if len(ordered_users) < 2:
            # 只有一个用户或没有用户
            self.user_clusters = {0: ordered_users} if ordered_users else {}
            self.last_clustering_round = round_id
            logging.info(f"第{round_id}轮聚类完成: 用户数不足，创建单一聚类")
            return
        
        # 使用1-相似性作为距离矩阵进行层次聚类
        distance_matrix = 1 - similarity_matrix
        np.fill_diagonal(distance_matrix, 0)  # 确保对角线为0
        
        n_clusters_actual = min(self.n_clusters, len(ordered_users))
        
        clustering = AgglomerativeClustering(
            n_clusters=n_clusters_actual,
            linkage='average',
            metric='precomputed'
        )
        cluster_labels = clustering.fit_predict(distance_matrix)
        
        # 构建聚类结果
        self.user_clusters = {}
        for i, label in enumerate(cluster_labels):
            if label not in self.user_clusters:
                self.user_clusters[label] = []
            self.user_clusters[label].append(ordered_users[i])
        
        # 过滤小聚类
        self.user_clusters = self._filter_small_clusters()
        
        self.last_clustering_round = round_id
        
        # 记录聚类统计
        cluster_sizes = [len(users) for users in self.user_clusters.values()]
        logging.info(f"第{round_id}轮累积交互聚类完成: {len(self.user_clusters)}个聚类, "
                    f"大小范围[{min(cluster_sizes)}, {max(cluster_sizes)}], "
                    f"平均大小{np.mean(cluster_sizes):.1f}")

    def compute_interaction_similarity(self, user_interactions_dict):
        """计算用户交互相似性矩阵"""
        users = list(user_interactions_dict.keys())
        n_users = len(users)
        
        if n_users < 2:
            return np.eye(n_users), users
        
        # 获取所有物品
        all_items = set()
        for items in user_interactions_dict.values():
            all_items.update(items)
        all_items = sorted(list(all_items))
        
        if len(all_items) == 0:
            return np.eye(n_users), users
        
        # 构建用户-物品交互矩阵
        interaction_matrix = np.zeros((n_users, len(all_items)))
        for i, user in enumerate(users):
            user_items = user_interactions_dict[user]
            for j, item in enumerate(all_items):
                if item in user_items:
                    interaction_matrix[i, j] = 1
        
        # 计算余弦相似性
        similarity_matrix = cosine_similarity(interaction_matrix)
        
        return similarity_matrix, users

    def cluster_users_by_interaction(self, user_interactions_dict, all_train_data):
        """基于交互历史进行用户聚类"""
        # 计算相似性矩阵
        similarity_matrix, users = self.compute_interaction_similarity(user_interactions_dict)
        
        if len(users) < 2:
            # 只有一个用户
            self.user_clusters = {0: users} if users else {}
            logging.info("用户数不足，创建单一聚类")
            return
        
        # 使用1-相似性作为距离矩阵进行层次聚类
        distance_matrix = 1 - similarity_matrix
        np.fill_diagonal(distance_matrix, 0)  # 确保对角线为0
        
        n_clusters_actual = min(self.n_clusters, len(users))
        
        clustering = AgglomerativeClustering(
            n_clusters=n_clusters_actual,
            linkage='average',
            metric='precomputed'
        )
        
        cluster_labels = clustering.fit_predict(distance_matrix)
        
        # 构建聚类结果
        self.user_clusters = {}
        for i, label in enumerate(cluster_labels):
            if label not in self.user_clusters:
                self.user_clusters[label] = []
            self.user_clusters[label].append(users[i])
        
        # 过滤小聚类
        self.user_clusters = self._filter_small_clusters()

    def _filter_small_clusters(self):
        """过滤掉过小的聚类，将其合并到最大的聚类中"""
        if not self.user_clusters:
            return {}
        
        large_clusters = {}
        small_cluster_users = []
        
        for cluster_id, users in self.user_clusters.items():
            if len(users) >= self.min_cluster_size:
                large_clusters[cluster_id] = users
            else:
                small_cluster_users.extend(users)
        
        # 如果没有大聚类，保留所有聚类
        if not large_clusters:
            return self.user_clusters
        
        # 将小聚类用户合并到最大的聚类中
        if small_cluster_users:
            largest_cluster_id = max(large_clusters.keys(), key=lambda x: len(large_clusters[x]))
            large_clusters[largest_cluster_id].extend(small_cluster_users)
        
        return large_clusters

    def cluster_then_graph_aggregation_topk_ef21(self, round_user_params, item_num, latent_dim, 
                                               current_global_embedding=None, round_id=0, **graph_config):
        """
        TopK+EF21专用的聚类后图聚合方法
        
        核心特性：
        1. 维护用户累积交互历史
        2. 基于累积历史进行稳定聚类
        3. 处理TopK选择的部分嵌入上传
        4. 定期更新聚类以适应用户行为变化
        5. 必须使用图聚合，不提供回退机制
        """
        
        # 步骤1: 更新用户累积交互历史
        self.update_user_interactions_from_topk(round_user_params, round_id)
        
        # 步骤2: 基于累积历史进行用户聚类
        participating_users = list(round_user_params.keys())
        self.cluster_users_by_cumulative_interaction(participating_users, round_id)
        
        # 步骤3: 重构完整嵌入矩阵（处理TopK稀疏性）
        full_user_params = {}
        topk_coverage_stats = []
        
        for user in participating_users:
            # 使用历史全局嵌入作为基础
            if current_global_embedding is not None:
                full_embedding = current_global_embedding.clone()
            else:
                # 第一轮使用小的随机初始化
                full_embedding = torch.randn(item_num, latent_dim) * 0.01
            
            # 更新TopK选择的物品嵌入
            topk_embedding = round_user_params[user]['embedding_item.weight']
            
            if 'item_indices' in round_user_params[user]:
                topk_indices = round_user_params[user]['item_indices']
                full_embedding[topk_indices] = topk_embedding
                
                # 统计TopK覆盖率
                cumulative_items = len(self.user_cumulative_interactions.get(user, set()))
                topk_items = len(topk_indices)
                coverage_ratio = topk_items / cumulative_items if cumulative_items > 0 else 0
                topk_coverage_stats.append(coverage_ratio)
            else:
                # 全物品模式
                full_embedding = topk_embedding
                topk_coverage_stats.append(1.0)
            
            full_user_params[user] = {'embedding_item.weight': full_embedding}
        
        # 记录TopK覆盖统计
        if topk_coverage_stats:
            avg_coverage = np.mean(topk_coverage_stats)
            logging.info(f"第{round_id}轮 TopK覆盖率: 平均{avg_coverage:.2%}, 范围[{min(topk_coverage_stats):.2%}, {max(topk_coverage_stats):.2%}]")
        
        # 步骤4: 聚类内图聚合
        cluster_embeddings = {}
        aggregation_stats = {'single_user': 0, 'multi_user': 0}
        
        for cluster_id, cluster_users in self.user_clusters.items():
            # 只聚合当前轮次参与的用户
            participating_cluster_users = [u for u in cluster_users if u in round_user_params]
            
            if not participating_cluster_users:
                continue
            
            if len(participating_cluster_users) == 1:
                # 单个用户直接使用其嵌入
                cluster_embeddings[cluster_id] = full_user_params[participating_cluster_users[0]]['embedding_item.weight']
                aggregation_stats['single_user'] += 1
            else:
                # 多个用户进行聚类内图聚合
                cluster_result = self._perform_cluster_graph_aggregation(
                    participating_cluster_users, full_user_params, item_num, latent_dim, graph_config
                )
                cluster_embeddings[cluster_id] = cluster_result
                aggregation_stats['multi_user'] += 1
        
        logging.info(f"聚类内聚合完成: {aggregation_stats['single_user']}个单用户, "
                    f"{aggregation_stats['multi_user']}个图聚合")
        
        # 步骤5: 聚类间聚合
        final_embedding = self._inter_cluster_aggregation(cluster_embeddings, round_user_params, item_num, latent_dim)
        
        # 构建返回格式
        result = {user: copy.deepcopy(final_embedding) for user in round_user_params.keys()}
        result['global'] = copy.deepcopy(final_embedding)
        
        return result
    
    def _perform_cluster_graph_aggregation(self, cluster_users, full_user_params, item_num, latent_dim, graph_config):
        """在聚类内执行图聚合 - 必须成功，不提供回退"""
        # 构建聚类内用户参数字典（重新编号）
        cluster_user_params = {}
        for new_id, original_user in enumerate(cluster_users):
            cluster_user_params[new_id] = full_user_params[original_user]
        
        # 在聚类内构建用户关系图
        user_relation_graph = construct_user_relation_graph_via_item(
            cluster_user_params, item_num, latent_dim,
            graph_config.get('similarity_metric', 'cosine')
        )
        
        # 选择top-k邻居
        topk_user_relation_graph = select_topk_neighboehood(
            user_relation_graph, 
            graph_config.get('neighborhood_size', 0),
            graph_config.get('neighborhood_threshold', 1.0)
        )
        
        # 执行消息传递
        cluster_mp_result = MP_on_graph(
            cluster_user_params, item_num, latent_dim,
            topk_user_relation_graph, 
            graph_config.get('mp_layers', 1)
        )
        
        return cluster_mp_result['global']
    
    def _inter_cluster_aggregation(self, cluster_embeddings, round_user_params, item_num, latent_dim):
        """聚类间聚合"""
        if len(cluster_embeddings) == 1:
            return list(cluster_embeddings.values())[0]
        
        final_embedding = torch.zeros(item_num, latent_dim)
        total_weight = 0
        cluster_weights = []
        
        for cluster_id, cluster_embedding in cluster_embeddings.items():
            # 聚类权重基于参与用户数量
            cluster_size = len([u for u in self.user_clusters[cluster_id] if u in round_user_params])
            weight = np.sqrt(cluster_size)  # 使用平方根权重
            final_embedding += weight * cluster_embedding
            total_weight += weight
            cluster_weights.append(weight)
        
        final_embedding = final_embedding / total_weight if total_weight > 0 else final_embedding
        logging.info(f"聚类间聚合: {len(cluster_embeddings)}个聚类，权重范围[{min(cluster_weights):.2f}, {max(cluster_weights):.2f}]")
        
        return final_embedding


def extract_user_interactions(all_train_data):
    """从训练数据中提取用户交互物品列表"""
    user_interactions = {}
    
    if len(all_train_data) >= 2:
        for user_id in range(len(all_train_data[1])):
            if user_id < len(all_train_data[1]):
                user_items = all_train_data[1][user_id] if all_train_data[1][user_id] is not None else []
                user_interactions[user_id] = list(set(user_items))  # 去重
            else:
                user_interactions[user_id] = []
    
    return user_interactions


def clustering_then_graph_aggregation_topk_ef21(round_user_params, item_num, latent_dim, 
                                             current_global_embedding=None, round_id=0,
                                             n_clusters=5, similarity_metric='cosine', 
                                             neighborhood_size=0, neighborhood_threshold=1.0, 
                                             mp_layers=1, clustering_update_frequency=10):
    """TopK+EF21专用聚类后图聚合方法入口函数"""
    
    # 创建TopK+EF21专用聚类聚合器
    if not hasattr(clustering_then_graph_aggregation_topk_ef21, 'aggregator'):
        clustering_then_graph_aggregation_topk_ef21.aggregator = UserClusteringAggregator(
            n_clusters=n_clusters,
            min_cluster_size=2
        )
        clustering_then_graph_aggregation_topk_ef21.aggregator.clustering_update_frequency = clustering_update_frequency
    
    # 图聚合配置
    graph_config = {
        'similarity_metric': similarity_metric,
        'neighborhood_size': neighborhood_size,
        'neighborhood_threshold': neighborhood_threshold,
        'mp_layers': mp_layers
    }
    
    # 执行TopK+EF21专用聚类后图聚合
    result = clustering_then_graph_aggregation_topk_ef21.aggregator.cluster_then_graph_aggregation_topk_ef21(
        round_user_params, item_num, latent_dim, current_global_embedding, round_id, **graph_config
    )
    
    return result


def get_topk_ef21_aggregator_stats():
    """获取TopK+EF21聚合器的统计信息"""
    if hasattr(clustering_then_graph_aggregation_topk_ef21, 'aggregator'):
        aggregator = clustering_then_graph_aggregation_topk_ef21.aggregator
        
        stats = {
            'total_users': len(aggregator.user_cumulative_interactions),
            'n_clusters': len(aggregator.user_clusters),
            'last_clustering_round': aggregator.last_clustering_round,
            'clustering_update_frequency': aggregator.clustering_update_frequency
        }
        
        if aggregator.user_clusters:
            cluster_sizes = [len(users) for users in aggregator.user_clusters.values()]
            stats.update({
                'cluster_sizes': cluster_sizes,
                'avg_cluster_size': np.mean(cluster_sizes),
                'min_cluster_size': min(cluster_sizes),
                'max_cluster_size': max(cluster_sizes)
            })
        
        return stats
    else:
        return {'status': 'aggregator_not_initialized'}


if __name__ == "__main__":
    # 测试代码
    print("改进的聚类聚合方法已实现")
    print("主要方法:")
    print("1. clustering_then_graph_aggregation - 聚类后图聚合（新增）")
    print("2. extract_user_interactions - 提取用户交互物品列表")
    print("3. 三种聚类方法: interaction_based, vector_based, statistical") 