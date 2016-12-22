-- phpMyAdmin SQL Dump
-- version 4.5.4.1deb2ubuntu2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Gegenereerd op: 25 nov 2016 om 10:35
-- Serverversie: 5.7.16-0ubuntu0.16.04.1
-- PHP-versie: 7.0.8-0ubuntu0.16.04.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


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
CREATE TABLE `genKeywords` (
  `genKeywordId` bigint(20) DEFAULT NULL,
  `movieId` bigint(20) DEFAULT NULL,
  `Keyword` varchar(63) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `genres`
--

DROP TABLE IF EXISTS `genres`;
CREATE TABLE `genres` (
  `genreId` int(2) NOT NULL,
  `genre` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `movieGenre`
--

DROP TABLE IF EXISTS `movieGenre`;
CREATE TABLE `movieGenre` (
  `movieId` int(20) NOT NULL,
  `genreId` int(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `movies`
--

DROP TABLE IF EXISTS `movies`;
CREATE TABLE `movies` (
  `movieId` bigint(20) NOT NULL,
  `imdbId` varchar(15) NOT NULL,
  `title` varchar(63) DEFAULT NULL,
  `year` int(4) NOT NULL,
  `genres` varchar(63) DEFAULT NULL,
  `Plot` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `user`
--

DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `userId` int(20) NOT NULL,
  `username` varchar(30) NOT NULL,
  `password` varchar(20) NOT NULL,
  `firstName` varchar(30) NOT NULL,
  `lastName` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `userInitialMovies`
--

DROP TABLE IF EXISTS `userInitialMovies`;
CREATE TABLE `userInitialMovies` (
  `userId` int(20) NOT NULL,
  `movieId` int(10) NOT NULL,
  `beginDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `endDate` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `userRating`
--

DROP TABLE IF EXISTS `userRating`;
CREATE TABLE `userRating` (
  `imdbId` varchar(15) NOT NULL,
  `rating` float NOT NULL,
  `userId` int(20) NOT NULL,
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Indexen voor geëxporteerde tabellen
--

--
-- Indexen voor tabel `genres`
--
ALTER TABLE `genres`
  ADD PRIMARY KEY (`genreId`);

--
-- Indexen voor tabel `movieGenre`
--
ALTER TABLE `movieGenre`
  ADD PRIMARY KEY (`movieId`,`genreId`);

--
-- Indexen voor tabel `movies`
--
ALTER TABLE `movies`
  ADD PRIMARY KEY (`movieId`);

--
-- Indexen voor tabel `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`userId`);

--
-- Indexen voor tabel `userInitialMovies`
--
ALTER TABLE `userInitialMovies`
  ADD PRIMARY KEY (`userId`,`movieId`);

--
-- AUTO_INCREMENT voor geëxporteerde tabellen
--

--
-- AUTO_INCREMENT voor een tabel `genres`
--
ALTER TABLE `genres`
  MODIFY `genreId` int(2) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
