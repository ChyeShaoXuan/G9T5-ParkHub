SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `session`

CREATE DATABASE IF NOT EXISTS `session` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `session`;

-- --------------------------------------------------------

--
-- Table structure for table `session`
--

DROP TABLE IF EXISTS `session`;
CREATE TABLE IF NOT EXISTS `session` (
  `sessionID` int NOT NULL AUTO_INCREMENT,
  `starttime` datetime NOT NULL,
  `endtime` datetime NOT NULL,
  `ppCode` varchar(5) NOT NULL,
  `userID` int NOT NULL,
  `notifAllowed` boolean NOT NULL,
  PRIMARY KEY (`sessionID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `session` (`sessionID`, `starttime`, `endtime`, `ppCode`, `userID`, `notifAllowed`) 
VALUES (NULL, '2024-03-15 07:02:37.000000', '2024-03-15 07:02:37.000000', '12', '6', '1');


