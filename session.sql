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
--
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
  PRIMARY KEY (`sessionID`),
  FOREIGN KEY (userID) REFERENCES User(userID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --
-- -- Dumping data for table `book`
-- --

-- INSERT INTO `user` (`name`, `email`, `password`, `phoneNo`, `notifAllowed`) VALUES
-- ('Amy Chan', 'amychan@gmail.com', 'iloveamy1', '91237789', False),
-- ('Ben Lim', 'benlim@gmail.com', 'weatherhot8', '87734672', False),
-- ('Chan Jun Jie', 'chanjunjie@gmail.com', 'iamcjj00', '90013008', False),
-- ('Daphne Tan', 'daphnetan@gmail.com', 'nyc88brooklyn', '97653303', False),
-- ('Evan Teo', 'evanteo@gmail.com', 'evanoet90', '81919089', False);
-- COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
