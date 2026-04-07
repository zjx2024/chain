import numpy as np
import torch
from sklearn.metrics import f1_score,auc,roc_curve
from utils import excel_to_dgl_graph
from model import HAN
import matplotlib.pyplot as plt
import os
import datetime

def determine_graph_path(industry_chain_id):
    """
    根据产业链ID返回对应的图数据文件路径
    
    Args:
        industry_chain_id (int): 产业链ID (1: 集成电路, 2: 电子信息)
        
    Returns:
        str: 图数据文件路径
    """
    if industry_chain_id == 1:
        # 集成电路产业链
        print(f"产业链ID=1，使用集成电路图文件: graph/Inte_Graph.pt")
        return "graph/Inte_Graph.pt"
    elif industry_chain_id == 2:
        # 电子信息产业链
        print(f"产业链ID=2，使用电子信息图文件: graph/Electric.pt")
        return "graph/Electric.pt"
    else:
        # 默认使用电子信息产业链图数据
        print(f"未知产业链ID={industry_chain_id}，默认使用电子信息产业链图数据")
        return "graph/Electric.pt"

#评估函数
def score(logits, labels):

    _, indices = torch.max(logits, dim=1)
    prediction = indices.long().cpu().numpy()
    labels = labels.cpu().numpy()

    accuracy = (prediction == labels).sum() / len(prediction)
    micro_f1 = f1_score(labels, prediction, average='binary')
    macro_f1 = f1_score(labels, prediction, average="macro")
    fpr, tpr, thresholds = roc_curve(labels, prediction)
    auc_score = auc(fpr, tpr)
    return accuracy, micro_f1, macro_f1,auc_score,fpr

def text_create(msg1,msg2,msg3,save_dir="."):
    path1 = os.path.join(save_dir, "acc.txt")
    path2 = os.path.join(save_dir, "f12.txt")
    path3 = os.path.join(save_dir, "auc.txt")
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
def evaluate(model,g, features, labels, mask, loss_func):
    model.eval()
    with torch.no_grad():
        logits = model(g, features)
    loss = loss_func(logits[mask], labels[mask])
    accuracy, micro_f1, macro_f1,auc_score,fpr = score(logits[mask], labels[mask])

    return loss, accuracy, micro_f1, macro_f1,auc_score,fpr


