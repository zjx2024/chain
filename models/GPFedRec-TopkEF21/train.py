import pandas as pd
import numpy as np
import datetime
import os
# 设置环境变量避免KMeans内存泄漏警告
os.environ["OMP_NUM_THREADS"] = "4"
os.environ["CUDA_VISIBLE_DEVICES"] = "0,2"
import argparse
# 先不导入engine，等日志初始化后再导入
from data import SampleGenerator
from utils import *
import logging

def str2bool(v):
    """将字符串转换为布尔值的辅助函数"""
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

# 训练设置 - GPFedRec-TopkEF21
parser = argparse.ArgumentParser()
parser.add_argument('--alias', type=str, default='gpfedrec_topk_ef21')
parser.add_argument('--clients_sample_ratio', type=float, default=0.5)
parser.add_argument('--clients_sample_num', type=int, default=0)
parser.add_argument('--num_round', type=int, default=200)
parser.add_argument('--local_epoch', type=int, default=1)
parser.add_argument('--neighborhood_size', type=int, default=0)
parser.add_argument('--neighborhood_threshold', type=float, default=1.)
parser.add_argument('--mp_layers', type=int, default=2)
parser.add_argument('--similarity_metric', type=str, default='cosine')

# 聚合方法固定为clustering_then_graph，无需参数控制
parser.add_argument('--n_clusters', type=int, default=5, help='聚类数量')

# 隐私保护配置
parser.add_argument('--privacy_method', type=str, default='differential_privacy',
                    choices=['differential_privacy', 'none'],
                    help='隐私保护方法：差分隐私或无保护')
parser.add_argument('--dp', type=float, default=1e-6)

# 正则化配置：用户自适应正则化
parser.add_argument('--reg', type=float, default=1.0)
parser.add_argument('--adaptive_reg', type=str, default='user', choices=['none', 'user'], 
                    help='GPFedRec-TopkEF21使用用户自适应正则化')
parser.add_argument('--reg_min', type=float, default=0.1, help='最小正则化系数')
parser.add_argument('--reg_max', type=float, default=2.0, help='最大正则化系数')

parser.add_argument('--lr_eta', type=int, default=80)
parser.add_argument('--batch_size', type=int, default=256)
parser.add_argument('--optimizer', type=str, default='sgd')
parser.add_argument('--lr', type=float, default=0.1)
parser.add_argument('--dataset', type=str, default='100k')
parser.add_argument('--num_users', type=int)
parser.add_argument('--num_items', type=int)
parser.add_argument('--latent_dim', type=int, default=32)
parser.add_argument('--num_negative', type=int, default=4)
parser.add_argument('--layers', type=str, default='64, 32, 16, 8')
parser.add_argument('--l2_regularization', type=float, default=0.)
parser.add_argument('--use_cuda', type=bool, default=True)
parser.add_argument('--device_id', type=int, default=0)
parser.add_argument('--model_dir', type=str, default='checkpoints/{}_Epoch{}_HR{:.4f}_NDCG{:.4f}.model')

# 新增参数：支持动态数据集路径和模型保存
parser.add_argument('--dataset_path', type=str, default=None, help='动态数据集文件路径')
parser.add_argument('--model_save_path', type=str, default=None, help='训练后模型保存路径')
parser.add_argument('--save_best_model', type=str2bool, nargs='?', const=True, default=False, help='是否保存最佳模型')
parser.add_argument('--progress_output', type=str2bool, nargs='?', const=True, default=True, help='是否输出训练进度')

# Top-k稀疏化与EF21配置（固定启用）
# use_topk_ef21已固定启用（项目专用功能）
parser.add_argument('--topk_ratio', type=float, default=0.1, 
                    help='Top-k稀疏化比例，保留梯度中变化最大的k%分量')
parser.add_argument('--ef21_warmup_rounds', type=int, default=3,
                    help='EF21错误反馈预热轮数，前几轮使用普通压缩')
parser.add_argument('--disable_ef21', type=str2bool, nargs='?', const=True, default=False,
                    help='是否禁用EF21错误反馈（仅保留Top-k压缩）')
# 自适应Top-k功能已移除，使用固定Top-k比例

# TopK+EF21聚类配合参数（固定启用）
parser.add_argument('--clustering_update_frequency', type=int, default=10,
                    help='聚类更新频率（每N轮重新聚类一次）')

# 注释：GPFedRec-TopkEF21专用Top-k+EF21稀疏上传策略

args = parser.parse_args()

# 模型配置
config = vars(args)
# 固定聚合方法为clustering_then_graph
config['aggregation_method'] = 'clustering_then_graph'

if len(config['layers']) > 1:
    config['layers'] = [int(item) for item in config['layers'].split(',')]
else:
    config['layers'] = int(config['layers'])
    
