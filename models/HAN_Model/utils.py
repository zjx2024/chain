import datetime
import errno
import os
import dgl
import numpy as np
import torch
import pandas as pd
import dgl
import torch
import random

from sklearn.model_selection import train_test_split


def set_random_seed(seed=324):
    """Set random seed.
    Parameters
    ----------
    seed : int
        Random seed to use
    """
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)

def mkdir_p(path, log=True):
    """Create a directory for the specified path.
    Parameters
    ----------
    path : str
        Path name
    log : bool
        Whether to print result for directory creation
    """
    try:
        os.makedirs(path)
        if log:
            print("Created directory {}".format(path))
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path) and log:
            print("Directory {} already exists.".format(path))
        else:
            raise

def get_date_postfix():
    """Get a date based postfix for directory name.
    Returns
    -------
    post_fix : str
    """
    dt = datetime.datetime.now()
    post_fix = "{}_{:02d}-{:02d}-{:02d}".format(
        dt.date(), dt.hour, dt.minute, dt.second
    )

    return post_fix

def setup_log_dir(args, sampling=False, custom_base_dir=None):
    """Name and create directory for logging.
    Parameters
    ----------
    args : dict
        Configuration
    sampling : bool
        Whether we are using sampling based training
    custom_base_dir : str
        Custom base directory for logging (if provided, will use this instead of args["log_dir"])
    Returns
    -------
    log_dir : str
        Path for logging directory
    """
    date_postfix = get_date_postfix()
    
    # 如果提供了自定义基础目录，使用它；否则使用args中的log_dir
    base_dir = custom_base_dir if custom_base_dir else args["log_dir"]
    
    log_dir = os.path.join(
        base_dir, "{}_{}".format(args["dataset"], date_postfix)
    )

    if sampling:
        log_dir = log_dir + "_sampling"

    mkdir_p(log_dir)
    return log_dir

def print_distribution(name, mask, labels):
    label_counts = torch.unique(labels[mask], return_counts=True)
    print(f"{name} 分布: 0类={label_counts[1][0].item()}, 1类={label_counts[1][1].item()}")


default_configure = {
    "lr": 0.001,  # Learning rate
    "num_heads": [12],  # Number of attention heads for node-level attention
    "hidden_units": 128,
    "dropout": 0.4,
    "weight_decay": 0.001,
    "num_epochs": 800,
    "patience": 80,
}

sampling_configure = {"batch_size": 20}

#设置
def setup(args):
    config = default_configure.copy()
    if "epochs" in args and args["epochs"] is not None:
        config["num_epochs"] = args["epochs"]
    if "lr" in args and args["lr"] is not None:
        config["lr"] = args["lr"]
    args.update(config)
    
    set_random_seed(args["seed"])
    args["dataset"] = "IndustryChain"
    args["device"] = "cuda:0" if torch.cuda.is_available() else "cpu"
    
    # 如果提供了自定义的模型保存目录，使用它作为日志目录的基础
    if "model_save_dir" in args and args["model_save_dir"]:
        args["log_dir"] = setup_log_dir(args, custom_base_dir=args["model_save_dir"])
    else:
        args["log_dir"] = setup_log_dir(args)
    
    return args


def setup_for_sampling(args):
    args.update(default_configure)
    args.update(sampling_configure)
    set_random_seed()
    args["device"] = "cuda:0" if torch.cuda.is_available() else "cpu"
    args["log_dir"] = setup_log_dir(args, sampling=True)
    return args

def get_binary_mask(total_size, indices):
    mask = torch.zeros(total_size, dtype=torch.bool)
    mask[indices] = True
    return mask

def get_data_split(g,node_labels):

    all_indices = np.arange(g.num_nodes('company'))
    idx_train, temp_idx_np = train_test_split(
    all_indices,
        test_size=0.4,
        stratify=node_labels.cpu().numpy(),  # 关键修改：添加分层
        random_state=42
    )
    labels_temp = node_labels[temp_idx_np]  # 获取临时集的标签
    idx_val, idx_test = train_test_split(
        temp_idx_np,
        test_size=0.5,
        stratify=labels_temp.cpu().numpy(),  # 分层
        random_state=42
    )
    idx_train = torch.tensor(idx_train.tolist())
    idx_val = torch.tensor(idx_val.tolist())
    idx_test = torch.tensor(idx_test.tolist())
    num_nodes = g.num_nodes('company') # 公司节点的数量
    train_mask = get_binary_mask(num_nodes, idx_train)
    val_mask = get_binary_mask(num_nodes, idx_val)
    test_mask = get_binary_mask(num_nodes, idx_test)


    print_distribution("训练集", train_mask, node_labels)
    print_distribution("验证集", val_mask, node_labels)
    print_distribution("测试集", test_mask, node_labels)

    return idx_train, idx_val, idx_test, train_mask, val_mask, test_mask
