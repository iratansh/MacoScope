-- MySQL dump 10.13  Distrib 9.0.1, for macos14.4 (arm64)
--
-- Host: localhost    Database: authentication
-- ------------------------------------------------------
-- Server version	9.0.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `account_emailaddress`
--

DROP TABLE IF EXISTS `account_emailaddress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_emailaddress` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(254) NOT NULL,
  `verified` tinyint(1) NOT NULL,
  `primary` tinyint(1) NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `account_emailaddress_user_id_email_987c8728_uniq` (`user_id`,`email`),
  KEY `account_emailaddress_email_03be32b2` (`email`),
  CONSTRAINT `account_emailaddress_user_id_2c513194_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_emailaddress`
--

LOCK TABLES `account_emailaddress` WRITE;
/*!40000 ALTER TABLE `account_emailaddress` DISABLE KEYS */;
/*!40000 ALTER TABLE `account_emailaddress` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `account_emailconfirmation`
--

DROP TABLE IF EXISTS `account_emailconfirmation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_emailconfirmation` (
  `id` int NOT NULL AUTO_INCREMENT,
  `created` datetime(6) NOT NULL,
  `sent` datetime(6) DEFAULT NULL,
  `key` varchar(64) NOT NULL,
  `email_address_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `key` (`key`),
  KEY `account_emailconfirm_email_address_id_5b7f8c58_fk_account_e` (`email_address_id`),
  CONSTRAINT `account_emailconfirm_email_address_id_5b7f8c58_fk_account_e` FOREIGN KEY (`email_address_id`) REFERENCES `account_emailaddress` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_emailconfirmation`
--

LOCK TABLES `account_emailconfirmation` WRITE;
/*!40000 ALTER TABLE `account_emailconfirmation` DISABLE KEYS */;
/*!40000 ALTER TABLE `account_emailconfirmation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=73 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add Token',7,'add_token'),(26,'Can change Token',7,'change_token'),(27,'Can delete Token',7,'delete_token'),(28,'Can view Token',7,'view_token'),(29,'Can add Token',8,'add_tokenproxy'),(30,'Can change Token',8,'change_tokenproxy'),(31,'Can delete Token',8,'delete_tokenproxy'),(32,'Can view Token',8,'view_tokenproxy'),(33,'Can add site',9,'add_site'),(34,'Can change site',9,'change_site'),(35,'Can delete site',9,'delete_site'),(36,'Can view site',9,'view_site'),(37,'Can add email address',10,'add_emailaddress'),(38,'Can change email address',10,'change_emailaddress'),(39,'Can delete email address',10,'delete_emailaddress'),(40,'Can view email address',10,'view_emailaddress'),(41,'Can add email confirmation',11,'add_emailconfirmation'),(42,'Can change email confirmation',11,'change_emailconfirmation'),(43,'Can delete email confirmation',11,'delete_emailconfirmation'),(44,'Can view email confirmation',11,'view_emailconfirmation'),(45,'Can add social account',12,'add_socialaccount'),(46,'Can change social account',12,'change_socialaccount'),(47,'Can delete social account',12,'delete_socialaccount'),(48,'Can view social account',12,'view_socialaccount'),(49,'Can add social application',13,'add_socialapp'),(50,'Can change social application',13,'change_socialapp'),(51,'Can delete social application',13,'delete_socialapp'),(52,'Can view social application',13,'view_socialapp'),(53,'Can add social application token',14,'add_socialtoken'),(54,'Can change social application token',14,'change_socialtoken'),(55,'Can delete social application token',14,'delete_socialtoken'),(56,'Can view social application token',14,'view_socialtoken'),(57,'Can add user',15,'add_customuser'),(58,'Can change user',15,'change_customuser'),(59,'Can delete user',15,'delete_customuser'),(60,'Can view user',15,'view_customuser'),(61,'Can add economic data',16,'add_economicdata'),(62,'Can change economic data',16,'change_economicdata'),(63,'Can delete economic data',16,'delete_economicdata'),(64,'Can view economic data',16,'view_economicdata'),(65,'Can add prediction',17,'add_prediction'),(66,'Can change prediction',17,'change_prediction'),(67,'Can delete prediction',17,'delete_prediction'),(68,'Can view prediction',17,'view_prediction'),(69,'Can add economic indicator',18,'add_economicindicator'),(70,'Can change economic indicator',18,'change_economicindicator'),(71,'Can delete economic indicator',18,'delete_economicindicator'),(72,'Can view economic indicator',18,'view_economicindicator');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (38,'pbkdf2_sha256$600000$4CPE3SUU5UHkrwo7mW6DyF$LlgHINM8pAUOSeqfLfiQ7cWnaEGdnNC4VcDdCGy4ksU=','2024-11-17 00:53:52.022753',0,'ishaanratanshi1','','','ishaanratanshi1@gmail.com',0,1,'2024-09-01 16:54:10.876219'),(39,'pbkdf2_sha256$600000$zOcYXfMms8oljfsYL61gon$EoGQzhiWsgFENZ1V7kK2VyEoCvVhlRI6v4GtZdHPj0g=','2024-09-14 20:24:11.565580',0,'i.ratanshi1','','','i.ratanshi1@gmail.com',0,1,'2024-09-14 20:23:25.859690'),(40,'pbkdf2_sha256$600000$ted3gyxUHoyyHnmUfkLLGK$VLkeYmPZKxAhYuy6whETxVSmhAECld6/lijwaNKeFuE=','2024-09-14 20:35:38.569585',1,'ishaanratanshi','','','i.ratanshi1@gmail.com',1,1,'2024-09-14 20:35:31.772109'),(41,'pbkdf2_sha256$600000$Eeq2l2dLzJKRQmPkpp7xlB$LqVvQK+m9r5MnkBpCL4ObXeOLyAQuPj0wh1ngRk/qi8=','2024-09-15 20:19:18.365079',0,'carl.pong4','','','carl.pong4@gmail.com',0,1,'2024-09-15 17:39:55.636558'),(42,'pbkdf2_sha256$600000$rKNnrxBpbgMXMhLJrqG4VY$Wqhh1jYliiYEjfceGDyABMJmJUWBdO4/hmtthic6m3c=',NULL,0,'testuser1726430967','','','testuser1726430967@gmail.com',0,0,'2024-09-15 20:09:27.785626'),(43,'pbkdf2_sha256$600000$gobMviilYxDLQ9PuuESxSS$MMA7ASxjJN/c/knJIJVVDatKXaM++VQ3/NYKU97ipMA=',NULL,0,'testuser1726431447','','','testuser1726431447@gmail.com',0,0,'2024-09-15 20:17:27.256553'),(44,'pbkdf2_sha256$600000$0JOjw0ujGduGmUThy43mlx$fkuvkYoW3ibWLqYs5T+0g7RcO3KUzXs70ZRa9kGZdsw=',NULL,0,'testuser1726431571','','','testuser1726431571@gmail.com',0,0,'2024-09-15 20:19:31.254524'),(45,'pbkdf2_sha256$600000$WdnoImFmKJ2RqeiUrkwA8j$axxfAVF6I2hHcwtO1t3sK0s18GGdeGowXOQ9sfVI3JY=','2024-09-24 01:22:05.179625',0,'iratansh','','','iratansh@ualberta.ca',0,1,'2024-09-24 01:21:36.045246'),(46,'pbkdf2_sha256$600000$8vz1AwoBjIT3bkQuoTJujl$NIH3S8uW5uGDPGN7c/e9yBqFzNbFVkncN13lMttnEyo=','2024-11-12 16:09:12.335632',1,'iratanshi','','','i.ratanshi1@gmail.com',1,1,'2024-11-12 16:08:16.862240');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `authtoken_token`
--

DROP TABLE IF EXISTS `authtoken_token`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `authtoken_token` (
  `key` varchar(40) NOT NULL,
  `created` datetime(6) NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`key`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `authtoken_token_user_id_35299eff_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authtoken_token`
--

LOCK TABLES `authtoken_token` WRITE;
/*!40000 ALTER TABLE `authtoken_token` DISABLE KEYS */;
/*!40000 ALTER TABLE `authtoken_token` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (10,'account','emailaddress'),(11,'account','emailconfirmation'),(1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(15,'authentication','customuser'),(7,'authtoken','token'),(8,'authtoken','tokenproxy'),(5,'contenttypes','contenttype'),(16,'forecasts','economicdata'),(18,'forecasts','economicindicator'),(17,'forecasts','prediction'),(6,'sessions','session'),(9,'sites','site'),(12,'socialaccount','socialaccount'),(13,'socialaccount','socialapp'),(14,'socialaccount','socialtoken');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2024-08-25 23:45:38.418333'),(12,'admin','0001_initial','2024-08-25 23:45:38.728724'),(13,'admin','0002_logentry_remove_auto_add','2024-08-25 23:45:38.733518'),(14,'admin','0003_logentry_add_action_flag_choices','2024-08-25 23:45:38.738525'),(15,'contenttypes','0002_remove_content_type_name','2024-08-25 23:45:38.763318'),(27,'authtoken','0001_initial','2024-08-25 23:45:38.913677'),(28,'authtoken','0002_auto_20160226_1747','2024-08-25 23:45:38.929612'),(29,'authtoken','0003_tokenproxy','2024-08-25 23:45:38.930998'),(30,'authtoken','0004_alter_tokenproxy_options','2024-08-25 23:45:38.933911'),(31,'sessions','0001_initial','2024-08-25 23:45:38.942021'),(32,'sites','0001_initial','2024-08-25 23:45:38.946410'),(33,'sites','0002_alter_domain_unique','2024-08-25 23:45:38.963368'),(34,'socialaccount','0001_initial','2024-08-25 23:45:39.137824'),(35,'socialaccount','0002_token_max_lengths','2024-08-25 23:45:39.162129'),(36,'socialaccount','0003_extra_data_default_dict','2024-08-25 23:45:39.167865'),(37,'socialaccount','0004_app_provider_id_settings','2024-08-25 23:45:39.210629'),(38,'socialaccount','0005_socialtoken_nullable_app','2024-08-25 23:45:39.241302'),(39,'socialaccount','0006_alter_socialaccount_extra_data','2024-08-25 23:45:39.258317'),(40,'authentication','0001_initial','2024-09-02 00:13:11.253932'),(41,'django_registration','0001_initial','2024-09-02 00:13:11.257364'),(42,'forecasts','0001_initial','2024-09-02 00:13:11.293817'),(43,'authentication','0002_delete_customuser','2024-09-22 15:34:46.249606'),(44,'forecasts','0002_economicindicator_delete_economicdata','2024-11-14 23:47:22.934487'),(45,'forecasts','0003_alter_economicindicator_table','2024-11-14 23:47:22.939514');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('0mv0ah9j1a20vap7lrtccqpv97zwefhp','.eJxVjEEOwiAQRe_C2pBCodO6dO8ZyDAzSNVAUtqV8e7apAvd_vfef6mA25rD1mQJM6uz6kd1-h0j0kPKTviO5VY11bIuc9S7og_a9LWyPC-H-3eQseVvLWlyJAnBR4_ClNCB-DhYsOTIJCBgtDgwj8ZwJD-x6dCkvoPonWX1_gBVJTl-:1tBkl1:qn9YksjW_zXQiosznnTvCbH4m_vauSjdJoCaWeWgZR8','2024-11-29 01:04:19.404529'),('25g6p6ayqye9v45f215l489xkwfqwge1','.eJxVjEEOwiAQRe_C2pBCodO6dO8ZyDAzSNVAUtqV8e7apAvd_vfef6mA25rD1mQJM6uz6kd1-h0j0kPKTviO5VY11bIuc9S7og_a9LWyPC-H-3eQseVvLWlyJAnBR4_ClNCB-DhYsOTIJCBgtDgwj8ZwJD-x6dCkvoPonWX1_gBVJTl-:1tCT4a:8_38AXBw5D9ScQhH2_Gnu22-Ds12Cv9DwZBWJfIGKLQ','2024-12-01 00:23:28.100402'),('2btw1nbvlqmcylc5sp0k7sey2ial17j8','.eJxVjEEOwiAQRe_C2pBCodO6dO8ZyDAzSNVAUtqV8e7apAvd_vfef6mA25rD1mQJM6uz6kd1-h0j0kPKTviO5VY11bIuc9S7og_a9LWyPC-H-3eQseVvLWlyJAnBR4_ClNCB-DhYsOTIJCBgtDgwj8ZwJD-x6dCkvoPonWX1_gBVJTl-:1tCTY0:gv9L1x-c-42RnzQg8nqVp76DqcJSfgVtXQTF9r-kpKQ','2024-12-01 00:53:52.028513'),('2zmzcrgzskkzewhkkxctc8zyfnsndqmq','.eJxVjEEOwiAQRe_C2pBCodO6dO8ZyDAzSNVAUtqV8e7apAvd_vfef6mA25rD1mQJM6uz6kd1-h0j0kPKTviO5VY11bIuc9S7og_a9LWyPC-H-3eQseVvLWlyJAnBR4_ClNCB-DhYsOTIJCBgtDgwj8ZwJD-x6dCkvoPonWX1_gBVJTl-:1tAxbf:u186EFEGRgqiUwP5zM1U8QJ0-04-APf3JkRNKkWbHfA','2024-11-26 20:35:23.196384'),('3wsnuuagxnfr7t0vrmptusaqpuhvqnq5','.eJxVjEEOwiAQRe_C2pBCodO6dO8ZyDAzSNVAUtqV8e7apAvd_vfef6mA25rD1mQJM6uz6kd1-h0j0kPKTviO5VY11bIuc9S7og_a9LWyPC-H-3eQseVvLWlyJAnBR4_ClNCB-DhYsOTIJCBgtDgwj8ZwJD-x6dCkvoPonWX1_gBVJTl-:1tBlL4:gUMZCP3lx0klz2J7Sk_yHGIJyFUeumVyRrzZN6sCFBQ','2024-11-29 01:41:34.270060'),('42e9fmn0tgux0u0yijip5vt1xi8x6jmn','.eJxVjEEOwiAQRe_C2pBCodO6dO8ZyDAzSNVAUtqV8e7apAvd_vfef6mA25rD1mQJM6uz6kd1-h0j0kPKTviO5VY11bIuc9S7og_a9LWyPC-H-3eQseVvLWlyJAnBR4_ClNCB-DhYsOTIJCBgtDgwj8ZwJD-x6dCkvoPonWX1_gBVJTl-:1tAxg0:XjOEWHWrUlHNi6TdVqP0FE8UoQFhdLVwX0jf69QXRoE','2024-11-26 20:39:52.510692'),('5qp3xxrn769ahva6s4bd9aa72vzpu7cc','.eJxVjEEOwiAQRe_C2pBCodO6dO8ZyDAzSNVAUtqV8e7apAvd_vfef6mA25rD1mQJM6uz6kd1-h0j0kPKTviO5VY11bIuc9S7og_a9LWyPC-H-3eQseVvLWlyJAnBR4_ClNCB-DhYsOTIJCBgtDgwj8ZwJD-x6dCkvoPonWX1_gBVJTl-:1tBjgK:OBWYNcLMoOrtg6nOJPUwsPkP7k3CLqeL3kUtYDEsbto','2024-11-28 23:55:24.937958'),('61p0kolyqmr4ht2jfyid67aeecful19z','.eJxVjEEOwiAQRe_C2pBCodO6dO8ZyDAzSNVAUtqV8e7apAvd_vfef6mA25rD1mQJM6uz6kd1-h0j0kPKTviO5VY11bIuc9S7og_a9LWyPC-H-3eQseVvLWlyJAnBR4_ClNCB-DhYsOTIJCBgtDgwj8ZwJD-x6dCkvoPonWX1_gBVJTl-:1tAy1A:0kT0VgJCjHLeKWeo8AAOIgjmEz4DC5Po3pmOMP1_ZLw','2024-11-26 21:01:44.522822'),('64xjbnk038yiugnqc4an2dql31b1py8k','.eJxVjEEOwiAQRe_C2pBCodO6dO8ZyDAzSNVAUtqV8e7apAvd_vfef6mA25rD1mQJM6uz6kd1-h0j0kPKTviO5VY11bIuc9S7og_a9LWyPC-H-3eQseVvLWlyJAnBR4_ClNCB-DhYsOTIJCBgtDgwj8ZwJD-x6dCkvoPonWX1_gBVJTl-:1tAxVd:iinI_dEL7XQsZqR7cpOdOCDGMeHHGhy0S_z03mvv-hE','2024-11-26 20:29:09.794833'),('6fuldv71oatii51t8bg8fhknooxxj354','.eJxVjEEOwiAQRe_C2pBCodO6dO8ZyDAzSNVAUtqV8e7apAvd_vfef6mA25rD1mQJM6uz6kd1-h0j0kPKTviO5VY11bIuc9S7og_a9LWyPC-H-3eQseVvLWlyJAnBR4_ClNCB-DhYsOTIJCBgtDgwj8ZwJD-x6dCkvoPonWX1_gBVJTl-:1tCSf2:Tm03wsAGSYtoRLjDUeUM5cgp3Af613vv1DwCZtHwcGw','2024-11-30 23:57:04.262031'),('6jhj8q38cvlhda2p5ii3xnwx4eurygwy','.eJxVjEEOwiAQRe_C2pBCodO6dO8ZyDAzSNVAUtqV8e7apAvd_vfef6mA25rD1mQJM6uz6kd1-h0j0kPKTviO5VY11bIuc9S7og_a9LWyPC-H-3eQseVvLWlyJAnBR4_ClNCB-DhYsOTIJCBgtDgwj8ZwJD-x6dCkvoPonWX1_gBVJTl-:1tAxp2:pxi2dPNbcIvBCLiEIUO_Huaa0M0aoScpcy3bEOmsFrQ','2024-11-26 20:49:12.092148'),('6nyuvmrjd1wvy3mginyenpu8ukha9gn7','.eJxVjEEOwiAQRe_C2pBCodO6dO8ZyDAzSNVAUtqV8e7apAvd_vfef6mA25rD1mQJM6uz6kd1-h0j0kPKTviO5VY11bIuc9S7og_a9LWyPC-H-3eQseVvLWlyJAnBR4_ClNCB-DhYsOTIJCBgtDgwj8ZwJD-x6dCkvoPonWX1_gBVJTl-:1tAxUV:B2SG9LoqtOfGiwdA0mgm4g-fqySkVQWiGW0oRv_SJ_w','2024-11-26 20:27:59.995342'),('8714g4lezsh98f4lw8jxepr7qe4c2rjm','.eJxVjEEOwiAQRe_C2pBCodO6dO8ZyDAzSNVAUtqV8e7apAvd_vfef6mA25rD1mQJM6uz6kd1-h0j0kPKTviO5VY11bIuc9S7og_a9LWyPC-H-3eQseVvLWlyJAnBR4_ClNCB-DhYsOTIJCBgtDgwj8ZwJD-x6dCkvoPonWX1_gBVJTl-:1tAy11:2jG2PbQVrBDmn4Al2fJJDk0O9OZrgYYGeZy7hxp3LzE','2024-11-26 21:01:35.168105'),('95v6x0yja5h5egq3bkj5ynexdvt2m4p1','.eJxVjEEOwiAQRe_C2pBCodO6dO8ZyDAzSNVAUtqV8e7apAvd_vfef6mA25rD1mQJM6uz6kd1-h0j0kPKTviO5VY11bIuc9S7og_a9LWyPC-H-3eQseVvLWlyJAnBR4_ClNCB-DhYsOTIJCBgtDgwj8ZwJD-x6dCkvoPonWX1_gBVJTl-:1tCSNB:bSSMPwtg1uypSvW0pTddU5hfgh1wExvM_gFS9CIhrHA','2024-11-30 23:38:37.371304'),('9fkm7yh2p23m6lhlgv8fynqltrj5u3ow','.eJxVjEEOwiAQRe_C2pBCodO6dO8ZyDAzSNVAUtqV8e7apAvd_vfef6mA25rD1mQJM6uz6kd1-h0j0kPKTviO5VY11bIuc9S7og_a9LWyPC-H-3eQseVvLWlyJAnBR4_ClNCB-DhYsOTIJCBgtDgwj8ZwJD-x6dCkvoPonWX1_gBVJTl-:1tBk2J:dlUWhBPVCVR6xPLCwYkFbEK1xavYB9_MK7c0oPuaQ5Y','2024-11-29 00:18:07.781230'),('9tgdyhyj1k27boaax43zo500j66x0wy3','.eJxVjEEOwiAQRe_C2pBCodO6dO8ZyDAzSNVAUtqV8e7apAvd_vfef6mA25rD1mQJM6uz6kd1-h0j0kPKTviO5VY11bIuc9S7og_a9LWyPC-H-3eQseVvLWlyJAnBR4_ClNCB-DhYsOTIJCBgtDgwj8ZwJD-x6dCkvoPonWX1_gBVJTl-:1tB1yN:yiVLumSkFF5lwlco06h0I50fSPWFory6KjWkdN6fglE','2024-11-27 01:15:07.531793'),('b1bil2n8p14vdflni46aooqe5ksfnzie','.eJxVjEEOwiAQRe_C2pBCodO6dO8ZyDAzSNVAUtqV8e7apAvd_vfef6mA25rD1mQJM6uz6kd1-h0j0kPKTviO5VY11bIuc9S7og_a9LWyPC-H-3eQseVvLWlyJAnBR4_ClNCB-DhYsOTIJCBgtDgwj8ZwJD-x6dCkvoPonWX1_gBVJTl-:1tBjZy:S5xmHcBMXvqKf5-2SPIOsogdgTzYMh8EUgsrF0OiMvo','2024-11-28 23:48:50.479314'),('chwnlf1t1tst2956rc6xh2em5m605oz8','.eJxVjEEOwiAQRe_C2pBCodO6dO8ZyDAzSNVAUtqV8e7apAvd_vfef6mA25rD1mQJM6uz6kd1-h0j0kPKTviO5VY11bIuc9S7og_a9LWyPC-H-3eQseVvLWlyJAnBR4_ClNCB-DhYsOTIJCBgtDgwj8ZwJD-x6dCkvoPonWX1_gBVJTl-:1tAtjK:wfT2gEVN4L4dLKX8uJsbsiqfxMqLu_Bp_xpUpxQBZ-A','2024-11-26 16:27:02.051340'),('cmg61q1ghzdm2cg7ewu3j30u7vsqv8jl','.eJxVjEEOwiAQRe_C2pBCodO6dO8ZyDAzSNVAUtqV8e7apAvd_vfef6mA25rD1mQJM6uz6kd1-h0j0kPKTviO5VY11bIuc9S7og_a9LWyPC-H-3eQseVvLWlyJAnBR4_ClNCB-DhYsOTIJCBgtDgwj8ZwJD-x6dCkvoPonWX1_gBVJTl-:1tAxWT:7tntIQENH0Dt6VGe6afY0EEDp5ZtB0HhdwzNJQuZBaA','2024-11-26 20:30:01.652009'),('cxkjm66csuqqwjsfa3p850ub6quuuj72','.eJxVjEEOwiAQRe_C2pBCodO6dO8ZyDAzSNVAUtqV8e7apAvd_vfef6mA25rD1mQJM6uz6kd1-h0j0kPKTviO5VY11bIuc9S7og_a9LWyPC-H-3eQseVvLWlyJAnBR4_ClNCB-DhYsOTIJCBgtDgwj8ZwJD-x6dCkvoPonWX1_gBVJTl-:1tAxow:HYZ-sy8_dOiKn2sB8GG_eV1R7DHJGHOU2ByTnAW9tPI','2024-11-26 20:49:06.618159'),('evi1m2gwfgh8mwh9ln29e5ey32dl7szd','.eJxVjEEOwiAQRe_C2pBCodO6dO8ZyDAzSNVAUtqV8e7apAvd_vfef6mA25rD1mQJM6uz6kd1-h0j0kPKTviO5VY11bIuc9S7og_a9LWyPC-H-3eQseVvLWlyJAnBR4_ClNCB-DhYsOTIJCBgtDgwj8ZwJD-x6dCkvoPonWX1_gBVJTl-:1tAxV4:1s5WgX3W7fjlYSf_DPi524_mvQi2DpBKUFQavTvB70Y','2024-11-26 20:28:34.536232'),('gix4owmx1y7xmf6wgck3j6xtjtuu8lpt','.eJxVjEEOwiAQRe_C2pBCodO6dO8ZyDAzSNVAUtqV8e7apAvd_vfef6mA25rD1mQJM6uz6kd1-h0j0kPKTviO5VY11bIuc9S7og_a9LWyPC-H-3eQseVvLWlyJAnBR4_ClNCB-DhYsOTIJCBgtDgwj8ZwJD-x6dCkvoPonWX1_gBVJTl-:1tCTOd:fTwDdwe-gkql8VmyJmp8I3BIG5CR3OptcxQN3Hj8JsE','2024-12-01 00:44:11.602202'),('h4y5iisb8k6bff6vgjuclftoat1yhdam','.eJxVjEEOwiAQRe_C2pBCodO6dO8ZyDAzSNVAUtqV8e7apAvd_vfef6mA25rD1mQJM6uz6kd1-h0j0kPKTviO5VY11bIuc9S7og_a9LWyPC-H-3eQseVvLWlyJAnBR4_ClNCB-DhYsOTIJCBgtDgwj8ZwJD-x6dCkvoPonWX1_gBVJTl-:1tAtld:aIZdXxYsk4SthkRuOjmniB_n6vpeIxMFyAG5cqzUGvo','2024-11-26 16:29:25.549203'),('iqgz9mmp1jz2xhdbzxs6r1u5gqc4n5hz','.eJxVjEEOwiAQRe_C2pBCodO6dO8ZyDAzSNVAUtqV8e7apAvd_vfef6mA25rD1mQJM6uz6kd1-h0j0kPKTviO5VY11bIuc9S7og_a9LWyPC-H-3eQseVvLWlyJAnBR4_ClNCB-DhYsOTIJCBgtDgwj8ZwJD-x6dCkvoPonWX1_gBVJTl-:1tBjrj:92JGV6n3GjfNpVRHqIXKblPbCRfZZwOUJMxQ9TN2q3k','2024-11-29 00:07:11.627731'),('jnscfyi5mq9hh8mn25i2tyf9mqbg2uln','.eJxVjEEOwiAQRe_C2pBCodO6dO8ZyDAzSNVAUtqV8e7apAvd_vfef6mA25rD1mQJM6uz6kd1-h0j0kPKTviO5VY11bIuc9S7og_a9LWyPC-H-3eQseVvLWlyJAnBR4_ClNCB-DhYsOTIJCBgtDgwj8ZwJD-x6dCkvoPonWX1_gBVJTl-:1tB2Hj:7QNYbfPs_JgeDajE7aCBErf3qcPDc6tIB8ChIqQIZ58','2024-11-27 01:35:07.247302'),('li7g6c0obzzaag9790ei4c1jcghxubsi','.eJxVjEEOwiAQRe_C2pBCodO6dO8ZyDAzSNVAUtqV8e7apAvd_vfef6mA25rD1mQJM6uz6kd1-h0j0kPKTviO5VY11bIuc9S7og_a9LWyPC-H-3eQseVvLWlyJAnBR4_ClNCB-DhYsOTIJCBgtDgwj8ZwJD-x6dCkvoPonWX1_gBVJTl-:1tCTNO:zKXWd8hhOtxuoPi0HzhEVeATvdAS4-rxMmxn3TXh7_4','2024-12-01 00:42:54.529954'),('lnc95b2f6wqvylp525bya5dddsewmy98','.eJxVjEEOwiAQRe_C2pBCodO6dO8ZyDAzSNVAUtqV8e7apAvd_vfef6mA25rD1mQJM6uz6kd1-h0j0kPKTviO5VY11bIuc9S7og_a9LWyPC-H-3eQseVvLWlyJAnBR4_ClNCB-DhYsOTIJCBgtDgwj8ZwJD-x6dCkvoPonWX1_gBVJTl-:1tCTGj:6S9hAqFScgnOHuBuzocZEbUlaPQRi0Ipz20Dk8GJ348','2024-12-01 00:36:01.388227'),('n2qvpsws4tqpdzd8g0qofaigc512kpx1','.eJxVjEEOwiAQRe_C2pBCodO6dO8ZyDAzSNVAUtqV8e7apAvd_vfef6mA25rD1mQJM6uz6kd1-h0j0kPKTviO5VY11bIuc9S7og_a9LWyPC-H-3eQseVvLWlyJAnBR4_ClNCB-DhYsOTIJCBgtDgwj8ZwJD-x6dCkvoPonWX1_gBVJTl-:1tAy0y:0HnKeAnI8tGv07A9pjMsUZBGP1IubJDuu2zuA0XsOew','2024-11-26 21:01:32.663350'),('r4z0bd2k0eh3nasub45ca3siijes6ba8','.eJxVjEEOwiAQRe_C2pBCodO6dO8ZyDAzSNVAUtqV8e7apAvd_vfef6mA25rD1mQJM6uz6kd1-h0j0kPKTviO5VY11bIuc9S7og_a9LWyPC-H-3eQseVvLWlyJAnBR4_ClNCB-DhYsOTIJCBgtDgwj8ZwJD-x6dCkvoPonWX1_gBVJTl-:1tBjxw:h1e-jKq4KCuMzXHcm-Hx2n8z_Jjt0vFNznGnBQLkK2w','2024-11-29 00:13:36.377409'),('sdgqf2nxplon6zud4hwnl59y6k9u10qo','.eJxVjEEOwiAQRe_C2pBCodO6dO8ZyDAzSNVAUtqV8e7apAvd_vfef6mA25rD1mQJM6uz6kd1-h0j0kPKTviO5VY11bIuc9S7og_a9LWyPC-H-3eQseVvLWlyJAnBR4_ClNCB-DhYsOTIJCBgtDgwj8ZwJD-x6dCkvoPonWX1_gBVJTl-:1tAtqY:nEPoADqOUlSi8M-Y6Aja1rpJ2csVMOFp6X9tYJK2b28','2024-11-26 16:34:30.700502'),('uzo2aqykekv7uhyt29wfzg0rt4xbv7kh','.eJxVjEEOwiAQRe_C2pBCodO6dO8ZyDAzSNVAUtqV8e7apAvd_vfef6mA25rD1mQJM6uz6kd1-h0j0kPKTviO5VY11bIuc9S7og_a9LWyPC-H-3eQseVvLWlyJAnBR4_ClNCB-DhYsOTIJCBgtDgwj8ZwJD-x6dCkvoPonWX1_gBVJTl-:1tAtmh:cbEKsWneV_GkrfOlYCoNE58nVWLP200yRJbyJORuNGg','2024-11-26 16:30:31.071644'),('v6ddwc75v737fm6s1ga4y02snssxwcjy','.eJxVjEEOwiAQRe_C2pBCodO6dO8ZyDAzSNVAUtqV8e7apAvd_vfef6mA25rD1mQJM6uz6kd1-h0j0kPKTviO5VY11bIuc9S7og_a9LWyPC-H-3eQseVvLWlyJAnBR4_ClNCB-DhYsOTIJCBgtDgwj8ZwJD-x6dCkvoPonWX1_gBVJTl-:1tAxOq:nIzjdutmtsaa64uoRf-KLUWvoxDphRfpuadcr_oEOwU','2024-11-26 20:22:08.663455'),('vbkm4bds4h956ort5ykr23t8iqvaw15c','.eJxVjEEOwiAQRe_C2pBCodO6dO8ZyDAzSNVAUtqV8e7apAvd_vfef6mA25rD1mQJM6uz6kd1-h0j0kPKTviO5VY11bIuc9S7og_a9LWyPC-H-3eQseVvLWlyJAnBR4_ClNCB-DhYsOTIJCBgtDgwj8ZwJD-x6dCkvoPonWX1_gBVJTl-:1tAtpm:7PVYYg0_PtQmeUp9RjcnT0sluE6hiD-7z-ojGKE1-xg','2024-11-26 16:33:42.369138'),('ve5bp62mbdo2o8fdav3jn7tegdbjwtqp','.eJxVjEEOwiAQRe_C2pBCodO6dO8ZyDAzSNVAUtqV8e7apAvd_vfef6mA25rD1mQJM6uz6kd1-h0j0kPKTviO5VY11bIuc9S7og_a9LWyPC-H-3eQseVvLWlyJAnBR4_ClNCB-DhYsOTIJCBgtDgwj8ZwJD-x6dCkvoPonWX1_gBVJTl-:1tBjqs:7oq2bKKbcwJ1O9NsjmEWB904_u7kEIMonanKIL6dWfI','2024-11-29 00:06:18.628422'),('vxwvufhglf7hpf69jbjspfpkrtaw9wth','.eJxVjEEOwiAQRe_C2pBCodO6dO8ZyDAzSNVAUtqV8e7apAvd_vfef6mA25rD1mQJM6uz6kd1-h0j0kPKTviO5VY11bIuc9S7og_a9LWyPC-H-3eQseVvLWlyJAnBR4_ClNCB-DhYsOTIJCBgtDgwj8ZwJD-x6dCkvoPonWX1_gBVJTl-:1tBkie:jGmmvdI9A0EPkmqmmq6mi1Q-MvqGdFfdql9Ps8aIbUw','2024-11-29 01:01:52.897481'),('x1gwcbqr3prsrq0pym1c3i4lqty68z7s','.eJxVjEEOwiAQRe_C2pBCodO6dO8ZyDAzSNVAUtqV8e7apAvd_vfef6mA25rD1mQJM6uz6kd1-h0j0kPKTviO5VY11bIuc9S7og_a9LWyPC-H-3eQseVvLWlyJAnBR4_ClNCB-DhYsOTIJCBgtDgwj8ZwJD-x6dCkvoPonWX1_gBVJTl-:1tAxhg:MZ62yb6_NzVPAtFI7jcuoNEYj8rvTi39sYumkAFjOL4','2024-11-26 20:41:36.061481'),('xatqwjhffzukusquyunh15fkz8ify9pe','.eJxVjEEOwiAQRe_C2pBCodO6dO8ZyDAzSNVAUtqV8e7apAvd_vfef6mA25rD1mQJM6uz6kd1-h0j0kPKTviO5VY11bIuc9S7og_a9LWyPC-H-3eQseVvLWlyJAnBR4_ClNCB-DhYsOTIJCBgtDgwj8ZwJD-x6dCkvoPonWX1_gBVJTl-:1tBjhS:t8Nb_QJWBFBLE5Um9qNqnDVr1EtvVNZxNVZZOPShMro','2024-11-28 23:56:34.183031'),('yb8wj5uj3gl3bwy7pw1wbmhpg105kodq','.eJxVjEEOwiAQRe_C2pBCodO6dO8ZyDAzSNVAUtqV8e7apAvd_vfef6mA25rD1mQJM6uz6kd1-h0j0kPKTviO5VY11bIuc9S7og_a9LWyPC-H-3eQseVvLWlyJAnBR4_ClNCB-DhYsOTIJCBgtDgwj8ZwJD-x6dCkvoPonWX1_gBVJTl-:1tBjvD:gJGKe-bDkpxm_x3co15w44W3NYog976_saBJpzAySjI','2024-11-29 00:10:47.450153'),('ymwl6xncrwkxcxv5rmauny51ku8lapfa','.eJxVjEEOwiAQRe_C2pBCodO6dO8ZyDAzSNVAUtqV8e7apAvd_vfef6mA25rD1mQJM6uz6kd1-h0j0kPKTviO5VY11bIuc9S7og_a9LWyPC-H-3eQseVvLWlyJAnBR4_ClNCB-DhYsOTIJCBgtDgwj8ZwJD-x6dCkvoPonWX1_gBVJTl-:1tAxVs:EJTvf3EW8LMh71GrFXfEoCmpq2oChUV5APnVKhNsiNQ','2024-11-26 20:29:24.512565'),('zsf65zp3thzzazk3sb50dvcq2iaqgglt','.eJxVjEEOwiAQRe_C2pBCodO6dO8ZyDAzSNVAUtqV8e7apAvd_vfef6mA25rD1mQJM6uz6kd1-h0j0kPKTviO5VY11bIuc9S7og_a9LWyPC-H-3eQseVvLWlyJAnBR4_ClNCB-DhYsOTIJCBgtDgwj8ZwJD-x6dCkvoPonWX1_gBVJTl-:1tCTPi:lBBm6wiaQzwPsRF4gTPbD4pQbs1mGPI-BlqXm59UQo4','2024-12-01 00:45:18.325911');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_site` (
  `id` int NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_site_domain_a2e37b91_uniq` (`domain`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_site`
--

LOCK TABLES `django_site` WRITE;
/*!40000 ALTER TABLE `django_site` DISABLE KEYS */;
INSERT INTO `django_site` VALUES (1,'example.com','example.com');
/*!40000 ALTER TABLE `django_site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `socialaccount_socialaccount`
--

DROP TABLE IF EXISTS `socialaccount_socialaccount`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `socialaccount_socialaccount` (
  `id` int NOT NULL AUTO_INCREMENT,
  `provider` varchar(200) NOT NULL,
  `uid` varchar(191) NOT NULL,
  `last_login` datetime(6) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `extra_data` json NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `socialaccount_socialaccount_provider_uid_fc810c6e_uniq` (`provider`,`uid`),
  KEY `socialaccount_socialaccount_user_id_8146e70c_fk_auth_user_id` (`user_id`),
  CONSTRAINT `socialaccount_socialaccount_user_id_8146e70c_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `socialaccount_socialaccount`
--

LOCK TABLES `socialaccount_socialaccount` WRITE;
/*!40000 ALTER TABLE `socialaccount_socialaccount` DISABLE KEYS */;
/*!40000 ALTER TABLE `socialaccount_socialaccount` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `socialaccount_socialapp`
--

DROP TABLE IF EXISTS `socialaccount_socialapp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `socialaccount_socialapp` (
  `id` int NOT NULL AUTO_INCREMENT,
  `provider` varchar(30) NOT NULL,
  `name` varchar(40) NOT NULL,
  `client_id` varchar(191) NOT NULL,
  `secret` varchar(191) NOT NULL,
  `key` varchar(191) NOT NULL,
  `provider_id` varchar(200) NOT NULL,
  `settings` json NOT NULL DEFAULT (_utf8mb3'{}'),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `socialaccount_socialapp`
--

LOCK TABLES `socialaccount_socialapp` WRITE;
/*!40000 ALTER TABLE `socialaccount_socialapp` DISABLE KEYS */;
/*!40000 ALTER TABLE `socialaccount_socialapp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `socialaccount_socialapp_sites`
--

DROP TABLE IF EXISTS `socialaccount_socialapp_sites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `socialaccount_socialapp_sites` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `socialapp_id` int NOT NULL,
  `site_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `socialaccount_socialapp_sites_socialapp_id_site_id_71a9a768_uniq` (`socialapp_id`,`site_id`),
  KEY `socialaccount_socialapp_sites_site_id_2579dee5_fk_django_site_id` (`site_id`),
  CONSTRAINT `socialaccount_social_socialapp_id_97fb6e7d_fk_socialacc` FOREIGN KEY (`socialapp_id`) REFERENCES `socialaccount_socialapp` (`id`),
  CONSTRAINT `socialaccount_socialapp_sites_site_id_2579dee5_fk_django_site_id` FOREIGN KEY (`site_id`) REFERENCES `django_site` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `socialaccount_socialapp_sites`
--

LOCK TABLES `socialaccount_socialapp_sites` WRITE;
/*!40000 ALTER TABLE `socialaccount_socialapp_sites` DISABLE KEYS */;
/*!40000 ALTER TABLE `socialaccount_socialapp_sites` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `socialaccount_socialtoken`
--

DROP TABLE IF EXISTS `socialaccount_socialtoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `socialaccount_socialtoken` (
  `id` int NOT NULL AUTO_INCREMENT,
  `token` longtext NOT NULL,
  `token_secret` longtext NOT NULL,
  `expires_at` datetime(6) DEFAULT NULL,
  `account_id` int NOT NULL,
  `app_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `socialaccount_socialtoken_app_id_account_id_fca4e0ac_uniq` (`app_id`,`account_id`),
  KEY `socialaccount_social_account_id_951f210e_fk_socialacc` (`account_id`),
  CONSTRAINT `socialaccount_social_account_id_951f210e_fk_socialacc` FOREIGN KEY (`account_id`) REFERENCES `socialaccount_socialaccount` (`id`),
  CONSTRAINT `socialaccount_social_app_id_636a42d7_fk_socialacc` FOREIGN KEY (`app_id`) REFERENCES `socialaccount_socialapp` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `socialaccount_socialtoken`
--

LOCK TABLES `socialaccount_socialtoken` WRITE;
/*!40000 ALTER TABLE `socialaccount_socialtoken` DISABLE KEYS */;
/*!40000 ALTER TABLE `socialaccount_socialtoken` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-11-21 20:33:57
