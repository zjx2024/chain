import dgl
import torch
import torch.nn as nn
import torch.nn.functional as F
from dgl.nn.pytorch import SAGEConv


class SemanticAttention(nn.Module):
    def __init__(self, in_size, hidden_size=128):
        super(SemanticAttention, self).__init__()

        self.project = nn.Sequential(
            nn.Linear(in_size, hidden_size),
            nn.Tanh(),
            nn.Linear(hidden_size, 1, bias=False),
        )

    def forward(self, z):
        w = self.project(z).mean(0)  # (M, 1)
        beta = torch.softmax(w, dim=0)  # (M, 1)
        beta = beta.expand((z.shape[0],) + beta.shape)  # (N, M, 1)

        return (beta * z).sum(1)  # (N, D * K)

class HANLayer(nn.Module):

    def __init__(self, meta_paths, in_size, out_size,layer_num_heads, dropout):
        super(HANLayer, self).__init__()
        self.Sag_layers = nn.ModuleList()

        for i in range(len(meta_paths)+1):
            self.Sag_layers.append(
                SAGEConv(
                    in_size,
                    out_size,
                    "mean",
                    dropout,
                    activation=F.elu
                )
            )

        self.semantic_attention = SemanticAttention(
            in_size = out_size
        )

        self.meta_paths = list(tuple(meta_path) for meta_path in meta_paths)

        self._cached_graph = None
        self._cached_coalesced_graph = {}

    def forward(self, g, h, drop_rate=0.8):
        """
        前向传播，应用丢弃边操作。

        参数：
        g : DGLGraph
            输入的异构图
        h : tensor
            节点特征
        drop_rate : float
            丢弃边的比例

        返回：
        tensor
            经过处理的节点特征
        """
        semantic_embeddings = []

        if self._cached_graph is None or self._cached_graph is not g:
            self._cached_graph = g
            self._cached_coalesced_graph.clear()
            for meta_path in self.meta_paths:
                # 获取元路径下的同构图
                self._cached_coalesced_graph[meta_path] = dgl.metapath_reachable_graph(g, meta_path)

        for i, meta_path in enumerate(self.meta_paths):
            # 获取当前元路径对应的子图
            new_g = self._cached_coalesced_graph[meta_path]
            # 应用DropEdge，丢弃边
            new_g = drop_edge(new_g, drop_rate)
            semantic_embeddings.append(self.Sag_layers[i](new_g, h).flatten(1))

        # 将所有元路径的语义嵌入聚合
        semantic_embeddings = torch.stack(semantic_embeddings, dim=1)  # (N, M, D * K)

        return self.semantic_attention(semantic_embeddings)  # (N, D * K)
        # return self.fusion(semantic_embeddings)

def drop_edge(g, drop_rate=0.8, etype=None):
    """
    在给定的图中随机丢弃一部分边。

    参数：
    g : DGLGraph
        输入图
    drop_rate : float
        丢弃的边的比例（0到1之间）
    etype : str or tuple
        边类型。如果是异构图，必须指定一个边类型。

    返回：
    DGLGraph
        返回丢弃部分边后的图
    """
    device = g.device

    # 获取指定边类型的所有边
    if etype:
        edges = g.edges(etype=etype)
    else:
        # 如果没有指定边类型，则处理所有边
        edges = g.edges()

    num_edges = edges[0].shape[0]  # 获取图中边的总数
    drop_num = int(drop_rate * num_edges)  # 计算丢弃的边数
    drop_idx = torch.randperm(num_edges)[:drop_num]  # 随机选择丢弃的边

    # 确保 drop_idx 张量在与图相同的设备上，并且转换为 int32 类型
    drop_idx = drop_idx.to(device)

    # 从图中移除选中的边
    g.remove_edges(drop_idx, etype=etype)  # 从图中移除选中的边
    return g

class HAN(nn.Module):
    def __init__(
        self,meta_paths, in_size, hidden_size, out_size, num_heads, dropout
    ):
        super(HAN, self).__init__()

        self.layers = nn.ModuleList()
        self.layers.append(
            HANLayer(meta_paths, in_size, hidden_size, num_heads[0], dropout)
        )
        for l in range(1, len(num_heads)):
            self.layers.append(
                HANLayer(
                    meta_paths,
                    hidden_size * num_heads[l - 1],
                    hidden_size,
                    num_heads[l],
                    dropout,
                )
            )

        # 分类层
        self.predict = nn.Linear(hidden_size, out_size)

    def forward(self, g, h,drop_rate=0.8,return_features=False):
        for gnn in self.layers:
            h = gnn(g, h,drop_rate)
        features = h
        # 预测结果
        out = self.predict(features)
        if return_features:
            return features, out
        else:
            return out
