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
-- Table structure for table `Menu`
--

DROP TABLE IF EXISTS `Menu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Menu` (
  `MenuID` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) NOT NULL,
  `Description` text DEFAULT NULL,
  `Price` decimal(10,2) NOT NULL,
  `ImagePath` varchar(255) DEFAULT NULL,
  `Category` varchar(100) DEFAULT NULL,
  `Available` tinyint(1) DEFAULT 1,
  PRIMARY KEY (`MenuID`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Menu`
--

LOCK TABLES `Menu` WRITE;
/*!40000 ALTER TABLE `Menu` DISABLE KEYS */;
INSERT INTO `Menu` VALUES (1,'BBQ Chicken Pizza','Smoky BBQ chicken on a crisp crust with rich cheese.',8.99,'images/Pizza/bbq_chicken.jpg','Pizza',1),(2,'BBQ Chicken Bacon Pizza','Grilled chicken and bacon topped with tangy BBQ sauce.',9.49,'images/Pizza/bbq-chicken-bacon.jpg','Pizza',1),(3,'Cheesy Spicy Delight','A cheesy delight with a kick of spicy flavors.',6.49,'images/Pizza/cheesy_spicy_delight.jpg','Pizza',1),(4,'Kadhai Paneer','Indian spiced kadhai paneer on a cheesy base.',7.99,'images/Pizza/kadhai_paneer.jpg','Pizza',1),(5,'Original Crust Cheese','Classic crust layered with rich mozzarella cheese.',7.49,'images/Pizza/Original_Crust_Cheese.jpg','Pizza',1),(6,'Crust Pepperoni','Pepperoni loaded on a classic crust with cheesy goodness.',10.99,'images/Pizza/Original_Crust_Pepperoni.jpg','Pizza',1),(7,'Sausage Pizza','Sausage lovers’ dream with bold flavor on every bite.',9.49,'images/Pizza/sausage_cheese.jpg','Pizza',1),(8,'Royal Spice Paneer','Paneer seasoned with royal spices on a golden crust.',9.49,'images/Pizza/royal_spice_paneer.jpg','Pizza',1),(9,'Chicken Dum Biryani','Tasty Chicken Dum Biryani made with Sytle and Spices',17.99,'images/Biryani/chicken_biryani.jpg','Biryani',1),(10,'Mutton Biryani','Tasty Mutton Biryani',21.99,'images/Biryani/mutton_biryani.jpg','Biryani',1),(11,'Prawns Biryani','Spicy Prawns Biryani made with ghee',17.99,'images/Biryani/prawns_biryani.jpeg','Biryani',1),(12,'Veg Biryani','Tasty Veg Biryani made with all vegitables only',14.99,'images/Biryani/veg_biryani.jpg','Biryani',1),(13,'Combo 4 Biryani','All 4 Types of Biryani Combo [ chicken, Mutton, Prawns, Veg ]',38.00,'images/Biryani/4_types_biryani.jpeg','Biryani',1),(14,'Special Chicken Dum Biryani','Restaurant Special Chicken Dum Biryani made with 54spices.',20.99,'images/Biryani/special_chicken_dum_biryani.jpg','Biryani',1);
/*!40000 ALTER TABLE `Menu` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-30  2:40:32
