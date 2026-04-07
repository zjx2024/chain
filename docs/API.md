# 产业链风险评估系统 API 文档

> 版本：1.1 ｜ 更新日期：2025 年 12 月

---

## 1. 基础信息

| 项目     | 说明                            |
| ------ | ----------------------------- |
| 系统名称   | 产业链风险评估系统                     |
| 基础 URL | `http://8.156.88.216:8080/api` |
| 数据格式   | `application/json`            |
| 字符编码   | UTF-8                         |
| 认证方式   | Token（Bearer），默认 24h 失效       |

---

## 2. 认证与安全

1. 通过 **POST `/api/user/login`** 获取 JWT；Token 24h 后失效，需要重新登录。
2. 除登录/注册以外所有 `/api/**` 接口都要求请求头 `Authorization: Bearer <token>`。
3. Token 缺失/过期/错误时，后端返回 `401 / TOKEN_EXPIRED / TOKEN_INVALID`，前端应删除本地 Token 并跳转登录页。

---

## 3. 请求 / 响应约定

### 3.1 统一响应结构

```json
{
  "code": 200,
  "message": "成功",
  "data": {/* 业务数据或 null */}
}
```

- `code`：业务状态码（见下文）。
- `message`：成功或失败提示。
- `data`：成功时为业务数据，失败时为 `null` 或包含错误上下文。

### 3.2 状态码

| 分类    | 代码   | 说明            |
| ----- | ---- | ------------- |
| 成功    | 200  | 操作成功          |
|       | 201  | 创建成功          |
| 客户端错误 | 400  | 请求参数错误        |
|       | 401  | 未认证或 Token 失效 |
|       | 403  | 权限不足          |
|       | 404  | 资源不存在         |
|       | 409  | 资源冲突          |
| 服务端错误 | 500  | 服务器内部错误       |
| 业务错误  | 1001 | 用户不存在         |
|       | 1002 | 密码错误          |
|       | 1003 | 账号被锁定         |
|       | 1004 | Token 已过期     |
|       | 1005 | Token 无效      |
|       | 1006 | 请求过于频繁        |

### 3.3 业务枚举

- **数据集类型 (`typeCode`)**：`FEATURE_LABEL`（特征与标签）、`INDUSTRY_RELATION`。
- **产业链类型**：`IC`（集成电路，ID为1）、`EI`（电子信息，ID为2）。
- **训练任务状态**：`PENDING`｜`RUNNING`｜`COMPLETED`｜`FAILED`｜`TERMINATED`。
- **训练模型状态**：`ACTIVE`｜`ARCHIVED`｜`DELETED`。
- **风险等级**：`LOW`｜`MEDIUM`｜`HIGH`｜`待评估`。

18 个节点风险评估因子（顺序与 `index` 对应）：

1. 每股营业收入 [单位]元
2. 净资产收益率ROE(平均) [单位]%
3. 销售净利率 [单位]%
4. 资产负债率 [单位]%
5. 流动比率
6. 速动比率
7. 现金比率
8. 净资产负债率
9. 经营活动产生的现金流量净额/负债合计
10. 存货周转率 [单位]次
11. 应收账款周转率(不含应收票据) [单位]次
12. 流动资产周转率 [单位]次
13. 非流动资产周转率 [单位]%
14. 总资产周转率 [单位]次
15. 营业收入同比增长率 [单位]%
16. 总资产同比增长率 [单位]%
17. 每股净资产相对年初增长率 [单位]%
18. 总资产净利率-不含少数股东损益 [单位]%

---

## 4. 模块接口

> 若无特殊说明，以下接口均需附带 `Authorization: Bearer <token>`。
> 
> **Postman 提示**：可以在一个环境变量中配置 `{{baseUrl}} = http://8.156.69.49:8080/api`、`{{token}} = Bearer <jwt>`，然后在请求里填 `{{baseUrl}}/xxx` 并在 Headers 中统一设置 `Authorization: {{token}}`。

### 4.1 用户管理 `/api/user`

#### POST /api/user/login

- **Body**：`{"username":"string","password":"string"}`

- 登录用账号密码：admin,123456

