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
) ENGINE=InnoDB AUTO_INCREMENT=73 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ligues`
--

LOCK TABLES `ligues` WRITE;
/*!40000 ALTER TABLE `ligues` DISABLE KEYS */;
INSERT INTO `ligues` VALUES (1,'Bundesliga','flashscore.fr/res/image/data/ddvweuSp-zZqYxzn7.png','allemagne'),(2,'2. Bundesliga','flashscore.fr/res/image/data/rFBMjGkd-zZqYxzn7.png','allemagne'),(3,'Premier League','flashscore.fr/res/image/data/Q1kHiLB7-SfPP5G2R.png','angleterre'),(4,'Championship','flashscore.fr/res/image/data/Ekb5ptRp-dStSpFQ1.png','angleterre'),(5,'Bundesliga','flashscore.fr/res/image/data/8tyQDTXI-AJhCVPhR.png','autriche'),(6,'Pro League','flashscore.fr/res/image/data/xMIJ8gB7-MPb5NuUT.png','belgique'),(7,'Vysshaya Liga','flashscore.fr/res/image/data/fZMMyDkd-QVvhN4Fe.png','bielorussie'),(8,'Serie A','flashscore.fr/res/image/data/G6SHESV1-67Zdj3qr.png','bresil'),(9,'Primera División','flashscore.fr/res/image/data/dAiJn4WI-bD0waFCj.png','chili'),(10,'Primera A','flashscore.fr/res/image/data/tzBVlFRp-4G8A06J2.png','colombie'),(11,'HNL','flashscore.fr/res/image/data/SjHs2Nmd-nw3y3cBl.png','croatie'),(12,'Superliga','flashscore.fr/res/image/data/pl7DBs7j-Qwe6iKrA.png','danemark'),(13,'Premiership','flashscore.fr/res/image/data/WpBh4DiD-Uegb2yr2.png','ecosse'),(14,'Liga Pro','flashscore.fr/res/image/data/ClxbEZU1-0W1ygTPi.png','equateur'),(15,'LaLiga','flashscore.fr/res/image/data/be5KoO97-pUMsmZR4.png','espagne'),(16,'LaLiga2','flashscore.fr/res/image/data/QNYn1IRp-pUMsmZR4.png','espagne'),(17,'Meistriliiga','flashscore.fr/res/image/data/W09EYEBO-fTc1W2g2.png','estonie'),(18,'Veikkausliiga','flashscore.fr/res/image/data/GAj2XBBO-UsSStIKi.png','finlande'),(19,'Ligue 1','flashscore.fr/res/image/data/EeVwWyWI-xUnj94R9.png','france'),(20,'Ligue 2','flashscore.fr/res/image/data/favt7YjD-xUnj94R9.png','france'),(21,'Super League','flashscore.fr/res/image/data/f1gozUQp-dfyoU0sg.png','grece'),(22,'OTP Bank Liga','flashscore.fr/res/image/data/d2TLmPnd-4d6vl0f8.png','hongrie'),(23,'Premier Division','flashscore.fr/res/image/data/dOM6dBB7-Qif0VL4l.png','irlande'),(24,'Besta-deild karla','flashscore.fr/res/image/data/UofN0zld-02UDhp1U.png','islande'),(25,'Premier League','flashscore.fr/res/image/data/fVl2yZkd-OfIOqaXB.png','israel'),(26,'Serie A','flashscore.fr/res/image/data/Uu776GVI-C6FwxqQr.png','italie'),(27,'Serie B','flashscore.fr/res/image/data/8rfDEpSp-MPzofkvt.png','italie'),(28,'J1 League','flashscore.fr/res/image/data/baoeO2kd-EJ7vUYrO.png','japon'),(29,'Eliteserien','flashscore.fr/res/image/data/zg2xsBDO-AXZMCRsF.png','norvege'),(30,'Primera Division','flashscore.fr/res/image/data/v9FkzfVI-QTVwyfxm.png','paraguay'),(31,'Ekstraklasa','flashscore.fr/res/image/data/bZBBEHYI-zaN1c1Tj.png','pologne'),(32,'Liga Portugal','flashscore.fr/res/image/data/ltrk8v9j-ddn4Dzs6.png','portugal'),(33,'Liga Portugal 2','flashscore.fr/res/image/data/OAOHZkSp-v9oasLTK.png','portugal'),(34,'1. Liga','flashscore.fr/res/image/data/xWejqGVI-pUMsmZR4.png','republique-tcheque'),(35,'Liga 1','flashscore.fr/res/image/data/6mP1X7EO-6R5aI25G.png','roumanie'),(36,'Premier League','flashscore.fr/res/image/data/ba3BzV9j-48lwBKcj.png','russie'),(37,'Fortuna liga','flashscore.fr/res/image/data/CvuVdN6j-nPkKAB37.png','slovaquie'),(38,'Prva Liga','flashscore.fr/res/image/data/vmQgRlYI-2wN7HsxK.png','slovenie'),(39,'Allsvenskan','flashscore.fr/res/image/data/A5Rrk7md-dCA2CnOC.png','suede'),(40,'Super League','flashscore.fr/res/image/data/z5jdjT7j-MNs0Ruzl.png','suisse'),(41,'Super Lig','flashscore.fr/res/image/data/zXKzgj7j-GIYgD8MG.png','turquie'),(42,'MLS','flashscore.fr/res/image/data/dWGLEQCO-0EpZLEDa.png','usa'),(43,'Premier League','flashscore.fr/res/image/data/6DUibp97-6B1cP1aH.png','bangladesh'),(44,'Super League','flashscore.fr/res/image/data/0WVh5pXI-v5HFu7WF.png','chine'),(45,'Jia League','flashscore.fr/res/image/data/zauN7hB7-v5HFu7WF.png','chine'),(46,'K League 1','flashscore.fr/res/image/data/v3xmnaYI-AXw0ozEb.png','coree-du-sud'),(47,'K League 2','flashscore.fr/res/image/data/I7M5vXiU-OSJoxWzo.png','coree-du-sud'),(48,'Primera División','flashscore.fr/res/image/data/ARGLphC7-vLkhhrRr.png','costa-rica'),(49,'Premier League','flashscore.fr/res/image/data/GbvVT9DO-8WoHxA9E.png','egypte'),(50,'Esiliiga','flashscore.fr/res/image/data/I9ssl9T1-fTc1W2g2.png','estonie'),(51,'Premier League','flashscore.fr/res/image/data/fLXTn7U1-0SmQCpfS.png','ethiopie'),(52,'Crystalbet Erovnuli Liga','flashscore.fr/res/image/data/jiopCrU1-O2l4ldWp.png','georgie'),(53,'Crystalbet Erovnuli Liga 2','flashscore.fr/res/image/data/CfVXd7YI-z9ITN8Dj.png','georgie'),(54,'Division 1','flashscore.fr/res/image/data/rXfZB5Tp-0KwUMfHh.png','irlande'),(55,'Division 2','flashscore.fr/res/image/data/W0PW37iD-xUMhOx9P.png','islande'),(56,'Premier League','flashscore.fr/res/image/data/IeKM91VI-dxAWVfEB.png','jamaique'),(58,'J2 League','flashscore.fr/res/image/data/GbC0scEO-EJ7vUYrO.png','japon'),(59,'Optibet Virsliga','flashscore.fr/res/image/data/UmeJnsDO-42Du3au1.png','lettonie'),(60,'A Lyga','flashscore.fr/res/image/data/04gMSOmd-ImWVKrv6.png','lituanie'),(61,'I Lyga','flashscore.fr/res/image/data/vu2O3L8j-f3QrXcmk.png','lituanie'),(62,'Liga MX','flashscore.fr/res/image/data/4OOue6fU-2wkItInr.png','mexique'),(63,'Premier League','flashscore.fr/res/image/data/Y1L9SGXI-t0vGqQah.png','mongolie'),(64,'Division Intermedia','flashscore.fr/res/image/data/rusxG5CO-8jSZw4tE.png','paraguay'),(65,'Super League','flashscore.fr/res/image/data/xx9We5VI-Qe8c2AbS.png','ouzbekistan'),(66,'Cymru Premier','flashscore.fr/res/image/data/OntVvLDO-A5RRjHSu.png','pays-de-galles'),(67,'Division 1','flashscore.fr/res/image/data/KUgy5WWI-zaN1c1Tj.png','pologne'),(68,'Liga 1','flashscore.fr/res/image/data/xnSEBqSp-tlnFJZfa.png','perou'),(69,'Premier League','flashscore.fr/res/image/data/Y9TU2HDO-zJ5nBrsi.png','singapour'),(70,'Superettan','flashscore.fr/res/image/data/S2LkqbXI-dCA2CnOC.png','suede'),(71,'Ligi Kuu Bara','flashscore.fr/res/image/data/Ues0HNmd-2sayc7ft.png','tanzanie'),(72,'Primera Division','flashscore.fr/res/image/data/UD8VlaXI-MNoVMfbg.png','uruguay');
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

-- Dump completed on 2022-07-10 12:02:33
