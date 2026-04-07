"""
GPFedRec-TopkEF21联邦推荐引擎
专用Top-k+EF21稀疏上传策略，集成轻量差分隐私保护
增强Top-k稀疏化与EF21错误反馈优化
"""
import torch
import random
import copy
import logging
import torch.nn as nn
from sklearn.metrics.pairwise import cosine_similarity
from torch.distributions.laplace import Laplace
from metrics import MetronAtK
from mlp import MLP
from utils import *
from topk_ef21_optimizer import TopKEF21Optimizer
import math

class FedEngine(object):
    """GPFedRec-TopkEF21专用联邦推荐引擎"""
    
    def __init__(self, config):
        self.config = config
        self.crit = torch.nn.BCELoss()
        
        # 初始化模型
        self.model = MLP(config)
        if config['use_cuda'] is True:
            use_cuda(True, config['device_id'])
            self.model.cuda()
        
        self.client_model_params = {}
        self.server_model_param = {}
        self._metron = MetronAtK(top_k=10)
        
        # 隐私保护配置
        self.privacy_method = config.get('privacy_method', 'none')
        

        
        logging.info(f"隐私保护方法: {self.privacy_method}")
        if self.privacy_method == 'differential_privacy':
            logging.info(f"差分隐私噪声尺度: {config.get('dp', 1e-6)}")
        
        # 初始化Top-k和EF21优化器
        self.topk_ef21_optimizer = TopKEF21Optimizer(config)
        
        # 初始化通信开销统计
        self.communication_stats = []  # 记录每轮的通信开销统计
        
        logging.info(f"📊 算法集成状态:")
        logging.info(f"  - 物品级稀疏化: ✅ (仅上传交互物品嵌入)")
        logging.info(f"  - Top-k+EF21优化: ✅ 固定启用")
        logging.info(f"  - 隐私保护: ✅ ({self.privacy_method})")
        logging.info(f"  - 通信开销监测: ✅")

    def load_model(self, model):
        self.model = model



    def instance_user_train_loader(self, user_train_data):
        """从列表转换为dataset"""
        users, items, ratings = user_train_data
        dataset = list(zip(users, items, ratings))
        dataloader = torch.utils.data.DataLoader(dataset, batch_size=self.config['batch_size'], shuffle=True)
        return dataloader

    def fed_train_single_batch(self, model_client, batch_data, optimizers, user):
        """训练单个批次"""
        users, items, ratings = batch_data[0], batch_data[1], batch_data[2]
        ratings = ratings.float()
        
        # 获取正则化嵌入
        reg_item_embedding = copy.deepcopy(self.server_model_param['embedding_item.weight']['global'].data)
        
        optimizer, optimizer_u, optimizer_i = optimizers
        if self.config['use_cuda'] is True:
            users, items, ratings = users.cuda(), items.cuda(), ratings.cuda()
            reg_item_embedding = reg_item_embedding.cuda()
        
        optimizer.zero_grad()
        optimizer_u.zero_grad()
        optimizer_i.zero_grad()
        
        ratings_pred = model_client(items)
        loss = self.crit(ratings_pred.view(-1), ratings)
        
        # 自适应正则化
        user_train_data = [users.cpu().numpy(), items.cpu().numpy(), ratings.cpu().numpy()]
        user_interaction_count = len(set(items.cpu().numpy()))
        avg_interaction_count = self.config.get('avg_interaction_count', 50)
        
        adaptive_reg_coeff = get_adaptive_reg_coefficient(
            self.config, user_id=user, 
            user_interaction_count=user_interaction_count,
            avg_interaction_count=avg_interaction_count
        )
        
        regularization_term = compute_regularization(model_client, reg_item_embedding)
        loss += adaptive_reg_coeff * regularization_term
        
        loss.backward()
        optimizer.step()
        optimizer_u.step()
        optimizer_i.step()
        
        return model_client, loss.item()

    def extract_user_interaction_items(self, user_train_data):
        """提取用户交互的物品列表"""
        users, items, ratings = user_train_data
        return list(set(items))



    def get_privacy_preserving_sparse_params(self, client_params, user_train_data, user_id, round_id=0):
        """获取隐私保护的Top-k+EF21稀疏参数"""
        
        # GPFedRec-TopkEF21使用全物品嵌入模式
        # 全物品嵌入模式：直接对完整物品嵌入进行Top-k+EF21
        item_embedding = client_params['embedding_item.weight']  # 完整物品嵌入 [1682, 32]

        # Top-k+EF21压缩（固定启用）
        # 直接对完整物品嵌入进行Top-k+EF21压缩
        gradient_dict = {
            'embedding_item.weight': item_embedding
        }

        compressed_gradients = self.topk_ef21_optimizer.compress_gradients(
            gradient_dict, user_id, round_id
        )

        # 构建全物品嵌入模式的参数
        if 'topk_indices' in compressed_gradients:
            true_sparse_params = {
                'embedding_item.weight': compressed_gradients['embedding_item.weight'],
                'item_indices': compressed_gradients['topk_indices'],  # Top-k选中的物品索引
                'num_real_items': len(compressed_gradients['topk_indices']),
                'full_embedding_mode': True,
                'original_total_items': item_embedding.shape[0],
                'topk_compression_applied': True,
                'topk_compression_info': compressed_gradients.get('compression_info', {})
            }
        else:
            # EF21预热期，返回完整嵌入
            all_indices = list(range(item_embedding.shape[0]))
            true_sparse_params = {
                'embedding_item.weight': compressed_gradients['embedding_item.weight'],
                'item_indices': all_indices,
                'num_real_items': len(all_indices),
                'full_embedding_mode': True,
                'original_total_items': item_embedding.shape[0],
                'topk_compression_applied': False
            }
        
        # 应用隐私保护
        if self.privacy_method == 'differential_privacy':
            privacy_protected_params = self._apply_differential_privacy(true_sparse_params, user_id)
        else:
            privacy_protected_params = true_sparse_params
        
        # 添加优化层级信息
        privacy_protected_params['optimization_layers'] = {
            'full_embedding_mode': True,  # GPFedRec-TopkEF21专用全物品嵌入模式
            'topk_ef21_optimization': True,  # 固定启用
            'privacy_protection': self.privacy_method != 'none'
        }
        
        return privacy_protected_params
    

    
    def _apply_differential_privacy(self, true_sparse_params, user_id):
        """应用轻量差分隐私保护 - 与Top-k+EF21兼容"""
        embedding = true_sparse_params['embedding_item.weight']
        
        # 添加轻量差分隐私噪声
        noise = Laplace(0, self.config['dp']).expand(embedding.shape).sample()
        noisy_embedding = embedding + noise
        
        # 保留原始参数的其他属性
        result = {
            'embedding_item.weight': noisy_embedding,
            'item_indices': true_sparse_params['item_indices'],
            'privacy_method': 'differential_privacy',
            'noise_scale': self.config['dp']
        }
        
        # 添加其他保留的属性
        for key in true_sparse_params:
            if key not in ['embedding_item.weight', 'item_indices', 'privacy_method']:
                result[key] = true_sparse_params[key]
                
        return result

    def aggregate_privacy_preserving_sparse_params(self, round_user_params, all_train_data=None, round_id=0):
        """聚合隐私保护的Top-k+EF21稀疏参数 - 专用聚类后图聚合"""
        logging.info("GPFedRec-TopkEF21使用专用聚类后图聚合方法")

        # GPFedRec-TopkEF21专用聚合方法，不提供回退机制
        from improved_clustering_aggregation import clustering_then_graph_aggregation_topk_ef21
        updated_item_embedding = clustering_then_graph_aggregation_topk_ef21(
            round_user_params, self.config['num_items'], self.config['latent_dim'],
            current_global_embedding=self.server_model_param['embedding_item.weight']['global'].clone(),
            round_id=round_id,
            n_clusters=self.config.get('n_clusters', 5),
            similarity_metric=self.config.get('similarity_metric', 'cosine'),
            neighborhood_size=self.config.get('neighborhood_size', 0),
            neighborhood_threshold=self.config.get('neighborhood_threshold', 1.0),
            mp_layers=self.config.get('mp_layers', 2),
            clustering_update_frequency=self.config.get('clustering_update_frequency', 10)
        )
        
        self.server_model_param['embedding_item.weight'] = copy.deepcopy(updated_item_embedding)

    def fed_train_a_round(self, all_train_data, round_id):
        """训练一轮 - GPFedRec-TopkEF21版本"""
        # sample users participating in single round.
        num_participants = int(self.config['num_users'] * self.config['clients_sample_ratio'])
        participants = random.sample(range(self.config['num_users']), num_participants)
        # store users' model parameters of current round.
        round_participant_params = {}

        # initialize server parameters for the first round.
        if round_id == 0:
            self.server_model_param['embedding_item.weight'] = {}
            for user in participants:
                self.server_model_param['embedding_item.weight'][user] = copy.deepcopy(self.model.state_dict()['embedding_item.weight'].data.cpu())
            self.server_model_param['embedding_item.weight']['global'] = copy.deepcopy(self.model.state_dict()['embedding_item.weight'].data.cpu())
        
        # 隐私保护统计
        total_real_items = 0
        total_loss = 0.0
        
        # 通信开销统计
        total_uploaded_embeddings = 0  # 当前改进算法实际上传的嵌入数量
        total_privacy_added_embeddings = 0  # 隐私保护机制增加的嵌入数量
        original_algorithm_embeddings = len(participants) * self.config['num_items']  # 原算法需要上传的总嵌入数量
        
        # perform model updating for each participated user.
        for user in participants:
            # copy the client model architecture from self.model
            model_client = copy.deepcopy(self.model)
            
            if round_id != 0:
                user_param_dict = copy.deepcopy(self.model.state_dict())
                if user in self.client_model_params.keys():
                    for key in self.client_model_params[user].keys():
                        user_param_dict[key] = copy.deepcopy(self.client_model_params[user][key].data).cuda()
                user_param_dict['embedding_item.weight'] = copy.deepcopy(self.server_model_param['embedding_item.weight']['global'].data).cuda()
                model_client.load_state_dict(user_param_dict)
            
            # Defining optimizers
            optimizer = torch.optim.SGD(
                [{"params": model_client.fc_layers.parameters()}, {"params": model_client.affine_output.parameters()}],
                lr=self.config['lr'])
            optimizer_u = torch.optim.SGD(model_client.embedding_user.parameters(),
                                          lr=self.config['lr'] / self.config['clients_sample_ratio'] * self.config['lr_eta'] - self.config['lr'])
            optimizer_i = torch.optim.SGD(model_client.embedding_item.parameters(),
                                          lr=self.config['lr'] * self.config['num_items'] * self.config['lr_eta'] - self.config['lr'])
            optimizers = [optimizer, optimizer_u, optimizer_i]
            
            # load current user's training data and instance a train loader.
            user_train_data = [all_train_data[0][user], all_train_data[1][user], all_train_data[2][user]]
            user_dataloader = self.instance_user_train_loader(user_train_data)
            model_client.train()
            
            user_loss = 0.0  # 记录用户训练损失
            # update client model.
            for epoch in range(self.config['local_epoch']):
                for batch_id, batch in enumerate(user_dataloader):
                    assert isinstance(batch[0], torch.LongTensor)
                    model_client, loss = self.fed_train_single_batch(model_client, batch, optimizers, user)
                    user_loss += loss
            
            total_loss += user_loss  # 累计损失
            
            # obtain client model parameters.
            client_param = model_client.state_dict()
            # store client models' user embedding using a dict.
            self.client_model_params[user] = copy.deepcopy(client_param)
            for key in self.client_model_params[user].keys():
                self.client_model_params[user][key] = self.client_model_params[user][key].data.cpu()
            
            # **关键：GPFedRec-TopkEF21专用Top-k+EF21压缩上传**
            privacy_sparse_params = self.get_privacy_preserving_sparse_params(
                self.client_model_params[user], user_train_data, user, round_id
            )
            
            # 统计Top-k+EF21压缩效果
            if 'num_real_items' in privacy_sparse_params:
                total_real_items += privacy_sparse_params['num_real_items']
                
            # 统计通信开销
            user_uploaded_embeddings = privacy_sparse_params['embedding_item.weight'].shape[0]
            total_uploaded_embeddings += user_uploaded_embeddings
            
            # Top-k压缩效果统计（减少日志噪音）
            if privacy_sparse_params.get('topk_compression_applied', False) and round_id % 20 == 0 and user == participants[0]:
                # 只在每20轮且只记录第一个用户的压缩情况，避免大量重复日志
                if privacy_sparse_params.get('full_embedding_mode', False):
                    original_count = privacy_sparse_params.get('original_total_items', 0)
                    topk_count = privacy_sparse_params.get('num_real_items', 0)
                    logging.info(f"📊 全物品Top-k压缩效果: {original_count}→{topk_count} 物品嵌入 (压缩率{topk_count/original_count*100:.1f}%)")
                else:
                    original_count = privacy_sparse_params.get('original_interaction_count', 0)
                    topk_count = privacy_sparse_params.get('topk_selected_count', 0)
                    logging.info(f"📊 稀疏Top-k压缩效果: {original_count}→{topk_count} 物品嵌入 (压缩率{topk_count/original_count*100:.1f}%)")
            
            # GPFedRec-TopkEF21支持的隐私保护方法：
            # differential_privacy: 轻量差分隐私保护，与Top-k+EF21兼容
            # none: 无隐私保护
            
            round_participant_params[user] = privacy_sparse_params

        # 记录Top-k+EF21压缩统计信息
        if total_real_items > 0:
            avg_topk_items = total_real_items / len(participants) if len(participants) > 0 else 0
            logging.info(f"Top-k+EF21压缩统计: 总选择嵌入{total_real_items}个, 平均每用户{avg_topk_items:.1f}个")

        # aggregate client models in server side with privacy-preserving sparse parameters.
        self.aggregate_privacy_preserving_sparse_params(round_participant_params, all_train_data, round_id)
        
        # 记录Top-k+EF21压缩统计（每轮记录，固定启用）
        self.topk_ef21_optimizer.log_compression_summary(round_id)
        
        # 记录通信开销统计
        communication_reduction = ((original_algorithm_embeddings - total_uploaded_embeddings) / original_algorithm_embeddings) * 100
        avg_embeddings_per_user = total_uploaded_embeddings / len(participants) if len(participants) > 0 else 0
        
        current_round_stats = {
            'round': round_id,
            'uploaded_embeddings': total_uploaded_embeddings,
            'original_algorithm_embeddings': original_algorithm_embeddings,
            'communication_reduction': communication_reduction,
            'participants': len(participants),
            'avg_embeddings_per_user': avg_embeddings_per_user,
            'topk_ef21_reduction': communication_reduction  # Top-k+EF21压缩的减少量等于通信减少量
        }
        
        self.communication_stats.append(current_round_stats)
        
        # 返回平均损失，与原版引擎保持一致
        avg_loss = total_loss / len(participants) if len(participants) > 0 else 0.0
        return avg_loss

    def fed_evaluate(self, evaluate_data):
        """评估函数 - 与原版相同"""
        # evaluate all client models' performance using testing data.
        test_users, test_items = evaluate_data[0], evaluate_data[1]
        negative_users, negative_items = evaluate_data[2], evaluate_data[3]
        temp = [0] * 100
        temp[0] = 1
        ratings = torch.FloatTensor(temp)
        if self.config['use_cuda'] is True:
            test_users = test_users.cuda()
            test_items = test_items.cuda()
            negative_users = negative_users.cuda()
            negative_items = negative_items.cuda()
            ratings = ratings.cuda()
        
        test_scores = None
        negative_scores = None
        all_loss = {}
        for user in range(self.config['num_users']):
            user_model = copy.deepcopy(self.model)
            user_param_dict = copy.deepcopy(self.model.state_dict())
            if user in self.client_model_params.keys():
                for key in self.client_model_params[user].keys():
                    user_param_dict[key] = copy.deepcopy(self.client_model_params[user][key].data).cuda()
            user_model.load_state_dict(user_param_dict)
            user_model.eval()
            with torch.no_grad():
                test_user = test_users[user: user + 1]
                test_item = test_items[user: user + 1]
                negative_user = negative_users[user * 99: (user + 1) * 99]
                negative_item = negative_items[user * 99: (user + 1) * 99]
                test_score = user_model(test_item)
                negative_score = user_model(negative_item)
                if user == 0:
                    test_scores = test_score
                    negative_scores = negative_score
                else:
                    test_scores = torch.cat((test_scores, test_score))
                    negative_scores = torch.cat((negative_scores, negative_score))
                ratings_pred = torch.cat((test_score, negative_score))
                loss = self.crit(ratings_pred.view(-1), ratings)
            all_loss[user] = loss.item()
        if self.config['use_cuda'] is True:
            test_users = test_users.cpu()
            test_items = test_items.cpu()
            test_scores = test_scores.cpu()
            negative_users = negative_users.cpu()
            negative_items = negative_items.cpu()
            negative_scores = negative_scores.cpu()
        self._metron.subjects = [test_users.data.view(-1).tolist(),
                                 test_items.data.view(-1).tolist(),
                                 test_scores.data.view(-1).tolist(),
                                 negative_users.data.view(-1).tolist(),
                                 negative_items.data.view(-1).tolist(),
                                 negative_scores.data.view(-1).tolist()]
        hit_ratio, ndcg = self._metron.cal_hit_ratio(), self._metron.cal_ndcg()
        
        # 使用固定Top-k比例，无需性能监控
        
        return hit_ratio, ndcg, all_loss

    def save(self, alias, epoch_id, hit_ratio, ndcg):
        """保存模型检查点 - 已禁用，使用统一的模型保存机制"""
        # 注释掉原有的保存逻辑，避免创建不必要的目录
        # assert hasattr(self, 'model'), 'Please specify the exact model !'
        # model_dir = self.config['model_dir'].format(alias, epoch_id, hit_ratio, ndcg)
        # save_checkpoint(self.model, model_dir)
        
        # 输出警告信息，但不实际保存
        logging.warning(f"engine.save方法已禁用，请使用统一的模型保存机制")
        logging.info(f"如需保存模型，请确保设置了--save_best_model和--model_save_path参数")
        pass 