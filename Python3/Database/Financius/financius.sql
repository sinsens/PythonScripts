/*
@Name: Fiancius Mysql 数据库表设计
@File: Financius.sql
@Date: 2018-08-29 18:00:50

@Updated Date: 2019-01-27 17:01 #Sinsen
更新字段，优化索引
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for accounts
-- ----------------------------
DROP TABLE IF EXISTS `accounts`;
CREATE TABLE `accounts` (
  `_id` int(11) NOT NULL AUTO_INCREMENT,
  `accounts_id` varchar(36) DEFAULT NULL COMMENT '账户GUID',
  `accounts_model_state` tinyint(1) DEFAULT '1' COMMENT '状态：1正常，0已删除.默认1',
  `accounts_sync_state` tinyint(1) DEFAULT '0' COMMENT '同步状态：1已同步，0未同步。默认0',
  `accounts_currency_code` varchar(10) DEFAULT NULL COMMENT '货币代码',
  `accounts_title` varchar(36) DEFAULT NULL COMMENT '账户标题',
  `accounts_note` text COMMENT '备注',
  `accounts_balance` int(11) DEFAULT '0' COMMENT '账户余额',
  `accounts_include_in_totals` tinyint(1) DEFAULT '1' COMMENT '是否包含在总计中：1是，0否，默认1',
  PRIMARY KEY (`accounts_id`),
  KEY (`_id`)
) ENGINE=Aria AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='账户';

-- ----------------------------
-- Table structure for categories
-- ----------------------------
DROP TABLE IF EXISTS `categories`;
CREATE TABLE `categories` (
  `_id` int(11) NOT NULL AUTO_INCREMENT,
  `categories_id` varchar(36) DEFAULT NULL COMMENT '分类GUID',
  `categories_model_state` tinyint(1) DEFAULT '1' COMMENT '状态：1正常，0已删除.默认1',
  `categories_sync_state` tinyint(1) DEFAULT '0' COMMENT '同步状态：1已同步，0未同步。默认0',
  `categories_transaction_type` tinyint(1) DEFAULT NULL COMMENT '分类',
  `categories_title` varchar(36) DEFAULT NULL COMMENT '分类标题',
  `categories_color` int(11) DEFAULT NULL COMMENT '分类颜色',
  `categories_sort_order` tinyint(3) DEFAULT NULL COMMENT '分类排序，0-255，越小越靠前',
  PRIMARY KEY (`categories_id`),
  KEY (`_id`)
) ENGINE=Aria AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='分类';

-- ----------------------------
-- Table structure for currencies
-- ----------------------------
DROP TABLE IF EXISTS `currencies`;
CREATE TABLE `currencies` (
  `_id` int(11) NOT NULL AUTO_INCREMENT,
  `currencies_id` varchar(36) COMMENT '货币GUID',
  `currencies_model_state` tinyint(1) DEFAULT '1' COMMENT '状态：1正常，0已删除.默认1',
  `currencies_sync_state` tinyint(1) DEFAULT '0' COMMENT '同步状态：1已同步，0未同步。默认0',
  `currencies_code` varchar(16) DEFAULT NULL COMMENT '货币代码',
  `currencies_symbol` varchar(16) DEFAULT NULL COMMENT '货币符号',
  `currencies_symbol_position` tinyint(2) DEFAULT NULL COMMENT '货币符号位置',
  `currencies_decimal_separator` varchar(16) DEFAULT NULL COMMENT '货币十进制分隔符',
  `currencies_group_separator` varchar(255) COMMENT '货币组分隔符',
  `currencies_decimal_count` tinyint(2) DEFAULT NULL COMMENT '货币小数位数',
  PRIMARY KEY (`currencies_id`),
  KEY (`_id`)
) ENGINE=Aria AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='货币';

-- ----------------------------
-- Table structure for exchange_rates
-- ----------------------------
DROP TABLE IF EXISTS `exchange_rates`;
CREATE TABLE `exchange_rates` (
  `_id` int(11) NOT NULL AUTO_INCREMENT,
  `exchange_rates_currency_from_id` varchar(36) DEFAULT NULL COMMENT '源货币',
  `exchange_rates_currency_to_id` varchar(36) DEFAULT NULL COMMENT '目标货币',
  `exchange_rates_rate` double DEFAULT NULL COMMENT '汇率:1234.12',
  PRIMARY KEY (`_id`),
  KEY (`exchange_rates_currency_from_id`, `exchange_rates_currency_to_id`)
) ENGINE=Aria DEFAULT CHARSET=utf8 COMMENT='汇率';

-- ----------------------------
-- Table structure for tags
-- ----------------------------
DROP TABLE IF EXISTS `tags`;
CREATE TABLE `tags` (
  `_id` int(11) NOT NULL AUTO_INCREMENT,
  `tags_id` varchar(36) DEFAULT NULL COMMENT '标签GUID',
  `tags_model_state` tinyint(1) DEFAULT '1' COMMENT '状态：1正常，0已删除.默认1',
  `tags_sync_state` tinyint(1) DEFAULT '0' COMMENT '同步状态：1已同步，0未同步。默认0',
  `tags_title` varchar(36) DEFAULT NULL COMMENT '标签标题',
  PRIMARY KEY `tags_id` (`tags_id`),
  KEY (`_id`)
) ENGINE=Aria AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='标签';

-- ----------------------------
-- Table structure for transactions
-- ----------------------------
DROP TABLE IF EXISTS `transactions`;
CREATE TABLE `transactions` (
  `_id` int(11) NOT NULL AUTO_INCREMENT,
  `transactions_id` varchar(36) DEFAULT NULL COMMENT '交易GUID',
  `transactions_model_state` tinyint(1) DEFAULT '1' COMMENT '状态：1正常，0已删除.默认1',
  `transactions_sync_state` tinyint(1) DEFAULT '0' COMMENT '同步状态：1已同步，0未同步。默认0',
  `transactions_account_from_id` varchar(36) DEFAULT NULL COMMENT '支出账户GUID',
  `transactions_account_to_id` varchar(36) DEFAULT NULL COMMENT '收入账户GUID',
  `transactions_category_id` varchar(36) DEFAULT NULL COMMENT '交易分类GUID',
  `transactions_date` datetime DEFAULT NULL COMMENT '发生时间',
  `transactions_amount` int(11) DEFAULT NULL COMMENT '金额',
  `transactions_exchange_rate` double DEFAULT NULL COMMENT '汇率',
  `transactions_note` text COMMENT '备注',
  `transactions_state` tinyint(1) DEFAULT NULL COMMENT '交易状态：1已确认，0未确认',
  `transactions_type` tinyint(1) DEFAULT NULL COMMENT '交易类型：1支出，2收入，3转账',
  `transactions_include_in_reports` tinyint(1) DEFAULT '1' COMMENT '是否包含在总计中：1包含，0不包含，默认1',
  PRIMARY KEY (`transactions_id`),
  KEY (`_id`, `transactions_account_from_id`, `transactions_account_to_id`, `transactions_category_id`)
) ENGINE=Aria AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='交易';

-- ----------------------------
-- Table structure for transaction_tags
-- ----------------------------
DROP TABLE IF EXISTS `transaction_tags`;
CREATE TABLE `transaction_tags` (
  `_id` int(11) NOT NULL AUTO_INCREMENT,
  `transaction_tags_transaction_id` varchar(36) NOT NULL COMMENT '交易GUID',
  `transaction_tags_tag_id` varchar(36) NOT NULL COMMENT '标签GUID',
  PRIMARY KEY (`_id`),
  KEY (`transaction_tags_transaction_id`, `transaction_tags_tag_id`)
) ENGINE=Aria DEFAULT CHARSET=utf8;
