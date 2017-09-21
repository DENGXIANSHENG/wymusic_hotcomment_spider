/*
Navicat MySQL Data Transfer

Source Server         : NewUnbuntuMysql
Source Server Version : 50719
Source Host           : 192.168.119.128:3306
Source Database       : wyyyy

Target Server Type    : MYSQL
Target Server Version : 50719
File Encoding         : 65001

Date: 2017-09-21 18:45:10
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for playList
-- ----------------------------
DROP TABLE IF EXISTS `playList`;
CREATE TABLE `playList` (
  `songListId` int(11) NOT NULL AUTO_INCREMENT,
  `listName` varchar(255) NOT NULL,
  `listAddr` varchar(255) NOT NULL,
  `spiderStatus` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`songListId`)
) ENGINE=InnoDB AUTO_INCREMENT=680 DEFAULT CHARSET=utf8;