- **Response**：
  
  ```json
  {
  "code": 200,
  "message": "登录成功",
  "data": {
    "token": "<jwt>",
    "userInfo": {
      "id": 1,
      "username": "admin",
      "realName": "管理员",
      "email": "admin@example.com",
      "role": "ADMIN"
    }
  }
  }
  ```

#### GET /api/user/info

- 返回当前登录用户信息，结构同上 `userInfo`。

---

### 4.2 数据集管理 `/api/dataset`

| 接口                           | 方法     | 说明                                                                  |
| ---------------------------- | ------ | ------------------------------------------------------------------- |
| `/list`                      | GET    | 分页查询数据集，支持 `pageNum`、`pageSize`、`name`、`typeCode`、`industryChainId` |
| `/{id}`                      | GET    | 获取数据集详情                                                             |
| `/upload`                    | POST   | 表单上传数据集（`DatasetUploadDTO` + `file`）                                |
| `/`                          | POST   | 新建数据集（JSON，同实体字段）                                                   |
| `/{id}`                      | PUT    | 更新数据集                                                               |
| `/{id}`                      | DELETE | 删除数据集                                                               |
| `/types`                     | GET    | 获取数据集类型列表                                                           |
| `/industry-chains`           | GET    | 获取产业链枚举                                                             |
| `/periods/{industryChainId}` | GET    | 获取产业链下可选数据期间（格式统一为 `YYYYQ1/2/3/4`，例如 `2024Q1`）                      |

分页响应示例：

```json
{
  "code": 200,
  "message": "获取成功",
  "data": {
    "records": [
      {
        "id": 1,
        "name": "IC特征2024Q1",
        "typeCode": "FEATURE_LABEL",
        "industryChainId": 1,
        "dataPeriod": "2024Q1",
        "filePath": "/datasets/ic/feature_2024Q1.xlsx",
        "fileSize": 1024,
        "createTime": "2025-01-01 10:00:00",
        "updateTime": "2025-01-01 10:00:00",
        "deleted": 0
      }
    ],
    "total": 10,
    "size": 10,
    "current": 1,
    "pages": 1
  }
}
```

**常用请求参数**

| 接口                    | 参数                | 位置       | 必填  | 说明                                |
| --------------------- | ----------------- | -------- | --- | --------------------------------- |
| `/api/dataset/list`   | `pageNum`         | Query    | ✔︎  | 页码，从 1 开始                         |
|                       | `pageSize`        | Query    | ✔︎  | 每页记录数                             |
|                       | `name`            | Query    | ✘   | 数据集名称模糊匹配                         |
|                       | `typeCode`        | Query    | ✘   | `FEATURE_LABEL/INDUSTRY_RELATION` |
|                       | `industryChainId` | Query    | ✘   | 产业链 ID                            |
| `/api/dataset/upload` | `file`            | FormData | ✔︎  | Excel/CSV 文件                      |
|                       | `name`            | FormData | ✔︎  | 数据集名称                             |
|                       | `typeCode`        | FormData | ✔︎  | 数据集类型                             |
|                       | `industryChainId` | FormData | ✔︎  | 产业链 ID                            |
|                       | `dataPeriod`      | FormData | ✔︎  | 季度格式 `2024Q1` 等                   |



---

### 4.3 产业链管理 `/api/industry-chain`

- `GET /api/industry-chain/list`：返回产业链实体数组（`id/code/name/createTime/updateTime`）。

---

### 4.4 风险可视化 `/api/risk-status`

#### GET /api/risk-status/graph/{industryChainId}

返回关系图谱数据：

```json
{
  "code": 200,
  "message": "成功",
  "data": {
    "nodes": [
      {"id":"P13","name":"组件","category":"产品","symbolSize":18},
      {"id":"C7","name":"企业A","category":"公司","symbolSize":22}
    ],
    "links": [
      {"source":"P13","target":"C7","value":1},
      {"source":"P13","target":"P25","value":1}
    ],
    "categories": [
      {"name":"product"},
      {"name":"company"}
    ]
  }
}
```

#### GET /api/risk-status/overview/{industryChainId}?dataPeriod=2024Q1

