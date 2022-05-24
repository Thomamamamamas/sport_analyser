-- MySQL dump 10.13  Distrib 8.0.28, for macos11 (x86_64)
--
-- Host: localhost    Database: football
-- ------------------------------------------------------
-- Server version	8.0.28

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
-- Table structure for table `ligues`
--

DROP TABLE IF EXISTS `ligues`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ligues` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `LIGUE_NAME` varchar(100) DEFAULT NULL,
  `LIGUE_LOGO` varchar(100) DEFAULT NULL,
  `LIGUE_PAYS` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ligues`
--

LOCK TABLES `ligues` WRITE;
/*!40000 ALTER TABLE `ligues` DISABLE KEYS */;
INSERT INTO `ligues` VALUES (1,'Bundesliga','flashscore.fr/res/image/data/bgn7cVkD-QcgaVHyL.png','allemagne'),(2,'2. Bundesliga','flashscore.fr/res/image/data/vce9YRA7-QcgaVHyL.png','allemagne'),(3,'Premier League','flashscore.fr/res/image/data/YXNYEC9j-KOA3eRk5.png','angleterre'),(4,'Championship','flashscore.fr/res/image/data/6a9KSp97-bF97fo5B.png','angleterre'),(5,'Bundesliga','flashscore.fr/res/image/data/W05KfZ8j-MNJgo8mj.png','autriche'),(6,'Pro League','flashscore.fr/res/image/data/YDHHaKRp-jTbLXcXo.png','belgique'),(7,'Vysshaya Liga','flashscore.fr/res/image/data/fZMMyDkd-QVvhN4Fe.png','bielorussie'),(8,'Serie A','flashscore.fr/res/image/data/G6SHESV1-67Zdj3qr.png','bresil'),(9,'Primera División','flashscore.fr/res/image/data/dAiJn4WI-bD0waFCj.png','chili'),(10,'Primera A','flashscore.fr/res/image/data/tzBVlFRp-4G8A06J2.png','colombie'),(11,'1. HNL','flashscore.fr/res/image/data/lIcUbHSp-nsL4puBE.png','croatie'),(12,'Superliga','flashscore.fr/res/image/data/lQLumE8j-dnFNwo1S.png','danemark'),(13,'Premiership','flashscore.fr/res/image/data/bDvLJ79j-tMLGFoII.png','ecosse'),(14,'Liga Pro','flashscore.fr/res/image/data/ClxbEZU1-0W1ygTPi.png','equateur'),(15,'LaLiga','flashscore.fr/res/image/data/CEyhlKT1-pnrpaxld.png','espagne'),(16,'LaLiga2','flashscore.fr/res/image/data/l8Md7EhU-pnrpaxld.png','espagne'),(17,'Meistriliiga','flashscore.fr/res/image/data/W09EYEBO-fTc1W2g2.png','estonie'),(18,'Veikkausliiga','flashscore.fr/res/image/data/GAj2XBBO-UsSStIKi.png','finlande'),(19,'Ligue 1','flashscore.fr/res/image/data/QmK6Kf97-hpy1uJgU.png','france'),(20,'Ligue 2','flashscore.fr/res/image/data/vPattcCO-hpy1uJgU.png','france'),(21,'Super League','flashscore.fr/res/image/data/f1gozUQp-dfyoU0sg.png','grece'),(22,'OTP Bank Liga','flashscore.fr/res/image/data/MF7TSQA7-ImbVPMnE.png','hongrie'),(23,'Premier Division','flashscore.fr/res/image/data/dOM6dBB7-Qif0VL4l.png','irlande'),(24,'Besta-deild karla','flashscore.fr/res/image/data/UofN0zld-02UDhp1U.png','islande'),(25,'Premier League','flashscore.fr/res/image/data/ljRyDVnd-8Wywg3AP.png','israel'),(26,'Serie A','flashscore.fr/res/image/data/6kM2mM6j-O64SURIF.png','italie'),(27,'Serie B','flashscore.fr/res/image/data/8rfDEpSp-MPzofkvt.png','italie'),(28,'J1 League','flashscore.fr/res/image/data/baoeO2kd-EJ7vUYrO.png','japon'),(29,'Eliteserien','flashscore.fr/res/image/data/zg2xsBDO-AXZMCRsF.png','norvege'),(30,'Primera Division','flashscore.fr/res/image/data/v9FkzfVI-QTVwyfxm.png','paraguay'),(31,'Ekstraklasa','flashscore.fr/res/image/data/08Vb3UfU-v7vSpCgb.png','pologne'),(32,'Liga Portugal','flashscore.fr/res/image/data/ltrk8v9j-ddn4Dzs6.png','portugal'),(33,'Liga Portugal 2','flashscore.fr/res/image/data/OAOHZkSp-v9oasLTK.png','portugal'),(34,'1. Liga','flashscore.fr/res/image/data/zgbOIqkD-AejvSm2G.png','republique-tcheque'),(35,'Liga 1','flashscore.fr/res/image/data/nsaWzNVI-W6ObaQQs.png','roumanie'),(36,'Premier League','flashscore.fr/res/image/data/ObQgZxhU-nLL6c4ef.png','russie'),(37,'Fortuna liga','flashscore.fr/res/image/data/4UFuA0V1-CGvP5SmE.png','slovaquie'),(38,'Prva Liga','flashscore.fr/res/image/data/UwWnPERp-n5a66KeM.png','slovenie'),(39,'Allsvenskan','flashscore.fr/res/image/data/A5Rrk7md-dCA2CnOC.png','suede'),(40,'Super League','flashscore.fr/res/image/data/Ys9iQ5V1-hEGODM5l.png','suisse'),(41,'Super Lig','flashscore.fr/res/image/data/zXKzgj7j-GIYgD8MG.png','turquie'),(42,'MLS','flashscore.fr/res/image/data/dWGLEQCO-0EpZLEDa.png','usa');
/*!40000 ALTER TABLE `ligues` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-05-24  9:36:57
