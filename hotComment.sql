/*
Navicat MySQL Data Transfer

Source Server         : NewUnbuntuMysql
Source Server Version : 50719
Source Host           : 192.168.119.128:3306
Source Database       : wyyyy

Target Server Type    : MYSQL
Target Server Version : 50719
File Encoding         : 65001

Date: 2017-09-21 18:45:03
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for hotComment
-- ----------------------------
DROP TABLE IF EXISTS `hotComment`;
CREATE TABLE `hotComment` (
  `songName` varchar(255) NOT NULL,
  `songId` int(11) NOT NULL,
  `comment` varchar(10240) DEFAULT NULL,
  `likeCount` int(11) DEFAULT NULL,
  `userNikeName` varchar(255) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=99740 DEFAULT CHARSET=utf8;