def main(args):
    feat_file = args.get("feat_file", "../datasets/Electric/Electric_2022Q2.xlsx")
    feat_sheet = "Sheet1"
    
    # 根据产业链ID选择对应的图数据文件
    industry_chain_id = args.get("industry_chain_id", 2)
    graph_path = determine_graph_path(industry_chain_id)
    
    # 获取模型保存目录（已在main函数外部创建）
    model_save_dir = args["model_save_dir"]
    dataset_name = os.path.basename(feat_file).replace('.xlsx', '')
    
    # 打印配置信息
    print("=" * 50)
    print("HAN Model 训练配置:")
    print(f"特征文件路径: {feat_file}")
    print(f"图数据路径: {graph_path}")
    print(f"训练轮次: {args['num_epochs']}")
    print(f"学习率: {args['lr']}")
    print(f"隐藏层维度: {args['hidden_units']}")
    print(f"注意力头数: {args['num_heads']}")
    print(f"Dropout率: {args['dropout']}")
    print(f"权重衰减: {args['weight_decay']}")
    print(f"随机种子: {args['seed']}")
    print(f"设备: {args['device']}")
    print(f"模型保存目录: {model_save_dir}")
    print("=" * 50)


    (
        g,
        features,
        labels,
        num_classes,
        train_idx,
        val_idx,
        test_idx,
        train_mask,
        val_mask,
        test_mask,
    ) = excel_to_dgl_graph(feat_file,feat_sheet,graph_path)
    #bool类型转换
    if hasattr(torch, "BoolTensor"):
        train_mask = train_mask.bool() #将train_mask的0-1类型转化为bool类型。
        val_mask = val_mask.bool()
        test_mask = test_mask.bool()



    features = features.to(args["device"])
    labels = labels.to(args["device"])
    train_mask = train_mask.to(args["device"])
    val_mask = val_mask.to(args["device"])
    test_mask = test_mask.to(args["device"])

    model = HAN(
        meta_paths=[["cp","pc"],["cp","pp","pc"]],#定义的边，组合成元路径PAP
        in_size=features.shape[1],
        hidden_size=args["hidden_units"],
        out_size=num_classes,
        num_heads=args["num_heads"],
        dropout=args["dropout"],
    ).to(args["device"])
    g = g.to(args["device"])

    #
    loss_fcn = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(
        model.parameters(), lr=args["lr"], weight_decay=args["weight_decay"]
    )
    acc_record = []
    auc_record = []
    f1_record = []

    test_acc_record,test_f1_record,test_auc_record=[],[],[]
    Best_f1,Best_acc,Best_auc,Best_loss=0,0,0,0
    for epoch in range(args["num_epochs"]):
        model.train()
        logits = model(g, features)
        loss = loss_fcn(logits[train_mask], labels[train_mask])

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        train_acc, train_micro_f1, train_macro_f1,train_auc_score,train_fpr = score(
            logits[train_mask], labels[train_mask]
        )
        acc_record.append(train_acc)
        auc_record.append(train_auc_score)
        f1_record.append(train_macro_f1)
        val_loss, val_acc, val_micro_f1, val_macro_f1,val_auc_score,val_fpr = evaluate(
            model, g, features, labels, val_mask, loss_fcn
        )

        print(
            "Epoch {:d} |Train Acc {:.4f}| Train Loss {:.4f} | Train f1 {:.4f} | Train auc {:.4f} | "
            "Val Loss {:.4f} | Val acc {:.4f} |Val f1 {:.4f}|val auc {:.4f} |".format(
                epoch + 1,
                train_acc,
                loss.item(),
                train_micro_f1,
                train_auc_score,
                val_loss.item(),
                val_acc,
                val_micro_f1,
                val_auc_score
            )
        )


        test_loss, test_acc, test_micro_f1, test_macro_f1,test_auc,test_fpr = evaluate(
            model, g, features, labels, test_mask, loss_fcn
        )
        test_acc_record.append(test_acc)
        test_f1_record.append(test_micro_f1)
        test_auc_record.append(test_auc)
        if Best_f1 < test_macro_f1:
            Best_f1 = test_macro_f1
            torch.save(model.state_dict(), os.path.join(model_save_dir, 'Best_f1_model.pth'))
        if Best_acc < test_acc:
            Best_acc = test_acc
            torch.save(model.state_dict(), os.path.join(model_save_dir, 'Best_acc_model.pth'))
        if Best_auc < test_auc:
            Best_auc = test_auc
            torch.save(model.state_dict(), os.path.join(model_save_dir, 'Best_auc_model.pth'))
    model.eval()
    model.load_state_dict(torch.load(os.path.join(model_save_dir, 'Best_f1_model.pth')))
    test_loss, test_acc, test_micro_f1, test_macro_f1, test_auc,test_fpr = evaluate(
        model, g, features, labels, test_mask, loss_fcn
    )

    print(
        "b f1 b Test f1 {:.4f} |b Test acc {:.4f}|b Test auc {:.4f} |".format(
            test_micro_f1, test_acc, test_auc
        )
    )
    model.eval()
    model.load_state_dict(torch.load(os.path.join(model_save_dir, 'Best_acc_model.pth')))
    test_loss, test_acc, test_micro_f1, test_macro_f1, test_auc,test_fpr = evaluate(
        model, g, features, labels, test_mask, loss_fcn
    )
    print(
        "b acc b Test f1 {:.4f} |b Test acc {:.4f}|b Test auc {:.4f} |".format(
            test_micro_f1, test_acc, test_auc
        )
    )
    model.eval()
    model.load_state_dict(torch.load(os.path.join(model_save_dir, 'Best_auc_model.pth')))
    test_loss, test_acc, test_micro_f1, test_macro_f1, test_auc,test_fpr = evaluate(
        model, g, features, labels, test_mask, loss_fcn
    )
    print(
        "b auc b Test f1 {:.4f} |b Test acc {:.4f}|b Test auc {:.4f} |".format(
            test_micro_f1, test_acc, test_auc
        )
    )
    
    # 保存模型信息文件
    model_info = {
        "model_name": "HAN_Model",
        "dataset_file": feat_file,
        "dataset_name": dataset_name,
        "graph_file": graph_path,
        "training_params": {
            "epochs": args['num_epochs'],
            "learning_rate": args['lr'],
            "hidden_units": args['hidden_units'],
            "num_heads": args['num_heads'],
            "dropout": args['dropout'],
            "weight_decay": args['weight_decay'],
            "seed": args['seed']
        },
        "best_results": {
            "best_f1": Best_f1,
            "best_acc": Best_acc,
            "best_auc": Best_auc
        },
        "training_time": os.path.basename(model_save_dir).split('_')[-1],
        "device": args['device']
    }
    
    model_info_path = os.path.join(model_save_dir, 'model_info.txt')
    with open(model_info_path, 'w', encoding='utf-8') as f:
        f.write("HAN Model 训练信息\n")
        f.write("=" * 50 + "\n")
        f.write(f"模型名称: {model_info['model_name']}\n")
        f.write(f"数据集文件: {model_info['dataset_file']}\n")
        f.write(f"数据集名称: {model_info['dataset_name']}\n")
        f.write(f"图数据文件: {model_info['graph_file']}\n")
        f.write(f"训练时间: {model_info['training_time']}\n")
        f.write(f"设备: {model_info['device']}\n")
        f.write("\n训练参数:\n")
        f.write("-" * 30 + "\n")
        for key, value in model_info['training_params'].items():
            f.write(f"{key}: {value}\n")
        f.write("\n最佳结果:\n")
        f.write("-" * 30 + "\n")
        f.write(f"最佳F1分数: {model_info['best_results']['best_f1']:.4f}\n")
        f.write(f"最佳准确率: {model_info['best_results']['best_acc']:.4f}\n")
        f.write(f"最佳AUC: {model_info['best_results']['best_auc']:.4f}\n")
        f.write("\n保存的模型文件:\n")
        f.write("-" * 30 + "\n")
        f.write("- Best_f1_model.pth (最佳F1分数模型)\n")
        f.write("- Best_acc_model.pth (最佳准确率模型)\n")
        f.write("- Best_auc_model.pth (最佳AUC模型)\n")
    
    print(f"模型信息已保存至: {model_info_path}")
    print(f"模型文件已保存至: {model_save_dir}")
    
    # 保存训练过程数据
    text_create(acc_record, f1_record, auc_record, model_save_dir)
    print(f"训练过程数据已保存至: {model_save_dir}")
    
    ############################################
    # 绘制并保存训练过程曲线图（优化版本）
    ############################################
    
    # 创建保存图片的目录 - 保存到模型存储目录中
    plots_dir = os.path.join(model_save_dir, "training_plots")
    os.makedirs(plots_dir, exist_ok=True)
    
    # 生成时间戳用于文件命名
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # 生成epoch列表
    epochs = list(range(1, len(acc_record) + 1))
    
    # 数据采样：如果数据点太多，进行采样以提高可视化效果
    def sample_data(data, max_points=200):
        if len(data) <= max_points:
            return list(range(len(data))), data
        step = len(data) // max_points
        indices = list(range(0, len(data), step))
        if indices[-1] != len(data) - 1:
            indices.append(len(data) - 1)
        return [i + 1 for i in indices], [data[i] for i in indices]
    
    # 采样数据
    sampled_epochs, sampled_acc = sample_data(acc_record)
    _, sampled_f1 = sample_data(f1_record)
    _, sampled_auc = sample_data(auc_record)
    _, sampled_test_acc = sample_data(test_acc_record)
    _, sampled_test_f1 = sample_data(test_f1_record)
    _, sampled_test_auc = sample_data(test_auc_record)
    
    # 设置更好的颜色方案和样式
    plt.style.use('default')
    colors = {
        'train_acc': '#2E86AB',      # 深蓝色
        'train_f1': '#A23B72',       # 深紫色  
        'train_auc': '#F18F01',      # 橙色
        'test_acc': '#C73E1D',       # 深红色
        'test_f1': '#592E83',        # 深紫色
        'test_auc': '#A4243B'        # 深红色
    }
    
    # 绘制训练过程曲线（训练集指标）
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    # 训练准确率
    axes[0].plot(sampled_epochs, sampled_acc, label='Train Accuracy', 
                linewidth=2.5, color=colors['train_acc'], marker='o', markersize=4, alpha=0.8)
    axes[0].set_xlabel("Epoch", fontsize=12, fontweight='bold')
    axes[0].set_ylabel("Accuracy", fontsize=12, fontweight='bold')
    axes[0].set_title("Training Accuracy", fontsize=14, fontweight='bold')
    axes[0].legend(fontsize=11)
    axes[0].grid(True, alpha=0.3, linestyle='--')
    axes[0].set_ylim([0, 1])
    
    # 训练F1分数
    axes[1].plot(sampled_epochs, sampled_f1, label='Train F1 Score', 
                linewidth=2.5, color=colors['train_f1'], marker='s', markersize=4, alpha=0.8)
    axes[1].set_xlabel("Epoch", fontsize=12, fontweight='bold')
    axes[1].set_ylabel("F1 Score", fontsize=12, fontweight='bold')
    axes[1].set_title("Training F1 Score", fontsize=14, fontweight='bold')
    axes[1].legend(fontsize=11)
    axes[1].grid(True, alpha=0.3, linestyle='--')
    axes[1].set_ylim([0, 1])
    
    # 训练AUC
    axes[2].plot(sampled_epochs, sampled_auc, label='Train AUC', 
                linewidth=2.5, color=colors['train_auc'], marker='^', markersize=4, alpha=0.8)
    axes[2].set_xlabel("Epoch", fontsize=12, fontweight='bold')
    axes[2].set_ylabel("AUC", fontsize=12, fontweight='bold')
    axes[2].set_title("Training AUC", fontsize=14, fontweight='bold')
    axes[2].legend(fontsize=11)
    axes[2].grid(True, alpha=0.3, linestyle='--')
    axes[2].set_ylim([0, 1])
    
    plt.tight_layout()
    
    # 保存训练过程曲线图
    train_plot_path = os.path.join(plots_dir, f"training_curves_improved_{timestamp}.png")
    plt.savefig(train_plot_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"优化版训练过程曲线图已保存至: {train_plot_path}")
    plt.close()

    # 绘制测试集指标变化曲线
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    # 测试准确率
    axes[0].plot(sampled_epochs, sampled_test_acc, label='Test Accuracy', 
                linewidth=2.5, color=colors['test_acc'], marker='o', markersize=4, alpha=0.8)
    axes[0].set_xlabel("Epoch", fontsize=12, fontweight='bold')
    axes[0].set_ylabel("Accuracy", fontsize=12, fontweight='bold')
    axes[0].set_title("Test Accuracy", fontsize=14, fontweight='bold')
    axes[0].legend(fontsize=11)
    axes[0].grid(True, alpha=0.3, linestyle='--')
    axes[0].set_ylim([0, 1])
    
    # 测试F1分数
    axes[1].plot(sampled_epochs, sampled_test_f1, label='Test F1 Score', 
                linewidth=2.5, color=colors['test_f1'], marker='s', markersize=4, alpha=0.8)
    axes[1].set_xlabel("Epoch", fontsize=12, fontweight='bold')
    axes[1].set_ylabel("F1 Score", fontsize=12, fontweight='bold')
    axes[1].set_title("Test F1 Score", fontsize=14, fontweight='bold')
    axes[1].legend(fontsize=11)
    axes[1].grid(True, alpha=0.3, linestyle='--')
    axes[1].set_ylim([0, 1])
    
    # 测试AUC
    axes[2].plot(sampled_epochs, sampled_test_auc, label='Test AUC', 
                linewidth=2.5, color=colors['test_auc'], marker='^', markersize=4, alpha=0.8)
    axes[2].set_xlabel("Epoch", fontsize=12, fontweight='bold')
    axes[2].set_ylabel("AUC", fontsize=12, fontweight='bold')
    axes[2].set_title("Test AUC", fontsize=14, fontweight='bold')
    axes[2].legend(fontsize=11)
    axes[2].grid(True, alpha=0.3, linestyle='--')
    axes[2].set_ylim([0, 1])
    
    plt.tight_layout()
    
    # 保存测试集指标曲线图
    test_plot_path = os.path.join(plots_dir, f"test_curves_improved_{timestamp}.png")
    plt.savefig(test_plot_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"优化版测试集指标曲线图已保存至: {test_plot_path}")
    plt.close()

    # 绘制训练集vs测试集性能对比图（改进版）
    fig, axes = plt.subplots(1, 3, figsize=(20, 6))
    
    # 准确率对比
    axes[0].plot(sampled_epochs, sampled_acc, label='Train Accuracy', 
                linewidth=3, color=colors['train_acc'], marker='o', markersize=5, alpha=0.9)
    axes[0].plot(sampled_epochs, sampled_test_acc, label='Test Accuracy', 
                linewidth=3, color=colors['test_acc'], marker='s', markersize=5, alpha=0.9)
    axes[0].set_xlabel("Epoch", fontsize=12, fontweight='bold')
    axes[0].set_ylabel("Accuracy", fontsize=12, fontweight='bold')
    axes[0].set_title("Accuracy Comparison", fontsize=14, fontweight='bold')
    axes[0].legend(fontsize=11)
    axes[0].grid(True, alpha=0.3, linestyle='--')
    axes[0].set_ylim([0, 1])

    # F1分数对比
    axes[1].plot(sampled_epochs, sampled_f1, label='Train F1 Score', 
                linewidth=3, color=colors['train_f1'], marker='o', markersize=5, alpha=0.9)
    axes[1].plot(sampled_epochs, sampled_test_f1, label='Test F1 Score', 
                linewidth=3, color=colors['test_f1'], marker='s', markersize=5, alpha=0.9)
    axes[1].set_xlabel("Epoch", fontsize=12, fontweight='bold')
    axes[1].set_ylabel("F1 Score", fontsize=12, fontweight='bold')
    axes[1].set_title("F1 Score Comparison", fontsize=14, fontweight='bold')
    axes[1].legend(fontsize=11)
    axes[1].grid(True, alpha=0.3, linestyle='--')
    axes[1].set_ylim([0, 1])

    # AUC对比
    axes[2].plot(sampled_epochs, sampled_auc, label='Train AUC', 
                linewidth=3, color=colors['train_auc'], marker='o', markersize=5, alpha=0.9)
    axes[2].plot(sampled_epochs, sampled_test_auc, label='Test AUC', 
                linewidth=3, color=colors['test_auc'], marker='s', markersize=5, alpha=0.9)
    axes[2].set_xlabel("Epoch", fontsize=12, fontweight='bold')
    axes[2].set_ylabel("AUC", fontsize=12, fontweight='bold')
    axes[2].set_title("AUC Comparison", fontsize=14, fontweight='bold')
    axes[2].legend(fontsize=11)
    axes[2].grid(True, alpha=0.3, linestyle='--')
    axes[2].set_ylim([0, 1])
    
    plt.tight_layout()
    
    # 保存对比图
    comparison_plot_path = os.path.join(plots_dir, f"train_vs_test_comparison_improved_{timestamp}.png")
    plt.savefig(comparison_plot_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"优化版训练集vs测试集对比图已保存至: {comparison_plot_path}")
    plt.close()
    
    print("所有训练过程图片已成功保存！")
    
    #  ###########################################################################
    # # 聚类评估与可视化部分（在训练与测试结束后添加）
    # ###########################################################################
    # model.eval()
    # model.load_state_dict(torch.load('modeldata/Best_auc_model.pth'))
    # with torch.no_grad():
    #     # 此处示例中使用模型的输出 logits 作为节点表示
    #     # 如果模型中有更好的中间层表示，建议改为提取那个表示
    #     embeddings,_ = model(g, features, return_features=True)
    # # 将 embeddings 转为 numpy 数组并标准化
    # features_np = embeddings.cpu().numpy()
    # from sklearn.preprocessing import StandardScaler
    # from sklearn.manifold import TSNE
    # from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score
    #
    # # 标准化
    # scaler = StandardScaler()
    # features_scaled = scaler.fit_transform(features_np)
    #
    # # 如果 features_np 本身不是 2 维，我们可以使用 TSNE 将其降为 2 维（此处可选）
    # # 例如，如果 features_np 的形状为 (N, D) 且 D > 2:
    # if features_scaled.shape[1] > 2:
    #     tsne = TSNE(n_components=2, random_state=42)
    #     features_2d = tsne.fit_transform(features_scaled)
    # else:
    #     features_2d = features_scaled
    #
    # # ========================
    # # 1. 使用谱聚类（Spectral Clustering）
    # # ========================
    # from sklearn.cluster import SpectralClustering
    #
    # # 注意：聚类数一般设为类别数或根据需要调整
    # num_clusters = num_classes  # 或者指定为其他值
    # spectral = SpectralClustering(n_clusters=num_clusters, affinity='nearest_neighbors', random_state=42)
    # cluster_labels_spectral = spectral.fit_predict(features_scaled)
    # # ========================
    # # 2. 使用 DBSCAN
    # # ========================
    # from sklearn.cluster import DBSCAN
    #
    # # eps 和 min_samples 需要根据数据分布调参
    # dbscan = DBSCAN(eps=0.5, min_samples=5)
    # cluster_labels_dbscan = dbscan.fit_predict(features_scaled)
    #
    # # ========================
    # # 3. 使用高斯混合模型（GMM）
    # # ========================
    # from sklearn.mixture import GaussianMixture
    #
    # gmm = GaussianMixture(n_components=num_clusters, random_state=42)
    # cluster_labels_gmm = gmm.fit_predict(features_scaled)
    #
    # # ========================
    # # 4. 计算聚类评价指标：ARI 和 NMI
    # # ========================
    # true_labels_np = labels.cpu().numpy()  # 假设 labels 是原始标签
    #
    # ari_spectral = adjusted_rand_score(true_labels_np, cluster_labels_spectral)
    # nmi_spectral = normalized_mutual_info_score(true_labels_np, cluster_labels_spectral)
    #
    # ari_dbscan = adjusted_rand_score(true_labels_np, cluster_labels_dbscan)
    # nmi_dbscan = normalized_mutual_info_score(true_labels_np, cluster_labels_dbscan)
    #
    # ari_gmm = adjusted_rand_score(true_labels_np, cluster_labels_gmm)
    # nmi_gmm = normalized_mutual_info_score(true_labels_np, cluster_labels_gmm)
    #
    # print("Spectral Clustering: ARI = {:.4f}, NMI = {:.4f}".format(ari_spectral, nmi_spectral))
    # print("DBSCAN: ARI = {:.4f}, NMI = {:.4f}".format(ari_dbscan, nmi_dbscan))
    # print("GMM: ARI = {:.4f}, NMI = {:.4f}".format(ari_gmm, nmi_gmm))

