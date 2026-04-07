import random
import argparse

import torch
import torch.nn as nn
import torch.nn.functional as F
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split
import numpy as np
import datetime
import os
from PreTrain import metapath2vec_pretraining_node
from utils import EarlyStopping
from model_pure import CompanyFeatureFusion, RiskEvaluationModel
from data_read import excel_to_dgl_graph_direct, excel_to_dgl_graph_separate



############################################
# 6. 主流程：整合预训练、特征融合、模型训练、评估及聚类可视化
############################################
def save_model(model, best_model_state, model_name, feat_file, epochs, lr, save_dir="../../models-storage/"):
    if best_model_state is not None:
        # 生成时间戳
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 从特征文件路径提取文件名（不含扩展名）
        feat_filename = os.path.splitext(os.path.basename(feat_file))[0]
        
        # 生成模型目录名
        model_dir_name = f"{model_name}_{feat_filename}_epochs{epochs}_lr{lr}_{timestamp}"
        model_dir_path = os.path.join(save_dir, model_dir_name)
        
        # 确保保存目录存在
        os.makedirs(model_dir_path, exist_ok=True)

        # 保存最佳模型
        best_model_path = os.path.join(model_dir_path, "best_model_latest.pth")
        torch.save(best_model_state, best_model_path)
        
        # 保存最终模型
        final_model_path = os.path.join(model_dir_path, "final_model.pth")
        torch.save(model.state_dict(), final_model_path)

        # 保存模型信息
        model_info = {
            "model_name": model_name,
            "dataset_file": feat_file,
            "epochs": epochs,
            "learning_rate": lr,
            "timestamp": timestamp,
            "model_dir": model_dir_path
        }
        
        info_path = os.path.join(model_dir_path, "model_info.txt")
        with open(info_path, 'w', encoding='utf-8') as f:
            for key, value in model_info.items():
                f.write(f"{key}: {value}\n")
        
        print(f"模型已保存至: {model_dir_path}", flush=True)
        print(f"最佳模型: {best_model_path}", flush=True)
        print(f"最终模型: {final_model_path}", flush=True)

        # 重新加载最优模型状态
        model.load_state_dict(best_model_state)
        
        return model_dir_path
    else:
        print("未检测到最佳模型状态，未进行保存。", flush=True)
        return None

def text_create(msg1,msg2,msg3,msg4):
    path1 = r"acc_4.txt"
    path2 = r"f1_4.txt"
    path3 = r"auc_4.txt"
    path4 =r"epoch_4.txt"

    file = open(path1,'w')
    for line in msg1:
        file.write(str(line)+'\n')
    file.close()

    file = open(path2,'w')
    for line in msg2:
        file.write(str(line)+'\n')
    file.close()

    file = open(path3,'w')
    for line in msg3:
        file.write(str(line)+'\n')
    file.close()

    file = open(path4,'w')
    for line in msg4:
        file.write(str(line)+'\n')
    file.close()