该接口对应课题三产业链风险评估结果、产业链完整性评估（三个得分）结果、产业链风险预警结果。调用时在 Postman 中按下表配置参数：

| 参数                | 位置    | 类型     | 必填  | 说明                                  |
| ----------------- | ----- | ------ | --- | ----------------------------------- |
| `industryChainId` | Path  | number | ✔︎  | 产业链 ID（1=IC，2=EI）                   |
| `dataPeriod`      | Query | string | ✔︎  | 季度格式 `2024Q1/2024Q2/...`；若不存在返回 404 |

真实返回字段：

```json
{
  "code": 200,
  "message": "成功",
  "data": {
    "riskCompanyCount": 646,
    "totalCompanyCount": 1793,
    "riskCompanies": ["1459","1457",...],
    "normalCompanies": ["1462","1461",...],
    "riskLevel": "中风险",
    "resilienceScore": 0.65,
    "recoveryScore": 0.70,
    "integrityScore": 0.68,
    "integrityLevel": "完整",
    "nextPeriodLabel": "T+1期",
    "nextPeriodRiskCompanyCount": 644,
    "nextPeriodRiskLevel": "中风险"
  }
}
```

- `resilienceScore/recoveryScore`：由系统生成的抵抗力/恢复力得分（0~1）。
- `integrityScore`：完整性得分。
- `integrityLevel`：完整性等级：完整/不完整。
- 错误示例：
  
  ```json
  {"code":404,"message":"未找到指定期间的特征标签数据","data":null}
  ```

---

### 4.5 节点风险页 `/api/node-risk`

| 接口           | 方法  | 说明                                                    |
| ------------ | --- | ----------------------------------------------------- |
| `/companies` | GET | `?industryChainId=1`，返回该链的公司名称列表                      |
| `/status`    | GET | `industryChainId`、`dataPeriod`、`companyName`，返回节点风险状态 |
| `/alerts`    | GET | 与 `/status` 相同的查询条件，返回智能告警说明                          |

> `dataPeriod` 的值同样使用季度枚举，如 `2024Q4`。公司名称需要与 Excel 中保持一致，可先调用 `/companies` 获取候选项。

#### GET /api/node-risk/status

该接口对应课题三产业链节点风险评估、产业链节点风险预警

| 参数                | 位置    | 类型     | 必填  | 说明                |
| ----------------- | ----- | ------ | --- | ----------------- |
| `industryChainId` | Query | number | ✔︎  | 产业链 ID            |
| `dataPeriod`      | Query | string | ✔︎  | 季度字符串（如 `2024Q4`） |
| `companyName`     | Query | string | ✔︎  | 公司名称，需与底表一致       |

```json
{
  "code": 200,
  "message": "成功",
  "data": {
    "companyName": "某公司",
    "dataPeriod": "2024Q4",
    "currentRisk": false,
    "nextPeriod": "T+1期",
    "nextPeriodRisk": true,
    "currentFactors": [
      {"index":0,"name":"每股营业收入 [单位]元","value":2.31},
      {"index":1,"name":"净资产收益率ROE(平均) [单位]%","value":8.5},
      ... 共 18 项
    ],
    "nextPeriodFactors": [
      {"index":0,"name":"每股营业收入 [单位]元","value":1.80},
      ...
    ]
  }
}
```

- `currentFactors`：当前期真实指标。
- `nextPeriodFactors`：T+1 期预测指标。
- `index` 对应上文 18 个指标的顺序。

#### GET /api/node-risk/alerts

该接口给出节点告警信息

| 参数                | 位置    | 类型     | 必填  | 说明             |
| ----------------- | ----- | ------ | --- | -------------- |
| `industryChainId` | Query | number | ✔︎  | 与 `/status` 相同 |
| `dataPeriod`      | Query | string | ✔︎  | 与 `/status` 相同 |
| `companyName`     | Query | string | ✔︎  | 与 `/status` 相同 |

