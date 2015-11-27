-- Adminer 4.1.0 MySQL dump
/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


SET NAMES utf8;
SET time_zone = '+00:00';

DROP DATABASE IF EXISTS `live_yeksatr`;
CREATE DATABASE `live_yeksatr` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_bin */;
USE `live_yeksatr`;

DELIMITER ;;

CREATE DEFINER=`live_user`@`localhost` FUNCTION `FIX_ARABIC_CHAR`(in_str VARCHAR(5000) ) RETURNS varchar(5000) CHARSET utf8 COLLATE utf8_persian_ci
BEGIN
 DECLARE ret_str VARCHAR(5000);

   


       SET ret_str  = replace(in_str,'ی' , 'ي' );
       SET ret_str  = replace(ret_str,'ک' , 'ك' );

        RETURN ret_str;
    END;;

DELIMITER ;

DROP TABLE IF EXISTS `tbl_bulletin`;
CREATE TABLE `tbl_bulletin` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(50) CHARACTER SET utf8 COLLATE utf8_persian_ci NOT NULL,
  `recipient_email` varchar(50) CHARACTER SET utf8 COLLATE utf8_persian_ci DEFAULT NULL,
  `fk_user_id` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_user_id` (`fk_user_id`),
  CONSTRAINT `tbl_bulletin_ibfk_1` FOREIGN KEY (`fk_user_id`) REFERENCES `tbl_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `tbl_bulletin_filter1`;
CREATE TABLE `tbl_bulletin_filter1` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `query_text` varchar(100) CHARACTER SET utf8 COLLATE utf8_persian_ci NOT NULL,
  `date1` int(11) NOT NULL,
  `date2` int(11) NOT NULL,
  `date_op` int(11) NOT NULL,
  `fk_source_id` int(10) unsigned NOT NULL,
  `fk_bulletin_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_source_id` (`fk_source_id`),
  KEY `fk_bulletin_id` (`fk_bulletin_id`),
  CONSTRAINT `tbl_bulletin_filter1_ibfk_1` FOREIGN KEY (`fk_source_id`) REFERENCES `tbl_source` (`id`),
  CONSTRAINT `tbl_bulletin_filter1_ibfk_2` FOREIGN KEY (`fk_bulletin_id`) REFERENCES `tbl_bulletin` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `tbl_bulletin_schedule`;
CREATE TABLE `tbl_bulletin_schedule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fk_bulletin` int(11) NOT NULL,
  `occurence` int(11) NOT NULL,
  `hour` int(11) NOT NULL,
  `minute` int(11) NOT NULL,
  `day_of_week` int(11) NOT NULL,
  `day_of_month` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_bulletin` (`fk_bulletin`),
  CONSTRAINT `tbl_bulletin_schedule_ibfk_1` FOREIGN KEY (`fk_bulletin`) REFERENCES `tbl_bulletin` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `tbl_category`;
CREATE TABLE `tbl_category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(50) CHARACTER SET utf8 COLLATE utf8_persian_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `tbl_crawl_log`;
CREATE TABLE `tbl_crawl_log` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `crawl_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `news_count` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_persian_ci;


DROP TABLE IF EXISTS `tbl_feed`;
CREATE TABLE `tbl_feed` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(45) COLLATE utf8_persian_ci NOT NULL,
  `fk_source_id` int(10) unsigned NOT NULL,
  `url` varchar(100) COLLATE utf8_persian_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_source_id` (`fk_source_id`),
  CONSTRAINT `tbl_feed_ibfk_1` FOREIGN KEY (`fk_source_id`) REFERENCES `tbl_source` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_persian_ci ROW_FORMAT=DYNAMIC;


DROP TABLE IF EXISTS `tbl_feedback`;
CREATE TABLE `tbl_feedback` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `contents` text CHARACTER SET utf8 COLLATE utf8_persian_ci NOT NULL,
  `fk_user_id` int(10) unsigned DEFAULT NULL,
  `submit_date` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_user_id` (`fk_user_id`),
  CONSTRAINT `tbl_feedback_ibfk_1` FOREIGN KEY (`fk_user_id`) REFERENCES `tbl_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;


DROP TABLE IF EXISTS `tbl_news`;
CREATE TABLE `tbl_news` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `fk_feed_id` int(10) unsigned NOT NULL,
  `url` varchar(2000) COLLATE utf8_persian_ci NOT NULL,
  `title` varchar(4000) COLLATE utf8_persian_ci NOT NULL,
  `publish_date` datetime NOT NULL,
  `fetch_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `url_hash` varchar(45) COLLATE utf8_persian_ci NOT NULL,
  `extracted` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `fk_feed_id` (`fk_feed_id`),
  CONSTRAINT `tbl_news_ibfk_1` FOREIGN KEY (`fk_feed_id`) REFERENCES `tbl_feed` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_persian_ci;


DROP TABLE IF EXISTS `tbl_news_content`;
CREATE TABLE `tbl_news_content` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `fk_news_id` int(10) unsigned NOT NULL,
  `text_content` text COLLATE utf8_persian_ci NOT NULL,
  `html_content` text COLLATE utf8_persian_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_news_id` (`fk_news_id`),
  CONSTRAINT `tbl_news_content_ibfk_1` FOREIGN KEY (`fk_news_id`) REFERENCES `tbl_news` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_persian_ci;


DROP TABLE IF EXISTS `tbl_source`;
CREATE TABLE `tbl_source` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(45) COLLATE utf8_persian_ci NOT NULL,
  `url` varchar(45) COLLATE utf8_persian_ci NOT NULL,
  `icon` varchar(45) COLLATE utf8_persian_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_persian_ci ROW_FORMAT=DYNAMIC;