def feature_label_read(file_path, sheet_name):
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    # 提取节点特征（公司节点1-18）
    node_features = df.iloc[:, 1:19].values  # 选取1到18列的数据
    node_features = torch.tensor(node_features, dtype=torch.float32)

    # 提取节点标签（公司节点标签，序号19）
    node_labels = df.iloc[:, 19].values  # 选取第19列的数据
    node_labels = torch.tensor(node_labels, dtype=torch.long)

    return node_features, node_labels

def excel_to_graph(file_name, pp_matrix_sheet, pc_matrix_sheet):
    """
    从 Excel 文件中读取产品-产品和产品-公司邻接矩阵，构造异构图。
    Args:
        file_name (str): Excel 文件路径
        pp_matrix_sheet (str): 产品-产品邻接矩阵所在 sheet（行列均为产品编号）
        pc_matrix_sheet (str): 产品-公司邻接矩阵所在 sheet（行为产品编号，列为公司编号）
    Returns:
        g (dgl.DGLHeteroGraph): 构造好的异构图
    """

    df_pp = pd.read_excel(file_name, sheet_name=pp_matrix_sheet, index_col=0, dtype=int)
    product_ids = df_pp.index.tolist()  # 产品编号列表

    # 读取产品-公司邻接矩阵（行：产品编号，列：公司编号）
    df_pc = pd.read_excel(file_name, sheet_name=pc_matrix_sheet, index_col=0, dtype=int)

    # 构造产品-产品边（邻接矩阵本身已对称，直接将所有满足条件的边加入）
    src_pp, dst_pp = [], []
    for src_id in product_ids:
        for dst_id in product_ids:
            if df_pp.loc[src_id, dst_id] == 1:
                src_pp.append(src_id)
                dst_pp.append(dst_id)

    # 构造产品-公司和公司-产品边
    src_pc, dst_pc = [], []  # 产品 -> 公司
    src_cp, dst_cp = [], []  # 公司 -> 产品
    for product_id in df_pc.index:
        for company_id in df_pc.columns:
            if df_pc.loc[product_id, company_id] == 1:
                src_pc.append(product_id)
                dst_pc.append(company_id)
                src_cp.append(company_id)
                dst_cp.append(product_id)

    # 构造异构图
    graph_data = {
        ('product', 'pp', 'product'): (src_pp, dst_pp),
        ('product', 'pc', 'company'): (src_pc, dst_pc),
        ('company', 'cp', 'product'): (src_cp, dst_cp)
    }
    g = dgl.heterograph(graph_data)
    print(g)
    dgl.save_graphs('graph/Inte_Graph.pt',g)

    return None

def excel_to_dgl_graph(file_name,feature_matrix_sheet,graph_path):

    #读取图
    g=dgl.load_graphs(graph_path)[0][0]
    # 读取公司节点特征和标签
    node_features, node_labels = feature_label_read(file_name, feature_matrix_sheet)
    idx_train, idx_val, idx_test, train_mask, val_mask, test_mask=get_data_split(g,node_labels)
    num_classes=2

    return (
        g,
        node_features,
        node_labels,
        num_classes,
        idx_train,
        idx_val,
        idx_test,
        train_mask,
        val_mask,
        test_mask,
    )
