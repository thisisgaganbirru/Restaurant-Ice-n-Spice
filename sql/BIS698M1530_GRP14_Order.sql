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
-- Table structure for table `Order`
--

DROP TABLE IF EXISTS `Order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Order` (
  `OrderID` int(7) NOT NULL AUTO_INCREMENT,
  `UserID` int(11) NOT NULL,
  `orderIDByUser` int(11) NOT NULL,
  `UserName` varchar(255) DEFAULT NULL,
  `Item_list` text DEFAULT NULL,
  `Total_price` decimal(10,2) NOT NULL,
  `Status` varchar(50) DEFAULT NULL,
  `CreatedAT` datetime DEFAULT current_timestamp(),
  `orderStatus` enum('pending','preparing','ready for pickup','delivered') DEFAULT 'pending',
  `statusUpdateAt` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`OrderID`),
  KEY `Order_ibfk_1` (`UserID`),
  CONSTRAINT `Order_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `users` (`userID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Order`
--

LOCK TABLES `Order` WRITE;
/*!40000 ALTER TABLE `Order` DISABLE KEYS */;
INSERT INTO `Order` VALUES (1,1,1,'gagan99','[{\"id\": 8, \"name\": \"Royal Spice Paneer\", \"price\": \"9.49\", \"quantity\": 2, \"image_path\": \"\"}]',18.98,'Cash','2025-04-13 17:20:34','delivered','2025-04-23 23:26:27'),(2,1,2,'gagan99','[{\"id\": 4, \"name\": \"Kadhai Paneer\", \"price\": \"7.99\", \"quantity\": 3, \"image_path\": \"\"}]',23.97,'pending','2025-04-13 19:37:35','ready for pickup','2025-04-26 01:53:23'),(3,1,3,'gagan99','[{\"id\": 2, \"name\": \"BBQ Chicken Bacon Pizza\", \"price\": \"9.49\", \"quantity\": 1, \"image_path\": \"\"}]',9.49,'pending','2025-04-13 19:38:09','pending','2025-04-27 02:45:56'),(4,1,4,'gagan99','[{\"MenuID\": 9, \"name\": \"Chicken Dum Biryani\", \"price\": \"17.99\", \"quantity\": 1, \"menuId\": null, \"category\": null}]',17.99,'pending','2025-04-27 23:06:03','pending','2025-04-27 23:06:03'),(5,1,5,'gagan99','[{\"MenuID\": 9, \"name\": \"Chicken Dum Biryani\", \"price\": \"17.99\", \"quantity\": 1, \"menuId\": null, \"category\": null}]',17.99,'pending','2025-04-27 23:06:10','pending','2025-04-27 23:06:10'),(6,1,6,'gagan99','[{\"MenuID\": 9, \"name\": \"Chicken Dum Biryani\", \"price\": \"17.99\", \"quantity\": 1, \"menuId\": null, \"category\": null}]',17.99,'pending','2025-04-27 23:06:13','pending','2025-04-27 23:06:13'),(7,1,7,'gagan99','[{\"MenuID\": 9, \"name\": \"Chicken Dum Biryani\", \"price\": \"17.99\", \"quantity\": 1, \"menuId\": null, \"category\": null}]',17.99,'pending','2025-04-27 23:06:17','pending','2025-04-27 23:06:17'),(8,1,8,'gagan99','[{\"MenuID\": 9, \"name\": \"Chicken Dum Biryani\", \"price\": \"17.99\", \"quantity\": 1, \"menuId\": null, \"category\": null}]',17.99,'pending','2025-04-27 23:06:18','pending','2025-04-27 23:06:18'),(9,1,9,'gagan99','[{\"MenuID\": 9, \"name\": \"Chicken Dum Biryani\", \"price\": \"17.99\", \"quantity\": 1, \"menuId\": null, \"category\": null}]',17.99,'pending','2025-04-27 23:06:18','pending','2025-04-27 23:06:18'),(10,1,10,'gagan99','[{\"MenuID\": 9, \"name\": \"Chicken Dum Biryani\", \"price\": \"17.99\", \"quantity\": 1, \"menuId\": null, \"category\": null}]',17.99,'pending','2025-04-27 23:06:19','pending','2025-04-27 23:06:19'),(11,1,11,'gagan99','[{\"MenuID\": 9, \"name\": \"Chicken Dum Biryani\", \"price\": \"17.99\", \"quantity\": 1, \"menuId\": null, \"category\": null}]',17.99,'pending','2025-04-27 23:06:19','pending','2025-04-27 23:06:19'),(12,1,12,'gagan99','[{\"MenuID\": 9, \"name\": \"Chicken Dum Biryani\", \"price\": \"17.99\", \"quantity\": 1, \"menuId\": null, \"category\": null}]',17.99,'pending','2025-04-27 23:06:19','pending','2025-04-27 23:06:19'),(13,1,13,'gagan99','[{\"MenuID\": 9, \"name\": \"Chicken Dum Biryani\", \"price\": \"17.99\", \"quantity\": 1, \"menuId\": null, \"category\": null}]',17.99,'pending','2025-04-27 23:06:20','pending','2025-04-27 23:06:20'),(14,1,14,'gagan99','[{\"MenuID\": 13, \"name\": \"Combo 4 Biryani\", \"price\": \"38.00\", \"quantity\": 1, \"category\": null}]',38.00,'pending','2025-04-27 23:27:50','pending','2025-04-27 23:27:50'),(21,1,15,'gagan99','[{\"MenuID\": 9, \"name\": \"Chicken Dum Biryani\", \"price\": \"17.99\", \"quantity\": 1, \"category\": \"Biryani\"}]',17.99,'pending','2025-04-28 00:53:41','pending','2025-04-28 00:53:41'),(22,1,16,'gagan99','[{\"MenuID\": 10, \"name\": \"Mutton Biryani\", \"price\": \"21.99\", \"quantity\": 1, \"category\": \"Biryani\"}]',21.99,'pending','2025-04-28 00:57:06','pending','2025-04-28 00:57:06'),(23,1,17,'gagan99','[{\"MenuID\": 10, \"name\": \"Mutton Biryani\", \"price\": \"21.99\", \"quantity\": 1, \"category\": \"Biryani\"}]',21.99,'pending','2025-04-28 01:02:22','pending','2025-04-28 01:02:22'),(24,1,18,'gagan99','[{\"MenuID\": 1, \"name\": \"BBQ Chicken Pizza\", \"price\": \"8.99\", \"quantity\": 1, \"category\": \"Pizza\"}]',8.99,'pending','2025-04-28 19:46:30','pending','2025-04-28 19:46:30'),(25,6,1,'padak1r','[{\"MenuID\": 10, \"name\": \"Mutton Biryani\", \"price\": \"21.99\", \"quantity\": 1, \"category\": \"Biryani\"}]',21.99,'pending','2025-04-28 19:51:26','pending','2025-04-28 19:51:26'),(26,6,2,'padak1r','[{\"MenuID\": 10, \"name\": \"Mutton Biryani\", \"price\": \"21.99\", \"quantity\": 1, \"category\": \"Biryani\"}]',21.99,'pending','2025-04-28 19:51:34','pending','2025-04-28 19:51:34'),(27,1,19,'gagan99','[{\"MenuID\": 2, \"name\": \"BBQ Chicken Bacon Pizza\", \"price\": \"9.49\", \"quantity\": 1, \"category\": \"Pizza\"}]',9.49,'pending','2025-04-28 19:54:44','pending','2025-04-28 19:54:44'),(28,1,20,'gagan99','[{\"MenuID\": 12, \"name\": \"Veg Biryani\", \"price\": \"14.99\", \"quantity\": 1, \"category\": \"Biryani\"}]',14.99,'pending','2025-04-28 19:56:41','pending','2025-04-28 19:56:41'),(29,1,21,'gagan99','[{\"MenuID\": 3, \"name\": \"Cheesy Spicy Delight\", \"price\": \"6.49\", \"quantity\": 1, \"category\": \"Pizza\"}]',6.49,'pending','2025-04-28 20:01:20','pending','2025-04-28 20:01:20'),(30,1,22,'gagan99','[{\"MenuID\": 14, \"name\": \"Special Chicken Dum Biryani\", \"price\": \"20.99\", \"quantity\": 1, \"category\": \"Biryani\"}]',20.99,'pending','2025-04-30 04:53:11','pending','2025-04-30 04:53:11');
/*!40000 ALTER TABLE `Order` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`birru1g`@`%`*/ /*!50003 TRIGGER trg_order_seq_by_user
BEFORE INSERT ON `Order`
FOR EACH ROW
BEGIN
  DECLARE last_seq INT;
  SELECT COALESCE(MAX(orderIDByUser),0)
    INTO last_seq
    FROM `Order`
   WHERE UserID = NEW.UserID;
  SET NEW.orderIDByUser = last_seq + 1;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-30  2:40:29