if __name__ == "__main__":
    import argparse

    from utils import setup

    parser = argparse.ArgumentParser("HAN")
    parser.add_argument("-s", "--seed", type=int, default=1, help="Random seed")
    parser.add_argument(
        "-ld",
        "--log-dir",
        type=str,
        default="results",
        help="Dir for saving training results",
    )
    parser.add_argument(
        "--hetero",
        action="store_true",
        help="Use metapath coalescing with DGL's own dataset",
    )
    parser.add_argument(
        "--feat-file",
        type=str,
        default="../datasets/Electric/Electric_2022Q2.xlsx",
        help="Path to the feature file (Excel format)",
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=800,
        help="Number of training epochs",
    )
    parser.add_argument(
        "--lr",
        type=float,
        default=0.001,
        help="Learning rate",
    )
    parser.add_argument(
        "--industry-chain-id",
        type=int,
        default=2,
        help="Industry chain ID (1: 集成电路, 2: 电子信息)",
    )
    args = parser.parse_args().__dict__
    
    # 创建模型保存目录 - 确保保存到正确的models-storage路径
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    feat_file = args.get("feat_file", "../datasets/Electric/Electric_2022Q2.xlsx")
    dataset_name = os.path.basename(feat_file).replace('.xlsx', '')
    epochs = args.get("epochs", 800)
    lr = args.get("lr", 0.001)
    
    # 获取当前脚本的绝对路径，然后构建models-storage的绝对路径
    current_dir = os.path.dirname(os.path.abspath(__file__))  # HAN_Model目录
    models_dir = os.path.dirname(current_dir)  # models目录
    project_root = os.path.dirname(models_dir)  # chain项目根目录
    models_storage_dir = os.path.join(project_root, "models-storage")  # models-storage目录
    
    model_save_dir = os.path.join(models_storage_dir, f"HAN_Model_{dataset_name}_epochs{epochs}_lr{lr}_{timestamp}")
    os.makedirs(model_save_dir, exist_ok=True)
    
    print(f"模型将保存到: {model_save_dir}")
    
    # 将模型保存目录添加到args中，供setup函数使用
    args["model_save_dir"] = model_save_dir
    
    args = setup(args)
    main(args)