def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='HierTransferGNN Model Training')
    parser.add_argument('--feat-file', type=str, required=True,
                       help='特征数据文件路径')
    parser.add_argument('--industry-chain-id', type=int, required=True,
                       help='产业链ID: 1-集成电路, 2-电子信息')
    parser.add_argument('--epochs', type=int, default=400, 
                       help='训练轮次 (默认: 400)')
    parser.add_argument('--lr', type=float, default=0.001, 
                       help='学习率 (默认: 0.001)')
    
    args = parser.parse_args()
    
    SEED = 999
    random.seed(SEED)
    np.random.seed(SEED)
    torch.manual_seed(SEED)

    # 根据产业链ID选择对应的图结构文件
    if args.industry_chain_id == 1:
        graph_file = "graph/Inte_graph.xlsx"
        industry_type = "集成电路"
        print(f"产业链ID=1，使用集成电路图文件: {graph_file}", flush=True)
    elif args.industry_chain_id == 2:
        graph_file = "graph/Electric_graph.xlsx"
        industry_type = "电子信息"
        print(f"产业链ID=2，使用电子信息图文件: {graph_file}", flush=True)
    else:
        # 默认使用集成电路
        graph_file = "graph/Inte_graph.xlsx"
        industry_type = "集成电路"
        print(f"未知产业链ID={args.industry_chain_id}，默认使用集成电路图文件: {graph_file}", flush=True)
    
    # 图结构文件的sheet名称
    pp_sheet = "P-P"
    pc_sheet = "P-C"
    
    print(f"特征数据文件: {args.feat_file}", flush=True)
    print(f"图结构文件: {graph_file}", flush=True)
    print(f"训练参数: 轮次={args.epochs}, 学习率={args.lr}", flush=True)
    start_time = datetime.datetime.now()

    g, product_id, comp_fin_feats, comp_labels = excel_to_dgl_graph_separate(
        graph_file=graph_file,
        pp_matrix_sheet=pp_sheet,
        pc_matrix_sheet=pc_sheet,
        feature_file=args.feat_file
    )

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    g = g.to(device)
    comp_fin_feats = comp_fin_feats.to(device)
    comp_labels = comp_labels.to(device)

    early_stopping = EarlyStopping(patience=10, delta=0.005)
    # -----------------------------
    # 数据划分：训练集、验证集、测试集（以公司节点为例）
    # -----------------------------
    all_indices = np.arange(g.num_nodes('company'))
    train_idx_np, temp_idx_np = train_test_split(all_indices, test_size=0.4, random_state=42)
    val_idx_np, test_idx_np = train_test_split(temp_idx_np, test_size=0.5, random_state=42)
    train_idx = torch.tensor(train_idx_np, dtype=torch.long, device=device)
    val_idx = torch.tensor(val_idx_np, dtype=torch.long, device=device)
    test_idx = torch.tensor(test_idx_np, dtype=torch.long, device=device)
    print("Train hash:", hash(tuple(train_idx_np)), flush=True)
    print("Val hash:  ", hash(tuple(val_idx_np)), flush=True)
    print("Test hash: ", hash(tuple(test_idx_np)), flush=True)

    # -----------------------------
    # 预训练部分
    # -----------------------------
    product_meta_path1 = [('product', 'pc', 'company'), ('company', 'cp', 'product')]
    product_meta_path2 = [('product', 'pp', 'product'), ('product', 'pc', 'company'), ('company', 'cp', 'product')]
    product_meta_path3 = [('product', 'pc', 'company'), ('company', 'cp', 'product'), ('product', 'pp', 'product')]
    product_meta_paths = [product_meta_path1, product_meta_path2, product_meta_path3]

    company_meta_path1 = [('company', 'cp', 'product'), ('product', 'pc', 'company')]
    company_meta_path2 = [('company', 'cp', 'product'), ('product', 'pp', 'product'), ('product', 'pc', 'company')]
    company_meta_paths = [company_meta_path1, company_meta_path2]

    prod_meta_emb = metapath2vec_pretraining_node(g, 'product', product_meta_paths, num_traces=10, trace_length=2, d=18).to(device)
    print("Pretrained product metapath embeddings shape:", prod_meta_emb.shape, flush=True)  # (num_products, 18)

    comp_meta_emb = metapath2vec_pretraining_node(g, 'company', company_meta_paths, num_traces=10, trace_length=2, d=18).to(device)
    print("Pretrained company metapath embeddings shape:", comp_meta_emb.shape, flush=True)  # (num_companies, 18)
    
    # -----------------------------
    # 特征融合
    # -----------------------------
    prod_final_emb = prod_meta_emb.to(device)
    print("Final product embeddings shape:", prod_final_emb.shape, flush=True)

    comp_fusion_module = CompanyFeatureFusion(fin_dim=18, meta_dim=18, out_dim=18).to(device)
    comp_final_emb = comp_fusion_module(comp_fin_feats, comp_meta_emb)
    print("Final company embeddings shape:", comp_final_emb.shape, flush=True)

    inputs = {
        'product': prod_final_emb,
        'company': comp_final_emb
    }

    # 定义边类型列表
    rel_names = g.etypes  # 如 ['pp', 'pc', 'cp']

    # 定义整体风险评估模型
    model = RiskEvaluationModel(in_feats=18, hidden_feats=128, num_layers=4, pool_hidden=64,
                                num_classes=2, rel_names=rel_names, risk_injection_alpha=0.5).to(device)

    # -----------------------------
    # 定义优化器与自适应学习率调度器
    # -----------------------------
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)

    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=10, verbose=True)
    criterion_node = nn.CrossEntropyLoss()
    criterion_graph = nn.MSELoss()
    num_epochs = args.epochs
    lambda_graph = 0.3

    # 用于记录训练过程中的指标变化（记录训练损失和验证指标）
    train_losses = []
    eval_accuracies = []
    eval_f1s = []
    eval_aucs = []
    eval_epochs = []
    best_val_auc = 0.0
    best_model_state = None

    model.train()
    for epoch in range(num_epochs):
        optimizer.zero_grad()
        prod_fused = prod_meta_emb
        comp_fused = comp_fusion_module(comp_fin_feats, comp_meta_emb)
        inputs = {'product': prod_fused, 'company': comp_fused}
        _, node_preds, graph_pred = model(g, inputs)

        # 只使用训练集节点计算交叉熵损失
        loss_node = criterion_node(node_preds['company'][train_idx], comp_labels[train_idx])
        avg_comp_pred = node_preds['company'][train_idx].mean(dim=0)
        loss_graph = criterion_graph(graph_pred, avg_comp_pred)
        loss = loss_node + lambda_graph * loss_graph
        loss.backward()
        optimizer.step()

        train_losses.append(loss.item())
        
        # 每个epoch都输出基本进度信息
        print(f"Epoch {epoch+1}/{num_epochs}: Train Loss: {loss.item():.4f}", flush=True)

        # 每隔 10 个 epoch 在验证集上评估
        if (epoch + 1) % 10 == 0:
            model.eval()  # 切换到评估模式
            with torch.no_grad():
                h, node_preds, graph_pred = model(g, inputs)
                comp_pred_logits = node_preds['company']
                comp_pred_val = torch.argmax(comp_pred_logits[val_idx], dim=1).cpu().numpy()
                true_labels_val = comp_labels[val_idx].cpu().numpy()

                acc = accuracy_score(true_labels_val, comp_pred_val)
                f1 = f1_score(true_labels_val, comp_pred_val, average='binary')
                prob = F.softmax(comp_pred_logits[val_idx], dim=1)[:, 1].cpu().numpy()
                auc = roc_auc_score(true_labels_val, prob)

            eval_accuracies.append(acc)
            eval_f1s.append(f1)
            eval_aucs.append(auc)
            eval_epochs.append(epoch + 1)

            print(f"Epoch {epoch+1}/{num_epochs}: Train Loss: {loss.item():.4f}, Val Acc: {acc:.4f}, F1: {f1:.4f}, AUC: {auc:.4f}", flush=True)
            early_stopping.step(auc, model.state_dict())
            # 保存最优模型：使用 AUC 来判断最优模型
            if auc > best_val_auc:
                best_val_auc = auc
                best_model_state = model.state_dict()

            model.train()  # 恢复训练模式

        # 更新学习率调度器（根据当前训练损失）
        scheduler.step(loss.item())
        # 如果早停触发，则停止训练
        if early_stopping.early_stop:
            print(f"Early stopping triggered at epoch {epoch+1}", flush=True)
            break
    text_create(eval_accuracies,eval_f1s,eval_aucs,eval_epochs)
    # 在训练结束后，保存模型
    model_save_path = save_model(model, best_model_state, "HierTransferGNN_Model", args.feat_file, args.epochs, args.lr)
    if model_save_path is None:
        print("No model saved as best model during training.")

    ############################################
    # 最终评估：在测试集上进行评估
    ############################################

    model.eval()
    with torch.no_grad():
        h, node_preds, graph_pred = model(g, inputs)
        comp_pred_logits = node_preds['company']
        comp_pred_test = torch.argmax(comp_pred_logits[test_idx], dim=1).cpu().numpy()
        true_labels_test = comp_labels[test_idx].cpu().numpy()

    test_acc = accuracy_score(true_labels_test, comp_pred_test)
    test_f1 = f1_score(true_labels_test, comp_pred_test, average='binary')
    prob_test = F.softmax(comp_pred_logits[test_idx], dim=1)[:, 1].cpu().numpy()
    test_auc = roc_auc_score(true_labels_test, prob_test)
    print("\nFinal Evaluation on Test Company Nodes:", flush=True)
    print("Test Accuracy: {:.4f}".format(test_acc), flush=True)
    print("Test F1 Score: {:.4f}".format(test_f1), flush=True)
    print("Test AUC: {:.4f}".format(test_auc), flush=True)
    print("Graph-level risk prediction (proxy):", graph_pred.cpu().numpy(), flush=True)
    end_time = datetime.datetime.now()
    print(f"总耗时: {end_time - start_time}", flush=True)
    ############################################
    # 绘制训练过程中的 Loss 变化及评估指标变化曲线（验证集上的指标）
    ############################################

    # 创建保存图片的目录
    if model_save_path:
        plots_dir = os.path.join(model_save_path, "training_plots")
    else:
        plots_dir = "training_plots"
    os.makedirs(plots_dir, exist_ok=True)
    
    # 生成时间戳用于文件命名
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # 设置更好的颜色方案和样式
    plt.style.use('default')
    colors = {
        'val_acc': '#2E86AB',      # 深蓝色
        'val_f1': '#A23B72',       # 深紫色  
        'val_auc': '#F18F01',      # 橙色
        'train_loss': '#C73E1D'    # 深红色
    }

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    # 验证AUC
    axes[0].plot(eval_epochs, eval_aucs, label='Val AUC', 
                linewidth=2.5, color=colors['val_auc'], marker='o', markersize=5, alpha=0.8)
    axes[0].set_xlabel("Epoch", fontsize=12, fontweight='bold')
    axes[0].set_ylabel("AUC", fontsize=12, fontweight='bold')
    axes[0].set_title("Validation AUC", fontsize=14, fontweight='bold')
    axes[0].legend(fontsize=11)
    axes[0].grid(True, alpha=0.3, linestyle='--')
    axes[0].set_ylim([0, 1])

    # 验证准确率
    axes[1].plot(eval_epochs, eval_accuracies, label='Val Accuracy', 
                linewidth=2.5, color=colors['val_acc'], marker='s', markersize=5, alpha=0.8)
    axes[1].set_xlabel("Epoch", fontsize=12, fontweight='bold')
    axes[1].set_ylabel("Accuracy", fontsize=12, fontweight='bold')
    axes[1].set_title("Validation Accuracy", fontsize=14, fontweight='bold')
    axes[1].legend(fontsize=11)
    axes[1].grid(True, alpha=0.3, linestyle='--')
    axes[1].set_ylim([0, 1])

    # 验证F1分数
    axes[2].plot(eval_epochs, eval_f1s, label='Val F1 Score', 
                linewidth=2.5, color=colors['val_f1'], marker='^', markersize=5, alpha=0.8)
    axes[2].set_xlabel("Epoch", fontsize=12, fontweight='bold')
    axes[2].set_ylabel("F1 Score", fontsize=12, fontweight='bold')
    axes[2].set_title("Validation F1 Score", fontsize=14, fontweight='bold')
    axes[2].legend(fontsize=11)
    axes[2].grid(True, alpha=0.3, linestyle='--')
    axes[2].set_ylim([0, 1])
    
    plt.tight_layout()
    
    # 保存训练过程曲线图
    plot_save_path = os.path.join(plots_dir, f"training_curves_improved_{timestamp}.png")
    plt.savefig(plot_save_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"训练过程曲线图已保存至: {plot_save_path}", flush=True)
    
    plt.close()  # 关闭图形，释放内存

    ############################################
    # 额外绘制训练损失曲线（优化版）
    ############################################
    
    # 对训练损失进行采样以提高可视化效果
    def sample_loss_data(data, max_points=500):
        if len(data) <= max_points:
            return list(range(1, len(data) + 1)), data
        step = len(data) // max_points
        indices = list(range(0, len(data), step))
        if indices[-1] != len(data) - 1:
            indices.append(len(data) - 1)
        return [i + 1 for i in indices], [data[i] for i in indices]
    
    sampled_loss_epochs, sampled_losses = sample_loss_data(train_losses)
    
    plt.figure(figsize=(12, 6))
    plt.plot(sampled_loss_epochs, sampled_losses, label='Training Loss', 
             linewidth=2.5, color=colors['train_loss'], alpha=0.8)
    plt.xlabel("Epoch", fontsize=12, fontweight='bold')
    plt.ylabel("Loss", fontsize=12, fontweight='bold')
    plt.title("Training Loss Curve", fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3, linestyle='--')
    
    # 保存测试曲线图
    loss_plot_path = os.path.join(plots_dir, f"test_curves_improved_{timestamp}.png")
    plt.savefig(loss_plot_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"测试曲线图已保存至: {loss_plot_path}", flush=True)
    
    plt.close()  # 关闭图形，释放内存

    ############################################
    # 绘制综合性能对比图（优化版）
    ############################################
    
    plt.figure(figsize=(12, 8))
    plt.plot(eval_epochs, eval_accuracies, label='Accuracy', 
             marker='o', linewidth=3, markersize=6, color=colors['val_acc'], alpha=0.9)
    plt.plot(eval_epochs, eval_f1s, label='F1 Score', 
             marker='s', linewidth=3, markersize=6, color=colors['val_f1'], alpha=0.9)
    plt.plot(eval_epochs, eval_aucs, label='AUC', 
             marker='^', linewidth=3, markersize=6, color=colors['val_auc'], alpha=0.9)
    plt.xlabel("Epoch", fontsize=12, fontweight='bold')
    plt.ylabel("Score", fontsize=12, fontweight='bold')
    plt.title("Model Performance Comparison", fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.ylim(0, 1)
    
    # 保存训练测试对比图
    comparison_plot_path = os.path.join(plots_dir, f"train_vs_test_comparison_improved_{timestamp}.png")
    plt.savefig(comparison_plot_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"训练测试对比图已保存至: {comparison_plot_path}", flush=True)
    
    plt.close()  # 关闭图形，释放内存

if __name__ == '__main__':
    main()
