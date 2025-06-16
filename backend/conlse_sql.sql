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

 Date: 14/06/2025 09:43:34
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

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
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

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
  `status` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '设备状态',
  `location` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '设备位置',
  `last_active` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后活跃时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ix_devices_id`(`id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of devices
-- ----------------------------

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
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

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
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of task_assignments
-- ----------------------------

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
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ix_tasks_id`(`id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tasks
-- ----------------------------

-- ----------------------------
-- Table structure for toolbox_tools
-- ----------------------------
DROP TABLE IF EXISTS `toolbox_tools`;
CREATE TABLE `toolbox_tools`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '工具名称',
  `command` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '执行命令',
  `icon` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '图标数据',
  `user_id` int(11) NULL DEFAULT NULL COMMENT '用户ID',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_id`(`user_id`) USING BTREE,
  INDEX `ix_toolbox_tools_id`(`id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of toolbox_tools
-- ----------------------------

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
) ENGINE = MyISAM AUTO_INCREMENT = 8 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (1, 'admin', '$2b$12$xxkbO0RDZWFFjTN7nvT4e.qWYd9MlJPYvqjZp8K./JK3Bq40anvzq', '管理员', '管理员', 'active', NULL, '2025-06-14 03:59:05', '2025-06-14 03:59:05');
INSERT INTO `users` VALUES (7, 'user2', '$2b$12$2ovFOSUky0/jls4hrS6cDOT4jymxt1LOUqIFfMabFXLIyT1OYaryy', '系统架构师', '操作员', 'active', NULL, '2025-06-14 05:52:58', '2025-06-14 05:52:58');
INSERT INTO `users` VALUES (6, 'user1', '$2b$12$E5PKmFH12Yh2m5/VjG2foeQt.VRx6JU.hk8yeb3LrlrhobXg/DGs2', '网络工程师', '操作员', 'active', NULL, '2025-06-14 05:31:42', '2025-06-14 05:31:42');
INSERT INTO `users` VALUES (5, 'user3', '$2b$12$O/nneEjY52QmDNEQcvG/gOAJFr5bHLI458kqOroxA83iHSJaFajHq', '系统规划与管理师', '操作员', 'active', NULL, '2025-06-14 05:26:04', '2025-06-14 05:26:04');

SET FOREIGN_KEY_CHECKS = 1;
