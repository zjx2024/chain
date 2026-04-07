import torch
from sklearn.model_selection import train_test_split
import numpy as np

class EarlyStopping:
    def __init__(self, patience=5, delta=0.01):
        """
        早停机制
        :param patience: 在多少个epoch内，若没有提升，则停止训练
        :param delta: 阈值，表示如果验证集的指标相对上一轮的提升小于该值，则认为没有改进
        """
        self.patience = patience
        self.delta = delta
        self.best_score = None
        self.best_model_state = None
        self.counter = 0
        self.early_stop = False

    def step(self, score, model_state):
        """
        根据当前指标进行判断是否继续训练
        :param score: 当前的验证指标（如 AUC）
        :param model_state: 当前模型的状态
        """
        if self.best_score is None:
            self.best_score = score
            self.best_model_state = model_state
        elif score > self.best_score + self.delta:
            self.best_score = score
            self.best_model_state = model_state
            self.counter = 0
        else:
            self.counter += 1
            if self.counter >= self.patience:
                self.early_stop = True

    def get_best_model(self):
        """
        获取最好的模型状态
        """
        return self.best_model_state


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

def print_distribution(name, mask, labels):
    label_counts = torch.unique(labels[mask], return_counts=True)
    print(f"{name} 分布: 0类={label_counts[1][0].item()}, 1类={label_counts[1][1].item()}")



def get_binary_mask(total_size, indices):
    mask = torch.zeros(total_size, dtype=torch.bool)
    mask[indices] = True
    return mask