# 数据集名称映射：数据库名称 -> 模型内部名称
dataset_name_mapping = {
    'ml-100k': '100k',
    'ml-1m': 'ml-1m',
    'lastfm-2k': 'lastfm-2k',
    'amazon': 'amazon'
}

# 如果数据集名称需要映射，进行转换
if config['dataset'] in dataset_name_mapping:
    config['dataset'] = dataset_name_mapping[config['dataset']]

if config['dataset'] == 'ml-1m':
    config['num_users'] = 6040
    config['num_items'] = 3706
elif config['dataset'] == '100k':
    config['num_users'] = 943
    config['num_items'] = 1682
elif config['dataset'] == 'lastfm-2k':
    config['num_users'] = 1600
    config['num_items'] = 12454
elif config['dataset'] == 'amazon':
    config['num_users'] = 8072
    config['num_items'] = 11830
else:
    pass

if __name__ == "__main__":
    # 生成参数化的日志文件名 - 方案1：详细版
    def generate_log_filename(config):
        """根据关键参数生成日志文件名"""
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')
        
        # 构建隐私参数部分
        privacy_part = config['privacy_method']
        if config['privacy_method'] == 'none':
            privacy_part = 'no_privacy'
        elif config['privacy_method'] == 'differential_privacy':
            privacy_part = f"differential_privacy{config['dp']}"
            
        # 构建Top-k和EF21优化部分（固定启用）
        topk_ratio = config.get('topk_ratio', 0.1)
        topk_part = f"topk{topk_ratio}"
        
        # GPFedRec-TopkEF21默认使用全物品嵌入模式
        topk_part = f"full_{topk_part}"
        
        # TopK+EF21聚类配合（固定启用累积交互）
        clustering_freq = config.get('clustering_update_frequency', 10)
        topk_part = f"{topk_part}_cumcluster{clustering_freq}"
        
        if config.get('disable_ef21', False):
            topk_ef21_part = f"_{topk_part}_noef21"
        else:
            ef21_warmup = config.get('ef21_warmup_rounds', 3)
            topk_ef21_part = f"_{topk_part}_ef21w{ef21_warmup}"
        
        # 构建聚合方法简码（固定为聚类聚合）
        aggregation_part = f"clustering_{config['n_clusters']}"
        
        # 构建客户端参与比例部分
        ratio_part = f"client{config['clients_sample_ratio']}"
        
        # 构建文件名 - 加入mp_layers参数和Top-k EF21优化
        filename = (f"{config['dataset']}_{config['adaptive_reg']}_{aggregation_part}_"
                   f"{privacy_part}{topk_ef21_part}_{ratio_part}_lr{config['lr']}_r{config['num_round']}_"
                   f"mp{config['mp_layers']}_{timestamp}.txt")
        
        return filename
    
    def log_experiment_parameters(config):
        """记录详细的实验参数信息"""
        logging.info("=" * 100)
        logging.info("GPFedRec-TopkEF21实验配置详情")
        logging.info("=" * 100)
        
        # 基础实验设置
        logging.info("📊 基础实验设置:")
        logging.info(f"  - 数据集: {config['dataset']}")
        logging.info(f"  - 用户数量: {config['num_users']}")
        logging.info(f"  - 物品数量: {config['num_items']}")
        logging.info(f"  - 训练轮数: {config['num_round']}")
        logging.info(f"  - 学习率: {config['lr']}")
        logging.info(f"  - 嵌入维度: {config['latent_dim']}")
        logging.info(f"  - 批量大小: {config['batch_size']}")
        logging.info(f"  - 本地训练轮数: {config['local_epoch']}")
        logging.info(f"  - 客户端采样比例: {config['clients_sample_ratio']}")
        
        # 核心改进特性
        logging.info("\n🚀 核心改进特性:")
        logging.info(f"  - 用户自适应正则化: {config['adaptive_reg']}")
        if config['adaptive_reg'] == 'user':
            logging.info(f"    * 最小正则化系数: {config['reg_min']}")
            logging.info(f"    * 最大正则化系数: {config['reg_max']}")
        else:
            logging.info(f"    * 固定正则化系数: {config['reg']}")
        
        logging.info("  - 聚合方法: clustering_then_graph (固定启用)")
        logging.info(f"    * 聚类数量: {config['n_clusters']}")
        logging.info(f"    * 相似度度量: {config['similarity_metric']}")
        
        logging.info("  - 稀疏上传策略: Top-k+EF21专用")
        logging.info("    * 使用智能Top-k+EF21压缩，大幅减少通信开销")
        
        # 隐私保护配置
        logging.info("\n🔒 隐私保护配置:")
        logging.info(f"  - 隐私保护方法: {config['privacy_method']}")
        
        if config['privacy_method'] == 'none':
            logging.info("    * 🚫 无隐私保护，直接传输Top-k+EF21压缩参数")
        elif config['privacy_method'] == 'differential_privacy':
            logging.info(f"  - 差分隐私噪声尺度: {config['dp']}")
            logging.info("    * 🔊 轻量差分隐私保护，与Top-k+EF21兼容")
        
        # 差分隐私已在上面详细说明，无需重复
        
        # 图神经网络配置
        logging.info("\n🔗 图神经网络配置:")
        logging.info(f"  - 邻域大小: {config['neighborhood_size']}")
        logging.info(f"  - 邻域阈值: {config['neighborhood_threshold']}")
        logging.info(f"  - 消息传递层数: {config['mp_layers']}")
        
        # 模型架构
        logging.info("\n🏗️ 模型架构:")
        logging.info(f"  - MLP层结构: {config['layers']}")
        logging.info(f"  - L2正则化: {config['l2_regularization']}")
        
        # Top-k稀疏化与EF21配置（固定启用）
        logging.info("\n🎯 Top-k稀疏化与EF21优化配置:")
        
        # GPFedRec-TopkEF21使用全物品嵌入模式
        logging.info("  - 🔄 全物品嵌入模式: 启用")
        logging.info(f"  - Top-k比例: {config.get('topk_ratio', 0.1)*100:.1f}%")
        logging.info("    * 直接对完整物品嵌入进行Top-k+EF21压缩")
        logging.info("    * EF21状态管理简化，无需处理动态物品集合")
        logging.info("    * 理论收敛性最佳，实现复杂度最低")
        logging.info(f"  - 固定Top-k比例: {config.get('topk_ratio', 0.1)*100:.1f}%")
        
        # TopK+EF21聚类配合配置（固定启用累积交互）
        logging.info(f"\n🔗 TopK+EF21聚类配合配置:")
        logging.info(f"  - 聚类更新频率: 每{config.get('clustering_update_frequency', 10)}轮")
        logging.info("  - 累积交互历史聚类: 固定启用")
        logging.info("    * 服务器维护用户累积交互历史，基于完整历史进行稳定聚类")
        logging.info("    * 从TopK上传参数中提取物品索引，逐步构建用户交互模式")
        logging.info("    * 聚类后在各聚类内部进行图聚合，提升聚合质量")
        
        if config.get('disable_ef21', False):
            logging.info("  - EF21错误反馈: ❌ 已禁用")
            logging.info("    * 仅使用Top-k压缩，无错误反馈补偿")
        else:
            logging.info(f"  - EF21预热轮数: {config.get('ef21_warmup_rounds', 3)}")
            logging.info("    * EF21错误反馈机制补偿压缩误差，提升收敛性")
        logging.info("    * Top-k选择梯度中变化最大的分量进行上传")
        
        # 日志存储
        logging.info(f"  - 负采样数量: {config['num_negative']}")
        logging.info(f"  - 学习率调节因子 η: {config['lr_eta']}")
        
        # 实验环境
        logging.info("\n💻 实验环境:")
        logging.info(f"  - 使用CUDA: {config['use_cuda']}")
        if config['use_cuda']:
            logging.info(f"  - GPU设备ID: {config['device_id']}")
        logging.info(f"  - 优化器: {config['optimizer']}")
        
        # 技术创新总结
        logging.info("\n✨ 技术创新总结:")
        innovations = []
        if config['adaptive_reg'] == 'user':
            innovations.append("用户自适应正则化")
        # 聚合方法固定为clustering_then_graph
        innovations.append("聚类后图聚合")
        # Top-k+EF21智能压缩（固定启用）
        innovations.append("Top-k+EF21智能压缩")
        
        privacy_innovations = []
        if config['privacy_method'] == 'none':
            privacy_innovations.append("🚫 无隐私保护")
        elif config['privacy_method'] == 'differential_privacy':
            privacy_innovations.append("🔊 轻量差分隐私保护")
        
        if innovations:
            logging.info(f"  - 算法改进: {', '.join(innovations)}")
        if privacy_innovations:
            logging.info(f"  - 隐私保护: {', '.join(privacy_innovations)}")
        
        logging.info("=" * 100)
        logging.info("实验开始")
        logging.info("=" * 100)
    
    # 生成日志文件名
    log_filename = generate_log_filename(config)
    path = 'log/'
    # 确保日志目录存在
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    logname = os.path.join(path, log_filename)
    initLogging(logname)
    
    # 记录详细的实验参数
    log_experiment_parameters(config)

    # 在日志初始化之后再导入和初始化引擎
    from engine import FedEngine
    engine = FedEngine(config)

    # 动态数据加载
    if config['dataset_path'] is not None:
        # 使用后端传入的数据集路径
        dataset_dir = config['dataset_path']
        logging.info(f"使用动态数据集路径: {dataset_dir}")
    else:
        # 使用默认路径
        dataset_dir = "data/" + config['dataset'] + "/" + "ratings.dat"
        logging.info(f"使用默认数据集路径: {dataset_dir}")
    
    # 检查文件是否存在
    if not os.path.exists(dataset_dir):
        logging.error(f"数据集文件不存在: {dataset_dir}")
        raise FileNotFoundError(f"数据集文件不存在: {dataset_dir}")
    
    # 验证模型保存路径配置
    if config.get('save_best_model', False):
        if not config.get('model_save_path'):
            # 如果没有指定保存路径，使用默认的models-storage路径
            default_save_path = "../../models-storage"
            config['model_save_path'] = default_save_path
            logging.warning(f"未指定模型保存路径，使用默认路径: {default_save_path}")
        
        # 记录接收到的模型保存路径（不在这里创建目录，统一在后面处理）
        logging.info(f"模型保存路径配置: {config['model_save_path']}")
    
    # 根据数据集类型加载数据
    logging.info(f"开始加载数据集: {config['dataset']}")
    if config['dataset'] == "ml-1m":
        rating = pd.read_csv(dataset_dir, sep='::', header=None, names=['uid', 'mid', 'rating', 'timestamp'], engine='python')
    elif config['dataset'] == "100k":
        # 支持多种格式
        try:
            # 首先尝试逗号分隔
            rating = pd.read_csv(dataset_dir, sep=",", header=None, names=['uid', 'mid', 'rating', 'timestamp'], engine='python')
        except:
            try:
                # 如果失败，尝试制表符分隔
                rating = pd.read_csv(dataset_dir, sep="\t", header=None, names=['uid', 'mid', 'rating', 'timestamp'], engine='python')
            except:
                # 最后尝试双冒号分隔（原始MovieLens格式）
                rating = pd.read_csv(dataset_dir, sep='::', header=None, names=['uid', 'mid', 'rating', 'timestamp'], engine='python')
    elif config['dataset'] == "lastfm-2k":
        rating = pd.read_csv(dataset_dir, sep=",", header=None, names=['uid', 'mid', 'rating', 'timestamp'],  engine='python')
    elif config['dataset'] == "amazon":
        rating = pd.read_csv(dataset_dir, sep=",", header=None, names=['uid', 'mid', 'rating', 'timestamp'], engine='python')
        rating = rating.sort_values(by='uid', ascending=True)
    else:
        # 默认尝试逗号分隔
        rating = pd.read_csv(dataset_dir, sep=",", header=None, names=['uid', 'mid', 'rating', 'timestamp'], engine='python')
    
    logging.info(f"数据集加载完成，共{len(rating)}条记录")

    # 重新索引
    user_id = rating[['uid']].drop_duplicates().reindex()
    user_id['userId'] = np.arange(len(user_id))
    rating = pd.merge(rating, user_id, on=['uid'], how='left')
    item_id = rating[['mid']].drop_duplicates()
    item_id['itemId'] = np.arange(len(item_id))
    rating = pd.merge(rating, item_id, on=['mid'], how='left')
    rating = rating[['userId', 'itemId', 'rating', 'timestamp']]
    logging.info('Range of userId is [{}, {}]'.format(rating.userId.min(), rating.userId.max()))
    logging.info('Range of itemId is [{}, {}]'.format(rating.itemId.min(), rating.itemId.max()))

    # 数据加载器
    sample_generator = SampleGenerator(ratings=rating)
    validate_data = sample_generator.validate_data
    test_data = sample_generator.test_data

    # 训练循环
    hit_ratio_list = []
    ndcg_list = []
    val_hr_list = []
    val_ndcg_list = []
    train_loss_list = []
    test_loss_list = []
    val_loss_list = []
    best_val_hr = 0
    best_test_hr = 0
    best_test_ndcg = 0
    best_test_round = 0
    final_test_round = 0
    
    # 为整个训练过程生成统一的时间戳和目录
    training_timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    training_model_dir = None
    
    if config.get('save_best_model', False) and config.get('model_save_path'):
        model_save_path = config['model_save_path']
        print(f"[调试] 接收到的原始模型保存路径: {model_save_path}", flush=True)
        print(f"[调试] 当前工作目录: {os.getcwd()}", flush=True)
        
        # 标准化路径分隔符（处理Windows路径）
        model_save_path = model_save_path.replace('\\', '/')
        print(f"[调试] 标准化路径分隔符后: {model_save_path}", flush=True)
        
        # 确保使用绝对路径 - 特别处理Windows盘符
        if not os.path.isabs(model_save_path):
            # 特别处理Windows盘符路径（可能没有被正确识别为绝对路径）
            if model_save_path.lower().startswith(('a:/', 'b:/', 'c:/', 'd:/', 'e:/', 'f:/', 'g:/', 'h:/', 'i:/', 'j:/', 'k:/', 'l:/', 'm:/', 'n:/', 'o:/', 'p:/', 'q:/', 'r:/', 's:/', 't:/', 'u:/', 'v:/', 'w:/', 'x:/', 'y:/', 'z:/')):
                # 已经是Windows绝对路径格式，只需标准化
                model_save_path = os.path.normpath(model_save_path)
                print(f"[调试] 识别为Windows绝对路径: {model_save_path}", flush=True)
            else:
                # 转换为绝对路径（基于当前工作目录）
                model_save_path = os.path.abspath(model_save_path)
                print(f"[调试] 转换相对路径为绝对路径: {model_save_path}", flush=True)
        else:
            print(f"[调试] 已识别为绝对路径: {model_save_path}", flush=True)
        
        # 再次标准化路径
        model_save_path = os.path.normpath(model_save_path)
        print(f"[调试] 最终标准化路径: {model_save_path}", flush=True)
        
        # 处理保存路径 - 确保是目录路径
        if os.path.splitext(model_save_path)[1]:  # 有扩展名，是文件路径
            save_dir = os.path.dirname(model_save_path)
        else:  # 是目录路径
            save_dir = model_save_path
        
        print(f"[调试] 确定的保存目录: {save_dir}", flush=True)
        
        # 创建统一的模型目录名
        model_dir_name = f"GPFedRec_TopkEF21_{config['dataset']}_r{config['num_round']}_lr{config['lr']}_{training_timestamp}"
        training_model_dir = os.path.join(save_dir, model_dir_name)
        
        print(f"[调试] 最终模型保存目录: {training_model_dir}", flush=True)
        
        # 确保目录存在（会自动创建所有父目录）
        try:
            # 使用makedirs递归创建完整的目录路径
            os.makedirs(training_model_dir, exist_ok=True)
            print(f"[调试] 成功确保模型目录存在: {training_model_dir}", flush=True)
            logging.info(f"成功确保模型保存目录存在: {training_model_dir}")
            
            # 验证目录确实存在
            if not os.path.exists(training_model_dir):
                raise Exception(f"目录创建后仍然不存在: {training_model_dir}")
            
            # 验证目录是否可写
            test_file = os.path.join(training_model_dir, 'test_write.tmp')
            try:
                with open(test_file, 'w') as f:
                    f.write('test')
                os.remove(test_file)
                print(f"[调试] 目录写入权限验证成功", flush=True)
                logging.info(f"目录写入权限验证成功: {training_model_dir}")
            except Exception as e:
                print(f"[错误] 目录写入权限验证失败: {e}", flush=True)
                logging.error(f"目录写入权限验证失败: {e}")
                raise Exception(f"目录无写入权限: {training_model_dir}")
                
        except Exception as e:
            print(f"[错误] 创建或验证模型目录失败: {e}", flush=True)
            logging.error(f"创建或验证模型保存目录失败: {e}")
            training_model_dir = None  # 如果创建失败，设为None以避免后续错误

    for round in range(config['num_round']):
        logging.info('-' * 80)
        logging.info('Round {} starts !'.format(round))
        
        # 标准化进度输出用于后端监控
        if config.get('progress_output', True):
            print(f"Round {round} starts !", flush=True)

        all_train_data = sample_generator.store_all_train_data(config['num_negative'])
        logging.info('-' * 80)
        logging.info('Training phase!')
        tr_loss = engine.fed_train_a_round(all_train_data, round_id=round)
        train_loss_list.append(tr_loss)

        logging.info('-' * 80)
        logging.info('Testing phase!')
        hit_ratio, ndcg, te_loss = engine.fed_evaluate(test_data)
        test_loss_list.append(te_loss)
        logging.info('[Testing Epoch {}] HR = {:.4f}, NDCG = {:.4f}'.format(round, hit_ratio, ndcg))
        hit_ratio_list.append(hit_ratio)
        ndcg_list.append(ndcg)

        # 记录最佳测试结果
        if hit_ratio > best_test_hr:
            best_test_hr = hit_ratio
            best_test_ndcg = ndcg
            best_test_round = round
            
            # 保存最佳模型 - 使用统一的目录
            if training_model_dir and os.path.exists(training_model_dir):
                try:
                    print(f"[调试] 保存最佳模型到统一目录: {training_model_dir}", flush=True)
                    
                    # 验证目录不是当前工作目录
                    if os.path.abspath(training_model_dir) != os.path.abspath(os.getcwd()):
                        # 保存模型状态
                        model_state = {
                            'model_state_dict': engine.model.state_dict() if hasattr(engine, 'model') else None,
                            'config': config,
                            'round': round,
                            'best_hr': best_test_hr,
                            'best_ndcg': best_test_ndcg,
                            'hit_ratio_list': hit_ratio_list,
                            'ndcg_list': ndcg_list,
                            'train_loss_list': train_loss_list,
                            'timestamp': datetime.datetime.now().isoformat()
                        }
                        
                        import torch
                        # 只保存全局最佳模型，不再保存每轮的模型
                        latest_best_path = os.path.join(training_model_dir, 'best_model_latest.pth')
                        torch.save(model_state, latest_best_path)
                        logging.info(f"全局最佳模型已更新: {latest_best_path} (第{round}轮)")
                        print(f"[调试] 全局最佳模型已更新: {latest_best_path} (第{round}轮)", flush=True)
                    else:
                        print(f"[警告] 拒绝保存到当前工作目录，跳过模型保存", flush=True)
                        logging.warning("拒绝保存到当前工作目录，跳过模型保存")
                    
                except Exception as e:
                    logging.error(f"保存最佳模型失败: {e}")
                    print(f"[错误] 保存最佳模型失败: {e}", flush=True)
            else:
                if config.get('save_best_model', False):
                    print(f"[警告] 模型保存目录无效，跳过最佳模型保存", flush=True)
                    logging.warning("模型保存目录无效，跳过最佳模型保存")

        logging.info('-' * 80)
        logging.info('Validating phase!')
        val_hit_ratio, val_ndcg, v_loss = engine.fed_evaluate(validate_data)
        val_loss_list.append(v_loss)
        logging.info('[Validating Epoch {}] HR = {:.4f}, NDCG = {:.4f}'.format(round, val_hit_ratio, val_ndcg))
        val_hr_list.append(val_hit_ratio)
        val_ndcg_list.append(val_ndcg)

        if val_hit_ratio >= best_val_hr:
            best_val_hr = val_hit_ratio
            final_test_round = round

        # 记录通信开销监测
        if hasattr(engine, 'communication_stats') and engine.communication_stats:
            current_stats = engine.communication_stats[-1]  # 获取当前轮的统计
            logging.info(f"📊 第{round}轮通信开销对比:")
            logging.info(f"  - 原GPFedRec算法: {current_stats['original_algorithm_embeddings']:,} 个嵌入")
            logging.info(f"  - 改进算法: {current_stats['uploaded_embeddings']:,} 个嵌入")
            logging.info(f"  - 通信减少: {current_stats['communication_reduction']:.2f}%")
            logging.info(f"  - 节省嵌入: {current_stats['original_algorithm_embeddings'] - current_stats['uploaded_embeddings']:,} 个")

    # 记录实验结果总结函数
    def log_experiment_results(config, hit_ratio_list, ndcg_list, val_hr_list, val_ndcg_list, 
                              best_test_hr, best_test_ndcg, best_test_round, final_test_round):
        """记录详细的实验结果信息"""
        logging.info("=" * 100)
        logging.info("实验结果总结")
        logging.info("=" * 100)
        
        # 最佳性能结果
        logging.info("🏆 最佳性能结果:")
        logging.info(f"  - 最佳测试HR@10: {best_test_hr:.6f} (第{best_test_round}轮)")
        logging.info(f"  - 对应NDCG@10: {best_test_ndcg:.6f}")
        
        # 最终性能结果（基于验证集选择）
        final_hr = hit_ratio_list[final_test_round]
        final_ndcg = ndcg_list[final_test_round]
        final_val_hr = val_hr_list[final_test_round]
        final_val_ndcg = val_ndcg_list[final_test_round]
        
        logging.info(f"\n📊 最终性能结果 (第{final_test_round}轮):")
        logging.info(f"  - 测试集HR@10: {final_hr:.6f}")
        logging.info(f"  - 测试集NDCG@10: {final_ndcg:.6f}")
        logging.info(f"  - 验证集HR@10: {final_val_hr:.6f}")
        logging.info(f"  - 验证集NDCG@10: {final_val_ndcg:.6f}")
        
        # 收敛分析
        logging.info(f"\n📈 收敛分析:")
        logging.info(f"  - 训练总轮数: {len(hit_ratio_list)}")
        logging.info(f"  - 最佳性能出现轮次: {best_test_round}")
        logging.info(f"  - 最终选择轮次: {final_test_round}")
        
        # 性能趋势
        if len(hit_ratio_list) >= 10:
            early_hr_avg = sum(hit_ratio_list[:10]) / 10
            late_hr_avg = sum(hit_ratio_list[-10:]) / 10
            early_ndcg_avg = sum(ndcg_list[:10]) / 10
            late_ndcg_avg = sum(ndcg_list[-10:]) / 10
            
            logging.info(f"  - 前10轮平均HR@10: {early_hr_avg:.6f}")
            logging.info(f"  - 后10轮平均HR@10: {late_hr_avg:.6f}")
            logging.info(f"  - 前10轮平均NDCG@10: {early_ndcg_avg:.6f}")
            logging.info(f"  - 后10轮平均NDCG@10: {late_ndcg_avg:.6f}")
            
            hr_improvement = (late_hr_avg - early_hr_avg) / early_hr_avg * 100
            ndcg_improvement = (late_ndcg_avg - early_ndcg_avg) / early_ndcg_avg * 100
            logging.info(f"  - HR@10整体提升: {hr_improvement:+.2f}%")
            logging.info(f"  - NDCG@10整体提升: {ndcg_improvement:+.2f}%")
        
        # 实验配置回顾
        logging.info(f"\n⚙️ 实验配置回顾:")
        logging.info(f"  - 算法版本: GPFedRec-TopkEF21")
        logging.info(f"  - 数据集: {config['dataset']}")
        logging.info(f"  - 学习率: {config['lr']}")
        logging.info(f"  - 训练轮数: {config['num_round']}")
        
        # 技术特性状态
        logging.info(f"\n🔧 启用的技术特性:")
        features = []
        if config['adaptive_reg'] == 'user':
            features.append("✅ 用户自适应正则化")
        else:
            features.append("❌ 用户自适应正则化 (使用固定正则化)")
            
        # 聚合方法固定为clustering_then_graph
        features.append(f"✅ 聚类后图聚合 (聚类数: {config['n_clusters']})")
            
        # GPFedRec-TopkEF21专用Top-k+EF21压缩
        features.append("✅ Top-k+EF21专用压缩")
            
        # 隐私保护状态
        if config['privacy_method'] == 'differential_privacy':
            features.append(f"🔒 隐私保护: 轻量差分隐私 (噪声尺度={config['dp']})")
        elif config['privacy_method'] == 'none':
            features.append("⚪ 隐私保护: 无")
        
        # Top-k稀疏化与EF21状态（固定启用）
        topk_desc = f"🎯 固定Top-k+EF21: {config.get('topk_ratio', 0.1)*100:.0f}%"
        
        # 添加聚类配合信息（固定启用累积交互）
        clustering_freq = config.get('clustering_update_frequency', 10)
        topk_desc += f" + 累积历史聚类(每{clustering_freq}轮)"
        
        features.append(topk_desc)
        
        for feature in features:
            logging.info(f"  {feature}")
        
        # 文件信息
        logging.info(f"\n📁 日志文件: {log_filename}")
        logging.info(f"📊 结果已保存到: sh_result/{config['dataset']}.txt")
        
        logging.info("=" * 100)
        logging.info("✅ 实验完成！")
        logging.info("=" * 100)

    # 记录详细的实验结果
    log_experiment_results(config, hit_ratio_list, ndcg_list, val_hr_list, val_ndcg_list,
                          best_test_hr, best_test_ndcg, best_test_round, final_test_round)
    
    # 训练完成后保存最终模型 - 使用同一个统一目录
    if training_model_dir and os.path.exists(training_model_dir):
        try:
            print(f"[调试] 保存最终模型到统一目录: {training_model_dir}", flush=True)
            
            # 验证目录不是当前工作目录
            if os.path.abspath(training_model_dir) != os.path.abspath(os.getcwd()):
                # 保存最终完整模型状态
                final_model_state = {
                    'model_state_dict': engine.model.state_dict() if hasattr(engine, 'model') else None,
                    'config': config,
                    'training_completed': True,
                    'total_rounds': config['num_round'],
                    'best_test_hr': best_test_hr,
                    'best_test_ndcg': best_test_ndcg,
                    'best_test_round': best_test_round,
                    'final_test_round': final_test_round,
                    'final_hr': hit_ratio_list[final_test_round],
                    'final_ndcg': ndcg_list[final_test_round],
                    'hit_ratio_list': hit_ratio_list,
                    'ndcg_list': ndcg_list,
                    'val_hr_list': val_hr_list,
                    'val_ndcg_list': val_ndcg_list,
                    'train_loss_list': train_loss_list,
                    'test_loss_list': test_loss_list,
                    'val_loss_list': val_loss_list,
                    'timestamp': datetime.datetime.now().isoformat()
                }
                
                import torch
                # 主要模型文件
                final_model_path = os.path.join(training_model_dir, 'final_model.pth')
                torch.save(final_model_state, final_model_path)
                logging.info(f"最终模型已保存到: {final_model_path}")
                print(f"[调试] 最终模型已保存到: {final_model_path}", flush=True)
                
                # 创建模型信息文件
                info_file_path = os.path.join(training_model_dir, 'model_info.txt')
                with open(info_file_path, 'w', encoding='utf-8') as f:
                    f.write(f"GPFedRec-TopkEF21 训练完成模型\n")
                    f.write(f"=" * 50 + "\n")
                    f.write(f"训练时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"数据集: {config['dataset']}\n")
                    f.write(f"训练轮数: {config['num_round']}\n")
                    f.write(f"学习率: {config['lr']}\n")
                    f.write(f"客户端采样比例: {config['clients_sample_ratio']}\n")
                    f.write(f"Top-k比例: {config.get('topk_ratio', 0.1)}\n")
                    f.write(f"聚类数量: {config['n_clusters']}\n")
                    f.write(f"隐私方法: {config['privacy_method']}\n")
                    f.write(f"\n性能结果:\n")
                    f.write(f"最佳测试HR@10: {best_test_hr:.6f} (第{best_test_round}轮)\n")
                    f.write(f"最佳测试NDCG@10: {best_test_ndcg:.6f}\n")
                    f.write(f"最终HR@10: {hit_ratio_list[final_test_round]:.6f} (第{final_test_round}轮)\n")
                    f.write(f"最终NDCG@10: {ndcg_list[final_test_round]:.6f}\n")
                
                logging.info(f"模型信息已保存到: {info_file_path}")
                print(f"[调试] 模型信息已保存到: {info_file_path}", flush=True)
                print(f"Training completed! Model saved to: {training_model_dir}", flush=True)
            else:
                print(f"[警告] 拒绝保存最终模型到当前工作目录", flush=True)
                logging.warning("拒绝保存最终模型到当前工作目录")
            
        except Exception as e:
            logging.error(f"保存最终模型失败: {e}")
            print(f"[错误] 保存最终模型失败: {e}", flush=True)
    else:
        if config.get('save_best_model', False):
            print(f"[警告] 模型保存目录无效，跳过最终模型保存", flush=True)
            logging.warning("模型保存目录无效，跳过最终模型保存")

    # 保存结果到文件 (保持原有格式兼容性)
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    result_str = current_time + '-' + 'layers: ' + str(config['layers']) + '-' + 'lr: ' + str(config['lr']) + '-' + \
          'clients_sample_ratio: ' + str(config['clients_sample_ratio']) + '-' + 'num_round: ' + str(config['num_round']) \
          + '-' 'neighborhood_size: ' + str(config['neighborhood_size']) + '-' + 'mp_layers: ' + str(config['mp_layers']) \
          + '-' + 'negatives: ' + str(config['num_negative']) + '-' + 'lr_eta: ' + str(config['lr_eta']) + '-' + \
          'batch_size: ' + str(config['batch_size']) + '-' + 'hr: ' + str(hit_ratio_list[final_test_round]) + '-' \
          + 'ndcg: ' + str(ndcg_list[final_test_round]) + '-' + 'best_round: ' + str(final_test_round) + '-' + \
          'similarity_metric: ' + str(config['similarity_metric']) + '-' + 'neighborhood_threshold: ' + \
          str(config['neighborhood_threshold']) + '-' + 'reg: ' + str(config['reg']) + '-' + \
          'topk_ef21_compression: True' + '-' + 'aggregation_method: clustering_then_graph' + \
          '-' + 'adaptive_reg: ' + str(config['adaptive_reg']) + '-' + 'n_clusters: ' + str(config['n_clusters']) + \
          '-' + 'privacy_method: ' + str(config['privacy_method'])

    file_name = "sh_result/"+'-'+config['dataset']+".txt"
    with open(file_name, 'a') as file:
        file.write(result_str + '\n')

    # 兼容性日志记录 (保持原有格式)
    logging.info('gpfedrec_topk_ef21')
    logging.info('clients_sample_ratio: {}, lr_eta: {}, bz: {}, lr: {}, dataset: {}, layers: {}, negatives: {}, '
                 'neighborhood_size: {}, neighborhood_threshold: {}, mp_layers: {}, similarity_metric: {}, '
                 'topk_ef21_compression: True, aggregation_method: clustering_then_graph, adaptive_reg: {}, n_clusters: {}'.
                 format(config['clients_sample_ratio'], config['lr_eta'], config['batch_size'], config['lr'],
                        config['dataset'], config['layers'], config['num_negative'], config['neighborhood_size'],
                        config['neighborhood_threshold'], config['mp_layers'], config['similarity_metric'],
                        config['adaptive_reg'], 
                        config['n_clusters']))

    logging.info('hit_list: {}'.format(hit_ratio_list))
    logging.info('ndcg_list: {}'.format(ndcg_list))
    logging.info('Best test hr: {}, ndcg: {} at round {}'.format(hit_ratio_list[final_test_round],
                                                                 ndcg_list[final_test_round],
                                                                 final_test_round))

    # 通信开销分析
    if hasattr(engine, 'communication_stats') and engine.communication_stats:
        logging.info(f"\n📡 通信开销总结 (vs 原GPFedRec算法):")
        all_stats = engine.communication_stats
        
        # 计算总体统计
        total_uploaded = sum(stat['uploaded_embeddings'] for stat in all_stats)
        total_original = sum(stat['original_algorithm_embeddings'] for stat in all_stats)
        avg_reduction = sum(stat['communication_reduction'] for stat in all_stats) / len(all_stats)
        
        logging.info(f"  - 原算法总需上传: {total_original:,} 个嵌入")
        logging.info(f"  - 改进算法实际上传: {total_uploaded:,} 个嵌入")
        logging.info(f"  - 平均通信减少: {avg_reduction:.2f}%")
        logging.info(f"  - 总节省嵌入: {total_original - total_uploaded:,} 个")
        logging.info(f"  - 压缩比: {total_uploaded / total_original:.4f}:1") 