DROP TABLE IF EXISTS `tbl_source_category`;
CREATE TABLE `tbl_source_category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fk_category_id` int(11) NOT NULL,
  `fk_source_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_category_id` (`fk_category_id`),
  KEY `fk_source_id` (`fk_source_id`),
  CONSTRAINT `tbl_source_category_ibfk_1` FOREIGN KEY (`fk_category_id`) REFERENCES `tbl_category` (`id`),
  CONSTRAINT `tbl_source_category_ibfk_2` FOREIGN KEY (`fk_source_id`) REFERENCES `tbl_source` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `tbl_source_tag`;
CREATE TABLE `tbl_source_tag` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `fk_source_id` int(10) unsigned NOT NULL,
  `tag_name` varchar(45) DEFAULT NULL,
  `tag_class` varchar(450) DEFAULT NULL,
  `tag_id` varchar(450) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_source_id` (`fk_source_id`),
  CONSTRAINT `tbl_source_tag_ibfk_1` FOREIGN KEY (`fk_source_id`) REFERENCES `tbl_source` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `tbl_user`;
CREATE TABLE `tbl_user` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(80) COLLATE utf8_persian_ci NOT NULL,
  `password` varchar(45) COLLATE utf8_persian_ci NOT NULL,
  `register_date` datetime NOT NULL,
  `email` varchar(75) COLLATE utf8_persian_ci NOT NULL,
  `fk_group_id` int(11) DEFAULT NULL,
  `name` varchar(50) COLLATE utf8_persian_ci DEFAULT NULL,
  `familly` varchar(70) COLLATE utf8_persian_ci DEFAULT NULL,
  `job` varchar(120) COLLATE utf8_persian_ci DEFAULT NULL,
  `mobile_number` varchar(15) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `gender` tinyint(4) DEFAULT NULL,
  `birthdate` datetime DEFAULT NULL,
  `reset_password_key` char(32) COLLATE utf8_persian_ci DEFAULT NULL,
  `reset_password_request_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_group_id` (`fk_group_id`),
  CONSTRAINT `tbl_user_ibfk_1` FOREIGN KEY (`fk_group_id`) REFERENCES `tbl_user_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_persian_ci;


DROP TABLE IF EXISTS `tbl_user_group`;
CREATE TABLE `tbl_user_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(50) CHARACTER SET utf8 COLLATE utf8_persian_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `tbl_user_news`;
CREATE TABLE `tbl_user_news` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fk_news_id` int(10) unsigned NOT NULL,
  `fk_user_id` int(10) unsigned NOT NULL,
  `title` varchar(50) CHARACTER SET utf8 COLLATE utf8_persian_ci NOT NULL,
  `publish_date` datetime NOT NULL,
  `is_flagged` tinyint(4) NOT NULL,
  `is_starred` tinyint(4) NOT NULL,
  `news_content` text CHARACTER SET utf8 COLLATE utf8_persian_ci NOT NULL,
  `edit_date` datetime NOT NULL,
  `tags` text NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_news_id` (`fk_news_id`),
  KEY `fk_user_id` (`fk_user_id`),
  CONSTRAINT `tbl_user_news_ibfk_1` FOREIGN KEY (`fk_news_id`) REFERENCES `tbl_source` (`id`),
  CONSTRAINT `tbl_user_news_ibfk_2` FOREIGN KEY (`fk_user_id`) REFERENCES `tbl_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `tbl_user_verify`;
CREATE TABLE `tbl_user_verify` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fk_user_id` int(10) unsigned NOT NULL,
  `verification_code` varchar(100) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `verification_type` tinyint(4) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_user_id` (`fk_user_id`),
  CONSTRAINT `tbl_user_verify_ibfk_1` FOREIGN KEY (`fk_user_id`) REFERENCES `tbl_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP VIEW IF EXISTS `vw_news_count`;
CREATE TABLE `vw_news_count` (`news_count` bigint(21), `id` int(10) unsigned, `title` varchar(45));


DROP TABLE IF EXISTS `vw_news_count`;
CREATE ALGORITHM=UNDEFINED DEFINER=`live_user`@`localhost` SQL SECURITY DEFINER VIEW `vw_news_count` AS select count(`tf`.`id`) AS `news_count`,`ts`.`id` AS `id`,`ts`.`title` AS `title` from (`tbl_source` `ts` left join (`tbl_news` `tn` join `tbl_feed` `tf` on((`tf`.`id` = `tn`.`fk_feed_id`))) on((`ts`.`id` = `tf`.`fk_source_id`))) group by `ts`.`id`,`ts`.`title`;

/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
-- 2015-01-17 01:17:17


GRANT ALL PRIVILEGES ON live_yeksatr.* To 'live_user'@'localhost' IDENTIFIED BY 'ykstr_thisislive_#$%_';

INSERT INTO `tbl_source` (`id`, `title`, `url`, `icon`) VALUES (1,'FarsNews','http://farsnews.com/', 'farsnews.png');

INSERT INTO `tbl_feed` (`id`, `title`, `fk_source_id`, `url`) VALUES
(1, 'Fars Politics', 1,'http://farsnews.com/rss.php?srv=1'),
(2, 'Fars Economy', 1, 'http://farsnews.com/rss.php?srv=2'),
(3, 'Fars Social', 1, 'http://farsnews.com/rss.php?srv=3'),
(4, 'Fars Sport', 1, 'http://farsnews.com/rss.php?srv=4'),
(5, 'Fars Iternational', 1, 'http://farsnews.com/rss.php?srv=6'),
(6, 'Fars Culture', 1, 'http://farsnews.com/rss.php?srv=7');
