import dgl
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from dgl.nn.pytorch import GraphConv,HeteroGraphConv,SAGEConv,GATConv
import torch

# 4.2 公司节点融合模块：门控融合原始财务、预训练嵌入
SEED = 42
np.random.seed(SEED)
torch.manual_seed(SEED)
class CompanyFeatureFusion(nn.Module):
    def __init__(self, fin_dim, meta_dim, out_dim):
        super(CompanyFeatureFusion, self).__init__()
        self.fin_linear = nn.Linear(fin_dim, out_dim)
        self.meta_linear = nn.Linear(meta_dim, out_dim)
        self.gate_layer = nn.Linear(2 * out_dim, 2)

    def forward(self, fin_feat, meta_emb):
        fin_emb = self.fin_linear(fin_feat)         # (N, out_dim)
        meta_emb = self.meta_linear(meta_emb)         # (N, out_dim)
        concat = torch.cat([fin_emb, meta_emb], dim=1)  # (N, 2*out_dim)
        gate_logits = self.gate_layer(concat)         # (N, 2)
        weights = torch.softmax(gate_logits, dim=1)    # (N, 2)
        weights = weights.unsqueeze(2)                # (N, 2, 1)
        stacked = torch.stack([fin_emb, meta_emb], dim=1)  # (N, 2, out_dim)
        fused = torch.sum(weights * stacked, dim=1)     # (N, out_dim)
        return fused

############################################
# 5. 异构图学习模块
############################################

class RiskInjection(nn.Module):
    def __init__(self, in_feats):
        super(RiskInjection, self).__init__()
        self.fc = nn.Linear(in_feats, in_feats)

    def forward(self, h):
        gate = torch.sigmoid(self.fc(h))
        return gate * h

class HeteroRGCNLayer(nn.Module):
    def __init__(self, in_feats, out_feats, rel_names, risk_injection_alpha=0.5):
        super(HeteroRGCNLayer, self).__init__()
        self.conv = HeteroGraphConv({
            rel: GraphConv(in_feats, out_feats) for rel in rel_names
            # rel: GATConv(in_feats, out_feats,12) for rel in rel_names
        }, aggregate='mean')
        self.self_fc = nn.Linear(in_feats, out_feats)
        self.risk_injection = RiskInjection(out_feats)
        self.risk_injection_alpha = risk_injection_alpha

    def forward(self, g, inputs):
        for ntype in inputs:
            g.nodes[ntype].data['h'] = inputs[ntype]
        h_dict = self.conv(g, inputs)
        for ntype in h_dict:
            h_self = self.self_fc(inputs[ntype])
            h_dict[ntype] = h_dict[ntype] + h_self
        if 'company' in h_dict:
            h_company = h_dict['company']
            risk = self.risk_injection(h_company)
            h_dict['company'] = h_company + self.risk_injection_alpha * risk
        for ntype in h_dict:
            h_dict[ntype] = F.relu(h_dict[ntype])
        return h_dict


class GlobalRiskPredictor(nn.Module):
    def __init__(self, in_feats, hidden_feats, num_classes):
        super(GlobalRiskPredictor, self).__init__()
        self.fc1 = nn.Linear(in_feats, hidden_feats)
        self.fc2 = nn.Linear(hidden_feats, num_classes)

    def forward(self, g, features):
        if 'company' in features:
            comp_feats = features['company']
            graph_feat = comp_feats.mean(dim=0)
        else:
            all_feats = torch.cat(list(features.values()), dim=0)
            graph_feat = all_feats.mean(dim=0)
        x = F.relu(self.fc1(graph_feat))
        x = self.fc2(x)
        return x

# class GlobalRiskPredictor(nn.Module):
#     def __init__(self, in_feats, hidden_feats, num_classes):
#         super().__init__()
#         self.fc1 = nn.Linear(in_feats, hidden_feats)
#         self.fc2 = nn.Linear(hidden_feats, num_classes)
#         self.attention = nn.Linear(in_feats, 1)  # 添加注意力机制
#
#     def forward(self, g, features):
#         if 'company' in features:
#             comp_feats = features['company']
#             weights = torch.softmax(self.attention(comp_feats), dim=0)  # 学习节点权重
#             graph_feat = (comp_feats * weights).sum(dim=0)             # 加权求和
#         else:
#             all_feats = torch.cat(list(features.values()), dim=0)
#             weights = torch.softmax(self.attention(all_feats), dim=0)
#             graph_feat = (all_feats * weights).sum(dim=0)
#         x = F.relu(self.fc1(graph_feat))
#         x = self.fc2(x)
#         return x

class RiskEvaluationModel(nn.Module):
    def __init__(self, in_feats, hidden_feats, num_layers, pool_hidden, num_classes, rel_names, risk_injection_alpha=0.5):
        super(RiskEvaluationModel, self).__init__()
        self.layers = nn.ModuleList()
        self.layers.append(HeteroRGCNLayer(in_feats, hidden_feats, rel_names, risk_injection_alpha))
        for i in range(1, num_layers):
            self.layers.append(HeteroRGCNLayer(hidden_feats, hidden_feats, rel_names, risk_injection_alpha))
        self.risk_predictor = GlobalRiskPredictor(hidden_feats, pool_hidden, num_classes)
        self.node_predictor = nn.Linear(hidden_feats, num_classes)

    def forward(self, g, inputs):
        h = inputs
        for layer in self.layers:
            h = layer(g, h)
        node_preds = {}
        if 'company' in h:
            node_preds['company'] = self.node_predictor(h['company'])
        graph_pred = self.risk_predictor(g, h)
        return h, node_preds, graph_pred
