import random
from datetime import datetime

import numpy as np
import pandas as pd
import torch
import dgl
from dgl.sampling import random_walk
from gensim.models import Word2Vec
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

############################################
# 修改后的数据读取和特征处理部分
############################################

def feature_label_read(file_path, sheet_name):
    """（保持不变）"""
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    # 提取公司节点特征（假设 Excel 中第 2 ~ 19 列为特征）
    node_features = df.iloc[:, 1:19].values  # 注意：iloc 不包括最后一列，实际取1-18列
    node_features = torch.tensor(node_features, dtype=torch.float32)

    # 提取公司节点标签（假设第 20 列为标签）
    node_labels = df.iloc[:, 19].values
    node_labels = torch.tensor(node_labels, dtype=torch.long)

    return node_features, node_labels

def excel_to_dgl_graph_direct(file_name, pp_matrix_sheet, pc_matrix_sheet, feature_matrix_sheet):
    """（保持不变）"""
    # [原有实现保持不变]
     # 读取产品-产品邻接矩阵（假设行列编号均为整数）
    df_pp = pd.read_excel(file_name, sheet_name=pp_matrix_sheet, index_col=0, dtype=int)
    product_ids = df_pp.index.tolist()  # 获取产品编号列表

    # 读取产品-公司邻接矩阵（行：产品编号，列：公司编号）
    df_pc = pd.read_excel(file_name, sheet_name=pc_matrix_sheet, index_col=0, dtype=int)

    # 构造产品-产品边：遍历邻接矩阵中每个元素，若值为1，则认为存在边
    src_pp, dst_pp = [], []
    for src_id in product_ids:
        for dst_id in product_ids:
            if df_pp.loc[src_id, dst_id] == 1:
                src_pp.append(src_id)
                dst_pp.append(dst_id)

    # 构造产品-公司边（以及公司-产品边，双向关系）
    src_pc, dst_pc = [], []  # 表示产品 -> 公司边
    src_cp, dst_cp = [], []  # 表示公司 -> 产品边
    for product_id in df_pc.index:
        for company_id in df_pc.columns:
            if df_pc.loc[product_id, company_id] == 1:
                src_pc.append(product_id)
                dst_pc.append(company_id)
                src_cp.append(company_id)
                dst_cp.append(product_id)

    # 构造异构图数据字典
    graph_data = {
        ('product', 'pp', 'product'): (src_pp, dst_pp),
        ('product', 'pc', 'company'): (src_pc, dst_pc),
        ('company', 'cp', 'product'): (src_cp, dst_cp)
    }
    g = dgl.heterograph(graph_data)
    # 读取公司节点特征和风险标签
    node_features, node_labels = feature_label_read(file_name, feature_matrix_sheet)

    g.nodes['company'].data['feat'] = node_features
    return g, product_ids, node_features, node_labels

############################################
# 新增的metapath2vec嵌入生成部分
############################################

def generate_metapath_embeddings(g, metapath, num_walks=10, walk_length=3, window_size=5, embedding_size=18):
    """
    改进后的元路径嵌入生成函数
    """
    # 将图转移到CPU
    g_cpu = g.cpu()

    # 计算完整元路径长度
    full_metapath = metapath * walk_length
    current_trace_length = walk_length * len(metapath)

    # 获取公司节点信息
    company_nodes = torch.arange(g.number_of_nodes('company')).tolist()

    # 收集所有游走路径
    all_walks = []
    for _ in range(num_walks):
        # 执行随机游走
        traces, _ = random_walk(
            g_cpu,
            nodes=company_nodes,
            metapath=full_metapath,
            length=current_trace_length
        )

        # 处理游走路径
        for walk in traces.numpy():
            # 过滤无效节点(-1)并转换为字符串
            valid_walk = [str(int(node_id)) for node_id in walk if node_id != -1]
            # 仅保留长度大于1的有效路径
            if len(valid_walk) > 1:
                all_walks.append(valid_walk)

    # 训练Word2Vec模型
    w2v_model = Word2Vec(
        sentences=all_walks,
        vector_size=embedding_size,
        window=window_size,
        min_count=0,  # 允许所有节点
        sg=1,         # 使用skip-gram
        workers=4,
        epochs=10     # 适当减少迭代次数
    )

    # 生成嵌入矩阵
    embeddings = torch.zeros(g.number_of_nodes('company'), embedding_size)
    for idx in range(g.number_of_nodes('company')):
        embeddings[idx] = torch.tensor(w2v_model.wv[str(idx)], dtype=torch.float32)

    return embeddings

############################################
# 完整的分类流程
############################################

def main():

    SEED = 999
    random.seed(SEED)
    np.random.seed(SEED)
    torch.manual_seed(SEED)
    start_time  = datetime.now()

    # src_file = "../data/output_product.xlsx"
    # pp_sheet = "产品-产品"
    # pc_sheet = "产品-公司"
    # feature_sheet = "Electric_2020Q4"

    src_file = "./Graph_generate.xlsx"
    pp_sheet = "P-P"
    pc_sheet = "P-C"
    feature_sheet = "2022Q2"

    # 1. 读取数据并构建图
    g, _, _, labels = excel_to_dgl_graph_direct(
        src_file,
        pp_matrix_sheet=pp_sheet,
        pc_matrix_sheet=pc_sheet,
        feature_matrix_sheet=feature_sheet
    )

    # 2. 定义元路径（公司 -> 产品 -> 公司）
    metapath = ['cp', 'pc']  # 基础元路径
    metapath =['cp','pp','pc']
    # 3. 生成节点嵌入
    embeddings = generate_metapath_embeddings(
        g,
        metapath=['cp', 'pc'],  # 基础元路径
        num_walks=20,           # 增加游走次数
        walk_length=5,          # 元路径重复次数
        window_size=5,          # 上下文窗口
        embedding_size=128     # 嵌入维度
    )
    X_combined = np.concatenate([g.nodes['company'].data['feat'], embeddings.numpy()], axis=1)
    # 4. 准备训练数据
    X = X_combined
    y = labels.numpy()

    # 5. 划分训练测试集
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.4, random_state=42
    )

    # 6. 训练分类器
    clf = LogisticRegression(max_iter=1000)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    y_proba = clf.predict_proba(X_test)[:, 1]  # 获取正类概率

    # 计算各项指标
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)               # 默认使用binary模式
    auc = roc_auc_score(y_test, y_proba)        # 直接使用正类概率

    print(f"评估结果:\n"
          f"准确率: {accuracy:.4f}\n"
          f"F1分数: {f1:.4f}\n"
          f"AUC值: {auc:.4f}")
      # 转换为 NumPy

    # PCA 降维到 2 维
    pca = PCA(n_components=2)
    reduced_embeddings_np = pca.fit_transform(X_combined)

    # 转回 PyTorch 张量（可选）
    reduced_embeddings = torch.from_numpy(reduced_embeddings_np)

    # 计算均值
    mean_embeddings = torch.mean(reduced_embeddings, dim=0)

    print(mean_embeddings)
    end_time=datetime.now()
    print(f"总耗时: {end_time - start_time}")
    # 添加异常值处理
    if len(np.unique(y_test)) < 2:
        print("警告：测试集只包含一个类别，无法计算AUC")
        auc = 0.0

if __name__ == "__main__":
    main()