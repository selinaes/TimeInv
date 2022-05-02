-- MySQL dump 10.14  Distrib 5.5.68-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: timeinv_db
-- ------------------------------------------------------
-- Server version	5.5.68-MariaDB

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

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product` (
  `sku` int(10) unsigned NOT NULL,
  `title` varchar(50) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `threshold` int(11) DEFAULT NULL,
  `last_modified_by` varchar(10) DEFAULT NULL,
  `image_file_name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`sku`),
  KEY `last_modified_by` (`last_modified_by`),
  CONSTRAINT `product_ibfk_1` FOREIGN KEY (`last_modified_by`) REFERENCES `staff` (`username`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
INSERT INTO `product` VALUES (37,'women\'s  double-zip crossbody',212.00,0,'kw1',NULL),(38,'women\'s  cardholder',150.00,0,'kw1',NULL),(40,'women\'s  large tote',183.00,0,'kw1',NULL),(41,'women\'s  flap crossbody',81.00,0,'kw1',NULL),(42,'women\'s  messenger bag',601.99,0,'kw1',NULL),(43,'men\'s fit t-shirt',42.99,0,'kw1',NULL),(44,'men\'s denim jacket',15.90,120,'ad1','44.jpeg'),(45,'men\'s tank top',42.99,0,'kw1',NULL),(47,'men\'s overalls',36.99,0,'kw1',NULL),(48,'men\'s fit hoodie',26.99,0,'kw1',NULL),(49,'men\'s fit pants',35.99,0,'kw1',NULL),(50,'men\'s rugby shirt',12.99,0,'kw1',NULL),(52,'men\'s twill cap',35.99,0,'kw1',NULL),(53,'men\'s leather jacket',26.99,0,'kw1',NULL),(54,'men\'s fit chinos',71.90,0,'ad1',NULL),(55,'men\'s denim overshirt',83.91,0,'at1','55.jpg'),(57,'men\'s water-repellent parka',15.99,0,'kw1',NULL),(58,'men\'s shacket',62.99,0,'kw1',NULL),(59,'men\'s fit shirt',36.99,0,'kw1',NULL),(60,'men\'s drawstring bucket hat',20.99,0,'at1','60.jpg'),(61,'men\'s fit blazer',35.91,0,'ad1','61.png'),(62,'men\'s suit pants',20.99,0,'kw1',NULL),(63,'men\'s fit jaggers',20.99,0,'kw1',NULL),(65,'men\'s slim jeans',61.99,0,'at1',NULL),(66,'men\'s regular jeans',50.99,0,'at1',NULL),(67,'men\'s sweatshorts',101.98,0,'at1',NULL),(69,'men\'s gloves',15.99,0,'at1',NULL),(70,'men\'s rib scarf',50.99,0,'at1',NULL),(72,'men\'s lounge socks',51.20,0,'at1',NULL),(88,'leather bomber jacket',151.00,5,'ad1','88.jpg'),(102,'women\'s hoop earrings',15.99,0,'ad1','101.png');
/*!40000 ALTER TABLE `product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `staff`
--

DROP TABLE IF EXISTS `staff`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `staff` (
  `username` varchar(10) NOT NULL DEFAULT '',
  `name` varchar(50) DEFAULT NULL,
  `role` varchar(30) DEFAULT NULL,
  `permission` set('product','transaction','staff','supplier','supplierTerm') DEFAULT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `staff`
--

LOCK TABLES `staff` WRITE;
/*!40000 ALTER TABLE `staff` DISABLE KEYS */;
INSERT INTO `staff` VALUES ('ad1','Ashlyn Drake','inventory planning clerk','product,transaction,staff'),('ag1','Avelina Gong','technician','product,transaction'),('al1','Anna Lenman','accountant','transaction'),('at1','Angelina Tharpe','inventory control clerk','product,transaction'),('be1','Amy Barlow','software engineer','product'),('bf1','Bronson Ferguson','cost reporting clerk','product,transaction'),('bm1','Brelle Myers','warehouse manager','product,transaction'),('ec1','Eden Campbell','warehouse clerk','product'),('hs1','Helen Sichel','inventory planning','product,transaction'),('jf1','Julio Fernandez','marketing analyst and PR','product,transaction'),('jk1','Jody Kim','inventory planning clerk','product,transaction'),('jr1','Jack Ryu','site coordinator','product,transaction,staff'),('jw1','John Wahl','accountant','product,transaction,staff'),('kw1','Kiara Winster','inventory control manager','product,transaction,staff'),('lb1','Matt Bensen','technician','product,transaction'),('uh2','Ulma Hamilton','sales representative','product,transaction');
/*!40000 ALTER TABLE `staff` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `supplier`
--

DROP TABLE IF EXISTS `supplier`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `supplier` (
  `sid` int(10) unsigned NOT NULL DEFAULT '0',
  `company_name` varchar(50) DEFAULT NULL,
  `last_modified_by` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`sid`),
  KEY `last_modified_by` (`last_modified_by`),
  CONSTRAINT `supplier_ibfk_1` FOREIGN KEY (`last_modified_by`) REFERENCES `staff` (`username`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `supplier`
--

LOCK TABLES `supplier` WRITE;
/*!40000 ALTER TABLE `supplier` DISABLE KEYS */;
INSERT INTO `supplier` VALUES (3,'Osewaya','jr1'),(4,'Ceekay','jr1');
/*!40000 ALTER TABLE `supplier` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `supplierTerm`
--

DROP TABLE IF EXISTS `supplierTerm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `supplierTerm` (
  `sid` int(10) unsigned NOT NULL DEFAULT '0',
  `sku` int(10) unsigned NOT NULL DEFAULT '0',
  `cost` decimal(10,2) DEFAULT NULL,
  `last_modified_by` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`sid`,`sku`),
  KEY `last_modified_by` (`last_modified_by`),
  KEY `sku` (`sku`),
  CONSTRAINT `supplierTerm_ibfk_1` FOREIGN KEY (`last_modified_by`) REFERENCES `staff` (`username`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `supplierTerm_ibfk_2` FOREIGN KEY (`sku`) REFERENCES `product` (`sku`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `supplierTerm`
--

LOCK TABLES `supplierTerm` WRITE;
/*!40000 ALTER TABLE `supplierTerm` DISABLE KEYS */;
INSERT INTO `supplierTerm` VALUES (3,37,63.00,'jr1'),(3,38,21.00,'jr1'),(3,40,80.00,'jr1'),(3,41,144.00,'jr1'),(3,42,89.00,'jr1'),(3,43,7.99,'jr1'),(3,45,0.99,'jr1'),(3,47,19.99,'jr1'),(3,48,19.99,'jr1'),(3,49,22.99,'jr1'),(3,50,11.99,'jr1'),(3,52,4.99,'jr1'),(3,54,17.99,'jr1'),(3,55,15.99,'jr1'),(3,57,56.99,'jr1'),(3,58,64.99,'jr1'),(3,59,10.99,'jr1'),(3,60,8.99,'jr1'),(3,61,44.99,'jr1'),(3,62,20.99,'jr1'),(3,63,12.00,'jr1'),(3,65,13.00,'jr1'),(3,66,14.00,'jr1'),(3,67,6.99,'jr1'),(3,69,42.99,'jr1'),(3,70,30.99,'jr1'),(3,72,12.99,'jr1'),(4,37,88.00,'jr1'),(4,38,12.00,'jr1'),(4,40,97.00,'jr1'),(4,41,91.00,'jr1'),(4,42,102.00,'jr1'),(4,43,4.00,'jr1'),(4,44,33.00,'jr1'),(4,45,1.00,'jr1'),(4,47,27.99,'jr1'),(4,48,22.99,'jr1'),(4,49,20.99,'jr1'),(4,50,12.99,'jr1'),(4,52,2.00,'jr1'),(4,53,46.00,'jr1'),(4,54,20.99,'jr1'),(4,55,18.99,'jr1'),(4,57,35.20,'jr1'),(4,58,51.99,'jr1'),(4,59,14.50,'jr1'),(4,61,28.99,'jr1'),(4,62,15.99,'jr1'),(4,63,9.00,'jr1'),(4,65,13.00,'jr1'),(4,66,13.20,'jr1'),(4,67,8.99,'jr1'),(4,69,43.80,'jr1'),(4,70,31.20,'jr1');
/*!40000 ALTER TABLE `supplierTerm` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transaction`
--

DROP TABLE IF EXISTS `transaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `transaction` (
  `timestamp` datetime DEFAULT NULL,
  `tid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `sku` int(10) unsigned NOT NULL DEFAULT '0',
  `amount` int(11) DEFAULT NULL,
  `last_modified_by` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`tid`,`sku`),
  KEY `timestamp` (`timestamp`),
  KEY `sku` (`sku`),
  KEY `last_modified_by` (`last_modified_by`),
  CONSTRAINT `transaction_ibfk_1` FOREIGN KEY (`sku`) REFERENCES `product` (`sku`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `transaction_ibfk_2` FOREIGN KEY (`last_modified_by`) REFERENCES `staff` (`username`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=168 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transaction`
--

LOCK TABLES `transaction` WRITE;
/*!40000 ALTER TABLE `transaction` DISABLE KEYS */;
INSERT INTO `transaction` VALUES ('2022-01-02 08:30:00',1,37,10,'hs1'),('2022-01-02 08:30:00',1,38,10,'hs1'),('2022-01-02 08:30:00',1,40,10,'hs1'),('2022-01-02 08:30:00',1,41,10,'hs1'),('2022-01-02 08:30:00',1,42,10,'hs1'),('2022-01-03 09:30:00',10,50,-3,'ad1'),('2022-01-03 10:30:00',12,60,-1,'ad1'),('2022-01-03 10:35:00',13,37,-4,'ad1'),('2022-01-03 16:00:00',15,57,-5,'ad1'),('2022-01-04 16:30:00',18,49,-2,'ad1'),('2022-01-06 08:30:00',22,57,9,'jk1'),('2022-01-06 08:30:00',22,63,7,'jk1'),('2022-01-07 08:30:00',25,70,46,'jk1'),('2022-01-09 08:30:00',26,59,36,'ad1'),('2022-01-12 08:30:00',32,40,8,'ad1'),('2022-01-11 08:30:00',32,66,24,'ad1'),('2022-01-13 08:30:00',33,53,30,'ad1'),('2022-01-13 08:30:00',33,62,8,'ad1'),('2022-01-14 08:30:00',34,58,9,'hs1'),('2022-01-14 08:30:00',34,61,23,'hs1'),('2022-01-15 09:33:00',38,43,-2,'jk1'),('2022-01-15 09:37:00',43,45,-2,'jk1'),('2022-01-15 09:52:00',46,37,-2,'jk1'),('2022-01-15 14:30:00',49,72,-2,'jk1'),('2022-01-15 14:45:00',51,69,-2,'jk1'),('2022-01-15 14:48:00',54,60,-2,'jk1'),('2022-01-15 16:30:00',55,63,-4,'jk1'),('2022-01-15 16:32:00',56,44,-1,'jk1'),('2022-01-15 16:33:00',57,57,-4,'jk1'),('2022-01-15 16:35:00',59,37,-4,'jk1'),('2022-01-15 16:36:00',60,57,-4,'jk1'),('2022-01-15 16:38:00',62,41,-4,'jk1'),('2022-01-15 16:45:00',64,61,-1,'jk1'),('2022-01-16 08:30:00',69,37,36,'jk1'),('2022-01-16 08:30:00',69,41,48,'jk1'),('2022-01-16 08:30:00',69,59,39,'jk1'),('2022-01-16 10:00:00',74,40,-1,'jk1'),('2022-01-16 14:30:00',75,60,-3,'jk1'),('2022-01-16 14:32:00',76,69,-1,'jk1'),('2022-01-16 14:36:00',80,62,-2,'jk1'),('2022-01-16 16:30:00',81,50,-3,'jk1'),('2022-01-16 16:37:00',88,44,-2,'jk1'),('2022-01-20 08:30:00',90,45,25,'jk1'),('2022-01-20 09:30:00',91,44,-2,'jk1'),('2022-01-20 09:31:00',92,48,-4,'jk1'),('2022-01-20 09:34:00',95,67,-3,'jk1'),('2022-01-20 09:45:00',96,48,-4,'jk1'),('2022-01-31 09:30:00',107,50,34,'ad1'),('2022-02-04 08:30:00',114,42,37,'ad1'),('2022-02-04 08:30:00',114,59,14,'ad1'),('2022-02-05 08:30:00',115,54,16,'ad1'),('2022-02-05 08:30:00',115,62,20,'ad1'),('2022-04-16 21:43:07',124,54,1,'ad1'),('2022-04-16 21:46:02',125,45,1,'ad1'),('2022-01-02 08:30:00',128,54,6,'at1'),('2022-04-17 16:05:26',129,54,6,'at1'),('2022-04-17 16:05:26',130,54,6,'at1'),('2022-04-17 16:08:51',131,54,6,'at1'),('2022-04-19 12:07:06',145,44,-2,'ad1'),('2022-04-19 12:29:46',146,44,-2,'ad1'),('2022-04-19 12:29:59',147,44,10,'at1'),('2022-04-24 14:49:51',149,88,8,'at1'),('2022-04-24 19:44:37',150,44,-2,'ad1'),('2022-04-27 17:47:33',151,44,-10,'ad1'),('2022-04-30 01:53:33',152,44,-2,'ad1'),('2022-04-30 02:01:32',153,44,10,'ad1'),('2022-05-01 16:09:54',154,43,10,'ad1'),('2022-05-01 16:10:09',155,44,100,'ad1'),('2022-05-01 16:10:20',156,48,100,'ad1'),('2022-05-01 16:10:50',157,49,150,'ad1'),('2022-05-01 16:10:55',158,57,152,'ad1'),('2022-05-01 16:11:00',159,60,20,'ad1'),('2022-05-01 16:11:07',160,67,70,'ad1'),('2022-05-01 16:11:13',161,69,22,'ad1'),('2022-05-01 16:11:17',162,72,50,'ad1'),('2022-05-02 01:22:56',163,42,-10,'ad1'),('2022-05-02 01:32:12',166,102,2,'ad1'),('2022-05-02 01:32:41',167,102,-2,'ad1');
/*!40000 ALTER TABLE `transaction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `userpass`
--

DROP TABLE IF EXISTS `userpass`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `userpass` (
  `username` varchar(10) NOT NULL,
  `hashed` char(60) NOT NULL,
  PRIMARY KEY (`username`),
  UNIQUE KEY `username` (`username`),
  KEY `username_2` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userpass`
--

LOCK TABLES `userpass` WRITE;
/*!40000 ALTER TABLE `userpass` DISABLE KEYS */;
INSERT INTO `userpass` VALUES ('ad1','$2b$12$puZ5tx.cUkfspYXDKArDtu5kuQhNysJY3k1d/IqlUBZP4WNmf0peK'),('ag1','$2b$12$XOb74pbnHl7pXWrXI59aC.Z8bj1jViZ51xF6Gb6DVrEnTB.pOrO4m'),('al1','$2b$12$hKrRgJguYgUFaW7ONCjVou7LsJiYIST02Zms1xI.LdlAb6uMBwz0C'),('at1','$2b$12$ZfgSFKV7M/JAUaoOtu7xie/LjQMHkSkl7AHuq1aiWv0.yEMtmoZra'),('bf1','$2b$12$ceT0Oo/7eAPYDif5GlIz7.h4yKEE6ymToRKpJtjtyFlIQwzUP57My'),('bm1','$2b$12$uhBSlB71xbzZc9Z7reT.7.JB40Gu.FRxD0WsUZY/ddzZ.fbXIL5nW'),('ec1','$2b$12$utL1nZuCU50H3FoiBhePqeXKKWn15svngde/Rq72sNhS6PjCmBchG'),('hs1','$2b$12$1FvuqLP7P.I1uTIvnZWihuSXpceThWkLcHnApvybV5X1pUOW1biDK'),('jf1','$2b$12$/UboNn7tVNRefancGovaKOTxAvZsLPcjzXpjlkJlViye7Gj2.uoLG'),('jk1','$2b$12$eF390PQ9mOAL8vjCk.RJM.H1sZG5hGZaAwCGt0A33oTZ0ZYGvqVZW');
/*!40000 ALTER TABLE `userpass` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-05-02  2:08:36
