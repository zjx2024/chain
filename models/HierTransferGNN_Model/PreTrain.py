import datetime
import os

import torch
from dgl.sampling import random_walk
from gensim.models import Word2Vec
import networkx as nx
# def compute_structural_features(g, node_type):
#     """
#     计算指定节点类型的结构特征：入度和 PageRank 得分。
#     对于产品节点，使用 'pp' 边计算入度；
#     对于公司节点，使用产品-公司边 ('product','pc','company') 计算入度，
#     然后基于产品-公司二分图投影构造同构的公司图计算 PageRank 得分.
#     返回张量形状为 (num_nodes, 2).
#     """
#     if node_type == 'product':
#         v = torch.arange(g.num_nodes('product'), device=g.device)
#         degree = g.in_degrees(v, etype=('product', 'pp', 'product')).float().unsqueeze(1)
#         sub_g = g['product', 'pp', 'product'].cpu()
#         nx_g = dgl.to_networkx(sub_g)
#         nodes = sorted(nx_g.nodes(), key=lambda x: int(x) if str(x).isdigit() else x)
#         pr_dict = nx.pagerank(nx_g)
#         num = len(nodes)
#         pr_scores = torch.zeros(num, 1)
#         for idx, node in enumerate(nodes):
#             pr_scores[idx] = pr_dict.get(node, 0)
#         struct_feats = torch.cat([degree.cpu(), pr_scores], dim=1)
#         return struct_feats
#     elif node_type == 'company':
#         # 使用产品-公司边计算公司节点入度
#         v = torch.arange(g.num_nodes('company'), device=g.device)
#         degree = g.in_degrees(v, etype=('product', 'pc', 'company')).float().unsqueeze(1)
#         # 构造产品-公司二分图
#         bipartite = g['product', 'pc', 'company'].cpu()
#         src, dst = bipartite.all_edges(form='uv')
#         prod_to_comp = {}
#         for p, c in zip(src, dst):
#             p = int(p)
#             c = int(c)
#             if p not in prod_to_comp:
#                 prod_to_comp[p] = []
#             prod_to_comp[p].append(c)
#         company_edges = []
#         for comp_list in prod_to_comp.values():
#             n = len(comp_list)
#             for i in range(n):
#                 for j in range(n):
#                     if i != j:
#                         company_edges.append((comp_list[i], comp_list[j]))
#         if company_edges:
#             src_c, dst_c = zip(*company_edges)
#             company_g = dgl.graph((list(src_c), list(dst_c)), num_nodes=g.num_nodes('company'))
#         else:
#             company_g = dgl.graph(([], []), num_nodes=g.num_nodes('company'))
#         nx_company = dgl.to_networkx(company_g)
#         nodes = sorted(nx_company.nodes(), key=lambda x: int(x) if str(x).isdigit() else x)
#         pr_dict = nx.pagerank(nx_company)
#         num = len(nodes)
#         pr_scores = torch.zeros(num, 1)
#         for idx, node in enumerate(nodes):
#             pr_scores[idx] = pr_dict.get(node, 0)
#         struct_feats = torch.cat([degree.cpu(), pr_scores], dim=1)
#         return struct_feats
#     else:
#         raise ValueError("Unsupported node type: {}".format(node_type))
"""
    对图 g 中指定节点类型（node_type）的节点进行 metapath2vec 预训练，
    使用给定的 meta_paths（每个元路径为一个列表，列表元素为 canonical edge type 元组，
    例如 ('product','pc','company') 或 ('company','cp','product')）。

    对于每个元路径，采样随机游走；随机游走的起始节点为所有 node_type 类型的节点。
    将所有随机游走转换为字符串序列后，用 gensim 的 Word2Vec 训练嵌入，
    最后返回形状为 (num_nodes, d) 的节点嵌入张量。

    参数：
      g           : DGLHeteroGraph
      node_type   : str，目标节点类型（如 'product' 或 'company'）
      meta_paths  : list，每个元素是一个元路径（列表），要求元路径第一个元素的源节点类型等于 node_type
      num_traces  : int，每个起始节点采样的随机游走数量
      trace_length: int，每次随机游走的步数（注意返回的序列长度为 trace_length+1）
      d           : int，嵌入维度

    返回：
      embeddings: Tensor，形状 (num_nodes, d)
"""
SEED = 999



