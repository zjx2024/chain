/*
 Navicat Premium Data Transfer

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 50744 (5.7.44-log)
 Source Host           : localhost:3306
 Source Schema         : industry_risk

 Target Server Type    : MySQL
 Target Server Version : 50744 (5.7.44-log)
 File Encoding         : 65001

 Date: 24/11/2025 15:08:14
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for dataset
-- ----------------------------
DROP TABLE IF EXISTS `dataset`;
CREATE TABLE `dataset`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '数据集名称',
  `type_code` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '数据集类型编码',
  `industry_chain_id` bigint(20) NOT NULL COMMENT '所属产业链ID',
  `data_period` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '数据期间(格式：2024Q1)',
  `file_path` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '文件存储路径',
  `file_size` bigint(20) NULL DEFAULT NULL COMMENT '文件大小(字节)',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `create_by` bigint(20) NOT NULL COMMENT '创建者ID',
  `deleted` tinyint(1) NULL DEFAULT 0 COMMENT '是否删除：0-未删除 1-已删除',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `industry_chain_id`(`industry_chain_id`) USING BTREE,
  INDEX `type_code`(`type_code`) USING BTREE,
  CONSTRAINT `dataset_ibfk_1` FOREIGN KEY (`industry_chain_id`) REFERENCES `industry_chain` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `dataset_ibfk_2` FOREIGN KEY (`type_code`) REFERENCES `dict_dataset_type` (`code`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 66 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '数据集表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of dataset
-- ----------------------------
INSERT INTO `dataset` VALUES (1, '集成电路产业特征数据2024', 'FEATURE_LABEL', 1, '2024Q1', NULL, NULL, '2025-02-25 17:53:19', '2025-02-26 16:20:47', 1, 1);
INSERT INTO `dataset` VALUES (2, '电子信息产业关系数据2024', 'INDUSTRY_RELATION', 2, '2024Q1', NULL, NULL, '2025-02-25 17:53:19', '2025-02-26 16:21:06', 1, 1);
INSERT INTO `dataset` VALUES (3, '集成电路_2023Q3', 'FEATURE_LABEL', 1, '2023Q3', '2025/02/26/7ec6af92-46ef-4cdd-93f9-778e51ad1ad5.xlsx', 451905, '2025-02-26 15:52:03', '2025-02-26 16:21:20', 1, 1);
INSERT INTO `dataset` VALUES (4, '集成电路关系数据', 'INDUSTRY_RELATION', 1, '', '2025/02/26/297c4b38-ad3f-4acc-ad3d-a93e6e45657b.xlsx', 7099396, '2025-02-26 15:56:08', '2025-02-26 16:22:51', 1, 1);
INSERT INTO `dataset` VALUES (5, '电子信息关系数据', 'INDUSTRY_RELATION', 2, '', '2025/02/26/ca95c6f3-5f76-42a4-a2b9-52a00087dcef.xlsx', 22244382, '2025-02-26 16:08:07', '2025-03-02 17:20:45', 1, 1);
INSERT INTO `dataset` VALUES (6, '集成电路关系数据', 'INDUSTRY_RELATION', 1, '', '2025/02/26/5a61a585-6af3-4b6d-b4d3-be1c7ed44018.xlsx', 7099396, '2025-02-26 16:23:54', '2025-03-01 16:34:12', 1, 1);
INSERT INTO `dataset` VALUES (7, '集成电路_2021Q4', 'FEATURE_LABEL', 1, '2021Q4', '2025/02/26/1afe0e27-6d79-4e59-968c-8483cd05f185.xlsx', 453044, '2025-02-26 16:27:11', '2025-03-02 17:20:39', 1, 1);
INSERT INTO `dataset` VALUES (8, '集成电路_2022Q2', 'FEATURE_LABEL', 1, '2022Q2', '2025/02/26/26bb9352-0499-4b0a-bfe4-dff3e4abee8c.xlsx', 451422, '2025-02-26 16:27:47', '2025-03-02 17:20:33', 1, 1);
INSERT INTO `dataset` VALUES (9, '集成电路_2022Q4', 'FEATURE_LABEL', 1, '2022Q2', '2025/02/26/777b34df-8edc-46de-a8ae-2269b3e30f36.xlsx', 451422, '2025-02-26 16:28:24', '2025-02-26 16:28:47', 1, 1);
INSERT INTO `dataset` VALUES (10, '集成电路_2022Q4', 'FEATURE_LABEL', 1, '', '2025/02/26/a2d9402f-887e-41f6-a66a-732d3c243067.xlsx', 452843, '2025-02-26 16:29:14', '2025-02-26 16:29:25', 1, 1);
INSERT INTO `dataset` VALUES (11, '集成电路_2022Q4', 'FEATURE_LABEL', 1, '2022Q4', '2025/02/26/b5e8b0a8-6c27-4b8f-ba19-cf424c67c452.xlsx', 452843, '2025-02-26 16:53:36', '2025-03-02 17:20:30', 1, 1);
INSERT INTO `dataset` VALUES (12, '集成电路_2023Q1', 'FEATURE_LABEL', 1, '2023Q1', '2025/02/26/c992f45d-d0a2-42e5-b425-0e3db96a8969.xlsx', 448870, '2025-02-26 16:54:00', '2025-03-02 17:20:27', 1, 1);
INSERT INTO `dataset` VALUES (13, '集成电路_2023Q2', 'FEATURE_LABEL', 1, '2023Q2', '2025/02/26/7c7475a9-6ccb-4432-aa11-94263dea97d1.xlsx', 450998, '2025-02-26 16:56:27', '2025-03-02 17:20:24', 1, 1);
INSERT INTO `dataset` VALUES (14, '集成电路_2023Q3', 'FEATURE_LABEL', 1, '2023Q3', '2025/02/26/cba75c06-c578-4710-965a-b022b68c2eb8.xlsx', 451905, '2025-02-26 16:56:48', '2025-03-02 17:20:23', 1, 1);
INSERT INTO `dataset` VALUES (15, '集成电路_2023Q4', 'FEATURE_LABEL', 1, '2023Q4', '2025/02/26/81beb597-7f89-40c2-b53b-ab67a50baab9.xlsx', 451692, '2025-02-26 16:57:12', '2025-03-02 17:20:19', 1, 1);
INSERT INTO `dataset` VALUES (16, '集成电路_2024Q1', 'FEATURE_LABEL', 1, '2024Q1', '2025/02/26/c4a423d8-377b-4f9f-8455-8687272fe1e8.xlsx', 447646, '2025-02-26 16:57:39', '2025-03-02 17:20:17', 1, 1);
INSERT INTO `dataset` VALUES (17, '集成电路_2024Q2', 'FEATURE_LABEL', 1, '2024Q2', '2025/02/26/9be45a73-1775-4d3a-a614-fc5f74ea538e.xlsx', 450577, '2025-02-26 16:58:04', '2025-03-02 17:20:13', 1, 1);
INSERT INTO `dataset` VALUES (18, '集成电路_2020Q4', 'FEATURE_LABEL', 1, '2020Q4', '2025/02/26/e4879b8e-454d-4002-96bf-7fb8fe74338c.xlsx', 452464, '2025-02-26 16:58:30', '2025-03-02 17:20:41', 1, 1);
INSERT INTO `dataset` VALUES (19, '电子信息_2019Q4', 'FEATURE_LABEL', 2, '2019Q4', '2025/02/26/b1a5cd93-7639-4231-946e-281e90fb4f19.xlsx', 604741, '2025-02-26 17:00:06', '2025-03-02 17:20:44', 1, 1);
INSERT INTO `dataset` VALUES (20, '电子信息_2020Q4', 'FEATURE_LABEL', 2, '2020Q4', '2025/02/26/66ad1f09-5106-446e-8eec-c39bbfd048b3.xlsx', 605150, '2025-02-26 17:00:40', '2025-03-02 17:20:42', 1, 1);
INSERT INTO `dataset` VALUES (21, '电子信息_2021Q4', 'FEATURE_LABEL', 2, '2021Q4', '2025/02/26/666d5e5d-a92c-488b-8c91-c2472c9c041e.xlsx', 605537, '2025-02-26 17:01:17', '2025-03-02 17:20:37', 1, 1);
INSERT INTO `dataset` VALUES (22, '电子信息_2022Q2', 'FEATURE_LABEL', 2, '2022Q2', '2025/02/26/aedbf517-a0b2-42b9-b0da-026c74753476.xlsx', 603430, '2025-02-26 17:01:42', '2025-03-02 17:20:36', 1, 1);
INSERT INTO `dataset` VALUES (23, '电子信息_2022Q4', 'FEATURE_LABEL', 2, '2022Q4', '2025/02/26/7695e14f-65dc-400b-aad3-ee4ecc0544be.xlsx', 608019, '2025-02-26 17:02:43', '2025-03-02 17:20:31', 1, 1);
INSERT INTO `dataset` VALUES (24, '电子信息_2023Q2', 'FEATURE_LABEL', 2, '2023Q2', '2025/02/26/311b0ce7-dd9b-4591-9ac9-2f7514435636.xlsx', 605972, '2025-02-26 17:03:02', '2025-03-02 17:20:26', 1, 1);
INSERT INTO `dataset` VALUES (25, '电子信息_2023Q4', 'FEATURE_LABEL', 2, '2023Q4', '2025/02/26/7a353ef7-f90d-4022-b035-c7d6e80567ae.xlsx', 603936, '2025-02-26 17:03:23', '2025-03-02 17:20:21', 1, 1);
INSERT INTO `dataset` VALUES (26, '电子信息_2024Q1', 'FEATURE_LABEL', 2, '2024Q1', '2025/02/26/78621be1-505c-4ffd-8bd0-d52051f8239c.xlsx', 599431, '2025-02-26 17:03:47', '2025-03-02 17:20:15', 1, 1);
INSERT INTO `dataset` VALUES (27, '电子信息_2024Q2', 'FEATURE_LABEL', 2, '2024Q2', '2025/02/26/bbf5b3e2-845b-4c10-aa2b-1d6a0ff5a3ed.xlsx', 602755, '2025-02-26 17:04:04', '2025-03-02 17:20:10', 1, 1);
INSERT INTO `dataset` VALUES (28, '集成电路关系数据', 'INDUSTRY_RELATION', 1, '', '2025/03/01/aca43265-f347-44c6-a0ba-56a273fdd7b9.xlsx', 7982178, '2025-03-01 16:34:48', '2025-03-02 17:20:46', 1, 1);
INSERT INTO `dataset` VALUES (29, '电子信息_2024Q2', 'FEATURE_LABEL', 2, '2024Q2', '2025/03/02/4b02a87f-a4ef-4d98-944c-54d60a2bf745.xlsx', 602755, '2025-03-02 17:22:12', '2025-03-02 17:40:56', 1, 1);
INSERT INTO `dataset` VALUES (30, '集成电路_2023Q4', 'FEATURE_LABEL', 1, '2023Q4', '2025/03/02/f0950188-f850-4daa-ac9a-052c49cec35b.xlsx', 451692, '2025-03-02 17:22:38', '2025-03-02 17:40:57', 1, 1);
INSERT INTO `dataset` VALUES (31, '电子信息关系数据', 'INDUSTRY_RELATION', 2, '', '2025/03/02/24842297-a32c-4f05-aa22-d4813472a4b5.xlsx', 22244382, '2025-03-02 17:31:02', '2025-03-02 17:40:59', 1, 1);
INSERT INTO `dataset` VALUES (32, '集成电路关系数据', 'INDUSTRY_RELATION', 1, '', '2025/03/02/204292cc-9e31-4a21-a4f2-c8f1b7244197.xlsx', 7982175, '2025-03-02 17:31:27', '2025-03-02 17:41:03', 1, 1);
INSERT INTO `dataset` VALUES (33, '电子信息关系数据', 'INDUSTRY_RELATION', 2, '', '2025/03/02/cf36c63f-bc40-4ba7-92e5-d51aeab2800e.xlsx', 22244382, '2025-03-02 17:41:49', '2025-03-25 23:55:24', 1, 1);
INSERT INTO `dataset` VALUES (34, '集成电路关系数据', 'INDUSTRY_RELATION', 1, '', '2025/03/02/ba39d765-60b5-4824-84b4-672fd77b3ab6.xlsx', 7982175, '2025-03-02 17:42:07', '2025-03-25 23:55:26', 1, 1);
INSERT INTO `dataset` VALUES (35, '电子信息_2023Q4', 'FEATURE_LABEL', 2, '2023Q4', '2025/03/02/4b77ef57-134c-4669-81cc-82b62165b129.xlsx', 603936, '2025-03-02 17:42:30', '2025-03-25 23:55:22', 1, 1);
INSERT INTO `dataset` VALUES (36, '集成电路_2024Q2', 'FEATURE_LABEL', 1, '2024Q2', '2025/03/02/91c25cb1-f4f4-4f35-826f-ad9fb117be2b.xlsx', 450577, '2025-03-02 17:42:52', '2025-03-25 23:55:20', 1, 1);
INSERT INTO `dataset` VALUES (37, '电子信息_2023Q4', 'FEATURE_LABEL', 2, '2023Q4', '2025/03/25/e7272c51-a3cb-4e6e-9b8e-8c1ec83b2da5.xlsx', 603936, '2025-03-25 23:56:33', '2025-03-26 09:35:37', 1, 1);
INSERT INTO `dataset` VALUES (38, '电子信息关系数据', 'INDUSTRY_RELATION', 2, '', '2025/03/25/1b45a3b7-e60d-4b25-b98e-48426a72a83b.xlsx', 22244382, '2025-03-25 23:57:02', '2025-03-26 09:35:41', 1, 1);
INSERT INTO `dataset` VALUES (39, '集成电路_2022Q2', 'FEATURE_LABEL', 1, '2022Q2', '2025/03/25/4e3ece9a-c9ae-4b6b-90eb-815058249b63.xlsx', 451422, '2025-03-25 23:57:35', '2025-03-26 09:35:39', 1, 1);
INSERT INTO `dataset` VALUES (40, '集成电路关系数据', 'INDUSTRY_RELATION', 1, '', '2025/03/25/56af391e-2d51-418d-9aa2-f3d7735e4737.xlsx', 7982175, '2025-03-25 23:58:01', '2025-03-26 09:35:43', 1, 1);
INSERT INTO `dataset` VALUES (41, '电子信息_2021Q4', 'FEATURE_LABEL', 2, '2021Q4', '2025/03/26/a0ecd87b-bde5-4517-ba74-6bfba00f3c79.xlsx', 605537, '2025-03-26 09:36:10', '2025-06-24 10:01:55', 1, 1);
INSERT INTO `dataset` VALUES (42, '集成电路_2022Q2', 'FEATURE_LABEL', 1, '2022Q2', '2025/03/26/4a95631b-c3ee-447e-af92-ced379950b62.xlsx', 451422, '2025-03-26 09:36:28', '2025-06-24 10:01:52', 1, 1);
INSERT INTO `dataset` VALUES (43, '电子信息关系数据', 'INDUSTRY_RELATION', 2, '', '2025/03/26/16d782a3-1216-4ae8-acc5-725303eb5491.xlsx', 22244382, '2025-03-26 09:36:47', '2025-06-24 10:01:58', 1, 1);
INSERT INTO `dataset` VALUES (44, '集成电路关系数据', 'INDUSTRY_RELATION', 1, '', '2025/03/26/8e170b66-f688-4af0-a45c-4972c592a6ec.xlsx', 7982175, '2025-03-26 09:37:02', '2025-06-24 10:01:56', 1, 1);
INSERT INTO `dataset` VALUES (45, '电子信息关系数据', 'INDUSTRY_RELATION', 2, '', '2025/06/24/1338a5a4-3020-4a79-b4e0-fb45767ca715.xlsx', 22244382, '2025-06-24 10:03:05', '2025-06-24 10:03:05', 1, 0);
INSERT INTO `dataset` VALUES (46, '电子信息_2022Q2', 'FEATURE_LABEL', 2, '2022Q2', '2025/06/24/8f07c931-9366-4a93-af25-e036be4a4af3.xlsx', 603430, '2025-06-24 10:04:03', '2025-06-24 10:04:03', 1, 0);
INSERT INTO `dataset` VALUES (48, '电子信息_2019Q4', 'FEATURE_LABEL', 2, '2019Q4', '2025/06/30/c7c51dce-b0d4-4699-abc6-805373460c96.xlsx', 604741, '2025-06-30 08:57:17', '2025-06-30 08:57:17', 1, 0);
INSERT INTO `dataset` VALUES (49, '电子信息_2020Q4', 'FEATURE_LABEL', 2, '2020Q4', '2025/06/30/3b466475-1563-4c4c-a072-a471fe03a41a.xlsx', 605150, '2025-06-30 08:57:49', '2025-06-30 08:57:49', 1, 0);
INSERT INTO `dataset` VALUES (50, '电子信息_2021Q4', 'FEATURE_LABEL', 2, '2021Q4', '2025/06/30/e4601054-4ab2-4340-9a16-0cab89dfc5e7.xlsx', 605537, '2025-06-30 08:58:10', '2025-06-30 08:58:10', 1, 0);
INSERT INTO `dataset` VALUES (51, '电子信息_2022Q4', 'FEATURE_LABEL', 2, '2022Q4', '2025/06/30/88f5d5bb-2ef1-4957-a4cb-59f03577ffe7.xlsx', 608019, '2025-06-30 08:58:51', '2025-06-30 08:58:51', 1, 0);
INSERT INTO `dataset` VALUES (52, '电子信息_2023Q2', 'FEATURE_LABEL', 2, '2023Q2', '2025/06/30/398f907c-14ab-4605-a6d8-b54bb6d12659.xlsx', 605972, '2025-06-30 08:59:17', '2025-06-30 08:59:17', 1, 0);
INSERT INTO `dataset` VALUES (53, '电子信息_2023Q4', 'FEATURE_LABEL', 2, '2023Q4', '2025/06/30/eef9ebfa-ff14-4038-b545-f9373ddfeb19.xlsx', 603936, '2025-06-30 08:59:37', '2025-06-30 08:59:37', 1, 0);
INSERT INTO `dataset` VALUES (54, '电子信息_2024Q1', 'FEATURE_LABEL', 2, '2024Q1', '2025/06/30/8209400e-2927-4ac7-8b89-d4d97890f41f.xlsx', 599431, '2025-06-30 08:59:56', '2025-06-30 08:59:56', 1, 0);
INSERT INTO `dataset` VALUES (55, '电子信息_2024Q2', 'FEATURE_LABEL', 2, '2024Q2', '2025/06/30/8b29f586-d9ec-47f1-8b22-ffe14ce03990.xlsx', 602755, '2025-06-30 09:00:16', '2025-06-30 09:00:16', 1, 0);
INSERT INTO `dataset` VALUES (56, '集成电路_2024Q2', 'FEATURE_LABEL', 1, '2024Q2', '2025/07/25/15a93ad6-3be8-41c4-848e-7db784406389.xlsx', 450577, '2025-07-25 16:57:24', '2025-07-25 17:18:21', 1, 1);
INSERT INTO `dataset` VALUES (57, '集成电路_2024Q2', 'FEATURE_LABEL', 1, '2024Q2', '2025/07/25/56ac110b-e054-4e6a-ba6c-0cdf404e7a16.xlsx', 450577, '2025-07-25 17:21:43', '2025-07-25 18:33:09', 1, 1);
INSERT INTO `dataset` VALUES (58, '集成电路_2023Q4', 'FEATURE_LABEL', 1, '2023Q4', '2025/07/25/f87a52fc-345e-4ada-97cc-5f1e45ec0427.xlsx', 451692, '2025-07-25 17:25:34', '2025-07-25 18:33:12', 1, 1);
INSERT INTO `dataset` VALUES (59, '集成电路_2022Q4', 'FEATURE_LABEL', 1, '2022Q4', '2025/07/25/2f9f5fe8-60eb-4b4c-8a62-0f36a9e7779d.xlsx', 452843, '2025-07-25 18:30:36', '2025-07-25 18:33:16', 1, 1);
INSERT INTO `dataset` VALUES (60, '集成电路_2024Q2', 'FEATURE_LABEL', 1, '2024Q2', '2025/07/25/f3541de5-4a71-4d39-b254-01762d12b7c3.xlsx', 450577, '2025-07-25 18:34:52', '2025-11-01 15:54:47', 1, 0);
INSERT INTO `dataset` VALUES (61, '集成电路关系数据', 'INDUSTRY_RELATION', 1, '', '2025/10/16/6879bb31-69fa-48e0-9933-993497d7a921.xlsx', 7982167, '2025-10-16 15:39:21', '2025-10-16 15:50:16', 1, 1);
INSERT INTO `dataset` VALUES (62, '集成电路关系数据', 'INDUSTRY_RELATION', 1, '', '2025/10/16/22127084-db84-428c-8d84-06996cb02f9e.xlsx', 7982175, '2025-10-16 15:52:27', '2025-10-16 15:52:27', 1, 0);
INSERT INTO `dataset` VALUES (63, '集成电路_2022Q2', 'FEATURE_LABEL', 1, '2022Q2', '2025/11/03/5187a343-8967-4f3f-8b2b-42a4ccc13bdc.xlsx', 451422, '2025-11-03 10:16:07', '2025-11-03 10:16:07', 1, 0);
INSERT INTO `dataset` VALUES (64, '集成电路_2022Q4', 'FEATURE_LABEL', 1, '2022Q4', '2025/11/03/165c11c9-545c-4876-b449-c102dfc1118c.xlsx', 452843, '2025-11-03 10:33:27', '2025-11-03 10:33:27', 1, 0);
INSERT INTO `dataset` VALUES (65, '集成电路_2023Q2', 'FEATURE_LABEL', 1, '2023Q2', '2025/11/03/45c8856a-da49-4cdc-a6ac-e15a09bdb526.xlsx', 450998, '2025-11-03 10:37:23', '2025-11-03 10:37:23', 1, 0);

-- ----------------------------
-- Table structure for dict_dataset_type
-- ----------------------------
DROP TABLE IF EXISTS `dict_dataset_type`;
CREATE TABLE `dict_dataset_type`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `code` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '类型编码',
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '类型名称',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `code`(`code`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '数据集类型字典表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of dict_dataset_type
-- ----------------------------
INSERT INTO `dict_dataset_type` VALUES (1, 'FEATURE_LABEL', '特征与标签数据', '2025-02-25 17:53:19');
INSERT INTO `dict_dataset_type` VALUES (2, 'INDUSTRY_RELATION', '产业链关系数据', '2025-02-25 17:53:19');
INSERT INTO `dict_dataset_type` VALUES (3, 'TRAIN_TEST', '训练测试数据', '2025-06-23 23:24:48');

-- ----------------------------
-- Table structure for dict_model
-- ----------------------------
DROP TABLE IF EXISTS `dict_model`;
CREATE TABLE `dict_model`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `code` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '模型编码',
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '模型名称',
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '模型描述',
  `model_path` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '模型文件路径',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `code`(`code`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '模型字典表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of dict_model
-- ----------------------------
INSERT INTO `dict_model` VALUES (1, 'GPFEDREC_TOPKEF21', 'GPFedRec-TopkEF21', '图联邦推荐模型-TopkEF21版本', 'GPFedRec-TopkEF21/', '2025-06-23 23:52:08', '2025-06-24 10:43:26');
INSERT INTO `dict_model` VALUES (2, 'HAN_MODEL', 'HAN Model', '结合层次图神经网络和LSTM的产业链风险预警模型', 'HAN_Model/', '2025-07-10 16:01:24', '2025-10-31 12:44:59');
INSERT INTO `dict_model` VALUES (3, 'HIERTRANSFERGNN_MODEL', 'HierTransferGNN Model', '基于分层知识可转移图神经网络的风险评估模型', 'HierTransferGNN_Model/', '2025-07-10 16:01:24', '2025-07-10 16:01:24');
INSERT INTO `dict_model` VALUES (4, 'METAPATH2VEC', 'MetaPath2vec', '基于链接预测的产业链完整性评估模型', 'MetaPath2vec/', '2025-10-31 14:47:58', '2025-11-01 19:55:45');

-- ----------------------------
-- Table structure for dict_optimizer
-- ----------------------------
DROP TABLE IF EXISTS `dict_optimizer`;
CREATE TABLE `dict_optimizer`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `code` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '优化器编码',
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '优化器名称',
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '优化器描述',
  `default_lr` decimal(10, 6) NULL DEFAULT 0.001000 COMMENT '默认学习率',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `code`(`code`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '优化器字典表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of dict_optimizer
-- ----------------------------
INSERT INTO `dict_optimizer` VALUES (1, 'SGD', 'SGD', '随机梯度下降优化器', 0.010000, '2025-06-23 23:52:08', '2025-06-23 23:52:08');
INSERT INTO `dict_optimizer` VALUES (2, 'ADAM', 'Adam', '自适应矩估计优化器', 0.001000, '2025-07-10 16:01:24', '2025-07-10 16:01:24');

-- ----------------------------
-- Table structure for dict_task_type
-- ----------------------------
DROP TABLE IF EXISTS `dict_task_type`;
CREATE TABLE `dict_task_type`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `code` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '任务类型编码',
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '任务类型名称',
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '任务描述',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `code`(`code`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '任务类型字典表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of dict_task_type
-- ----------------------------
INSERT INTO `dict_task_type` VALUES (1, 'TEST_TASK', '测试训练任务', '用于测试和验证的训练任务类型', '2025-06-23 23:52:08', '2025-06-23 23:52:08');
INSERT INTO `dict_task_type` VALUES (2, 'INDUSTRY_RISK_ASSESSMENT', '产业链风险评估', '基于图神经网络的产业链风险评估任务', '2025-07-10 16:01:24', '2025-07-10 16:01:24');
INSERT INTO `dict_task_type` VALUES (3, 'INTEGRITY_ASSESSMENT', '产业链完整性评估', '完整性评估任务', '2025-10-31 12:45:42', '2025-10-31 12:45:42');
INSERT INTO `dict_task_type` VALUES (4, 'RISK_WARNING', '产业链风险预警', '风险预警任务', '2025-10-31 12:45:42', '2025-10-31 12:45:42');

-- ----------------------------
-- Table structure for industry_chain
-- ----------------------------
DROP TABLE IF EXISTS `industry_chain`;
CREATE TABLE `industry_chain`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `code` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '产业链编码',
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '产业链名称',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `code`(`code`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '产业链表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of industry_chain
-- ----------------------------
INSERT INTO `industry_chain` VALUES (1, 'IC', '集成电路产业链', '2025-02-25 17:53:19', '2025-02-25 17:53:19');
INSERT INTO `industry_chain` VALUES (2, 'EI', '电子信息产业链', '2025-02-25 17:53:19', '2025-02-25 17:53:19');

-- ----------------------------
-- Table structure for model_optimizer
-- ----------------------------
DROP TABLE IF EXISTS `model_optimizer`;
CREATE TABLE `model_optimizer`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `model_id` bigint(20) NOT NULL COMMENT '模型ID',
  `optimizer_id` bigint(20) NOT NULL COMMENT '优化器ID',
  `default_lr` decimal(10, 6) NULL DEFAULT NULL COMMENT '默认学习率',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `model_optimizer_unique`(`model_id`, `optimizer_id`) USING BTREE,
  INDEX `model_id`(`model_id`) USING BTREE,
  INDEX `optimizer_id`(`optimizer_id`) USING BTREE,
  CONSTRAINT `model_optimizer_ibfk_1` FOREIGN KEY (`model_id`) REFERENCES `dict_model` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `model_optimizer_ibfk_2` FOREIGN KEY (`optimizer_id`) REFERENCES `dict_optimizer` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '模型与优化器关联表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of model_optimizer
-- ----------------------------
INSERT INTO `model_optimizer` VALUES (1, 1, 1, 0.100000, '2025-06-23 23:53:29');
INSERT INTO `model_optimizer` VALUES (2, 2, 2, 0.001000, '2025-07-10 16:01:24');
INSERT INTO `model_optimizer` VALUES (3, 3, 2, 0.001000, '2025-07-10 16:01:24');
INSERT INTO `model_optimizer` VALUES (4, 4, 2, 0.001000, '2025-10-31 14:50:12');

-- ----------------------------
-- Table structure for task_type_model
-- ----------------------------
DROP TABLE IF EXISTS `task_type_model`;
CREATE TABLE `task_type_model`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `task_type_id` bigint(20) NOT NULL COMMENT '任务类型ID',
  `model_id` bigint(20) NOT NULL COMMENT '模型ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `task_model_unique`(`task_type_id`, `model_id`) USING BTREE,
  INDEX `task_type_id`(`task_type_id`) USING BTREE,
  INDEX `model_id`(`model_id`) USING BTREE,
  CONSTRAINT `task_type_model_ibfk_1` FOREIGN KEY (`task_type_id`) REFERENCES `dict_task_type` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `task_type_model_ibfk_2` FOREIGN KEY (`model_id`) REFERENCES `dict_model` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '任务类型与模型关联表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of task_type_model
-- ----------------------------
INSERT INTO `task_type_model` VALUES (2, 1, 1, '2025-06-23 23:53:29');
INSERT INTO `task_type_model` VALUES (4, 2, 3, '2025-07-10 16:01:24');
INSERT INTO `task_type_model` VALUES (5, 4, 2, '2025-10-31 12:46:49');
INSERT INTO `task_type_model` VALUES (6, 3, 4, '2025-10-31 14:49:31');

-- ----------------------------
-- Table structure for trained_model
-- ----------------------------
DROP TABLE IF EXISTS `trained_model`;
CREATE TABLE `trained_model`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `trained_model_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '训练后模型名称(模型名+日志文件名)',
  `original_model_id` bigint(20) NOT NULL COMMENT '原始模型ID',
  `original_model_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '原始模型名称',
  `training_task_id` bigint(20) NOT NULL COMMENT '关联的训练任务ID',
  `model_save_path` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '模型保存路径',
  `log_file_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '训练日志文件名',
  `training_epochs` int(11) NOT NULL COMMENT '训练轮次',
  `learning_rate` decimal(10, 8) NULL DEFAULT NULL COMMENT '学习率',
  `best_epoch` int(11) NULL DEFAULT NULL COMMENT '最佳性能轮次',
  `model_size` bigint(20) NULL DEFAULT NULL COMMENT '模型文件大小(字节)',
  `training_duration` int(11) NULL DEFAULT NULL COMMENT '训练时长(分钟)',
  `dataset_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '训练使用的数据集',
  `optimizer_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '使用的优化器',
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT 'ACTIVE' COMMENT '模型状态: ACTIVE-可用, ARCHIVED-已归档, DELETED-已删除',
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '模型描述',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_trained_model_name`(`trained_model_name`) USING BTREE,
  INDEX `idx_original_model_id`(`original_model_id`) USING BTREE,
  INDEX `idx_training_task_id`(`training_task_id`) USING BTREE,
  INDEX `idx_status`(`status`) USING BTREE,
  INDEX `idx_create_time`(`create_time`) USING BTREE,
  CONSTRAINT `fk_trained_model_original` FOREIGN KEY (`original_model_id`) REFERENCES `dict_model` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `fk_trained_model_task` FOREIGN KEY (`training_task_id`) REFERENCES `training_task` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 83 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '训练后模型表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of trained_model
-- ----------------------------
INSERT INTO `trained_model` VALUES (26, 'HAN_Model_398f907c-14ab-4605-a6d8-b54bb6d12659_epochs800_lr0.001_20250710_175338', 2, 'HAN Model', 57, 'E:\\projects\\chain\\models-storage\\HAN_Model_398f907c-14ab-4605-a6d8-b54bb6d12659_epochs800_lr0.001_20250710_175338', '', 800, 0.00100000, 800, NULL, NULL, '电子信息_2023Q2', 'Adam', 'DELETED', NULL, '2025-07-10 17:54:26', '2025-07-10 17:54:26');
INSERT INTO `trained_model` VALUES (27, 'HierTransferGNN_Model_8b29f586-d9ec-47f1-8b22-ffe14ce03990_epochs400_lr0.001_20250710_210729', 3, 'HierTransferGNN Model', 62, 'E:\\projects\\chain\\models-storage\\HierTransferGNN_Model_8b29f586-d9ec-47f1-8b22-ffe14ce03990_epochs400_lr0.001_20250710_210729', '', 400, 0.00100000, 400, NULL, NULL, '电子信息_2024Q2', 'Adam', 'DELETED', NULL, '2025-07-10 21:07:32', '2025-07-10 21:07:32');
INSERT INTO `trained_model` VALUES (28, 'HierTransferGNN_Model_8209400e-2927-4ac7-8b89-d4d97890f41f_epochs400_lr0.001_20250710_211236', 3, 'HierTransferGNN Model', 63, 'E:\\projects\\chain\\models-storage\\HierTransferGNN_Model_8209400e-2927-4ac7-8b89-d4d97890f41f_epochs400_lr0.001_20250710_211236', '', 400, 0.00100000, 400, NULL, NULL, '电子信息_2024Q1', 'Adam', 'DELETED', NULL, '2025-07-10 21:12:38', '2025-07-10 21:12:38');
INSERT INTO `trained_model` VALUES (29, 'HierTransferGNN_Model_eef9ebfa-ff14-4038-b545-f9373ddfeb19_epochs400_lr0.001_20250710_211835', 3, 'HierTransferGNN Model', 64, 'E:\\projects\\chain\\models-storage\\HierTransferGNN_Model_eef9ebfa-ff14-4038-b545-f9373ddfeb19_epochs400_lr0.001_20250710_211835', '', 400, 0.00100000, 400, NULL, NULL, '电子信息_2023Q4', 'Adam', 'DELETED', NULL, '2025-07-10 21:18:37', '2025-07-10 21:18:37');
INSERT INTO `trained_model` VALUES (30, 'HierTransferGNN_Model_8209400e-2927-4ac7-8b89-d4d97890f41f_epochs400_lr0.001_20250725_165102', 3, 'HierTransferGNN Model', 65, 'E:\\projects\\chain\\models-storage\\HierTransferGNN_Model_8209400e-2927-4ac7-8b89-d4d97890f41f_epochs400_lr0.001_20250725_165102', '', 400, 0.00100000, 400, NULL, NULL, '电子信息_2024Q1', 'Adam', 'DELETED', NULL, '2025-07-25 16:51:07', '2025-07-25 16:51:07');
INSERT INTO `trained_model` VALUES (31, 'HierTransferGNN_Model_15a93ad6-3be8-41c4-848e-7db784406389_epochs200_lr0.001_20250725_165917', 3, 'HierTransferGNN Model', 66, 'E:\\projects\\chain\\models-storage\\HierTransferGNN_Model_15a93ad6-3be8-41c4-848e-7db784406389_epochs200_lr0.001_20250725_165917', '', 200, 0.00100000, 200, NULL, NULL, '集成电路_2024Q2', 'Adam', 'DELETED', NULL, '2025-07-25 16:59:20', '2025-07-25 16:59:20');
INSERT INTO `trained_model` VALUES (32, 'HAN_Model_8b29f586-d9ec-47f1-8b22-ffe14ce03990_epochs100_lr0.001_20250725_170554', 2, 'HAN Model', 69, 'E:\\projects\\chain\\models-storage\\HAN_Model_8b29f586-d9ec-47f1-8b22-ffe14ce03990_epochs100_lr0.001_20250725_170554', '', 100, 0.00100000, 100, NULL, NULL, '电子信息_2024Q2', 'Adam', 'DELETED', NULL, '2025-07-25 17:06:12', '2025-07-25 17:06:12');
INSERT INTO `trained_model` VALUES (33, 'HAN_Model_8b29f586-d9ec-47f1-8b22-ffe14ce03990_epochs100_lr0.001_20250725_171101', 2, 'HAN Model', 70, 'E:\\projects\\chain\\models-storage\\HAN_Model_8b29f586-d9ec-47f1-8b22-ffe14ce03990_epochs100_lr0.001_20250725_171101', '', 100, 0.00100000, 100, NULL, NULL, '电子信息_2024Q2', 'Adam', 'DELETED', NULL, '2025-07-25 17:11:17', '2025-07-25 17:11:17');
INSERT INTO `trained_model` VALUES (34, 'HAN_Model_15a93ad6-3be8-41c4-848e-7db784406389_epochs100_lr0.001_20250725_171636', 2, 'HAN Model', 71, 'E:\\projects\\chain\\models-storage\\HAN_Model_15a93ad6-3be8-41c4-848e-7db784406389_epochs100_lr0.001_20250725_171636', '', 100, 0.00100000, 100, NULL, NULL, '集成电路_2024Q2', 'Adam', 'DELETED', NULL, '2025-07-25 17:16:49', '2025-07-25 17:16:49');
INSERT INTO `trained_model` VALUES (35, 'HAN_Model_56ac110b-e054-4e6a-ba6c-0cdf404e7a16_epochs100_lr0.001_20250725_172212', 2, 'HAN Model', 72, 'E:\\projects\\chain\\models-storage\\HAN_Model_56ac110b-e054-4e6a-ba6c-0cdf404e7a16_epochs100_lr0.001_20250725_172212', '', 100, 0.00100000, 100, NULL, NULL, '集成电路_2024Q2', 'Adam', 'DELETED', NULL, '2025-07-25 17:22:26', '2025-07-25 17:22:26');
INSERT INTO `trained_model` VALUES (36, 'HAN_Model_f87a52fc-345e-4ada-97cc-5f1e45ec0427_epochs100_lr0.001_20250725_172601', 2, 'HAN Model', 73, 'E:\\projects\\chain\\models-storage\\HAN_Model_f87a52fc-345e-4ada-97cc-5f1e45ec0427_epochs100_lr0.001_20250725_172601', '', 100, 0.00100000, 100, NULL, NULL, '集成电路_2023Q4', 'Adam', 'DELETED', NULL, '2025-07-25 17:26:15', '2025-07-25 17:26:15');
INSERT INTO `trained_model` VALUES (37, 'HierTransferGNN_Model_f87a52fc-345e-4ada-97cc-5f1e45ec0427_epochs100_lr0.001_20250725_172708', 3, 'HierTransferGNN Model', 74, 'E:\\projects\\chain\\models-storage\\HierTransferGNN_Model_f87a52fc-345e-4ada-97cc-5f1e45ec0427_epochs100_lr0.001_20250725_172708', '', 100, 0.00100000, 100, NULL, NULL, '集成电路_2023Q4', 'Adam', 'DELETED', NULL, '2025-07-25 17:27:12', '2025-07-25 17:27:12');
INSERT INTO `trained_model` VALUES (38, 'HAN_Model_f87a52fc-345e-4ada-97cc-5f1e45ec0427_epochs100_lr0.001_20250725_175835', 2, 'HAN Model', 79, 'E:\\projects\\chain\\models-storage\\HAN_Model_f87a52fc-345e-4ada-97cc-5f1e45ec0427_epochs100_lr0.001_20250725_175835', '', 100, 0.00100000, 100, NULL, NULL, '集成电路_2023Q4', 'Adam', 'DELETED', NULL, '2025-07-25 17:58:51', '2025-07-25 17:58:51');
INSERT INTO `trained_model` VALUES (39, 'HierTransferGNN_Model_f87a52fc-345e-4ada-97cc-5f1e45ec0427_epochs100_lr0.001_20250725_180229', 3, 'HierTransferGNN Model', 81, 'E:\\projects\\chain\\models-storage\\HierTransferGNN_Model_f87a52fc-345e-4ada-97cc-5f1e45ec0427_epochs100_lr0.001_20250725_180229', '', 100, 0.00100000, 100, NULL, NULL, '集成电路_2023Q4', 'Adam', 'DELETED', NULL, '2025-07-25 18:02:33', '2025-07-25 18:02:33');
INSERT INTO `trained_model` VALUES (40, 'HAN_Model_f87a52fc-345e-4ada-97cc-5f1e45ec0427_epochs100_lr0.001_20250725_180703', 2, 'HAN Model', 83, 'E:\\projects\\chain\\models-storage\\HAN_Model_f87a52fc-345e-4ada-97cc-5f1e45ec0427_epochs100_lr0.001_20250725_180703', '', 100, 0.00100000, 100, NULL, NULL, '集成电路_2023Q4', 'Adam', 'DELETED', NULL, '2025-07-25 18:07:20', '2025-07-25 18:07:20');
INSERT INTO `trained_model` VALUES (41, 'HierTransferGNN_Model_f87a52fc-345e-4ada-97cc-5f1e45ec0427_epochs100_lr0.001_20250725_180743', 3, 'HierTransferGNN Model', 82, 'E:\\projects\\chain\\models-storage\\HierTransferGNN_Model_f87a52fc-345e-4ada-97cc-5f1e45ec0427_epochs100_lr0.001_20250725_180743', '', 100, 0.00100000, 100, NULL, NULL, '集成电路_2023Q4', 'Adam', 'DELETED', NULL, '2025-07-25 18:07:46', '2025-07-25 18:07:46');
INSERT INTO `trained_model` VALUES (42, 'HierTransferGNN_Model_f87a52fc-345e-4ada-97cc-5f1e45ec0427_epochs100_lr0.001_20250725_182503', 3, 'HierTransferGNN Model', 86, 'E:\\projects\\chain\\models-storage\\HierTransferGNN_Model_f87a52fc-345e-4ada-97cc-5f1e45ec0427_epochs100_lr0.001_20250725_182503', '', 100, 0.00100000, 100, NULL, NULL, '集成电路_2023Q4', 'Adam', 'DELETED', NULL, '2025-07-25 18:25:06', '2025-07-25 18:25:06');
INSERT INTO `trained_model` VALUES (43, 'HAN_Model_8209400e-2927-4ac7-8b89-d4d97890f41f_epochs100_lr0.001_20250725_182804', 2, 'HAN Model', 87, 'E:\\projects\\chain\\models-storage\\HAN_Model_8209400e-2927-4ac7-8b89-d4d97890f41f_epochs100_lr0.001_20250725_182804', '', 100, 0.00100000, 100, NULL, NULL, '电子信息_2024Q1', 'Adam', 'DELETED', NULL, '2025-07-25 18:28:13', '2025-07-25 18:28:13');
INSERT INTO `trained_model` VALUES (44, 'HierTransferGNN_Model_56ac110b-e054-4e6a-ba6c-0cdf404e7a16_epochs20_lr0.001_20250725_182842', 3, 'HierTransferGNN Model', 88, 'E:\\projects\\chain\\models-storage\\HierTransferGNN_Model_56ac110b-e054-4e6a-ba6c-0cdf404e7a16_epochs20_lr0.001_20250725_182842', '', 20, 0.00100000, 20, NULL, NULL, '集成电路_2024Q2', 'Adam', 'DELETED', NULL, '2025-07-25 18:28:44', '2025-07-25 18:28:44');
INSERT INTO `trained_model` VALUES (45, 'HAN_Model_2f9f5fe8-60eb-4b4c-8a62-0f36a9e7779d_epochs100_lr0.001_20250725_183101', 2, 'HAN Model', 89, 'E:\\projects\\chain\\models-storage\\HAN_Model_2f9f5fe8-60eb-4b4c-8a62-0f36a9e7779d_epochs100_lr0.001_20250725_183101', '', 100, 0.00100000, 100, NULL, NULL, '集成电路_2022Q4', 'Adam', 'DELETED', NULL, '2025-07-25 18:31:15', '2025-07-25 18:31:15');
INSERT INTO `trained_model` VALUES (46, 'HierTransferGNN_Model_2f9f5fe8-60eb-4b4c-8a62-0f36a9e7779d_epochs50_lr0.001_20250725_183157', 3, 'HierTransferGNN Model', 90, 'E:\\projects\\chain\\models-storage\\HierTransferGNN_Model_2f9f5fe8-60eb-4b4c-8a62-0f36a9e7779d_epochs50_lr0.001_20250725_183157', '', 50, 0.00100000, 50, NULL, NULL, '集成电路_2022Q4', 'Adam', 'DELETED', NULL, '2025-07-25 18:32:00', '2025-07-25 18:32:00');
INSERT INTO `trained_model` VALUES (47, 'HAN_Model_f3541de5-4a71-4d39-b254-01762d12b7c3_epochs100_lr0.001_20250725_183509', 2, 'HAN Model', 91, 'E:\\projects\\chain\\models-storage\\HAN_Model_f3541de5-4a71-4d39-b254-01762d12b7c3_epochs100_lr0.001_20250725_183509', '', 100, 0.00100000, 100, NULL, NULL, '集成电路_2024Q2', 'Adam', 'DELETED', NULL, '2025-07-25 18:35:16', '2025-07-25 18:35:16');
INSERT INTO `trained_model` VALUES (48, 'HierTransferGNN_Model_f3541de5-4a71-4d39-b254-01762d12b7c3_epochs50_lr0.001_20250725_183544', 3, 'HierTransferGNN Model', 92, 'E:\\projects\\chain\\models-storage\\HierTransferGNN_Model_f3541de5-4a71-4d39-b254-01762d12b7c3_epochs50_lr0.001_20250725_183544', '', 50, 0.00100000, 50, NULL, NULL, '集成电路_2024Q2', 'Adam', 'DELETED', NULL, '2025-07-25 18:35:46', '2025-07-25 18:35:46');
INSERT INTO `trained_model` VALUES (49, 'HAN_Model_f3541de5-4a71-4d39-b254-01762d12b7c3_epochs100_lr0.001_20250725_184147', 2, 'HAN Model', 93, 'E:\\projects\\chain\\models-storage\\HAN_Model_f3541de5-4a71-4d39-b254-01762d12b7c3_epochs100_lr0.001_20250725_184147', '', 100, 0.00100000, 100, NULL, NULL, '集成电路_2024Q2', 'Adam', 'DELETED', NULL, '2025-07-25 18:41:54', '2025-07-25 18:41:54');
INSERT INTO `trained_model` VALUES (50, 'HierTransferGNN_Model_f3541de5-4a71-4d39-b254-01762d12b7c3_epochs50_lr0.001_20250725_184226', 3, 'HierTransferGNN Model', 94, 'E:\\projects\\chain\\models-storage\\HierTransferGNN_Model_f3541de5-4a71-4d39-b254-01762d12b7c3_epochs50_lr0.001_20250725_184226', '', 50, 0.00100000, 50, NULL, NULL, '集成电路_2024Q2', 'Adam', 'DELETED', NULL, '2025-07-25 18:42:28', '2025-07-25 18:42:28');
INSERT INTO `trained_model` VALUES (51, 'HAN_Model_f3541de5-4a71-4d39-b254-01762d12b7c3_epochs100_lr0.001_20250725_212146', 2, 'HAN Model', 95, 'E:\\projects\\chain\\models-storage\\HAN_Model_f3541de5-4a71-4d39-b254-01762d12b7c3_epochs100_lr0.001_20250725_212146', '', 100, 0.00100000, 100, NULL, NULL, '集成电路_2024Q2', 'Adam', 'DELETED', NULL, '2025-07-25 21:21:54', '2025-07-25 21:21:54');
INSERT INTO `trained_model` VALUES (52, 'HAN_Model_f3541de5-4a71-4d39-b254-01762d12b7c3_epochs100_lr0.001_20250725_212355', 2, 'HAN Model', 96, 'E:\\projects\\chain\\models-storage\\HAN_Model_f3541de5-4a71-4d39-b254-01762d12b7c3_epochs100_lr0.001_20250725_212355', '', 100, 0.00100000, 100, NULL, NULL, '集成电路_2024Q2', 'Adam', 'DELETED', NULL, '2025-07-25 21:24:03', '2025-07-25 21:24:03');
INSERT INTO `trained_model` VALUES (53, 'HAN_Model_f3541de5-4a71-4d39-b254-01762d12b7c3_epochs100_lr0.001_20250725_213053', 2, 'HAN Model', 97, 'E:\\projects\\chain\\models-storage\\HAN_Model_f3541de5-4a71-4d39-b254-01762d12b7c3_epochs100_lr0.001_20250725_213053', '', 100, 0.00100000, 100, NULL, NULL, '集成电路_2024Q2', 'Adam', 'DELETED', NULL, '2025-07-25 21:31:01', '2025-07-25 21:31:01');
INSERT INTO `trained_model` VALUES (54, 'HAN_Model_f3541de5-4a71-4d39-b254-01762d12b7c3_epochs100_lr0.001_20250725_214052', 2, 'HAN Model', 98, 'E:\\projects\\chain\\models-storage\\HAN_Model_f3541de5-4a71-4d39-b254-01762d12b7c3_epochs100_lr0.001_20250725_214052', '', 100, 0.00100000, 100, NULL, NULL, '集成电路_2024Q2', 'Adam', 'DELETED', NULL, '2025-07-25 21:41:00', '2025-07-25 21:41:00');
INSERT INTO `trained_model` VALUES (55, 'HAN_Model_f3541de5-4a71-4d39-b254-01762d12b7c3_epochs100_lr0.001_20250725_214400', 2, 'HAN Model', 99, 'E:\\projects\\chain\\models-storage\\HAN_Model_f3541de5-4a71-4d39-b254-01762d12b7c3_epochs100_lr0.001_20250725_214400', '', 100, 0.00100000, 100, NULL, NULL, '集成电路_2024Q2', 'Adam', 'DELETED', NULL, '2025-07-25 21:44:07', '2025-07-25 21:44:07');
INSERT INTO `trained_model` VALUES (56, 'HierTransferGNN_Model_8209400e-2927-4ac7-8b89-d4d97890f41f_epochs50_lr0.001_20250725_214644', 3, 'HierTransferGNN Model', 100, 'E:\\projects\\chain\\models-storage\\HierTransferGNN_Model_8209400e-2927-4ac7-8b89-d4d97890f41f_epochs50_lr0.001_20250725_214644', '', 50, 0.00100000, 50, NULL, NULL, '电子信息_2024Q1', 'Adam', 'DELETED', NULL, '2025-07-25 21:46:46', '2025-07-25 21:46:46');
INSERT INTO `trained_model` VALUES (57, 'HAN_Model_eef9ebfa-ff14-4038-b545-f9373ddfeb19_epochs100_lr0.001_20250725_215426', 2, 'HAN Model', 101, 'E:\\projects\\chain\\models-storage\\HAN_Model_eef9ebfa-ff14-4038-b545-f9373ddfeb19_epochs100_lr0.001_20250725_215426', '', 100, 0.00100000, 100, NULL, NULL, '电子信息_2023Q4', 'Adam', 'DELETED', NULL, '2025-07-25 21:54:35', '2025-07-25 21:54:35');
INSERT INTO `trained_model` VALUES (58, 'HierTransferGNN_Model_f3541de5-4a71-4d39-b254-01762d12b7c3_epochs40_lr0.001_20250725_215625', 3, 'HierTransferGNN Model', 102, 'E:\\projects\\chain\\models-storage\\HierTransferGNN_Model_f3541de5-4a71-4d39-b254-01762d12b7c3_epochs40_lr0.001_20250725_215625', '', 40, 0.00100000, 40, NULL, NULL, '集成电路_2024Q2', 'Adam', 'DELETED', NULL, '2025-07-25 21:56:27', '2025-07-25 21:56:27');
INSERT INTO `trained_model` VALUES (59, 'HAN_Model_8209400e-2927-4ac7-8b89-d4d97890f41f_epochs600_lr0.001_20250726_114611', 2, 'HAN Model', 103, 'E:\\projects\\chain\\models-storage\\HAN_Model_8209400e-2927-4ac7-8b89-d4d97890f41f_epochs600_lr0.001_20250726_114611', '', 600, 0.00100000, 600, NULL, NULL, '电子信息_2024Q1', 'Adam', 'DELETED', NULL, '2025-07-26 11:46:47', '2025-07-26 11:46:47');
INSERT INTO `trained_model` VALUES (60, 'HierTransferGNN_Model_8209400e-2927-4ac7-8b89-d4d97890f41f_epochs600_lr0.001_20250726_114840', 3, 'HierTransferGNN Model', 104, 'E:\\projects\\chain\\models-storage\\HierTransferGNN_Model_8209400e-2927-4ac7-8b89-d4d97890f41f_epochs600_lr0.001_20250726_114840', '', 600, 0.00100000, 600, NULL, NULL, '电子信息_2024Q1', 'Adam', 'DELETED', NULL, '2025-07-26 11:48:42', '2025-07-26 11:48:42');
INSERT INTO `trained_model` VALUES (61, 'HAN_Model_f3541de5-4a71-4d39-b254-01762d12b7c3_epochs100_lr0.001_20251030_170325', 2, 'HAN Model', 105, 'E:\\projects\\chain\\models-storage\\HAN_Model_f3541de5-4a71-4d39-b254-01762d12b7c3_epochs100_lr0.001_20251030_170325', '', 100, 0.00100000, 100, NULL, NULL, '集成电路_2024Q2', 'Adam', 'DELETED', NULL, '2025-10-30 17:03:33', '2025-10-30 17:03:33');
INSERT INTO `trained_model` VALUES (62, 'HierTransferGNN_Model_8b29f586-d9ec-47f1-8b22-ffe14ce03990_epochs800_lr0.001_20251031_141653', 3, 'HierTransferGNN Model', 106, 'E:\\projects\\chain\\models-storage\\HierTransferGNN_Model_8b29f586-d9ec-47f1-8b22-ffe14ce03990_epochs800_lr0.001_20251031_141653', '', 800, 0.00100000, 800, NULL, NULL, '电子信息_2024Q2', 'Adam', 'DELETED', NULL, '2025-10-31 14:16:57', '2025-10-31 14:16:57');
INSERT INTO `trained_model` VALUES (63, 'HAN_Model_f3541de5-4a71-4d39-b254-01762d12b7c3_epochs600_lr0.001_20251031_141729', 2, 'HAN Model', 107, 'E:\\projects\\chain\\models-storage\\HAN_Model_f3541de5-4a71-4d39-b254-01762d12b7c3_epochs600_lr0.001_20251031_141729', '', 600, 0.00100000, 600, NULL, NULL, '集成电路_2024Q2', 'Adam', 'DELETED', NULL, '2025-10-31 14:17:58', '2025-10-31 14:17:58');
INSERT INTO `trained_model` VALUES (64, 'MetaPath2vec_集成电路_2024Q2_epochs200_lr0.001_20251031_151808', 4, 'MetaPath2vec', 111, 'E:\\projects\\chain\\models-storage\\MetaPath2vec_集成电路_2024Q2_epochs200_lr0.001_20251031_151808', 'stdout.txt', 200, 0.00100000, 200, NULL, NULL, '集成电路_2024Q2', 'Adam', 'DELETED', '评估结果:\r\n准确率: 818\r\nF1分数: 0.4944\r\nAUC值: 0.7563\r\n', '2025-10-31 15:18:09', '2025-10-31 15:18:09');
INSERT INTO `trained_model` VALUES (65, 'MetaPath2vec_集成电路_2024Q2_epochs200_lr0.001_20251031_154143', 4, 'MetaPath2vec', 112, 'E:\\projects\\chain\\models-storage\\MetaPath2vec_集成电路_2024Q2_epochs200_lr0.001_20251031_154143', 'stdout.txt', 200, 0.00100000, 200, NULL, NULL, '集成电路_2024Q2', 'Adam', 'DELETED', '评估结果:\r\n准确率: 818\r\nF1分数: 0.4800\r\nAUC值: 0.7598\r\n', '2025-10-31 15:41:44', '2025-10-31 15:41:44');
INSERT INTO `trained_model` VALUES (66, 'MetaPath2vec_集成电路_2024Q2_epochs200_lr0.001_20251031_160307', 4, 'MetaPath2vec', 113, 'E:\\projects\\chain\\models-storage\\MetaPath2vec_集成电路_2024Q2_epochs200_lr0.001_20251031_160307', 'stdout.txt', 200, 0.00100000, 200, NULL, NULL, '集成电路_2024Q2', 'Adam', 'DELETED', '评估结果:\r\n准确率: 818\r\nF1分数: 0.5000\r\nAUC值: 0.7560\r\n', '2025-10-31 16:03:07', '2025-10-31 16:03:07');
INSERT INTO `trained_model` VALUES (67, 'MetaPath2vec_集成电路_2024Q2_epochs200_lr0.001_20251031_161329', 4, 'MetaPath2vec', 114, 'E:\\projects\\chain\\models-storage\\MetaPath2vec_集成电路_2024Q2_epochs200_lr0.001_20251031_161329', 'stdout.txt', 200, 0.00100000, 200, NULL, NULL, '集成电路_2024Q2', 'Adam', 'DELETED', '评估结果:\r\n准确率: 818\r\nF1分数: 0.5109\r\nAUC值: 0.7475\r\n', '2025-10-31 16:13:30', '2025-10-31 16:13:30');
INSERT INTO `trained_model` VALUES (68, 'MetaPath2vec_集成电路_2024Q2_epochs200_lr0.001_20251031_163024', 4, 'MetaPath2vec', 115, 'E:\\projects\\chain\\models-storage\\MetaPath2vec_集成电路_2024Q2_epochs200_lr0.001_20251031_163024', 'stdout.txt', 200, 0.00100000, 200, NULL, NULL, '集成电路_2024Q2', 'Adam', 'DELETED', '评估结果:\r\n准确率: 818\r\nF1分数: 0.4971\r\nAUC值: 0.7635\r\n', '2025-10-31 16:30:24', '2025-10-31 16:30:24');
INSERT INTO `trained_model` VALUES (69, 'MetaPath2vec_集成电路_2024Q2_epochs600_lr0.001_20251031_164612', 4, 'MetaPath2vec', 116, 'E:\\projects\\chain\\models-storage\\MetaPath2vec_集成电路_2024Q2_epochs600_lr0.001_20251031_164612', 'stdout.txt', 600, 0.00100000, 600, NULL, NULL, '集成电路_2024Q2', 'Adam', 'DELETED', '评估结果:\r\n准确率: 818\r\nF1分数: 0.4901\r\nAUC值: 0.7518\r\n', '2025-10-31 16:46:13', '2025-10-31 16:46:13');
INSERT INTO `trained_model` VALUES (70, 'MetaPath2vec_集成电路_2024Q2_epochs200_lr0.001_20251101_192015', 4, 'MetaPath2vec', 117, 'E:\\projects\\chain\\models-storage\\MetaPath2vec_集成电路_2024Q2_epochs200_lr0.001_20251101_192015', 'stdout.txt', 200, 0.00100000, 200, NULL, NULL, '集成电路_2024Q2', 'Adam', 'DELETED', '评估结果:\r\n准确率: 818\r\nF1分数: 0.5042\r\nAUC值: 0.7690\r\n', '2025-11-01 19:20:16', '2025-11-01 19:20:16');
INSERT INTO `trained_model` VALUES (71, 'MetaPath2vec_集成电路_2024Q2_epochs200_lr0.001_20251101_192620', 4, 'MetaPath2vec', 118, 'E:\\projects\\chain\\models-storage\\MetaPath2vec_集成电路_2024Q2_epochs200_lr0.001_20251101_192620', 'stdout.txt', 200, 0.00100000, 200, NULL, NULL, '集成电路_2024Q2', 'Adam', 'DELETED', '评估结果:\r\n准确率: 818\r\nF1分数: 0.5307\r\nAUC值: 0.7783\r\n', '2025-11-01 19:26:21', '2025-11-01 19:26:21');
INSERT INTO `trained_model` VALUES (72, 'MetaPath2vec_集成电路_2022Q2_epochs200_lr0.001_20251103_102122', 4, 'MetaPath2vec', 119, 'E:\\projects\\chain\\models-storage\\MetaPath2vec_集成电路_2022Q2_epochs200_lr0.001_20251103_102122', 'stdout.txt', 200, 0.00100000, 200, NULL, NULL, '集成电路_2022Q2', 'Adam', 'DELETED', '评估结果:\r\n准确率: 818\r\nF1分数: 0.5312\r\nAUC值: 0.7489\r\n', '2025-11-03 10:21:22', '2025-11-03 10:21:22');
INSERT INTO `trained_model` VALUES (73, 'HierTransferGNN_Model_5187a343-8967-4f3f-8b2b-42a4ccc13bdc_epochs600_lr0.001_20251103_102311', 3, 'HierTransferGNN Model', 120, 'E:\\projects\\chain\\models-storage\\HierTransferGNN_Model_5187a343-8967-4f3f-8b2b-42a4ccc13bdc_epochs600_lr0.001_20251103_102311', '', 600, 0.00100000, 600, NULL, NULL, '集成电路_2022Q2', 'Adam', 'DELETED', NULL, '2025-11-03 10:23:14', '2025-11-03 10:23:14');
INSERT INTO `trained_model` VALUES (74, 'HierTransferGNN_Model_45c8856a-da49-4cdc-a6ac-e15a09bdb526_epochs200_lr0.001_20251119_190814', 3, 'HierTransferGNN Model', 121, 'E:\\projects\\chain\\models-storage\\HierTransferGNN_Model_45c8856a-da49-4cdc-a6ac-e15a09bdb526_epochs200_lr0.001_20251119_190814', '', 200, 0.00100000, 200, NULL, NULL, '集成电路_2023Q2', 'Adam', 'DELETED', NULL, '2025-11-19 19:08:17', '2025-11-19 19:08:17');
INSERT INTO `trained_model` VALUES (75, '基于链接预测的产业链完整性评估模型_集成电路_2023Q2_epochs200_lr0.001_20251119_191617', 4, 'MetaPath2vec', 122, 'E:\\projects\\chain\\models-storage\\MetaPath2vec_集成电路_2023Q2_epochs200_lr0.001_20251119_191617', 'stdout.txt', 200, 0.00100000, 200, NULL, NULL, '集成电路_2023Q2', 'Adam', 'ACTIVE', '评估结果:\r\nF1分数: 0.5124\r\nAUC值: 0.7554\r\n', '2025-11-19 19:16:17', '2025-11-19 19:16:17');
INSERT INTO `trained_model` VALUES (76, '基于分层知识可转移图神经网络的风险评估模型_45c8856a-da49-4cdc-a6ac-e15a09bdb526_epochs200_lr0.001_20251119_192122', 3, 'HierTransferGNN Model', 123, 'E:\\projects\\chain\\models-storage\\HierTransferGNN_Model_45c8856a-da49-4cdc-a6ac-e15a09bdb526_epochs200_lr0.001_20251119_192122', '', 200, 0.00100000, 200, NULL, NULL, '集成电路_2023Q2', 'Adam', 'ACTIVE', NULL, '2025-11-19 19:21:25', '2025-11-19 19:21:25');
INSERT INTO `trained_model` VALUES (77, '结合层次图神经网络和LSTM的产业链风险预警模型_eef9ebfa-ff14-4038-b545-f9373ddfeb19_epochs800_lr0.001_20251119_192253', 2, 'HAN Model', 124, 'E:\\projects\\chain\\models-storage\\HAN_Model_eef9ebfa-ff14-4038-b545-f9373ddfeb19_epochs800_lr0.001_20251119_192253', '', 800, 0.00100000, 800, NULL, NULL, '电子信息_2023Q4', 'Adam', 'ACTIVE', NULL, '2025-11-19 19:23:40', '2025-11-19 19:23:40');
INSERT INTO `trained_model` VALUES (78, '基于链接预测的产业链完整性评估模型_集成电路_2022Q2_epochs600_lr0.001_20251119_203249', 4, 'MetaPath2vec', 125, 'E:\\projects\\chain\\models-storage\\MetaPath2vec_集成电路_2022Q2_epochs600_lr0.001_20251119_203249', 'stdout.txt', 600, 0.00100000, 600, NULL, NULL, '集成电路_2022Q2', 'Adam', 'ACTIVE', '评估结果:\r\nF1分数: 0.4680\r\nAUC值: 0.7487\r\n', '2025-11-19 20:32:50', '2025-11-19 20:32:50');
INSERT INTO `trained_model` VALUES (79, '基于链接预测的产业链完整性评估模型_集成电路_2023Q2_epochs200_lr0.001_20251120_142544', 4, 'MetaPath2vec', 126, 'E:\\projects\\chain\\models-storage\\MetaPath2vec_集成电路_2023Q2_epochs200_lr0.001_20251120_142544', 'stdout.txt', 200, 0.00100000, 200, NULL, NULL, '集成电路_2023Q2', 'Adam', 'ACTIVE', '评估结果:\r\n准确率: 0.7521\r\nF1分数: 0.5340\r\nAUC值: 0.7419\r\n', '2025-11-20 14:25:44', '2025-11-20 14:25:44');
INSERT INTO `trained_model` VALUES (80, '基于分层知识可转移图神经网络的风险评估模型_8209400e-2927-4ac7-8b89-d4d97890f41f_epochs600_lr0.001_20251120_142730', 3, 'HierTransferGNN Model', 127, 'E:\\projects\\chain\\models-storage\\HierTransferGNN_Model_8209400e-2927-4ac7-8b89-d4d97890f41f_epochs600_lr0.001_20251120_142730', '', 600, 0.00100000, 600, NULL, NULL, '电子信息_2024Q1', 'Adam', 'ACTIVE', NULL, '2025-11-20 14:27:33', '2025-11-20 14:27:33');
INSERT INTO `trained_model` VALUES (81, '结合层次图神经网络和LSTM的产业链风险预警模型_8209400e-2927-4ac7-8b89-d4d97890f41f_epochs800_lr0.001_20251120_142823', 2, 'HAN Model', 128, 'E:\\projects\\chain\\models-storage\\HAN_Model_8209400e-2927-4ac7-8b89-d4d97890f41f_epochs800_lr0.001_20251120_142823', '', 800, 0.00100000, 800, NULL, NULL, '电子信息_2024Q1', 'Adam', 'ACTIVE', NULL, '2025-11-20 14:29:10', '2025-11-20 14:29:10');
INSERT INTO `trained_model` VALUES (82, '基于链接预测的产业链完整性评估模型_电子信息_2024Q2_epochs200_lr0.001_20251120_144509', 4, 'MetaPath2vec', 129, 'E:\\projects\\chain\\models-storage\\MetaPath2vec_电子信息_2024Q2_epochs200_lr0.001_20251120_144509', 'stdout.txt', 200, 0.00100000, 200, NULL, NULL, '电子信息_2024Q2', 'Adam', 'ACTIVE', '评估结果:\r\n准确率: 0.7577\r\nF1分数: 0.5220\r\nAUC值: 0.7661\r\n', '2025-11-20 14:45:09', '2025-11-20 14:45:09');

-- ----------------------------
-- Table structure for training_task
-- ----------------------------
DROP TABLE IF EXISTS `training_task`;
CREATE TABLE `training_task`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `task_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '任务名称',
  `dataset_id` bigint(20) NOT NULL COMMENT '数据集ID',
  `dataset_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '数据集名称',
  `data_period` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '数据期间',
  `task_type_id` bigint(20) NOT NULL COMMENT '任务类型ID',
  `task_type_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '任务类型名称',
  `model_id` bigint(20) NOT NULL COMMENT '模型ID',
  `model_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '模型名称',
  `optimizer_id` bigint(20) NOT NULL COMMENT '优化器ID',
  `optimizer_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '优化器名称',
  `learning_rate` decimal(10, 8) NULL DEFAULT NULL COMMENT '学习率',
  `total_epochs` int(11) NOT NULL COMMENT '总训练轮次',
  `current_epoch` int(11) NULL DEFAULT 0 COMMENT '当前训练轮次',
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT 'PENDING' COMMENT '训练状态: PENDING-待启动, RUNNING-训练中, COMPLETED-已完成, TERMINATED-已终止, FAILED-失败',
  `start_time` datetime NULL DEFAULT NULL COMMENT '训练开始时间',
  `end_time` datetime NULL DEFAULT NULL COMMENT '训练结束时间',
  `process_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '训练进程ID',
  `error_message` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '错误信息',
  `training_params` json NULL COMMENT '训练参数(JSON格式)',
  `trained_model_id` bigint(20) NULL DEFAULT NULL COMMENT '训练后模型ID',
  `trained_model_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '训练后模型名称(模型名+日志文件名)',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_status`(`status`) USING BTREE,
  INDEX `idx_start_time`(`start_time`) USING BTREE,
  INDEX `idx_dataset_id`(`dataset_id`) USING BTREE,
  INDEX `idx_model_id`(`model_id`) USING BTREE,
  INDEX `fk_training_task_task_type`(`task_type_id`) USING BTREE,
  INDEX `fk_training_task_optimizer`(`optimizer_id`) USING BTREE,
  CONSTRAINT `fk_training_task_dataset` FOREIGN KEY (`dataset_id`) REFERENCES `dataset` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `fk_training_task_model` FOREIGN KEY (`model_id`) REFERENCES `dict_model` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `fk_training_task_optimizer` FOREIGN KEY (`optimizer_id`) REFERENCES `dict_optimizer` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `fk_training_task_task_type` FOREIGN KEY (`task_type_id`) REFERENCES `dict_task_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 130 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '训练任务表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of training_task
-- ----------------------------
INSERT INTO `training_task` VALUES (51, 'HAN Model_电子信息_2024Q2_800_Adam_0.0010', 55, '电子信息_2024Q2', '2024Q2', 4, '产业链风险预警', 2, 'HAN Model', 2, 'Adam', 0.00100000, 800, 0, 'FAILED', '2025-07-10 17:17:13', '2025-07-10 17:17:13', NULL, 'String index out of range: -1', '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', NULL, NULL, '2025-07-10 17:17:13', '2025-10-31 12:49:29');
INSERT INTO `training_task` VALUES (52, 'HAN Model_电子信息_2024Q2_800_Adam_0.0010', 55, '电子信息_2024Q2', '2024Q2', 4, '产业链风险预警', 2, 'HAN Model', 2, 'Adam', 0.00100000, 800, 0, 'FAILED', '2025-07-10 17:20:08', '2025-07-10 17:20:08', NULL, '训练进程异常退出，退出码: 1', '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', NULL, NULL, '2025-07-10 17:20:08', '2025-10-31 12:49:29');
INSERT INTO `training_task` VALUES (53, 'HAN Model_电子信息_2024Q2_800_Adam_0.0010', 55, '电子信息_2024Q2', '2024Q2', 4, '产业链风险预警', 2, 'HAN Model', 2, 'Adam', 0.00100000, 800, 800, 'COMPLETED', '2025-07-10 17:25:08', '2025-07-10 17:25:57', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', NULL, NULL, '2025-07-10 17:25:08', '2025-10-31 12:49:29');
INSERT INTO `training_task` VALUES (54, 'HAN Model_电子信息_2023Q4_800_Adam_0.0010', 53, '电子信息_2023Q4', '2023Q4', 4, '产业链风险预警', 2, 'HAN Model', 2, 'Adam', 0.00100000, 800, 800, 'COMPLETED', '2025-07-10 17:33:30', '2025-07-10 17:34:21', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', NULL, NULL, '2025-07-10 17:33:30', '2025-10-31 12:49:29');
INSERT INTO `training_task` VALUES (55, 'HAN Model_电子信息_2024Q1_800_Adam_0.0010', 54, '电子信息_2024Q1', '2024Q1', 4, '产业链风险预警', 2, 'HAN Model', 2, 'Adam', 0.00100000, 800, 800, 'COMPLETED', '2025-07-10 17:35:04', '2025-07-10 17:35:53', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', NULL, NULL, '2025-07-10 17:35:04', '2025-10-31 12:49:29');
INSERT INTO `training_task` VALUES (56, 'HAN Model_电子信息_2024Q1_800_Adam_0.0010', 54, '电子信息_2024Q1', '2024Q1', 4, '产业链风险预警', 2, 'HAN Model', 2, 'Adam', 0.00100000, 800, 800, 'COMPLETED', '2025-07-10 17:50:21', '2025-07-10 17:51:12', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', NULL, NULL, '2025-07-10 17:50:21', '2025-10-31 12:49:29');
INSERT INTO `training_task` VALUES (57, 'HAN Model_电子信息_2023Q2_800_Adam_0.0010', 52, '电子信息_2023Q2', '2023Q2', 4, '产业链风险预警', 2, 'HAN Model', 2, 'Adam', 0.00100000, 800, 800, 'COMPLETED', '2025-07-10 17:53:35', '2025-07-10 17:54:26', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', 26, 'HAN_Model_398f907c-14ab-4605-a6d8-b54bb6d12659_epochs800_lr0.001_20250710_175338', '2025-07-10 17:53:35', '2025-10-31 12:49:29');
INSERT INTO `training_task` VALUES (58, 'HierTransferGNN Model_电子信息_2024Q1_400_Adam_0.0010', 54, '电子信息_2024Q1', '2024Q1', 2, '训练任务', 3, 'HierTransferGNN Model', 2, 'Adam', 0.00100000, 400, 0, 'FAILED', '2025-07-10 20:32:52', '2025-07-10 20:32:52', NULL, '训练进程异常退出，退出码: 2', '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', NULL, NULL, '2025-07-10 20:32:51', '2025-07-10 20:32:51');
INSERT INTO `training_task` VALUES (59, 'HierTransferGNN Model_电子信息_2024Q2_400_Adam_0.0010', 55, '电子信息_2024Q2', '2024Q2', 2, '训练任务', 3, 'HierTransferGNN Model', 2, 'Adam', 0.00100000, 400, 0, 'FAILED', '2025-07-10 20:36:03', '2025-07-10 20:36:30', NULL, '训练进程异常退出，退出码: 1', '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', NULL, NULL, '2025-07-10 20:36:03', '2025-07-10 20:36:03');
INSERT INTO `training_task` VALUES (60, 'HierTransferGNN Model_电子信息_2023Q2_400_Adam_0.0010', 52, '电子信息_2023Q2', '2023Q2', 2, '训练任务', 3, 'HierTransferGNN Model', 2, 'Adam', 0.00100000, 400, 0, 'FAILED', '2025-07-10 20:50:00', '2025-07-10 20:50:28', NULL, '训练进程异常退出，退出码: 1', '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', NULL, NULL, '2025-07-10 20:50:00', '2025-07-10 20:50:00');
INSERT INTO `training_task` VALUES (61, 'HierTransferGNN Model_电子信息_2024Q2_400_Adam_0.0010', 55, '电子信息_2024Q2', '2024Q2', 2, '训练任务', 3, 'HierTransferGNN Model', 2, 'Adam', 0.00100000, 400, 400, 'COMPLETED', '2025-07-10 20:57:07', '2025-07-10 20:58:33', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', NULL, NULL, '2025-07-10 20:57:07', '2025-07-10 20:58:33');
INSERT INTO `training_task` VALUES (62, 'HierTransferGNN Model_电子信息_2024Q2_400_Adam_0.0010', 55, '电子信息_2024Q2', '2024Q2', 2, '训练任务', 3, 'HierTransferGNN Model', 2, 'Adam', 0.00100000, 400, 400, 'COMPLETED', '2025-07-10 21:06:03', '2025-07-10 21:07:32', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', 27, 'HierTransferGNN_Model_8b29f586-d9ec-47f1-8b22-ffe14ce03990_epochs400_lr0.001_20250710_210729', '2025-07-10 21:06:03', '2025-07-10 21:06:03');
INSERT INTO `training_task` VALUES (63, 'HierTransferGNN Model_电子信息_2024Q1_400_Adam_0.0010', 54, '电子信息_2024Q1', '2024Q1', 2, '训练任务', 3, 'HierTransferGNN Model', 2, 'Adam', 0.00100000, 400, 400, 'COMPLETED', '2025-07-10 21:11:18', '2025-07-10 21:12:38', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', 28, 'HierTransferGNN_Model_8209400e-2927-4ac7-8b89-d4d97890f41f_epochs400_lr0.001_20250710_211236', '2025-07-10 21:11:18', '2025-07-10 21:11:18');
INSERT INTO `training_task` VALUES (64, 'HierTransferGNN Model_电子信息_2023Q4_400_Adam_0.0010', 53, '电子信息_2023Q4', '2023Q4', 2, '训练任务', 3, 'HierTransferGNN Model', 2, 'Adam', 0.00100000, 400, 400, 'COMPLETED', '2025-07-10 21:17:04', '2025-07-10 21:18:37', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', 29, 'HierTransferGNN_Model_eef9ebfa-ff14-4038-b545-f9373ddfeb19_epochs400_lr0.001_20250710_211835', '2025-07-10 21:17:04', '2025-07-10 21:17:04');
INSERT INTO `training_task` VALUES (65, 'HierTransferGNN Model_电子信息_2024Q1_400_Adam_0.0010', 54, '电子信息_2024Q1', '2024Q1', 2, '训练任务', 3, 'HierTransferGNN Model', 2, 'Adam', 0.00100000, 400, 400, 'COMPLETED', '2025-07-25 16:48:34', '2025-07-25 16:51:07', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', 30, 'HierTransferGNN_Model_8209400e-2927-4ac7-8b89-d4d97890f41f_epochs400_lr0.001_20250725_165102', '2025-07-25 16:48:34', '2025-07-25 16:48:34');
INSERT INTO `training_task` VALUES (66, 'HierTransferGNN Model_集成电路_2024Q2_200_Adam_0.0010', 56, '集成电路_2024Q2', '2024Q2', 2, '训练任务', 3, 'HierTransferGNN Model', 2, 'Adam', 0.00100000, 200, 200, 'COMPLETED', '2025-07-25 16:57:58', '2025-07-25 16:59:20', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', 31, 'HierTransferGNN_Model_15a93ad6-3be8-41c4-848e-7db784406389_epochs200_lr0.001_20250725_165917', '2025-07-25 16:57:58', '2025-07-25 16:57:58');
INSERT INTO `training_task` VALUES (67, 'HAN Model_集成电路_2024Q2_100_Adam_0.0010', 56, '集成电路_2024Q2', '2024Q2', 4, '产业链风险预警', 2, 'HAN Model', 2, 'Adam', 0.00100000, 100, 0, 'FAILED', '2025-07-25 17:00:38', '2025-07-25 17:00:45', NULL, '训练进程异常退出，退出码: 1', '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', NULL, NULL, '2025-07-25 17:00:38', '2025-10-31 12:49:29');
INSERT INTO `training_task` VALUES (68, 'HAN Model_集成电路_2024Q2_100_Adam_0.0010', 56, '集成电路_2024Q2', '2024Q2', 4, '产业链风险预警', 2, 'HAN Model', 2, 'Adam', 0.00100000, 100, 0, 'FAILED', '2025-07-25 17:05:22', '2025-07-25 17:05:29', NULL, '训练进程异常退出，退出码: 1', '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', NULL, NULL, '2025-07-25 17:05:22', '2025-10-31 12:49:29');
INSERT INTO `training_task` VALUES (69, 'HAN Model_电子信息_2024Q2_100_Adam_0.0010', 55, '电子信息_2024Q2', '2024Q2', 4, '产业链风险预警', 2, 'HAN Model', 2, 'Adam', 0.00100000, 100, 100, 'COMPLETED', '2025-07-25 17:05:49', '2025-07-25 17:06:12', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', 32, 'HAN_Model_8b29f586-d9ec-47f1-8b22-ffe14ce03990_epochs100_lr0.001_20250725_170554', '2025-07-25 17:05:49', '2025-10-31 12:49:29');
INSERT INTO `training_task` VALUES (70, 'HAN Model_电子信息_2024Q2_100_Adam_0.0010', 55, '电子信息_2024Q2', '2024Q2', 4, '产业链风险预警', 2, 'HAN Model', 2, 'Adam', 0.00100000, 100, 100, 'COMPLETED', '2025-07-25 17:10:56', '2025-07-25 17:11:17', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', 33, 'HAN_Model_8b29f586-d9ec-47f1-8b22-ffe14ce03990_epochs100_lr0.001_20250725_171101', '2025-07-25 17:10:56', '2025-10-31 12:49:29');
INSERT INTO `training_task` VALUES (71, 'HAN Model_集成电路_2024Q2_100_Adam_0.0010', 56, '集成电路_2024Q2', '2024Q2', 4, '产业链风险预警', 2, 'HAN Model', 2, 'Adam', 0.00100000, 100, 100, 'COMPLETED', '2025-07-25 17:16:30', '2025-07-25 17:16:49', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', 34, 'HAN_Model_15a93ad6-3be8-41c4-848e-7db784406389_epochs100_lr0.001_20250725_171636', '2025-07-25 17:16:30', '2025-10-31 12:49:29');
INSERT INTO `training_task` VALUES (72, 'HAN Model_集成电路_2024Q2_100_Adam_0.0010', 57, '集成电路_2024Q2', '2024Q2', 4, '产业链风险预警', 2, 'HAN Model', 2, 'Adam', 0.00100000, 100, 100, 'COMPLETED', '2025-07-25 17:22:07', '2025-07-25 17:22:26', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', 35, 'HAN_Model_56ac110b-e054-4e6a-ba6c-0cdf404e7a16_epochs100_lr0.001_20250725_172212', '2025-07-25 17:22:07', '2025-10-31 12:49:29');
INSERT INTO `training_task` VALUES (73, 'HAN Model_集成电路_2023Q4_100_Adam_0.0010', 58, '集成电路_2023Q4', '2023Q4', 4, '产业链风险预警', 2, 'HAN Model', 2, 'Adam', 0.00100000, 100, 100, 'COMPLETED', '2025-07-25 17:25:56', '2025-07-25 17:26:15', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', 36, 'HAN_Model_f87a52fc-345e-4ada-97cc-5f1e45ec0427_epochs100_lr0.001_20250725_172601', '2025-07-25 17:25:56', '2025-10-31 12:49:29');
INSERT INTO `training_task` VALUES (74, 'HierTransferGNN Model_集成电路_2023Q4_100_Adam_0.0010', 58, '集成电路_2023Q4', '2023Q4', 2, '训练任务', 3, 'HierTransferGNN Model', 2, 'Adam', 0.00100000, 100, 100, 'COMPLETED', '2025-07-25 17:26:11', '2025-07-25 17:27:12', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', 37, 'HierTransferGNN_Model_f87a52fc-345e-4ada-97cc-5f1e45ec0427_epochs100_lr0.001_20250725_172708', '2025-07-25 17:26:11', '2025-07-25 17:26:11');
INSERT INTO `training_task` VALUES (75, 'HierTransferGNN Model_集成电路_2023Q4_100_Adam_0.0010', 58, '集成电路_2023Q4', '2023Q4', 2, '训练任务', 3, 'HierTransferGNN Model', 2, 'Adam', 0.00100000, 100, 0, 'FAILED', '2025-07-25 17:36:52', '2025-07-25 17:36:52', NULL, '训练进程异常退出，退出码: 1', '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', NULL, NULL, '2025-07-25 17:36:52', '2025-07-25 17:36:52');
INSERT INTO `training_task` VALUES (76, 'HierTransferGNN Model_集成电路_2023Q4_100_Adam_0.0010', 58, '集成电路_2023Q4', '2023Q4', 2, '训练任务', 3, 'HierTransferGNN Model', 2, 'Adam', 0.00100000, 100, 0, 'FAILED', '2025-07-25 17:41:23', '2025-07-25 17:41:23', NULL, '训练进程异常退出，退出码: 1', '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', NULL, NULL, '2025-07-25 17:41:23', '2025-07-25 17:41:23');
INSERT INTO `training_task` VALUES (77, 'HierTransferGNN Model_集成电路_2023Q4_100_Adam_0.0010', 58, '集成电路_2023Q4', '2023Q4', 2, '训练任务', 3, 'HierTransferGNN Model', 2, 'Adam', 0.00100000, 100, 0, 'FAILED', '2025-07-25 17:43:18', '2025-07-25 17:43:18', NULL, '训练进程异常退出，退出码: 1', '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', NULL, NULL, '2025-07-25 17:43:18', '2025-07-25 17:43:18');
INSERT INTO `training_task` VALUES (78, 'HAN Model_集成电路_2023Q4_100_Adam_0.0010', 58, '集成电路_2023Q4', '2023Q4', 4, '产业链风险预警', 2, 'HAN Model', 2, 'Adam', 0.00100000, 100, 0, 'FAILED', '2025-07-25 17:56:28', '2025-07-25 17:56:32', NULL, '训练进程异常退出，退出码: 1', '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', NULL, NULL, '2025-07-25 17:56:28', '2025-10-31 12:49:29');
INSERT INTO `training_task` VALUES (79, 'HAN Model_集成电路_2023Q4_100_Adam_0.0010', 58, '集成电路_2023Q4', '2023Q4', 4, '产业链风险预警', 2, 'HAN Model', 2, 'Adam', 0.00100000, 100, 100, 'COMPLETED', '2025-07-25 17:58:30', '2025-07-25 17:58:51', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', 38, 'HAN_Model_f87a52fc-345e-4ada-97cc-5f1e45ec0427_epochs100_lr0.001_20250725_175835', '2025-07-25 17:58:30', '2025-10-31 12:49:29');
INSERT INTO `training_task` VALUES (80, 'HierTransferGNN Model_集成电路_2023Q4_100_Adam_0.0010', 58, '集成电路_2023Q4', '2023Q4', 2, '训练任务', 3, 'HierTransferGNN Model', 2, 'Adam', 0.00100000, 100, 0, 'FAILED', '2025-07-25 17:59:10', '2025-07-25 17:59:10', NULL, '训练进程异常退出，退出码: 1', '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', NULL, NULL, '2025-07-25 17:59:10', '2025-07-25 17:59:10');
INSERT INTO `training_task` VALUES (81, 'HierTransferGNN Model_集成电路_2023Q4_100_Adam_0.0010', 58, '集成电路_2023Q4', '2023Q4', 2, '训练任务', 3, 'HierTransferGNN Model', 2, 'Adam', 0.00100000, 100, 100, 'COMPLETED', '2025-07-25 18:01:29', '2025-07-25 18:02:33', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', 39, 'HierTransferGNN_Model_f87a52fc-345e-4ada-97cc-5f1e45ec0427_epochs100_lr0.001_20250725_180229', '2025-07-25 18:01:29', '2025-07-25 18:01:29');
INSERT INTO `training_task` VALUES (82, 'HierTransferGNN Model_集成电路_2023Q4_100_Adam_0.0010', 58, '集成电路_2023Q4', '2023Q4', 2, '训练任务', 3, 'HierTransferGNN Model', 2, 'Adam', 0.00100000, 100, 100, 'COMPLETED', '2025-07-25 18:06:43', '2025-07-25 18:07:46', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', 41, 'HierTransferGNN_Model_f87a52fc-345e-4ada-97cc-5f1e45ec0427_epochs100_lr0.001_20250725_180743', '2025-07-25 18:06:43', '2025-07-25 18:06:43');
INSERT INTO `training_task` VALUES (83, 'HAN Model_集成电路_2023Q4_100_Adam_0.0010', 58, '集成电路_2023Q4', '2023Q4', 4, '产业链风险预警', 2, 'HAN Model', 2, 'Adam', 0.00100000, 100, 100, 'COMPLETED', '2025-07-25 18:06:57', '2025-07-25 18:07:20', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', 40, 'HAN_Model_f87a52fc-345e-4ada-97cc-5f1e45ec0427_epochs100_lr0.001_20250725_180703', '2025-07-25 18:06:57', '2025-10-31 12:49:29');
INSERT INTO `training_task` VALUES (84, 'HierTransferGNN Model_集成电路_2023Q4_100_Adam_0.0010', 58, '集成电路_2023Q4', '2023Q4', 2, '训练任务', 3, 'HierTransferGNN Model', 2, 'Adam', 0.00100000, 100, 1, 'FAILED', '2025-07-25 18:19:54', '2025-07-25 18:20:28', NULL, '训练进程异常退出，退出码: 1', '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', NULL, NULL, '2025-07-25 18:19:54', '2025-07-25 18:20:27');
INSERT INTO `training_task` VALUES (85, 'HierTransferGNN Model_集成电路_2023Q4_100_Adam_0.0010', 58, '集成电路_2023Q4', '2023Q4', 2, '训练任务', 3, 'HierTransferGNN Model', 2, 'Adam', 0.00100000, 100, 1, 'FAILED', '2025-07-25 18:20:50', '2025-07-25 18:21:29', NULL, '训练进程异常退出，退出码: 1', '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', NULL, NULL, '2025-07-25 18:20:50', '2025-07-25 18:21:28');
INSERT INTO `training_task` VALUES (86, 'HierTransferGNN Model_集成电路_2023Q4_100_Adam_0.0010', 58, '集成电路_2023Q4', '2023Q4', 2, '训练任务', 3, 'HierTransferGNN Model', 2, 'Adam', 0.00100000, 100, 100, 'COMPLETED', '2025-07-25 18:24:05', '2025-07-25 18:25:06', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', 42, 'HierTransferGNN_Model_f87a52fc-345e-4ada-97cc-5f1e45ec0427_epochs100_lr0.001_20250725_182503', '2025-07-25 18:24:05', '2025-07-25 18:24:05');
INSERT INTO `training_task` VALUES (87, 'HAN Model_电子信息_2024Q1_100_Adam_0.0010', 54, '电子信息_2024Q1', '2024Q1', 4, '产业链风险预警', 2, 'HAN Model', 2, 'Adam', 0.00100000, 100, 100, 'COMPLETED', '2025-07-25 18:28:00', '2025-07-25 18:28:13', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', 43, 'HAN_Model_8209400e-2927-4ac7-8b89-d4d97890f41f_epochs100_lr0.001_20250725_182804', '2025-07-25 18:28:00', '2025-10-31 12:49:29');
INSERT INTO `training_task` VALUES (88, 'HierTransferGNN Model_集成电路_2024Q2_20_Adam_0.0010', 57, '集成电路_2024Q2', '2024Q2', 2, '训练任务', 3, 'HierTransferGNN Model', 2, 'Adam', 0.00100000, 20, 20, 'COMPLETED', '2025-07-25 18:28:12', '2025-07-25 18:28:44', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', 44, 'HierTransferGNN_Model_56ac110b-e054-4e6a-ba6c-0cdf404e7a16_epochs20_lr0.001_20250725_182842', '2025-07-25 18:28:12', '2025-07-25 18:28:12');
INSERT INTO `training_task` VALUES (89, 'HAN Model_集成电路_2022Q4_100_Adam_0.0010', 59, '集成电路_2022Q4', '2022Q4', 4, '产业链风险预警', 2, 'HAN Model', 2, 'Adam', 0.00100000, 100, 100, 'COMPLETED', '2025-07-25 18:30:55', '2025-07-25 18:31:15', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', 45, 'HAN_Model_2f9f5fe8-60eb-4b4c-8a62-0f36a9e7779d_epochs100_lr0.001_20250725_183101', '2025-07-25 18:30:55', '2025-10-31 12:49:29');
INSERT INTO `training_task` VALUES (90, 'HierTransferGNN Model_集成电路_2022Q4_50_Adam_0.0010', 59, '集成电路_2022Q4', '2022Q4', 2, '训练任务', 3, 'HierTransferGNN Model', 2, 'Adam', 0.00100000, 50, 50, 'COMPLETED', '2025-07-25 18:31:08', '2025-07-25 18:32:00', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', 46, 'HierTransferGNN_Model_2f9f5fe8-60eb-4b4c-8a62-0f36a9e7779d_epochs50_lr0.001_20250725_183157', '2025-07-25 18:31:08', '2025-07-25 18:31:08');
INSERT INTO `training_task` VALUES (91, 'HAN Model_集成电路_2024Q2_100_Adam_0.0010', 60, '集成电路_2024Q2', '2024Q2', 4, '产业链风险预警', 2, 'HAN Model', 2, 'Adam', 0.00100000, 100, 100, 'COMPLETED', '2025-07-25 18:35:05', '2025-07-25 18:35:16', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', 47, 'HAN_Model_f3541de5-4a71-4d39-b254-01762d12b7c3_epochs100_lr0.001_20250725_183509', '2025-07-25 18:35:05', '2025-10-31 12:49:29');
INSERT INTO `training_task` VALUES (92, 'HierTransferGNN Model_集成电路_2024Q2_50_Adam_0.0010', 60, '集成电路_2024Q2', '2024Q2', 2, '训练任务', 3, 'HierTransferGNN Model', 2, 'Adam', 0.00100000, 50, 50, 'COMPLETED', '2025-07-25 18:35:15', '2025-07-25 18:35:46', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', 48, 'HierTransferGNN_Model_f3541de5-4a71-4d39-b254-01762d12b7c3_epochs50_lr0.001_20250725_183544', '2025-07-25 18:35:15', '2025-07-25 18:35:15');
INSERT INTO `training_task` VALUES (93, 'HAN Model_集成电路_2024Q2_100_Adam_0.0010', 60, '集成电路_2024Q2', '2024Q2', 4, '产业链风险预警', 2, 'HAN Model', 2, 'Adam', 0.00100000, 100, 100, 'COMPLETED', '2025-07-25 18:41:43', '2025-07-25 18:41:54', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', 49, 'HAN_Model_f3541de5-4a71-4d39-b254-01762d12b7c3_epochs100_lr0.001_20250725_184147', '2025-07-25 18:41:43', '2025-10-31 12:49:29');
INSERT INTO `training_task` VALUES (94, 'HierTransferGNN Model_集成电路_2024Q2_50_Adam_0.0010', 60, '集成电路_2024Q2', '2024Q2', 2, '训练任务', 3, 'HierTransferGNN Model', 2, 'Adam', 0.00100000, 50, 50, 'COMPLETED', '2025-07-25 18:41:56', '2025-07-25 18:42:28', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', 50, 'HierTransferGNN_Model_f3541de5-4a71-4d39-b254-01762d12b7c3_epochs50_lr0.001_20250725_184226', '2025-07-25 18:41:56', '2025-07-25 18:41:56');
INSERT INTO `training_task` VALUES (95, 'HAN Model_集成电路_2024Q2_100_Adam_0.0010', 60, '集成电路_2024Q2', '2024Q2', 4, '产业链风险预警', 2, 'HAN Model', 2, 'Adam', 0.00100000, 100, 100, 'COMPLETED', '2025-07-25 21:21:42', '2025-07-25 21:21:54', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', 51, 'HAN_Model_f3541de5-4a71-4d39-b254-01762d12b7c3_epochs100_lr0.001_20250725_212146', '2025-07-25 21:21:42', '2025-10-31 12:49:29');
INSERT INTO `training_task` VALUES (96, 'HAN Model_集成电路_2024Q2_100_Adam_0.0010', 60, '集成电路_2024Q2', '2024Q2', 4, '产业链风险预警', 2, 'HAN Model', 2, 'Adam', 0.00100000, 100, 100, 'COMPLETED', '2025-07-25 21:23:52', '2025-07-25 21:24:03', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', 52, 'HAN_Model_f3541de5-4a71-4d39-b254-01762d12b7c3_epochs100_lr0.001_20250725_212355', '2025-07-25 21:23:52', '2025-10-31 12:49:29');
INSERT INTO `training_task` VALUES (97, 'HAN Model_集成电路_2024Q2_100_Adam_0.0010', 60, '集成电路_2024Q2', '2024Q2', 4, '产业链风险预警', 2, 'HAN Model', 2, 'Adam', 0.00100000, 100, 100, 'COMPLETED', '2025-07-25 21:30:50', '2025-07-25 21:31:01', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', 53, 'HAN_Model_f3541de5-4a71-4d39-b254-01762d12b7c3_epochs100_lr0.001_20250725_213053', '2025-07-25 21:30:50', '2025-10-31 12:49:29');
INSERT INTO `training_task` VALUES (98, 'HAN Model_集成电路_2024Q2_100_Adam_0.0010', 60, '集成电路_2024Q2', '2024Q2', 4, '产业链风险预警', 2, 'HAN Model', 2, 'Adam', 0.00100000, 100, 100, 'COMPLETED', '2025-07-25 21:40:49', '2025-07-25 21:41:00', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', 54, 'HAN_Model_f3541de5-4a71-4d39-b254-01762d12b7c3_epochs100_lr0.001_20250725_214052', '2025-07-25 21:40:49', '2025-10-31 12:49:29');
INSERT INTO `training_task` VALUES (99, 'HAN Model_集成电路_2024Q2_100_Adam_0.0010', 60, '集成电路_2024Q2', '2024Q2', 4, '产业链风险预警', 2, 'HAN Model', 2, 'Adam', 0.00100000, 100, 100, 'COMPLETED', '2025-07-25 21:43:56', '2025-07-25 21:44:07', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', 55, 'HAN_Model_f3541de5-4a71-4d39-b254-01762d12b7c3_epochs100_lr0.001_20250725_214400', '2025-07-25 21:43:56', '2025-10-31 12:49:29');
INSERT INTO `training_task` VALUES (100, 'HierTransferGNN Model_电子信息_2024Q1_50_Adam_0.0010', 54, '电子信息_2024Q1', '2024Q1', 2, '训练任务', 3, 'HierTransferGNN Model', 2, 'Adam', 0.00100000, 50, 50, 'COMPLETED', '2025-07-25 21:45:40', '2025-07-25 21:46:46', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', 56, 'HierTransferGNN_Model_8209400e-2927-4ac7-8b89-d4d97890f41f_epochs50_lr0.001_20250725_214644', '2025-07-25 21:45:40', '2025-07-25 21:45:40');
INSERT INTO `training_task` VALUES (101, 'HAN Model_电子信息_2023Q4_100_Adam_0.0010', 53, '电子信息_2023Q4', '2023Q4', 4, '产业链风险预警', 2, 'HAN Model', 2, 'Adam', 0.00100000, 100, 100, 'COMPLETED', '2025-07-25 21:54:23', '2025-07-25 21:54:35', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', 57, 'HAN_Model_eef9ebfa-ff14-4038-b545-f9373ddfeb19_epochs100_lr0.001_20250725_215426', '2025-07-25 21:54:23', '2025-10-31 12:49:29');
INSERT INTO `training_task` VALUES (102, 'HierTransferGNN Model_集成电路_2024Q2_40_Adam_0.0010', 60, '集成电路_2024Q2', '2024Q2', 2, '训练任务', 3, 'HierTransferGNN Model', 2, 'Adam', 0.00100000, 40, 40, 'COMPLETED', '2025-07-25 21:55:56', '2025-07-25 21:56:27', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', 58, 'HierTransferGNN_Model_f3541de5-4a71-4d39-b254-01762d12b7c3_epochs40_lr0.001_20250725_215625', '2025-07-25 21:55:56', '2025-07-25 21:55:56');
INSERT INTO `training_task` VALUES (103, 'HAN Model_电子信息_2024Q1_600_Adam_0.0010', 54, '电子信息_2024Q1', '2024Q1', 4, '产业链风险预警', 2, 'HAN Model', 2, 'Adam', 0.00100000, 600, 600, 'COMPLETED', '2025-07-26 11:46:01', '2025-07-26 11:46:47', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', 59, 'HAN_Model_8209400e-2927-4ac7-8b89-d4d97890f41f_epochs600_lr0.001_20250726_114611', '2025-07-26 11:46:01', '2025-10-31 12:49:29');
INSERT INTO `training_task` VALUES (104, 'HierTransferGNN Model_电子信息_2024Q1_600_Adam_0.0010', 54, '电子信息_2024Q1', '2024Q1', 2, '训练任务', 3, 'HierTransferGNN Model', 2, 'Adam', 0.00100000, 600, 600, 'COMPLETED', '2025-07-26 11:47:25', '2025-07-26 11:48:42', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', 60, 'HierTransferGNN_Model_8209400e-2927-4ac7-8b89-d4d97890f41f_epochs600_lr0.001_20250726_114840', '2025-07-26 11:47:25', '2025-07-26 11:47:25');
INSERT INTO `training_task` VALUES (105, 'HAN Model_集成电路_2024Q2_100_Adam_0.0010', 60, '集成电路_2024Q2', '2024Q2', 4, '产业链风险预警', 2, 'HAN Model', 2, 'Adam', 0.00100000, 100, 100, 'COMPLETED', '2025-10-30 17:03:13', '2025-10-30 17:03:33', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', 61, 'HAN_Model_f3541de5-4a71-4d39-b254-01762d12b7c3_epochs100_lr0.001_20251030_170325', '2025-10-30 17:03:13', '2025-10-31 12:49:29');
INSERT INTO `training_task` VALUES (106, 'HierTransferGNN Model_电子信息_2024Q2_800_Adam_0.0010', 55, '电子信息_2024Q2', '2024Q2', 2, '训练任务', 3, 'HierTransferGNN Model', 2, 'Adam', 0.00100000, 800, 800, 'COMPLETED', '2025-10-31 14:15:12', '2025-10-31 14:16:57', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', 62, 'HierTransferGNN_Model_8b29f586-d9ec-47f1-8b22-ffe14ce03990_epochs800_lr0.001_20251031_141653', '2025-10-31 14:15:12', '2025-10-31 14:15:12');
INSERT INTO `training_task` VALUES (107, 'HAN Model_集成电路_2024Q2_600_Adam_0.0010', 60, '集成电路_2024Q2', '2024Q2', 4, '训练任务', 2, 'HAN Model', 2, 'Adam', 0.00100000, 600, 600, 'COMPLETED', '2025-10-31 14:17:26', '2025-10-31 14:17:58', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', 63, 'HAN_Model_f3541de5-4a71-4d39-b254-01762d12b7c3_epochs600_lr0.001_20251031_141729', '2025-10-31 14:17:26', '2025-10-31 14:17:26');
INSERT INTO `training_task` VALUES (108, 'MetaPath2vec_集成电路_2024Q2_1200_Adam_0.0010', 60, '集成电路_2024Q2', '2024Q2', 3, '训练任务', 4, 'MetaPath2vec', 2, 'Adam', 0.00100000, 1200, 0, 'FAILED', '2025-10-31 15:05:53', '2025-10-31 15:05:53', NULL, '训练进程异常退出，退出码: 2', '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', NULL, NULL, '2025-10-31 15:05:53', '2025-10-31 15:05:53');
INSERT INTO `training_task` VALUES (109, 'MetaPath2vec_集成电路_2024Q2_200_Adam_0.0010', 60, '集成电路_2024Q2', '2024Q2', 3, '训练任务', 4, 'MetaPath2vec', 2, 'Adam', 0.00100000, 200, 0, 'FAILED', '2025-10-31 15:07:53', '2025-10-31 15:07:53', NULL, '训练进程异常退出，退出码: 2', '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', NULL, NULL, '2025-10-31 15:07:53', '2025-10-31 15:07:53');
INSERT INTO `training_task` VALUES (110, 'MetaPath2vec_集成电路_2024Q2_200_Adam_0.0010', 60, '集成电路_2024Q2', '2024Q2', 3, '训练任务', 4, 'MetaPath2vec', 2, 'Adam', 0.00100000, 200, 0, 'FAILED', '2025-10-31 15:16:50', '2025-10-31 15:16:50', NULL, '训练进程异常退出，退出码: 2', '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', NULL, NULL, '2025-10-31 15:16:50', '2025-10-31 15:16:50');
INSERT INTO `training_task` VALUES (111, 'MetaPath2vec_集成电路_2024Q2_200_Adam_0.0010', 60, '集成电路_2024Q2', '2024Q2', 3, '训练任务', 4, 'MetaPath2vec', 2, 'Adam', 0.00100000, 200, 200, 'COMPLETED', '2025-10-31 15:17:47', '2025-10-31 15:18:09', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', 64, 'MetaPath2vec_集成电路_2024Q2_epochs200_lr0.001_20251031_151808', '2025-10-31 15:17:47', '2025-10-31 15:17:47');
INSERT INTO `training_task` VALUES (112, 'MetaPath2vec_集成电路_2024Q2_200_Adam_0.0010', 60, '集成电路_2024Q2', '2024Q2', 3, '训练任务', 4, 'MetaPath2vec', 2, 'Adam', 0.00100000, 200, 200, 'COMPLETED', '2025-10-31 15:41:25', '2025-10-31 15:41:44', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', 65, 'MetaPath2vec_集成电路_2024Q2_epochs200_lr0.001_20251031_154143', '2025-10-31 15:41:25', '2025-10-31 15:41:25');
INSERT INTO `training_task` VALUES (113, 'MetaPath2vec_集成电路_2024Q2_200_Adam_0.0010', 60, '集成电路_2024Q2', '2024Q2', 3, '训练任务', 4, 'MetaPath2vec', 2, 'Adam', 0.00100000, 200, 200, 'COMPLETED', '2025-10-31 16:02:50', '2025-10-31 16:03:07', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', 66, 'MetaPath2vec_集成电路_2024Q2_epochs200_lr0.001_20251031_160307', '2025-10-31 16:02:50', '2025-10-31 16:02:50');
INSERT INTO `training_task` VALUES (114, 'MetaPath2vec_集成电路_2024Q2_200_Adam_0.0010', 60, '集成电路_2024Q2', '2024Q2', 3, '训练任务', 4, 'MetaPath2vec', 2, 'Adam', 0.00100000, 200, 200, 'COMPLETED', '2025-10-31 16:13:12', '2025-10-31 16:13:30', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', 67, 'MetaPath2vec_集成电路_2024Q2_epochs200_lr0.001_20251031_161329', '2025-10-31 16:13:12', '2025-10-31 16:13:12');
INSERT INTO `training_task` VALUES (115, 'MetaPath2vec_集成电路_2024Q2_200_Adam_0.0010', 60, '集成电路_2024Q2', '2024Q2', 3, '训练任务', 4, 'MetaPath2vec', 2, 'Adam', 0.00100000, 200, 200, 'COMPLETED', '2025-10-31 16:30:07', '2025-10-31 16:30:24', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', 68, 'MetaPath2vec_集成电路_2024Q2_epochs200_lr0.001_20251031_163024', '2025-10-31 16:30:07', '2025-10-31 16:30:07');
INSERT INTO `training_task` VALUES (116, 'MetaPath2vec_集成电路_2024Q2_600_Adam_0.0010', 60, '集成电路_2024Q2', '2024Q2', 3, '训练任务', 4, 'MetaPath2vec', 2, 'Adam', 0.00100000, 600, 600, 'COMPLETED', '2025-10-31 16:45:54', '2025-10-31 16:46:13', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', 69, 'MetaPath2vec_集成电路_2024Q2_epochs600_lr0.001_20251031_164612', '2025-10-31 16:45:54', '2025-10-31 16:45:54');
INSERT INTO `training_task` VALUES (117, 'MetaPath2vec_集成电路_2024Q2_200_Adam_0.0010', 60, '集成电路_2024Q2', '2024Q2', 3, '训练任务', 4, 'MetaPath2vec', 2, 'Adam', 0.00100000, 200, 200, 'COMPLETED', '2025-11-01 19:19:50', '2025-11-01 19:20:16', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', 70, 'MetaPath2vec_集成电路_2024Q2_epochs200_lr0.001_20251101_192015', '2025-11-01 19:19:50', '2025-11-01 19:19:50');
INSERT INTO `training_task` VALUES (118, 'MetaPath2vec_集成电路_2024Q2_200_Adam_0.0010', 60, '集成电路_2024Q2', '2024Q2', 3, '训练任务', 4, 'MetaPath2vec', 2, 'Adam', 0.00100000, 200, 200, 'COMPLETED', '2025-11-01 19:26:00', '2025-11-01 19:26:21', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', 71, 'MetaPath2vec_集成电路_2024Q2_epochs200_lr0.001_20251101_192620', '2025-11-01 19:26:00', '2025-11-01 19:26:00');
INSERT INTO `training_task` VALUES (119, 'MetaPath2vec_集成电路_2022Q2_200_Adam_0.0010', 63, '集成电路_2022Q2', '2022Q2', 3, '训练任务', 4, 'MetaPath2vec', 2, 'Adam', 0.00100000, 200, 200, 'COMPLETED', '2025-11-03 10:20:51', '2025-11-03 10:21:22', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', 72, 'MetaPath2vec_集成电路_2022Q2_epochs200_lr0.001_20251103_102122', '2025-11-03 10:20:51', '2025-11-03 10:20:51');
INSERT INTO `training_task` VALUES (120, 'HierTransferGNN Model_集成电路_2022Q2_600_Adam_0.0010', 63, '集成电路_2022Q2', '2022Q2', 2, '训练任务', 3, 'HierTransferGNN Model', 2, 'Adam', 0.00100000, 600, 600, 'COMPLETED', '2025-11-03 10:22:16', '2025-11-03 10:23:14', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', 73, 'HierTransferGNN_Model_5187a343-8967-4f3f-8b2b-42a4ccc13bdc_epochs600_lr0.001_20251103_102311', '2025-11-03 10:22:16', '2025-11-03 10:22:16');
INSERT INTO `training_task` VALUES (121, 'HierTransferGNN Model_集成电路_2023Q2_200_Adam_0.0010', 65, '集成电路_2023Q2', '2023Q2', 2, '训练任务', 3, 'HierTransferGNN Model', 2, 'Adam', 0.00100000, 200, 200, 'COMPLETED', '2025-11-19 19:07:14', '2025-11-19 19:08:17', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', 74, 'HierTransferGNN_Model_45c8856a-da49-4cdc-a6ac-e15a09bdb526_epochs200_lr0.001_20251119_190814', '2025-11-19 19:07:14', '2025-11-19 19:07:14');
INSERT INTO `training_task` VALUES (122, 'MetaPath2vec_集成电路_2023Q2_200_Adam_0.0010', 65, '集成电路_2023Q2', '2023Q2', 3, '训练任务', 4, 'MetaPath2vec', 2, 'Adam', 0.00100000, 200, 200, 'COMPLETED', '2025-11-19 19:15:54', '2025-11-19 19:16:17', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', 75, '基于链接预测的产业链完整性评估模型_集成电路_2023Q2_epochs200_lr0.001_20251119_191617', '2025-11-19 19:15:54', '2025-11-19 19:15:54');
INSERT INTO `training_task` VALUES (123, 'HierTransferGNN Model_集成电路_2023Q2_200_Adam_0.0010', 65, '集成电路_2023Q2', '2023Q2', 2, '训练任务', 3, 'HierTransferGNN Model', 2, 'Adam', 0.00100000, 200, 200, 'COMPLETED', '2025-11-19 19:20:33', '2025-11-19 19:21:25', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', 76, '基于分层知识可转移图神经网络的风险评估模型_45c8856a-da49-4cdc-a6ac-e15a09bdb526_epochs200_lr0.001_20251119_192122', '2025-11-19 19:20:33', '2025-11-19 19:20:33');
INSERT INTO `training_task` VALUES (124, '结合层次图神经网络和LSTM的产业链风险预警模型_电子信息_2023Q4_800_Adam_0.0010', 53, '电子信息_2023Q4', '2023Q4', 4, '训练任务', 2, '结合层次图神经网络和LSTM的产业链风险预警模型', 2, 'Adam', 0.00100000, 800, 800, 'COMPLETED', '2025-11-19 19:22:48', '2025-11-19 19:23:40', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', 77, '结合层次图神经网络和LSTM的产业链风险预警模型_eef9ebfa-ff14-4038-b545-f9373ddfeb19_epochs800_lr0.001_20251119_192253', '2025-11-19 19:22:48', '2025-11-19 19:22:48');
INSERT INTO `training_task` VALUES (125, '基于链接预测的产业链完整性评估模型_集成电路_2022Q2_600_Adam_0.0010', 63, '集成电路_2022Q2', '2022Q2', 3, '训练任务', 4, '基于链接预测的产业链完整性评估模型', 2, 'Adam', 0.00100000, 600, 600, 'COMPLETED', '2025-11-19 20:32:29', '2025-11-19 20:32:50', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', 78, '基于链接预测的产业链完整性评估模型_集成电路_2022Q2_epochs600_lr0.001_20251119_203249', '2025-11-19 20:32:29', '2025-11-19 20:32:29');
INSERT INTO `training_task` VALUES (126, '基于链接预测的产业链完整性评估模型_集成电路_2023Q2_200_Adam_0.0010', 65, '集成电路_2023Q2', '2022Q4', 3, '训练任务', 4, '基于链接预测的产业链完整性评估模型', 2, 'Adam', 0.00100000, 200, 200, 'COMPLETED', '2025-11-20 14:25:15', '2025-11-20 14:25:44', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', 79, '基于链接预测的产业链完整性评估模型_集成电路_2023Q2_epochs200_lr0.001_20251120_142544', '2025-11-20 14:25:15', '2025-11-20 14:25:15');
INSERT INTO `training_task` VALUES (127, '基于分层知识可转移图神经网络的风险评估模型_电子信息_2024Q1_600_Adam_0.0010', 54, '电子信息_2024Q1', '2024Q1', 2, '训练任务', 3, '基于分层知识可转移图神经网络的风险评估模型', 2, 'Adam', 0.00100000, 600, 600, 'COMPLETED', '2025-11-20 14:26:07', '2025-11-20 14:27:33', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', 80, '基于分层知识可转移图神经网络的风险评估模型_8209400e-2927-4ac7-8b89-d4d97890f41f_epochs600_lr0.001_20251120_142730', '2025-11-20 14:26:07', '2025-11-20 14:26:07');
INSERT INTO `training_task` VALUES (128, '结合层次图神经网络和LSTM的产业链风险预警模型_电子信息_2024Q1_800_Adam_0.0010', 54, '电子信息_2024Q1', '2024Q1', 4, '训练任务', 2, '结合层次图神经网络和LSTM的产业链风险预警模型', 2, 'Adam', 0.00100000, 800, 800, 'COMPLETED', '2025-11-20 14:28:20', '2025-11-20 14:29:10', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', 81, '结合层次图神经网络和LSTM的产业链风险预警模型_8209400e-2927-4ac7-8b89-d4d97890f41f_epochs800_lr0.001_20251120_142823', '2025-11-20 14:28:20', '2025-11-20 14:28:20');
INSERT INTO `training_task` VALUES (129, '基于链接预测的产业链完整性评估模型_电子信息_2024Q2_200_Adam_0.0010', 55, '电子信息_2024Q2', '2024Q2', 3, '训练任务', 4, '基于链接预测的产业链完整性评估模型', 2, 'Adam', 0.00100000, 200, 200, 'COMPLETED', '2025-11-20 14:44:49', '2025-11-20 14:45:09', NULL, NULL, '{\"dp\": 0.000001, \"nClusters\": 5, \"topkRatio\": 0.1, \"privacyMethod\": \"none\", \"clientsSampleRatio\": 1}', 82, '基于链接预测的产业链完整性评估模型_电子信息_2024Q2_epochs200_lr0.001_20251120_144509', '2025-11-20 14:44:49', '2025-11-20 14:44:49');

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '用户名',
  `password` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '密码',
  `real_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '真实姓名',
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '邮箱',
  `role` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT 'user' COMMENT '角色：admin-管理员，user-普通用户',
  `status` tinyint(4) NULL DEFAULT 1 COMMENT '状态：0-禁用，1-启用',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username`) USING BTREE,
  INDEX `idx_username`(`username`) USING BTREE,
  INDEX `idx_status`(`status`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '用户表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (1, 'admin', '$2a$10$Vi16YSZ1IuojOb9dblNXme5zovqtnn8Zii4CVYQpnVtn61IPnw5X2', '管理员', 'admin@example.com', 'admin', 1, '2025-02-25 11:13:13', '2025-02-25 12:18:08');
INSERT INTO `user` VALUES (5, 'test', '$2a$10$Vi16YSZ1IuojOb9dblNXme5zovqtnn8Zii4CVYQpnVtn61IPnw5X2', '测试用户', 'test@example.com', 'user', 1, '2025-02-25 11:16:47', '2025-02-25 12:18:25');

SET FOREIGN_KEY_CHECKS = 1;