```json
{
  "code": 200,
  "message": "成功",
  "data": {
    "companyName": "某公司",
    "period": "T+1期",
    "alertLevel": "MEDIUM",
    "keyFactors": [
      {"name":"资产负债率 [单位]%","value":78.3,"impact":"杠杆水平偏高"},
      {"name":"现金比率","value":0.12,"impact":"短期偿债能力承压"}
    ],
    "suggestions": [
      "降杠杆：将资产负债率控制在 60% 以下",
      "增加货币资金储备，提高现金比率至 0.2 以上"
    ],
    "generatedAt": "2025-01-05 10:11:23",
    "modelName": "dashscope-qwen",
    "remark": "智能分析未启用则为fallback"
  }
}
```

- `alertLevel` 取值 `LOW/MEDIUM/HIGH`，fallback 场景会写明 `remark`。
- `keyFactors` 长度 2~5，包含阈值解释。
- 

---

### 4.6 模型训练 `/api/model-training`

| 接口                          | 方法   | 说明                                 |
| --------------------------- | ---- | ---------------------------------- |
| `/task-types`               | GET  | 获取任务类型（`id/code/name/description`） |
| `/models/{taskTypeId}`      | GET  | 根据任务类型获取模型列表                       |
| `/optimizers/{modelId}`     | GET  | 获取模型支持的优化器（含默认学习率）                 |
| `/model/{modelId}`          | GET  | 模型详情                               |
| `/model/{modelId}/path`     | PUT  | 更新模型权重文件路径（`text/plain`）           |
| `/model/{modelId}/exists`   | GET  | 检查模型文件是否存在                         |
| `/model/{modelId}/fullpath` | GET  | 返回模型在服务器上的绝对路径                     |
| `/start`                    | POST | 启动训练任务（见下）                         |
| `/tasks/running`            | GET  | 获取运行中的训练任务                         |
| `/tasks/recent?limit=10`    | GET  | 获取最近任务                             |
| `/tasks/{taskId}/terminate` | POST | 终止任务                               |

启动训练请求体：

```json
{
  "datasetId": 1,
  "dataPeriod": "2024Q1",
  "taskTypeId": 1,
  "modelId": 1,
  "optimizerId": 1,
  "epochs": 100,
  "learningRate": 0.001,
  "clientsSampleRatio": 0.8,
  "topkRatio": 0.1,
  "nClusters": 5,
  "privacyMethod": "DP",
  "dp": 0.01
}
```

| 字段                                                        | 类型            | 必填  | 说明                    |
| --------------------------------------------------------- | ------------- | --- | --------------------- |
| `datasetId`                                               | number        | ✔︎  | 使用的数据集 ID             |
| `dataPeriod`                                              | string        | ✔︎  | 数据期间（季度格式，如 `2024Q1`） |
| `taskTypeId`                                              | number        | ✔︎  | 任务类型 ID               |
| `modelId`                                                 | number        | ✔︎  | 模型 ID                 |
| `optimizerId`                                             | number        | ✔︎  | 优化器 ID                |
| `epochs`                                                  | number        | ✔︎  | 训练轮数                  |
| `learningRate`                                            | number        | ✘   | 学习率，不填则使用优化器默认值       |
| `clientsSampleRatio/topkRatio/nClusters/privacyMethod/dp` | number/string | ✘   | 针对联邦/隐私训练的参数，可按需填写    |

响应为 `TrainingTask`：包括 `id/taskName/taskTypeName/modelName/optimizerName/learningRate/totalEpochs/currentEpoch/status/startTime/endTime/...`。

---

### 4.7 训练模型管理 `/api/trained-models`

| 接口                                | 方法     | 说明                                |
| --------------------------------- | ------ | --------------------------------- |
| `/`                               | GET    | 分页获取训练后模型（`current/size/keyword`） |
| `/all`                            | GET    | 获取全部训练后模型（不分页）                    |
| `/{id}`                           | GET    | 获取单个模型详情，附带 `taskType` 元信息        |
| `/{id}/training-plots`            | GET    | 获取训练过程图片列表（不需要 Token，可公开查看）       |
| `/{id}/training-plots/{filename}` | GET    | 图片二进制流（`responseType=blob`）       |
| `/by-training-task/{taskId}`      | GET    | 通过任务 ID 查询模型                      |
| `/by-name/{modelName}`            | GET    | 通过训练后模型名称查询                       |
| `/{id}/archive`                   | PUT    | 归档模型（状态从 ACTIVE→ARCHIVED）         |
| `/{id}`                           | DELETE | 删除模型                              |
| `/test`                           | POST   | 同步测试模型（见下）                        |
| `/test-async`                     | POST   | 异步测试模型                            |
| `/test/validate-environment`      | GET    | 检查测试环境依赖是否就绪                      |
| `/fix-missing-records`            | POST   | **内部修复**：为缺失记录的任务补模型记录            |
| `/test-path-generation`           | GET    | **调试**：验证模型保存路径生成逻辑               |