def metapath2vec_pretraining_node(g, node_type, meta_paths, num_traces, trace_length, d=18,save_dir='embeddings_save/', save_format='pt'):

    all_walks = []
    num_nodes = g.num_nodes(node_type)
    start_nodes = list(range(num_nodes))
    g_cpu = g.cpu()
    for meta_path in meta_paths:

        current_trace_length = trace_length*len(meta_path) if trace_length is not None else len(meta_path)
        for _ in range(num_traces):
            traces, _ = random_walk(g_cpu, start_nodes, metapath=meta_path*trace_length, length=current_trace_length)
            traces = traces.tolist()
            for walk in traces:
                walk_str = [str(x) for x in walk if x != -1]
                if len(walk_str) > 1:
                    all_walks.append(walk_str)
    # 用 gensim 训练 Word2Vec 模型
    w2v_model = Word2Vec(sentences=all_walks,
                         vector_size=d,
                         window=5,
                         min_count=0,
                         sg=1,
                         workers=4,
                         epochs=60)
    embeddings = []
    for i in range(num_nodes):
        embeddings.append(torch.tensor(w2v_model.wv[str(i)], dtype=torch.float32))
    embeddings = torch.stack(embeddings, dim=0)

    return embeddings


import hashlib

def save_pretrain_emb(g, emb_dict, product_meta_paths, company_meta_paths, save_dir="saved_embeddings/"):
    """
    保存预训练嵌入及关联元数据
    :param g: 图对象
    :param emb_dict: {'product': tensor, 'company': tensor}
    """
    # 生成图结构哈希
    graph_hash = hashlib.sha256(str(g.canonical_etypes).encode()).hexdigest()[:8]

    # 生成时间戳
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    for ntype in emb_dict:
        # 构建保存路径
        type_dir = os.path.join(save_dir, ntype)
        os.makedirs(type_dir, exist_ok=True)

        # 准备元数据
        metadata = {
            'embeddings': emb_dict[ntype].cpu(),
            'node_ids': g.nodes(ntype).tolist(),
            'meta_paths': product_meta_paths if ntype=='product' else company_meta_paths,
            'graph_hash': graph_hash,
            'create_time': timestamp
        }

        # 保存文件
        save_path = os.path.join(type_dir, f"{timestamp}_{graph_hash}_meta_emb.pt")
        torch.save(metadata, save_path)
        print(f"Saved {ntype} embeddings to {save_path}")


# def load_pretrain_emb(g, ntype, save_dir="saved_embeddings"):
#     """
#     加载最新且匹配图结构的预训练嵌入
#     :return: tensor 或 None（未找到时）
#     """
#     # 计算当前图哈希
#     current_hash = hashlib.sha256(str(g.canonical_etypes).encode()).hexdigest()[:8]
#
#     # 获取所有候选文件
#     emb_dir = os.path.join(save_dir, ntype)
#     if not os.path.exists(emb_dir):
#         return None
#
#     candidates = []
#     for fname in os.listdir(emb_dir):
#         if fname.endswith(".pt"):
#             timestamp, hash_part = fname.split('_')[:2]
#             candidates.append( (timestamp, hash_part, fname) )
#
#     # 按时间倒序检查哈希匹配
#     for ts, h, f in sorted(candidates, reverse=True):
#         if h == current_hash:
#             metadata = torch.load(os.path.join(emb_dir, f))
#             # 验证节点ID一致性
#             if metadata['node_ids'] == g.nodes(ntype).tolist():
#                 print(f"Loading cached {ntype} embeddings ({ts})")
#                 return metadata['embeddings'].to(device)
#     return None

############################################
# 示例：定义元路径列表并调用预训练函数
############################################
def test32():
    # 定义针对产品节点的元路径（均以 'product' 作为起始）
    product_meta_path1 = [('product','pc','company'), ('company','cp','product')]
    product_meta_path2 = [('product','pp','product'), ('product','pc','company'), ('company','cp','product')]
    product_meta_path3 = [('product','pc','company'), ('company','cp','product'), ('product','pp','product')]
    product_meta_paths = [product_meta_path1, product_meta_path2, product_meta_path3]

    # 定义针对公司节点的元路径（均以 'company' 作为起始）
    company_meta_path1 = [('company','cp','product'), ('product','pc','company')]
    company_meta_path2 = [('company','cp','product'), ('product','pp','product'), ('product','pc','company')]
    company_meta_paths = [company_meta_path1, company_meta_path2]


    from data_read import excel_to_dgl_graph_direct
    src_file="../data/output_product.xlsx"
    pp_sheet = "产品-产品"
    pc_sheet = "产品-公司"
    feature_sheet = "2022Q4"
    # 构造模拟图
    g,_,_,_ = excel_to_dgl_graph_direct(file_name=src_file,
                                  pp_matrix_sheet=pp_sheet,
                                  pc_matrix_sheet=pc_sheet,
                                  feature_matrix_sheet=feature_sheet)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    g = g.to(device)

    # 调用产品节点预训练
    prod_embeddings = metapath2vec_pretraining_node(g, 'product', product_meta_paths, num_traces=10, trace_length=20, d=18).to(device)
    print("Pretrained product embeddings shape:", prod_embeddings.shape)

    # 调用公司节点预训练
    comp_embeddings = metapath2vec_pretraining_node(g, 'company', company_meta_paths, num_traces=10, trace_length=20, d=18).to(device)
    print("Pretrained company embeddings shape:", comp_embeddings.shape)
