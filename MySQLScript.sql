-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: librarydb
-- ------------------------------------------------------
-- Server version	8.0.41

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
-- Table structure for table `books`
--

DROP TABLE IF EXISTS `books`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `books` (
  `BookID` int NOT NULL AUTO_INCREMENT,
  `Title` varchar(255) DEFAULT NULL,
  `Author` varchar(100) DEFAULT NULL,
  `ISBN` varchar(20) DEFAULT NULL,
  `CategoryID` int DEFAULT NULL,
  `AvailabilityStatus` int DEFAULT '1',
  `Publisher` varchar(100) DEFAULT NULL,
  `PublicationYear` int DEFAULT NULL,
  PRIMARY KEY (`BookID`),
  UNIQUE KEY `ISBN` (`ISBN`),
  KEY `CategoryID` (`CategoryID`),
  CONSTRAINT `books_ibfk_1` FOREIGN KEY (`CategoryID`) REFERENCES `categories` (`CategoryID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books`
--

LOCK TABLES `books` WRITE;
/*!40000 ALTER TABLE `books` DISABLE KEYS */;
INSERT INTO `books` VALUES (1,'The Time Machine','H.G. Wells','9780451528551',1,1,'Penguin',1895),(2,'A Brief History of Time','Stephen Hawking','9780553380163',2,1,'Bantam',1988),(3,'Sapiens','Yuval Noah Harari','9780099590088',3,2,'Harvill Secker',2011);
/*!40000 ALTER TABLE `books` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `borrow`
--

DROP TABLE IF EXISTS `borrow`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `borrow` (
  `BorrowID` int NOT NULL AUTO_INCREMENT,
  `BookID` int DEFAULT NULL,
  `MemberID` int DEFAULT NULL,
  `BorrowDate` date DEFAULT NULL,
  `DueDate` date DEFAULT NULL,
  `ReturnDate` date DEFAULT NULL,
  PRIMARY KEY (`BorrowID`),
  KEY `BookID` (`BookID`),
  KEY `MemberID` (`MemberID`),
  CONSTRAINT `borrow_ibfk_1` FOREIGN KEY (`BookID`) REFERENCES `books` (`BookID`),
  CONSTRAINT `borrow_ibfk_2` FOREIGN KEY (`MemberID`) REFERENCES `members` (`MemberID`)
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `borrow`
--

LOCK TABLES `borrow` WRITE;
/*!40000 ALTER TABLE `borrow` DISABLE KEYS */;
INSERT INTO `borrow` VALUES (1,3,1,'2025-05-01','2025-05-15','2025-05-27'),(2,1,2,'2025-04-10','2025-04-25','2025-04-20'),(3,3,1,'2025-05-01','2025-05-15','2025-05-27'),(4,1,2,'2025-04-10','2025-04-25','2025-04-20'),(5,1,1,'2025-05-27','2025-06-11','2025-05-27'),(6,1,1,'2025-05-27','2025-06-11','2025-05-27'),(7,1,2,'2025-05-27','2025-06-11','2025-05-27'),(8,2,1,'2025-05-27','2025-06-11','2025-05-27'),(9,2,3,'2025-05-27','2025-06-11','2025-05-27'),(10,1,2,'2025-05-27','2025-06-11','2025-05-27'),(11,1,1,'2025-05-27','2025-06-11','2025-05-27'),(12,3,1,'2025-05-27','2025-06-11','2025-05-27'),(13,3,1,'2025-05-27','2025-06-11','2025-05-27'),(14,3,2,'2025-05-27','2025-06-11','2025-05-27'),(15,3,1,'2025-05-27','2025-06-11','2025-05-27'),(16,3,1,'2025-05-27','2025-06-11','2025-05-27'),(17,1,1,'2025-05-27','2025-06-11','2025-05-27'),(18,1,2,'2025-05-27','2025-06-11','2025-05-27'),(19,1,1,'2025-05-27','2025-06-11','2025-05-27'),(20,1,1,'2025-05-27','2025-06-11','2025-05-27'),(21,3,1,'2025-05-27','2025-06-11','2025-05-27'),(22,3,1,'2025-05-27','2025-06-11','2025-05-27'),(23,3,2,'2025-05-27','2025-06-11','2025-05-27'),(24,3,1,'2025-05-27','2025-06-11','2025-05-27'),(25,3,1,'2025-05-27','2025-06-11','2025-05-27'),(26,3,2,'2025-05-27','2025-06-11','2025-05-27'),(27,3,1,'2025-05-27','2025-06-11','2025-05-27'),(28,3,2,'2025-05-27','2025-06-11','2025-05-27'),(29,3,2,'2025-05-27','2025-06-11','2025-05-27'),(30,3,1,'2025-05-27','2025-06-11','2025-05-27'),(31,3,3,'2025-05-27','2025-06-11','2025-05-27'),(32,3,1,'2025-05-27','2025-06-11','2025-05-27'),(33,3,2,'2025-05-27','2025-06-11','2025-05-27'),(34,3,1,'2025-05-27','2025-06-11','2025-05-27'),(35,3,3,'2025-05-27','2025-06-11','2025-05-27'),(36,3,2,'2025-05-27','2025-06-11','2025-05-27'),(37,3,1,'2025-05-27','2025-06-11','2025-05-27'),(38,3,1,'2025-05-27','2025-06-11','2025-05-27'),(39,3,2,'2025-05-27','2025-06-11','2025-05-27'),(40,3,3,'2025-05-27','2025-06-11','2025-05-27'),(41,3,2,'2025-05-27','2025-06-11','2025-05-27'),(42,3,1,'2025-05-27','2025-06-11','2025-05-27'),(43,3,2,'2025-05-27','2025-06-11','2025-05-27'),(44,3,3,'2025-05-27','2025-06-11','2025-05-27'),(45,3,1,'2025-05-27','2025-06-11','2025-05-27'),(46,3,2,'2025-05-27','2025-06-11','2025-05-27'),(47,3,1,'2025-05-27','2025-06-11','2025-05-27'),(48,3,2,'2025-05-27','2025-06-11','2025-05-27'),(49,3,3,'2025-05-27','2025-06-11','2025-05-27'),(50,3,1,'2025-05-27','2025-06-11','2025-05-27'),(51,3,3,'2025-05-27','2025-06-11','2025-05-27'),(52,3,1,'2025-05-27','2025-06-11','2025-05-27'),(53,3,1,'2025-05-27','2025-06-11','2025-05-27'),(54,3,3,'2025-05-27','2025-06-11','2025-05-27'),(55,2,3,'2025-05-27','2025-06-11','2025-05-27'),(56,3,1,'2025-05-27','2025-06-11','2025-05-27');
/*!40000 ALTER TABLE `borrow` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categories` (
  `CategoryID` int NOT NULL AUTO_INCREMENT,
  `CategoryName` varchar(100) DEFAULT NULL,
  `Description` text,
  PRIMARY KEY (`CategoryID`),
  UNIQUE KEY `CategoryName` (`CategoryName`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` VALUES (1,'Fiction','Fictional books including novels and stories.'),(2,'Science','Books related to scientific studies and discoveries.'),(3,'History','Books about historical events and figures.');
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `librarians`
--

DROP TABLE IF EXISTS `librarians`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `librarians` (
  `LibrarianID` int NOT NULL AUTO_INCREMENT,
  `FullName` varchar(100) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `Username` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`LibrarianID`),
  UNIQUE KEY `Email` (`Email`),
  UNIQUE KEY `Username` (`Username`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `librarians`
--

LOCK TABLES `librarians` WRITE;
/*!40000 ALTER TABLE `librarians` DISABLE KEYS */;
INSERT INTO `librarians` VALUES (1,'Talha Eken','talha@ankara.edu.tr','teken'),(2,'Bayram Kıcalı','bayram@ankara.edu.tr','bayramk'),(3,'Ayşe Gül Pekgöz','ayşeg@ankara.edu.tr','agp'),(4,'Selman Bedri Gün','sbedri@ankara.edu.tr','bedrii');
/*!40000 ALTER TABLE `librarians` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `members`
--

DROP TABLE IF EXISTS `members`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `members` (
  `MemberID` int NOT NULL AUTO_INCREMENT,
  `FullName` varchar(100) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `MembershipDate` date DEFAULT NULL,
  PRIMARY KEY (`MemberID`),
  UNIQUE KEY `Email` (`Email`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `members`
--

LOCK TABLES `members` WRITE;
/*!40000 ALTER TABLE `members` DISABLE KEYS */;
INSERT INTO `members` VALUES (1,'Ali Veli','ali@ankara.edu.tr','2023-06-10'),(2,'Ayşe Demir','ayse@ankara.edu.tr','2024-01-22'),(3,'Mehmet Can','mehmet@ankara.edu.tr','2024-11-15');
/*!40000 ALTER TABLE `members` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reservations`
--

DROP TABLE IF EXISTS `reservations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reservations` (
  `ReservationID` int NOT NULL AUTO_INCREMENT,
  `BookID` int DEFAULT NULL,
  `MemberID` int DEFAULT NULL,
  `ReservationDate` date DEFAULT NULL,
  `Status` enum('Active','Cancelled','Completed') DEFAULT NULL,
  PRIMARY KEY (`ReservationID`),
  KEY `BookID` (`BookID`),
  KEY `MemberID` (`MemberID`),
  CONSTRAINT `reservations_ibfk_1` FOREIGN KEY (`BookID`) REFERENCES `books` (`BookID`),
  CONSTRAINT `reservations_ibfk_2` FOREIGN KEY (`MemberID`) REFERENCES `members` (`MemberID`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reservations`
--

LOCK TABLES `reservations` WRITE;
/*!40000 ALTER TABLE `reservations` DISABLE KEYS */;
INSERT INTO `reservations` VALUES (1,2,3,'2025-05-20','Completed'),(3,2,3,'2025-05-20','Completed'),(4,3,2,'2025-05-05','Completed'),(5,1,1,'2025-05-27','Completed'),(6,3,1,'2025-05-27','Cancelled'),(7,3,2,'2025-05-27','Completed'),(8,3,2,'2025-05-27','Cancelled'),(9,1,1,'2025-05-27','Cancelled'),(10,1,1,'2025-05-27','Cancelled'),(11,3,3,'2025-05-27','Cancelled'),(12,3,3,'2025-05-27','Completed'),(13,3,3,'2025-05-27','Completed'),(14,3,2,'2025-05-27','Cancelled'),(15,3,3,'2025-05-27','Completed'),(16,3,3,'2025-05-27','Completed'),(17,3,2,'2025-05-27','Cancelled'),(18,3,3,'2025-05-27','Cancelled'),(19,3,1,'2025-05-27','Cancelled'),(20,3,2,'2025-05-27','Cancelled'),(21,3,1,'2025-05-27','Completed'),(22,3,2,'2025-05-27','Completed'),(23,3,3,'2025-05-27','Cancelled'),(24,3,2,'2025-05-27','Cancelled'),(25,2,1,'2025-05-27','Cancelled');
/*!40000 ALTER TABLE `reservations` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-27 17:27:08
