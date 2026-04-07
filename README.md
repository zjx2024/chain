# 产业链风险评估系统

## 项目简介

产业链风险评估系统由三个部分组成：

- **前端**：`industry-risk-assessment/`，使用 Vue 3 + Vite 构建交互式管理界面，覆盖数据上传、训练管理、风险可视化等功能。
- **后端**：`industry-risk-assessment-server/`，基于 Spring Boot 2.7 + MyBatis-Plus + MySQL，暴露 REST API、管理业务逻辑，并调度 Python 模型训练。
- **算法与数据**：`datasets/`、`models/`、`models-storage/` 分别存放原始数据、Python 训练脚本和训练得到的模型文件，后端直接从这些目录中读取或写入。

## 目录结构

```
.
├── README.md
├── API接口文档.txt               # 后端 API 规格
├── datasets/                     # 原始/加工后的数据集，供训练与推理使用
├── models/                       # Python 图神经网络脚本（HAN、HierTransferGNN、GPFedRec…）
├── models-storage/               # 模型权重与版本快照
├── industry-risk-assessment/     # 前端（Vue 3 + Vite）
└── industry-risk-assessment-server/  # 后端（Spring Boot）
```

## 技术栈

- **前端**：Vue 3、TypeScript、Pinia、Element Plus、Vite
- **后端**：Spring Boot 2.7、Spring Security + JWT、MyBatis-Plus、MySQL、Apache POI
- **算法**：Python 3.8+、PyTorch、DGL、pandas、scikit-learn
- **构建/部署**：Maven Wrapper、npm、Conda、Nginx

## 配置与多环境

后端使用 Spring Profile（`dev`/`prod`）+ 环境变量组合管理配置：

- `SPRING_PROFILES_ACTIVE`：选择 `dev`（默认，指向本地 MySQL、Windows 路径）或 `prod`。
- `MYSQL_HOST/PORT/USERNAME/PASSWORD`：注入数据库连接信息，可指向本地实例或 RDS。
- `CHAIN_BASE_PATH`：数据与模型的根目录，默认 `/opt/chain`；自动派生 `CHAIN_DATASETS_PATH`、`CHAIN_MODELS_PATH`、`CHAIN_RISK_STATE_PATH` 等。
- `CHAIN_PYTHON_ENV`：Python 解释器路径，供后端调度训练/推理脚本。
- `BAILIAN_*`：阿里云百炼（DashScope）调用所需参数。

`application.yml` 保存通用配置，`application-dev.yml` 与 `application-prod.yml` 只放差异化内容，因此在不同机器上只需设置环境变量即可完成切换。

## 本地运行

### 后端
```bash
cd industry-risk-assessment-server
./mvnw spring-boot:run           # 默认 dev profile
# 或
SPRING_PROFILES_ACTIVE=prod \
CHAIN_BASE_PATH=/data/chain \
MYSQL_HOST=127.0.0.1 \
./mvnw spring-boot:run
```
> 确保本地 MySQL 中存在 `industry_risk` 数据库，并将 `datasets/`、`models-storage/` 等目录与配置对应。

### 前端
```bash
cd industry-risk-assessment
npm install
npm run dev
npm run build   # 生产构建，输出 dist/
```

### Python / 模型训练
```bash
cd models
conda create -n chain python=3.8
conda activate chain
pip install -r requirements.txt
CHAIN_BASE_PATH=/data/chain python train_han.py --config configs/han_ic.yaml
```
将训练生成的模型文件放入 `models-storage/`，后端即可加载。

## 功能概览

- **数据管理**：上传/验证/查询 Excel 数据，支持企业、周期、字典等多维检索。
- **模型训练与管理**：触发不同 GNN 模型的训练任务，查看日志、版本与指标，把最新结果存入 `models-storage/`。
- **风险评估**：通过训练好的模型对企业或产业链节点进行风险评分并输出报告。
- **可视化与交互**：前端仪表盘展示指标、趋势、风险点分布，支持模型对比与结果导出。
- **鉴权与审计**：Spring Security + JWT 保护接口，`API接口文档.txt` 中列出所有 REST API。

## 部署指南（ECS 单机方案示例）

1. **准备服务器**：申请 2C8G+ 的 Alibaba Cloud Linux/CentOS ECS，开放 `22/80/443/8080` 端口。
2. **初始化环境**：
   - 安装 OpenJDK 8、Maven（或使用项目自带 Wrapper）。
   - 安装 Node.js（前端构建）、Nginx（托管静态资源）。
   - 安装 MySQL 或连接 RDS；安装 Miniconda/venv 并创建 `Chain` 环境。
3. **同步数据**：上传 `datasets/`、`models/`、`models-storage/` 到服务器，建议放在 `/data/chain/` 下并设置 `CHAIN_BASE_PATH=/data/chain`。
4. **构建与部署**：
   - 后端：`./mvnw clean package` → 上传 `target/industry-risk-assessment-server-*.jar` → `SPRING_PROFILES_ACTIVE=prod CHAIN_* MYSQL_* java -jar ...`，可编写 `systemd` 服务保证开机自启。
   - 前端：本地 `npm run build`，把 `dist/` 上传至 `/var/www/chain`，Nginx `root` 指向该目录并将 `/api` 代理到 `http://127.0.0.1:8080`。
5. **验证**：通过域名或公网 IP 访问，检查前端页面、API、Python 训练触发和文件读写是否正常；日志位于 `/var/log/industry-risk/`（可在 `application-prod.yml` 中自定义）。

若训练任务需要更多算力，可再增加训练专用 ECS 或使用阿里云 PAI，但系统默认配置即支持在单台服务器上“前端 + 后端 + 数据库 + 模型训练”一体化运行。

## API 文档

- 根目录的 `API接口文档.txt` 包含用户、数据集、模型、训练、风险评估等全部接口说明（请求/响应示例、鉴权方式、状态码）。
- 后端统一响应结构 `{ code, message, data }`，除登录/注册外均需 `Authorization: Bearer <token>`。

## 数据与模型说明

- **datasets/**：按年份/月份组织的 Excel/CSV/JSON，用于描述企业特征、关系网络、风险标签等。
- **models/**：Python 脚本实现 HAN、HierTransferGNN、GPFedRec 等 GNN 模型，支持传参训练或推理。
- **models-storage/**：保存训练输出，文件名包含模型类型、批次、时间戳，可由后端读取加载。

如需更多部署或参数说明，可结合 `API接口文档.txt` 与代码中的注释查看，并根据实际业务扩展配置。