def excel_to_dgl_graph_direct(file_name, pp_matrix_sheet, pc_matrix_sheet, feature_matrix_sheet):
    """
    从 Excel 文件中读取产品-产品和产品-公司邻接矩阵，构造异构图。

    Args:
        file_name (str): Excel 文件路径
        pp_matrix_sheet (str): 产品-产品邻接矩阵所在 sheet（行列均为产品编号）
        pc_matrix_sheet (str): 产品-公司邻接矩阵所在 sheet（行为产品编号，列为公司编号）
        feature_matrix_sheet(str): 财务特征矩阵所在 sheet，包含公司节点的特征和标签
    Returns:
        g (dgl.DGLHeteroGraph): 构造好的异构图
        product_ids (list): 产品节点的编号列表
    """
    # 读取产品-产品邻接矩阵（假设行列编号均为整数）
    df_pp = pd.read_excel(file_name, sheet_name=pp_matrix_sheet, index_col=0, dtype=int)
    product_ids = df_pp.index.tolist()  # 产品编号列表

    # 读取产品-公司邻接矩阵（行：产品编号，列：公司编号）
    df_pc = pd.read_excel(file_name, sheet_name=pc_matrix_sheet, index_col=0, dtype=int)

    # 构造产品-产品边（邻接矩阵本身已对称，直接将所有满足条件的边加入）
    src_pp, dst_pp = [], []
    for src_id in product_ids:
        for dst_id in product_ids:
            if df_pp.loc[src_id, dst_id] == 1:
                src_pp.append(src_id)
                dst_pp.append(dst_id)

    # 构造产品-公司和公司-产品边
    src_pc, dst_pc = [], []  # 产品 -> 公司
    src_cp, dst_cp = [], []  # 公司 -> 产品
    for product_id in df_pc.index:
        for company_id in df_pc.columns:
            if df_pc.loc[product_id, company_id] == 1:
                src_pc.append(product_id)
                dst_pc.append(company_id)
                src_cp.append(company_id)
                dst_cp.append(product_id)

    # 构造异构图
    graph_data = {
        ('product', 'pp', 'product'): (src_pp, dst_pp),
        ('product', 'pc', 'company'): (src_pc, dst_pc),
        ('company', 'cp', 'product'): (src_cp, dst_cp)
    }
    g = dgl.heterograph(graph_data)

    # 读取公司节点特征和标签
    node_features, node_labels = feature_label_read(file_name, feature_matrix_sheet)


    all_indices = np.arange(g.num_nodes('company'))
    idx_train, temp_idx_np = train_test_split(all_indices, test_size=0.4, random_state=42)
    idx_val, idx_test = train_test_split(temp_idx_np, test_size=0.5, random_state=42)


    # idx_train,idx_val,idx_test=get_index(2405,0.6)
    idx_train = torch.tensor(idx_train.tolist())
    idx_val = torch.tensor(idx_val.tolist())
    idx_test = torch.tensor(idx_test.tolist())
    num_classes = 2
    num_nodes = 2405# 公司节点的数量
    train_mask = get_binary_mask(num_nodes, idx_train)
    val_mask = get_binary_mask(num_nodes, idx_val)
    test_mask = get_binary_mask(num_nodes, idx_test)

    return (
        g,
        node_features,
        node_labels,
        num_classes,
        idx_train,
        idx_val,
        idx_test,
        train_mask,
        val_mask,
        test_mask,
    )
def get_index(data_shape,percent):
    if percent==0.6:
        t = []
        for i in range(data_shape):
            t.append(i)
        a = random.sample(t, 1443)
        t = [i for i in t if i not in a]
        b = random.sample(t, 240)
        c = [i for i in t if i not in b]
        c = random.sample(c,240)
        return a,b,c
    elif percent==0.2:
        t = []
        for i in range(data_shape):
            t.append(i)
        a = random.sample(t, 481)
        t = [i for i in t if i not in a]
        b = random.sample(t, 240)
        c = [i for i in t if i not in b]
        c = random.sample(c,240)
        return a, b, c
    elif percent == 0.8:
        t = []
        for i in range(data_shape):
            t.append(i)
        a = random.sample(t, 1924)
        t = [i for i in t if i not in a]
        b = random.sample(t, 240)
        c = [i for i in t if i not in b]
        return a, b, c
    elif percent==0.4:
        t = []
        for i in range(data_shape):
            t.append(i)
        a = random.sample(t, 962)
        t = [i for i in t if i not in a]
        b = random.sample(t, 240)
        c = [i for i in t if i not in b]
        c = random.sample(c, 240)

        return a, b, c

# if __name__ == '__main__':
#     file_name="../data/Inte/Graph_generate.xlsx"
#     p_c_matrix_sheet = "P-C"
#     p_p_matrix_sheet = "P-P"
#
#     excel_to_graph(file_name,p_p_matrix_sheet,p_c_matrix_sheet)
