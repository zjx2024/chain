import pandas as pd
import torch
import dgl
############################################
# 1. 数据读取函数定义
############################################

def feature_label_read(file_path, sheet_name):
    """
    从指定的 sheet 中读取公司节点的财务特征和风险标签。

    Args:
        file_path (str): Excel 文件路径
        sheet_name (str): 包含财务特征和标签的 sheet 名称

    Returns:
        node_features (torch.Tensor): 公司节点的特征，形状 (num_company, 18)
        node_labels (torch.Tensor): 公司节点的标签，形状 (num_company,)
    """
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    # 提取公司节点特征（假设 Excel 中第 2 ~ 19 列为特征）
    node_features = df.iloc[:, 1:19].values  # 注意：iloc 不包括最后一列，实际取1-18列
    node_features = torch.tensor(node_features, dtype=torch.float32)

    # 提取公司节点标签（假设第 20 列为标签）
    node_labels = df.iloc[:, 19].values
    node_labels = torch.tensor(node_labels, dtype=torch.long)

    return node_features, node_labels


def excel_to_dgl_graph(file_name,feature_matrix_sheet,graph_path):

    #读取图
    g=dgl.load_graphs(graph_path)[0][0]
    # 读取公司节点特征和标签
    node_features, node_labels = feature_label_read(file_name, feature_matrix_sheet)
    return (
        g,
        node_features,
        node_labels,
    )

def excel_to_dgl_graph_direct(file_name, pp_matrix_sheet, pc_matrix_sheet, feature_matrix_sheet):
    """
    从 Excel 文件中读取产品-产品邻接矩阵、产品-公司邻接矩阵，
    构造一个包含产品和公司节点的异构图，并读取公司节点的财务特征和标签。

    Args:
        file_name (str): Excel 文件路径
        pp_matrix_sheet (str): 产品-产品邻接矩阵所在的 sheet（行列均为产品编号）
        pc_matrix_sheet (str): 产品-公司邻接矩阵所在的 sheet（行：产品编号，列：公司编号）
        feature_matrix_sheet (str): 公司节点财务特征与标签所在的 sheet

    Returns:
        g (dgl.DGLHeteroGraph): 构造好的异构图
        product_ids (list): 产品节点的编号列表（用于后续参考）
        node_features (torch.Tensor): 公司节点的特征（用于后续监督）
        node_labels (torch.Tensor): 公司节点的风险标签（用于监督）
    """
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

    return g, product_ids, node_features, node_labels


def excel_to_dgl_graph_separate(graph_file, pp_matrix_sheet, pc_matrix_sheet, feature_file):
    """
    从不同的Excel文件中读取图结构和特征数据，构造异构图。

    Args:
        graph_file (str): 包含图结构的Excel文件路径
        pp_matrix_sheet (str): 产品-产品邻接矩阵所在的 sheet（行列均为产品编号）
        pc_matrix_sheet (str): 产品-公司邻接矩阵所在的 sheet（行：产品编号，列：公司编号）
        feature_file (str): 包含特征和标签的Excel文件路径（使用第一个sheet）

    Returns:
        g (dgl.DGLHeteroGraph): 构造好的异构图
        product_ids (list): 产品节点的编号列表（用于后续参考）
        node_features (torch.Tensor): 公司节点的特征（用于后续监督）
        node_labels (torch.Tensor): 公司节点的风险标签（用于监督）
    """
    # 读取产品-产品邻接矩阵（假设行列编号均为整数）
    df_pp = pd.read_excel(graph_file, sheet_name=pp_matrix_sheet, index_col=0, dtype=int)
    product_ids = df_pp.index.tolist()  # 获取产品编号列表

    # 读取产品-公司邻接矩阵（行：产品编号，列：公司编号）
    df_pc = pd.read_excel(graph_file, sheet_name=pc_matrix_sheet, index_col=0, dtype=int)

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

    # 从特征文件读取公司节点特征和风险标签（使用第一个sheet）
    node_features, node_labels = feature_label_read(feature_file, 0)  # 0表示第一个sheet

    return g, product_ids, node_features, node_labels


