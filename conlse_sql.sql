/*
 Navicat Premium Dump SQL

 Source Server         : root
 Source Server Type    : MySQL
 Source Server Version : 80012 (8.0.12)
 Source Host           : localhost:3306
 Source Schema         : conlse_sql

 Target Server Type    : MySQL
 Target Server Version : 80012 (8.0.12)
 File Encoding         : 65001

 Date: 09/07/2025 00:47:23
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for ai_models
-- ----------------------------
DROP TABLE IF EXISTS `ai_models`;
CREATE TABLE `ai_models`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '模型名称',
  `model_type` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '模型类型：embedding/chat/completion',
  `provider` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '提供商：openai/azure/local',
  `api_endpoint` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'API端点',
  `api_key` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'API密钥',
  `model_config` json NULL COMMENT '模型配置参数',
  `is_default` tinyint(1) NULL DEFAULT NULL COMMENT '是否为默认模型',
  `status` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '状态',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ix_ai_models_id`(`id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of ai_models
-- ----------------------------

-- ----------------------------
-- Table structure for projects
-- ----------------------------
DROP TABLE IF EXISTS `projects`;
CREATE TABLE `projects`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '项目名称',
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '项目描述',
  `status` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '开发中' COMMENT '项目状态',
  `icon` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT 'Briefcase' COMMENT '项目图标',
  `manager_id` int(11) NULL DEFAULT NULL COMMENT '负责人ID',
  `planning` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '项目策划',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `ix_projects_name`(`name`(250)) USING BTREE,
  INDEX `ix_projects_id`(`id`) USING BTREE,
  INDEX `fk_projects_manager`(`manager_id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of projects
-- ----------------------------
INSERT INTO `projects` VALUES (1, '智慧银行平台', '提供银行网点智能化服务与管理平台', '在线', 'Monitor', 1, '构建银行网点智能化管理平台，支持设备管理、任务分配、性能监控等功能。', '2025-07-08 10:00:00', '2025-07-08 10:00:00');
INSERT INTO `projects` VALUES (2, '金融科技创新实验室', '探索区块链、人工智能在金融领域的应用', '开发中', 'DataAnalysis', 1, '研究区块链、AI等新技术在金融服务中的创新应用，提升金融服务水平。', '2025-07-08 10:05:00', '2025-07-08 10:05:00');

-- ----------------------------
-- Table structure for desktop_items
-- ----------------------------
DROP TABLE IF EXISTS `desktop_items`;
CREATE TABLE `desktop_items`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '项目名称',
  `type` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '项目类型',
  `path` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '项目路径',
  `icon` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '图标数据',
  `user_id` int(11) NULL DEFAULT NULL COMMENT '用户ID',
  `role` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '适用角色',
  `position_x` int(11) NULL DEFAULT NULL COMMENT 'X坐标',
  `position_y` int(11) NULL DEFAULT NULL COMMENT 'Y坐标',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_id`(`user_id`) USING BTREE,
  INDEX `ix_desktop_items_id`(`id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of desktop_items
-- ----------------------------

-- ----------------------------
-- Table structure for devices
-- ----------------------------
DROP TABLE IF EXISTS `devices`;
CREATE TABLE `devices`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '设备名称',
  `type` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '设备类型',
  `ip` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '设备IP地址',
  `status` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '设备状态',
  `location` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '设备位置',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ix_devices_id`(`id`) USING BTREE,
  INDEX `idx_devices_ip`(`ip`) USING BTREE,
  INDEX `idx_devices_name`(`name`) USING BTREE,
  INDEX `idx_devices_type`(`type`) USING BTREE,
  INDEX `idx_devices_status`(`status`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 15 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of devices
-- ----------------------------
INSERT INTO `devices` VALUES (14, 'DB服务器001', '数据库服务器', '192.168.1.200', 'offline', '机房B-机柜01');
INSERT INTO `devices` VALUES (13, 'Web服务器001', '服务器', '192.168.1.100', 'online', '机房A-机柜01');
INSERT INTO `devices` VALUES (5, '核心交换机002', '交换机', '192.168.1.11', 'offline', '机房B-网络区');
INSERT INTO `devices` VALUES (6, '防火墙001', '安全设备', '192.168.1.1', 'online', '机房A-安全区');
INSERT INTO `devices` VALUES (7, '负载均衡器001', '负载均衡器', '192.168.1.50', 'online', '机房A-网络区');
INSERT INTO `devices` VALUES (8, '存储服务器001', '存储设备', '192.168.1.150', 'maintenance', '机房B-存储区');
INSERT INTO `devices` VALUES (9, '监控服务器001', '监控设备', '192.168.1.250', 'online', '机房A-管理区');
INSERT INTO `devices` VALUES (10, '备份服务器001', '备份设备', '192.168.1.251', 'error', '机房B-备份区');
INSERT INTO `devices` VALUES (11, 'test1', '服务器', '192.168.1.124', 'online', '机房A-机柜01');
INSERT INTO `devices` VALUES (12, 'test12', '交换机', '192.168.41.1', 'online', '机房A-网络区');

-- ----------------------------
-- Table structure for knowledge_bases
-- ----------------------------
DROP TABLE IF EXISTS `knowledge_bases`;
CREATE TABLE `knowledge_bases`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '知识库名称',
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '知识库描述',
  `category` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '知识库分类',
  `tags` json NULL COMMENT '标签',
  `is_public` tinyint(1) NULL DEFAULT NULL COMMENT '是否公开',
  `status` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '状态：active/inactive/archived',
  `creator_id` int(11) NULL DEFAULT NULL COMMENT '创建者ID',
  `assigned_engineer_id` int(11) NULL DEFAULT NULL COMMENT '分配的工程师ID',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `creator_id`(`creator_id`) USING BTREE,
  INDEX `ix_knowledge_bases_id`(`id`) USING BTREE,
  INDEX `assigned_engineer_id`(`assigned_engineer_id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 9 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of knowledge_bases
-- ----------------------------
INSERT INTO `knowledge_bases` VALUES (7, '网络设备', '', '网络工程师', 'null', 1, 'active', 1, NULL, '2025-06-30 15:35:59', '2025-06-30 15:35:59');
INSERT INTO `knowledge_bases` VALUES (8, '架构知识', '', '架构师', 'null', 1, 'active', 1, NULL, '2025-06-30 15:43:45', '2025-06-30 15:43:45');

-- ----------------------------
-- Table structure for knowledge_documents
-- ----------------------------
DROP TABLE IF EXISTS `knowledge_documents`;
CREATE TABLE `knowledge_documents`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '文档标题',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '文档内容',
  `source_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '来源类型：manual/upload/web/api',
  `source_url` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '来源URL',
  `file_path` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '文件路径',
  `file_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '文件类型',
  `file_size` int(11) NULL DEFAULT NULL COMMENT '文件大小(字节)',
  `keywords` json NULL COMMENT '关键词',
  `embedding_vector` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '向量化表示',
  `is_processed` tinyint(1) NULL DEFAULT NULL COMMENT '是否已处理',
  `knowledge_base_id` int(11) NULL DEFAULT NULL COMMENT '所属知识库ID',
  `creator_id` int(11) NULL DEFAULT NULL COMMENT '创建者ID',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `parse_status` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT 'success' COMMENT '解析状态：pending/processing/success/failed',
  `chunk_method` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT 'general' COMMENT '切片方法：general/semantic/custom',
  `chunk_count` int(11) NULL DEFAULT 0 COMMENT '分块数量',
  `is_enabled` tinyint(1) NULL DEFAULT 1 COMMENT '是否启用',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `knowledge_base_id`(`knowledge_base_id`) USING BTREE,
  INDEX `creator_id`(`creator_id`) USING BTREE,
  INDEX `ix_knowledge_documents_id`(`id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of knowledge_documents
-- ----------------------------
INSERT INTO `knowledge_documents` VALUES (5, '无线一本通', NULL, 'upload', NULL, 'uploads/knowledge\\970bd983-4746-42a2-9fd1-34636a198ceb.pdf', 'application/pdf', 106287, '[]', NULL, 1, 7, 1, '2025-06-30 15:37:05', '2025-06-30 15:37:05', 'success', 'general', 0, 1);
INSERT INTO `knowledge_documents` VALUES (6, '交换机配置一本通', NULL, 'upload', NULL, 'uploads/knowledge\\1f2cf9d1-3401-45d7-b711-a01055405d7d.pdf', 'application/pdf', 4534465, '[]', NULL, 1, 7, 1, '2025-06-30 15:42:45', '2025-06-30 15:42:45', 'success', 'general', 0, 1);
INSERT INTO `knowledge_documents` VALUES (7, '路由器配置一本通', NULL, 'upload', NULL, 'uploads/knowledge\\a354a8db-4af3-49fb-9730-ae8aab0499f1.pdf', 'application/pdf', 108114, '[]', NULL, 1, 7, 1, '2025-06-30 15:43:20', '2025-06-30 15:43:20', 'success', 'general', 0, 1);

-- ----------------------------
-- Table structure for system_settings
-- ----------------------------
DROP TABLE IF EXISTS `system_settings`;
CREATE TABLE `system_settings`  (
  `id` int(11) NOT NULL COMMENT '设置ID',
  `max_users` int(11) NULL DEFAULT NULL COMMENT '最大用户数',
  `max_devices` int(11) NULL DEFAULT NULL COMMENT '最大设备数',
  `default_password` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '默认密码',
  `log_retention_days` int(11) NULL DEFAULT NULL COMMENT '日志保留天数',
  `refresh_rate` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '刷新频率',
  `encryption_level` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '加密级别',
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of system_settings
-- ----------------------------

-- ----------------------------
-- Table structure for task_assignments
-- ----------------------------
DROP TABLE IF EXISTS `task_assignments`;
CREATE TABLE `task_assignments`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `task_id` int(11) NULL DEFAULT NULL COMMENT '任务ID',
  `user_id` int(11) NULL DEFAULT NULL COMMENT '用户ID',
  `username` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '用户名',
  `assigned_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '分配时间',
  `status` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '执行状态',
  `progress` int(11) NULL DEFAULT NULL COMMENT '进度百分比',
  `performance_score` int(11) NULL DEFAULT NULL COMMENT '性能评分',
  `comments` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '备注',
  `last_update` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后更新',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `task_id`(`task_id`) USING BTREE,
  INDEX `user_id`(`user_id`) USING BTREE,
  INDEX `ix_task_assignments_id`(`id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 110 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of task_assignments
-- ----------------------------
INSERT INTO `task_assignments` VALUES (108, 161, 38, '20190002', '2025-07-06 21:42:41', '进行中', 0, 0, '', '2025-07-06 21:42:41');
INSERT INTO `task_assignments` VALUES (109, 160, 38, '20190002', '2025-07-06 21:42:41', '进行中', 0, 0, '', '2025-07-06 21:42:41');
INSERT INTO `task_assignments` VALUES (107, 164, 38, '20190002', '2025-07-06 21:42:41', '进行中', 0, 0, '', '2025-07-06 21:42:41');
INSERT INTO `task_assignments` VALUES (105, 162, 38, '20190002', '2025-07-06 21:42:41', '进行中', 0, 0, '', '2025-07-06 21:42:41');
INSERT INTO `task_assignments` VALUES (106, 163, 38, '20190002', '2025-07-06 21:42:41', '进行中', 0, 0, '', '2025-07-06 21:42:41');
INSERT INTO `task_assignments` VALUES (100, 165, 39, '20190003', '2025-07-06 21:42:16', '已完成', 100, 100, '通过桌面管理器选择提交完成', '2025-07-06 21:51:26');
INSERT INTO `task_assignments` VALUES (101, 166, 39, '20190003', '2025-07-06 21:42:16', '已完成', 100, 100, '通过桌面管理器选择提交完成', '2025-07-06 21:55:02');
INSERT INTO `task_assignments` VALUES (102, 171, 40, '20190004', '2025-07-06 21:42:22', '进行中', 0, 0, '', '2025-07-06 21:42:22');
INSERT INTO `task_assignments` VALUES (103, 169, 40, '20190004', '2025-07-06 21:42:22', '进行中', 0, 0, '', '2025-07-06 21:42:22');
INSERT INTO `task_assignments` VALUES (104, 170, 40, '20190004', '2025-07-06 21:42:22', '进行中', 0, 0, '', '2025-07-06 21:42:22');
INSERT INTO `task_assignments` VALUES (97, 157, 37, '20190001', '2025-07-06 21:42:04', '进行中', 0, 0, '', '2025-07-06 21:42:04');
INSERT INTO `task_assignments` VALUES (98, 168, 39, '20190003', '2025-07-06 21:42:16', '已完成', 100, 100, '通过桌面管理器选择提交完成', '2025-07-06 21:51:32');
INSERT INTO `task_assignments` VALUES (96, 158, 37, '20190001', '2025-07-06 21:42:04', '进行中', 0, 0, '', '2025-07-06 21:42:04');
INSERT INTO `task_assignments` VALUES (99, 167, 39, '20190003', '2025-07-06 21:42:16', '已完成', 100, 100, '通过桌面管理器选择提交完成', '2025-07-06 21:55:02');
INSERT INTO `task_assignments` VALUES (95, 159, 37, '20190001', '2025-07-06 21:42:04', '进行中', 0, 0, '', '2025-07-06 21:42:04');

-- ----------------------------
-- Table structure for tasks
-- ----------------------------
DROP TABLE IF EXISTS `tasks`;
CREATE TABLE `tasks`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '任务名称',
  `type` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '任务类型',
  `phase` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '任务阶段',
  `description` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '任务描述',
  `status` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '任务状态',
  `role_binding` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '绑定角色',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ix_tasks_id`(`id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 172 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of tasks
-- ----------------------------
INSERT INTO `tasks` VALUES (171, '验证孪生平台数据正常', '系统运维任务', '验收阶段', '通过智慧银行可视化管控平台查看设备信息', '进行中', '系统分析师', '2025-07-06 21:41:32', '2025-07-06 21:42:22');
INSERT INTO `tasks` VALUES (168, '验证微服务架构应用', '软件开发任务', '验证阶段', '验证惠农APP微服务是否正常并编写测试AI自动审批工作流', '已完成', '系统架构设计师', '2025-07-06 21:41:32', '2025-07-06 21:51:32');
INSERT INTO `tasks` VALUES (169, '部署运维平台', '系统运维任务', '计划阶段', '设计部署运维平台，监控网设备运行状态', '进行中', '系统分析师', '2025-07-06 21:41:32', '2025-07-06 21:42:22');
INSERT INTO `tasks` VALUES (170, '实现全网设备可视化管理', '系统运维任务', '执行阶段', '1.运维平台添加网络设备监控\n2.日志平台添加k8s系统日志监控', '进行中', '系统分析师', '2025-07-06 21:41:32', '2025-07-06 21:42:22');
INSERT INTO `tasks` VALUES (167, '自动部署测试工作流验证', '软件开发任务', '执行阶段', '提交微服务应用代码测试自动部署自动测试功能是否正常', '已完成', '系统架构设计师', '2025-07-06 21:41:32', '2025-07-06 21:55:02');
INSERT INTO `tasks` VALUES (162, 'TiDB数据库搭建', '集群架构任务', '执行阶段', '在分部搭建TiDB数据库，并接入总部TiDB数据库集群，完成数据库同步', '进行中', '系统规划与管理师', '2025-07-06 21:41:32', '2025-07-06 21:42:41');
INSERT INTO `tasks` VALUES (163, 'OA办公系统分部调度验证', '集群架构任务', '验收阶段', '在Karmada-Manager平台中动态调度OA办公系统到分部集群中', '进行中', '系统规划与管理师', '2025-07-06 21:41:32', '2025-07-06 21:42:41');
INSERT INTO `tasks` VALUES (164, '自动化工作流程全平台搭建', '集群架构任务', '执行阶段', '搭建Jenkins、MeterShpere、Jaeger等云原生自动化流程平台', '进行中', '系统规划与管理师', '2025-07-06 21:41:32', '2025-07-06 21:42:41');
INSERT INTO `tasks` VALUES (165, '微服务架构规范代码编写', '软件开发任务', '计划阶段', '根据微服务架构最佳实践，以及金融银行场景需求编写微服务应用代码', '已完成', '系统架构设计师', '2025-07-06 21:41:32', '2025-07-06 21:51:26');
INSERT INTO `tasks` VALUES (166, '编写Jenkins自动工作流', '软件开发任务', '执行阶段', '在Jenkins中编写微服务架构自动部署测试工作流', '已完成', '系统架构设计师', '2025-07-06 21:41:32', '2025-07-06 21:55:02');
INSERT INTO `tasks` VALUES (161, '高可用集群构建及Karmada集群应用调度', '集群架构任务', '执行阶段', '通过总部Karmada-Manager管平台搭建分部银行高可用集群', '进行中', '系统规划与管理师', '2025-07-06 21:41:32', '2025-07-06 21:42:41');
INSERT INTO `tasks` VALUES (160, '集群系统架构设计', '集群架构任务', '计划阶段', '设计企业多集群架构和技术方案', '进行中', '系统规划与管理师', '2025-07-06 21:41:32', '2025-07-06 21:42:41');
INSERT INTO `tasks` VALUES (159, 'ping命令测试验证', '网络搭建任务', '验收阶段', '1.查看获取的Ip地址信息 2.ping业务网络验证', '进行中', '网络规划设计师', '2025-07-06 21:41:32', '2025-07-06 21:42:04');
INSERT INTO `tasks` VALUES (158, '业务网络搭建', '网络搭建任务', '执行阶段', '1.配置分部IPsec VPN 2.多厂商翻译技术 3.配置AC', '进行中', '网络规划设计师', '2025-07-06 21:41:32', '2025-07-06 21:42:04');
INSERT INTO `tasks` VALUES (157, '网络架构设计', '网络搭建任务', '计划阶段', '设计分部银行光网络拓扑架构及技术方案', '进行中', '网络规划设计师', '2025-07-06 21:41:32', '2025-07-06 21:42:04');

-- ----------------------------
-- Table structure for toolbox_tools
-- ----------------------------
DROP TABLE IF EXISTS `toolbox_tools`;
CREATE TABLE `toolbox_tools`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `command` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `icon` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 17 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of toolbox_tools
-- ----------------------------
INSERT INTO `toolbox_tools` VALUES (1, 'CMD', 'cmd.exe', './images/cmd.png', '2025-06-03 12:42:24');
INSERT INTO `toolbox_tools` VALUES (2, 'PowerShell', 'powershell.exe', './images/powershell.png', '2025-06-03 12:42:24');
INSERT INTO `toolbox_tools` VALUES (3, '网络诊断', 'ncpa.cpl', './images/network.png', '2025-06-03 12:42:24');
INSERT INTO `toolbox_tools` VALUES (4, '远程桌面', 'mstsc.exe', './images/remote.png', '2025-06-03 12:42:24');
INSERT INTO `toolbox_tools` VALUES (5, 'Wireshark', 'C:/Program Files/Wireshark/Wireshark.exe', './images/wireshark.png', '2025-06-03 12:42:24');
INSERT INTO `toolbox_tools` VALUES (6, '任务管理器', 'taskmgr.exe', './images/taskmanager.png', '2025-06-03 12:42:24');
INSERT INTO `toolbox_tools` VALUES (7, '事件查看器', 'eventvwr.msc', './images/event.png', '2025-06-03 12:42:24');
INSERT INTO `toolbox_tools` VALUES (8, '服务', 'services.msc', './images/services.png', '2025-06-03 12:42:24');
INSERT INTO `toolbox_tools` VALUES (9, '注册表', 'regedit.exe', './images/registry.png', '2025-06-03 12:42:24');
INSERT INTO `toolbox_tools` VALUES (10, '磁盘管理', 'diskmgmt.msc', './images/disk.png', '2025-06-03 12:42:24');
INSERT INTO `toolbox_tools` VALUES (11, 'VS Code', 'code', './images/vscode.png', '2025-06-03 12:42:24');
INSERT INTO `toolbox_tools` VALUES (12, '记事本', 'notepad.exe', './images/notepad.png', '2025-06-03 12:42:24');
INSERT INTO `toolbox_tools` VALUES (13, '计算器', 'calc.exe', './images/calc.png', '2025-06-03 12:42:24');
INSERT INTO `toolbox_tools` VALUES (14, 'Git', 'git-bash.exe', './images/git.png', '2025-06-03 12:42:24');
INSERT INTO `toolbox_tools` VALUES (15, '控制面板', 'control.exe', './images/control.png', '2025-06-03 12:42:24');

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `password` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `role` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '用户角色',
  `type` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '用户类型',
  `status` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '用户状态',
  `photo_data` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '头像数据',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `ix_users_username`(`username`) USING BTREE,
  INDEX `ix_users_id`(`id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 41 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (1, 'admin', '$2b$12$xxkbO0RDZWFFjTN7nvT4e.qWYd9MlJPYvqjZp8K./JK3Bq40anvzq', '管理员', '管理员', 'active', NULL, '2025-06-14 03:59:05', '2025-06-15 12:43:14');
INSERT INTO `users` VALUES (37, '20190001', '$2b$12$p2kGGxlUex1jHHj5zZ7Sw.nW.k8mwutPd3tFmJH3PfeVYgGSCpqIO', '网络规划与设计师', '操作员', 'active', NULL, '2025-07-06 21:32:34', '2025-07-06 21:32:34');
INSERT INTO `users` VALUES (40, '20190004', '$2b$12$OuHiKct3s1TMEVVZ1.EQHO8kujT9EP4F/dqUdqDwUoMUnWeYqG2Om', '系统分析师', '操作员', 'active', NULL, '2025-07-06 21:32:34', '2025-07-06 21:32:34');
INSERT INTO `users` VALUES (39, '20190003', '$2b$12$mWvR9kH0hym7y5EI53g6R.uIOpOp6FwLY5FbDphROXHkNXsT2Z5x6', '系统架构设计师', '操作员', 'active', NULL, '2025-07-06 21:32:34', '2025-07-06 21:32:34');
INSERT INTO `users` VALUES (38, '20190002', '$2b$12$h5COrqprwlzy2zzXvF0xiOASUy6TXMxfpC4yUcnru/kJJ1kZEc726', '系统规划与管理师', '操作员', 'active', NULL, '2025-07-06 21:32:34', '2025-07-06 21:32:34');

SET FOREIGN_KEY_CHECKS = 1;