分页响应示例：

```json
{
  "code": 200,
  "message": "获取成功",
  "data": {
    "records": [
      {
        "id": 101,
        "trainedModelName": "HAN_Model_uuid_epochs100_lr0.001_20250101_100000",
        "originalModelId": 1,
        "originalModelName": "HAN",
        "trainingTaskId": 88,
        "taskTypeId": 3,
        "taskTypeCode": "RISK_FORECAST",
        "taskTypeName": "风险预测",
        "modelSavePath": "/data/chain/models-storage/...",
        "logFileName": "training.log",
        "trainingEpochs": 100,
        "learningRate": 0.001,
        "bestEpoch": 85,
        "modelSize": 1024000,
        "trainingDuration": 3600,
        "datasetName": "IC特征2025-01",
        "optimizerName": "Adam",
        "status": "ACTIVE",
        "description": "准确率: 0.82\nF1分数: 0.79\nAUC值: 0.85",
        "createTime": "2025-01-01 11:00:00",
        "updateTime": "2025-01-01 11:00:00"
      }
    ],
    "total": 12,
    "current": 1,
    "size": 10,
    "pages": 2
  }
}
```

训练过程图片列表：

```json
{
  "code": 200,
  "message": "获取成功",
  "data": [
    {"filename":"training_curves.png","displayName":"训练曲线","url":"/api/trained-models/1/training-plots/training_curves.png"},
    {"filename":"test_curves.png","displayName":"测试曲线","url":"/api/trained-models/1/training-plots/test_curves.png"}
  ]
}
```

模型测试请求：

```json
{
  "trainedModelId": 1,
  "trainedModelName": "HAN_Model_uuid_epochs100_lr0.001_20250101_100000",
  "testDatasetId": 3,
  "testDatasetPath": "/data/chain/datasets/eval/ic_test.csv",
  "testBatchSize": 64,
  "device": "cuda:0",
  "saveResults": true,
  "outputPath": "/data/chain/test-results/"
}
```

响应：

```json
{
  "code": 200,
  "message": "测试完成",
  "data": {
    "testTime": "2025-01-05 12:30:00",
    "trainedModelName": "HAN_Model_uuid_epochs100_lr0.001_20250101_100000",
    "testDatasetName": "IC Test 2024Q4",
    "hr10": 0.85,
    "ndcg10": 0.78,
    "testLoss": 0.23,
    "performanceComparison": {
      "hrRelativeChange": 0.05,
      "ndcgRelativeChange": 0.03,
      "hrDifference": 0.04,
      "ndcgDifference": 0.02,
      "trainingBestHr": 0.81,
      "trainingBestNdcg": 0.76
    },
    "resultFilePath": "/data/chain/test-results/HAN_20250105.json",
    "status": "SUCCESS",
    "additionalInfo": {}
  }
}
```

异步接口返回 `{"message":"模型测试已启动，请稍后查看结果"}`。

> `/fix-missing-records` 与 `/test-path-generation` 为排障用途，请谨慎暴露给前端。

---

## 5. 错误示例

```json
{
  "code": 401,
  "message": "token已过期",
  "data": null
}
```

客户端收到此响应时应立即登出并重定向到登录页。

---

## 6. 更新历史

| 日期         | 说明            |
| ---------- | ------------- |
| 2025-01-01 | 初始版本，包含核心接口说明 |
| 2025-12-10 | 同步当前实现：       |

- 风险概览新增指标与 T+1 预测字段。
- 新增节点风险（公司列表/状态/告警）接口说明。
- 更新图谱节点字段（移除 `value/x/y`）。
- 补全训练模型管理、模型测试及内部维护接口。 |
