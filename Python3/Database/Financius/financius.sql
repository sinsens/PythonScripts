/*
Navicat MariaDB Data Transfer

Source Server         : localhost_3306
Source Server Version : 100109
Source Host           : localhost:3306
Source Database       : financius

Target Server Type    : MariaDB
Target Server Version : 100109
File Encoding         : 65001

Date: 2018-08-29 18:00:50
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for accounts
-- ----------------------------
DROP TABLE IF EXISTS `accounts`;
CREATE TABLE `accounts` (
  `_id` int(11) NOT NULL AUTO_INCREMENT,
  `accounts_id` varchar(36) DEFAULT NULL COMMENT '账户GUID',
  `accounts_model_state` tinyint(1) DEFAULT '1' COMMENT '账户状态：1正常，2已删除',
  `accounts_sync_state` tinyint(1) DEFAULT '1' COMMENT '同步状态',
  `accounts_currency_code` varchar(10) DEFAULT NULL COMMENT '货币代码',
  `accounts_title` varchar(36) DEFAULT NULL COMMENT '账户标题',
  `accounts_note` text COMMENT '备注',
  `accounts_balance` int(11) DEFAULT '0' COMMENT '账户余额',
  `accounts_include_in_totals` tinyint(1) DEFAULT '1' COMMENT '是否包含在总计中：1是，0否，默认1',
  PRIMARY KEY (`_id`)
) ENGINE=MyISAM AUTO_INCREMENT=33 DEFAULT CHARSET=utf8 COMMENT='账户';

-- ----------------------------
-- Table structure for categories
-- ----------------------------
DROP TABLE IF EXISTS `categories`;
CREATE TABLE `categories` (
  `_id` int(11) NOT NULL AUTO_INCREMENT,
  `categories_id` varchar(36) DEFAULT NULL COMMENT '分类GUID',
  `categories_model_state` tinyint(1) DEFAULT '1' COMMENT '分类状态：1正常，2已删除',
  `categories_sync_state` tinyint(1) DEFAULT '1',
  `categories_transaction_type` tinyint(1) DEFAULT NULL COMMENT '分类',
  `categories_title` varchar(36) DEFAULT NULL COMMENT '分类标题',
  `categories_color` int(11) DEFAULT NULL COMMENT '分类颜色',
  `categories_sort_order` int(11) DEFAULT NULL COMMENT '分类排序，0-n，越小越靠前',
  PRIMARY KEY (`_id`)
) ENGINE=MyISAM AUTO_INCREMENT=103 DEFAULT CHARSET=utf8 COMMENT='分类';

-- ----------------------------
-- Table structure for currencies
-- ----------------------------
DROP TABLE IF EXISTS `currencies`;
CREATE TABLE `currencies` (
  `_id` int(11) NOT NULL AUTO_INCREMENT,
  `currencies_id` text COMMENT '货币GUID',
  `currencies_model_state` int(11) DEFAULT '1' COMMENT '货币状态：1正常，2已删除',
  `currencies_sync_state` int(11) DEFAULT '1' COMMENT '货币同步状态',
  `currencies_code` varchar(16) DEFAULT NULL COMMENT '货币代码',
  `currencies_symbol` varchar(16) DEFAULT NULL COMMENT '货币符号',
  `currencies_symbol_position` int(11) DEFAULT NULL COMMENT '货币符号位置',
  `currencies_decimal_separator` varchar(16) DEFAULT NULL COMMENT '货币十进制分隔符',
  `currencies_group_separator` text COMMENT '货币组分隔符',
  `currencies_decimal_count` int(11) DEFAULT NULL COMMENT '货币小数位数',
  PRIMARY KEY (`_id`)
) ENGINE=MyISAM AUTO_INCREMENT=50 DEFAULT CHARSET=utf8 COMMENT='货币';

-- ----------------------------
-- Table structure for exchange_rates
-- ----------------------------
DROP TABLE IF EXISTS `exchange_rates`;
CREATE TABLE `exchange_rates` (
  `_id` int(11) NOT NULL AUTO_INCREMENT,
  `exchange_rates_currency_code_from` varchar(16) DEFAULT NULL COMMENT '源货币',
  `exchange_rates_currency_code_to` varchar(16) DEFAULT NULL COMMENT '目标货币',
  `exchange_rates_rate` double DEFAULT NULL COMMENT '汇率',
  PRIMARY KEY (`_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='汇率';

-- ----------------------------
-- Table structure for tags
-- ----------------------------
DROP TABLE IF EXISTS `tags`;
CREATE TABLE `tags` (
  `_id` int(11) NOT NULL AUTO_INCREMENT,
  `tags_id` varchar(36) DEFAULT NULL COMMENT '标签GUID',
  `tags_model_state` tinyint(1) DEFAULT '1' COMMENT '标签状态：1正常，2已删除',
  `tags_sync_state` tinyint(1) DEFAULT '1' COMMENT '标签同步状态',
  `tags_title` varchar(36) DEFAULT NULL COMMENT '标签标题',
  PRIMARY KEY (`_id`),
  KEY `tags_id` (`tags_id`)
) ENGINE=MyISAM AUTO_INCREMENT=103 DEFAULT CHARSET=utf8 COMMENT='标签';

-- ----------------------------
-- Table structure for transactions
-- ----------------------------
DROP TABLE IF EXISTS `transactions`;
CREATE TABLE `transactions` (
  `_id` int(11) NOT NULL AUTO_INCREMENT,
  `transactions_id` varchar(36) DEFAULT NULL COMMENT '交易GUID',
  `transactions_model_state` tinyint(1) DEFAULT '1' COMMENT '交易状态：1正常，2已删除',
  `transactions_sync_state` tinyint(1) DEFAULT '1' COMMENT '交易同步状态',
  `transactions_account_from_id` varchar(36) DEFAULT NULL COMMENT '支出账户GUID',
  `transactions_account_to_id` varchar(36) DEFAULT NULL COMMENT '收入账户GUID',
  `transactions_category_id` varchar(36) DEFAULT NULL COMMENT '交易分类GUID',
  `transactions_date` datetime DEFAULT NULL COMMENT '发生时间',
  `transactions_amount` int(11) DEFAULT NULL COMMENT '金额',
  `transactions_exchange_rate` double DEFAULT NULL COMMENT '汇率',
  `transactions_note` text COMMENT '备注',
  `transactions_state` tinyint(1) DEFAULT NULL COMMENT '交易状态：1已确认，2未确认',
  `transactions_type` tinyint(1) DEFAULT NULL COMMENT '交易类型：1支出，2收入，3转账',
  `transactions_include_in_reports` tinyint(1) DEFAULT '1' COMMENT '是否包含在总计中：1包含，0不包含，默认1',
  PRIMARY KEY (`_id`),
  KEY `transactions_id` (`transactions_id`)
) ENGINE=MyISAM AUTO_INCREMENT=1224 DEFAULT CHARSET=utf8 COMMENT='交易';

-- ----------------------------
-- Table structure for transaction_tags
-- ----------------------------
DROP TABLE IF EXISTS `transaction_tags`;
CREATE TABLE `transaction_tags` (
  `transaction_tags_transaction_id` varchar(36) NOT NULL COMMENT '交易GUID',
  `transaction_tags_tag_id` varchar(36) NOT NULL COMMENT '标签GUID',
  KEY `transaction_tags_transaction_id` (`transaction_tags_transaction_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
