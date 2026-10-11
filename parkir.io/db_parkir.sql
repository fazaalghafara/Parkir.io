-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 11, 2026 at 12:26 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_parkir`
--

-- --------------------------------------------------------

--
-- Table structure for table `log_parkir`
--

CREATE TABLE `log_parkir` (
  `id` int(11) NOT NULL,
  `waktu` datetime NOT NULL,
  `tipe_kendaraan` varchar(20) NOT NULL,
  `track_id` int(11) NOT NULL,
  `lokasi` varchar(50) DEFAULT 'Parkir A',
  `status` varchar(10) DEFAULT 'MASUK'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `log_parkir`
--

INSERT INTO `log_parkir` (`id`, `waktu`, `tipe_kendaraan`, `track_id`, `lokasi`, `status`) VALUES
(1, '2026-06-18 19:37:24', 'mobil', 3, 'Parkir A', 'MASUK'),
(2, '2026-06-19 03:11:25', 'motor', 4, 'Parkir A', 'MASUK'),
(3, '2026-06-19 04:18:55', 'RFID_Card', 7, 'Parkir A', 'KELUAR'),
(4, '2026-06-19 04:26:31', 'mobil', 15, 'Parkir A', 'MASUK'),
(5, '2026-06-19 04:27:12', 'mobil', 26, 'Parkir A', 'MASUK'),
(6, '2026-06-19 04:28:15', 'mobil', 39, 'Parkir A', 'MASUK'),
(7, '2026-06-19 04:28:37', 'mobil', 45, 'Parkir A', 'MASUK'),
(8, '2026-06-19 04:29:40', 'RFID_Card', 7, 'Parkir A', 'KELUAR'),
(9, '2026-06-19 04:29:50', 'RFID_Card', 7, 'Parkir A', 'KELUAR'),
(10, '2026-06-19 04:29:58', 'RFID_Card', 7, 'Parkir A', 'KELUAR'),
(11, '2026-06-20 15:35:35', 'RFID_Card', 7, 'Parkir A', 'KELUAR'),
(12, '2026-06-20 15:35:37', 'RFID_Card', 7, 'Parkir A', 'KELUAR'),
(13, '2026-06-20 15:39:20', 'motor', 4, 'Parkir A', 'MASUK'),
(14, '2026-06-20 15:40:06', 'motor', 8, 'Parkir A', 'MASUK'),
(15, '2026-06-20 15:40:32', 'truk', 10, 'Parkir A', 'MASUK'),
(16, '2026-06-20 17:41:20', 'RFID_Card', 7, 'Parkir A', 'KELUAR'),
(17, '2026-06-20 17:41:29', 'RFID_Card', 42, 'Parkir A', 'KELUAR'),
(18, '2026-06-20 17:51:44', 'mobil', 4, 'Parkir A', 'MASUK'),
(19, '2026-06-20 18:05:46', 'bus', 1, 'Parkir A', 'MASUK'),
(20, '2026-06-20 18:25:07', 'RFID_Card', 7, 'Parkir A', 'KELUAR'),
(21, '2026-06-20 18:25:24', 'RFID_Card', 7, 'Parkir A', 'KELUAR'),
(22, '2026-06-20 18:25:29', 'RFID_Card', 7, 'Parkir A', 'KELUAR');

-- --------------------------------------------------------

--
-- Table structure for table `status_parkir`
--

CREATE TABLE `status_parkir` (
  `lokasi` varchar(50) NOT NULL,
  `kapasitas_maks` int(11) DEFAULT NULL,
  `slot_terisi` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `status_parkir`
--

INSERT INTO `status_parkir` (`lokasi`, `kapasitas_maks`, `slot_terisi`) VALUES
('Parkir A', 50, 0);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `log_parkir`
--
ALTER TABLE `log_parkir`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `status_parkir`
--
ALTER TABLE `status_parkir`
  ADD PRIMARY KEY (`lokasi`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `log_parkir`
--
ALTER TABLE `log_parkir`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
