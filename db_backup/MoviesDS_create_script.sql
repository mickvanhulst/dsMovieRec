-- phpMyAdmin SQL Dump
-- version 4.5.4.1deb2ubuntu2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Gegenereerd op: 08 dec 2016 om 15:00
-- Serverversie: 5.7.16-0ubuntu0.16.04.1
-- PHP-versie: 7.0.8-0ubuntu0.16.04.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `MoviesDS`
--
CREATE DATABASE IF NOT EXISTS `MoviesDS` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `MoviesDS`;

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `genKeywords`
--

DROP TABLE IF EXISTS `genKeywords`;
CREATE TABLE IF NOT EXISTS `genKeywords` (
  `genKeywordId` int(2) NOT NULL AUTO_INCREMENT,
  `movieId` bigint(20) DEFAULT NULL,
  `Keyword` varchar(63) DEFAULT NULL,
  PRIMARY KEY (`genKeywordId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- RELATIES VOOR TABEL `genKeywords`:
--

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `movies`
--

DROP TABLE IF EXISTS `movies`;
CREATE TABLE IF NOT EXISTS `movies` (
  `movieId` bigint(20) NOT NULL,
  `imdbId` varchar(255) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `year` int(4) DEFAULT NULL,
  `genres` varchar(255) DEFAULT NULL,
  `Plot` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`movieId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- RELATIES VOOR TABEL `movies`:
--

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `ratings`
--

DROP TABLE IF EXISTS `ratings`;
CREATE TABLE IF NOT EXISTS `ratings` (
  `userId` int(20) NOT NULL,
  `movieId` int(20) NOT NULL,
  `rating` double NOT NULL,
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`userId`,`movieId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- RELATIES VOOR TABEL `ratings`:
--

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `sampleUserInitial`
--

DROP TABLE IF EXISTS `sampleUserInitial`;
CREATE TABLE IF NOT EXISTS `sampleUserInitial` (
  `movieId` int(20) NOT NULL,
  `points` int(30) NOT NULL,
  `timestamp` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`movieId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- RELATIES VOOR TABEL `sampleUserInitial`:
--

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `user`
--

DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `userId` int(20) NOT NULL,
  `username` varchar(30) NOT NULL,
  `password` varchar(20) DEFAULT NULL,
  `firstName` varchar(30) DEFAULT NULL,
  `lastName` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`userId`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- RELATIES VOOR TABEL `user`:
--

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `userRecommendations`
--

DROP TABLE IF EXISTS `userRecommendations`;
CREATE TABLE IF NOT EXISTS `userRecommendations` (
  `userId` int(20) NOT NULL,
  `movieId` int(10) NOT NULL,
  `beginDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `endDate` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`userId`,`movieId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- RELATIES VOOR TABEL `userRecommendations`:
--

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
