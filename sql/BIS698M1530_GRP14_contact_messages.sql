CREATE DATABASE  IF NOT EXISTS `BIS698M1530_GRP14` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `BIS698M1530_GRP14`;
-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: 141.209.241.57    Database: BIS698M1530_GRP14
-- ------------------------------------------------------
-- Server version	5.5.5-10.3.39-MariaDB-0ubuntu0.20.04.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `contact_messages`
--

DROP TABLE IF EXISTS `contact_messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contact_messages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `message` text NOT NULL,
  `status` enum('unread','read') DEFAULT 'unread',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `parent_id` int(11) DEFAULT NULL,
  `is_reply` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `parent_id` (`parent_id`),
  CONSTRAINT `contact_messages_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `contact_messages` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contact_messages`
--

LOCK TABLES `contact_messages` WRITE;
/*!40000 ALTER TABLE `contact_messages` DISABLE KEYS */;
INSERT INTO `contact_messages` VALUES (1,'gagan','birru1g@gmail.com','Message:','read','2025-04-20 22:05:11',NULL,0),(2,'','','Message:','read','2025-04-20 22:05:14',NULL,0),(3,'gagan','birru1g@gmail.com','hi this is for testing...','read','2025-04-20 22:20:39',NULL,0),(4,'Gagansai Birru','birru1g@gmail.com','hi this is foir testing','read','2025-04-20 23:53:41',NULL,0),(5,'Ice\'n Spice','support@icenspice.com','Dear gagan,\nHi thanks for testing\n\n\n\n\nBest regards,\nIce\'n Spice Support Team','read','2025-04-26 23:27:16',3,1),(6,'Ice\'n Spice','support@icenspice.com','Dear gagan,\n\n\nthanks for reaching us!\n\nwe will get back to you.\n\n\nBest regards,\nIce\'n Spice Support Team','read','2025-04-27 21:47:00',1,1),(7,'Ice\'n Spice','support@icenspice.com','Dear gagan,\n\n\nthanks for reaching us!\n\nwe will get back to you.\n\n\nBest regards,\nIce\'n Spice Support Team','read','2025-04-27 21:47:20',1,1),(8,'Rishith Reddy','padak1r@cmich.edu','It shows my order is palced,but i could not see it on the home screen.','unread','2025-04-28 19:37:03',NULL,0);
/*!40000 ALTER TABLE `contact_messages` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-30  2:40:31
