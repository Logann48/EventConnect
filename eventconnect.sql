-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 26-09-2023 a las 21:21:55
-- Versión del servidor: 10.4.28-MariaDB
-- Versión de PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `eventconnect`
--
CREATE DATABASE IF NOT EXISTS `eventconnect` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `eventconnect`;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `compra`
--

CREATE TABLE `compra` (
  `id_Compra` int(11) NOT NULL,
  `cedula` int(11) NOT NULL,
  `id_Evento` int(11) NOT NULL,
  `id_DetallePago` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `compra`
--

INSERT INTO `compra` (`id_Compra`, `cedula`, `id_Evento`, `id_DetallePago`) VALUES
(12, 28019006, 1, 28),
(13, 28019006, 1, 29),
(14, 28019006, 1, 30),
(15, 28019006, 1, 31);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_compra`
--

CREATE TABLE `detalle_compra` (
  `id_DetalleCompra` int(11) NOT NULL,
  `id_Compra` int(11) NOT NULL,
  `precio` int(11) NOT NULL,
  `id_TipoEntrada` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `detalle_compra`
--

INSERT INTO `detalle_compra` (`id_DetalleCompra`, `id_Compra`, `precio`, `id_TipoEntrada`, `cantidad`) VALUES
(13, 12, 5000, 1, 3),
(14, 12, 6000, 2, 2),
(15, 13, 5000, 1, 9),
(16, 13, 6000, 2, 0),
(17, 13, 7000, 3, 0),
(18, 14, 6000, 2, 11),
(19, 15, 6000, 2, 11);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_pago`
--

CREATE TABLE `detalle_pago` (
  `id_DetallePago` int(11) NOT NULL,
  `cedula` int(11) NOT NULL,
  `fecha_Compra` datetime NOT NULL,
  `Nombre_Apellido` text NOT NULL,
  `cedula_Pagador` int(11) NOT NULL,
  `Metodo_Pago` text NOT NULL,
  `fecha_Pago` date NOT NULL,
  `Referencia_Pago` int(11) NOT NULL,
  `telefono_Cuenta` int(11) NOT NULL,
  `monto` int(11) NOT NULL,
  `id_Capture` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `detalle_pago`
--

INSERT INTO `detalle_pago` (`id_DetallePago`, `cedula`, `fecha_Compra`, `Nombre_Apellido`, `cedula_Pagador`, `Metodo_Pago`, `fecha_Pago`, `Referencia_Pago`, `telefono_Cuenta`, `monto`, `id_Capture`) VALUES
(1, 28019006, '2023-09-22 17:42:32', 'carlos', 28019006, 'Pago Movil', '2023-09-20', 132312, 3216, 200, 'caps/Acer_Wallpaper_03_3840x2400.jpg'),
(2, 28019006, '2023-09-22 18:38:30', 'ramon', 0, 'Pago Movil', '2023-09-20', 2147483647, 3674, 700, 'caps/Acer_Wallpaper_03_3840x2400.jpg'),
(3, 28019006, '2023-09-22 18:39:36', 'nahomy', 15884430, 'Transferencia', '2023-09-20', 2147483647, 54665465, 350, 'caps/Acer_Wallpaper_01_3840x2400.jpg'),
(28, 28019006, '2023-09-22 22:39:14', 'calo', 5248071, 'Transferencia', '2023-09-27', 132131231, 2147483647, 350, 'caps/Acer_Wallpaper_01_3840x2400.jpg'),
(29, 28019006, '2023-09-23 14:10:12', 'joan', 897987967, 'Pago Movil', '2023-09-22', 2147483647, 9876543, 251, 'caps/Acer_Wallpaper_05_3840x2400.jpg'),
(30, 28019006, '2023-09-23 14:19:22', 'cratos', 2147483647, 'Pago Movil', '2023-11-06', 2147483647, 2147483647, 109, 'caps/Acer_Wallpaper_02_3840x2400.jpg'),
(31, 28019006, '2023-09-23 16:50:11', 'ghghgjhgj', 12345698, 'Pago Movil', '2023-06-01', 98765777, 2147483647, 124, 'caps/Acer_Wallpaper_01_3840x2400.jpg');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `entrada_evento`
--

CREATE TABLE `entrada_evento` (
  `id_Entrada_Evento` int(11) NOT NULL,
  `id_Evento` int(11) NOT NULL,
  `id_TipoEntrada` int(11) DEFAULT NULL,
  `Cantidad_Disp` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `entrada_evento`
--

INSERT INTO `entrada_evento` (`id_Entrada_Evento`, `id_Evento`, `id_TipoEntrada`, `Cantidad_Disp`) VALUES
(3, 1, 1, 100),
(4, 1, 2, 101),
(5, 1, 3, 102),
(11, 47, 22, 100),
(12, 47, 23, 100);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `eventos`
--

CREATE TABLE `eventos` (
  `id_Evento` int(11) NOT NULL,
  `cedula` int(11) NOT NULL,
  `nombre` varchar(300) NOT NULL,
  `fecha_Evento` datetime NOT NULL,
  `descripcion` longtext NOT NULL,
  `estado` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `eventos`
--

INSERT INTO `eventos` (`id_Evento`, `cedula`, `nombre`, `fecha_Evento`, `descripcion`, `estado`) VALUES
(1, 8064454, 'caramelos', '2023-09-20 19:42:00', 'asdasfasfafasdasdasd', 1),
(2, 8064454, 'sifuentes', '2023-09-20 20:46:00', 'pinpinpinpum', 1),
(3, 8064454, 'tribilines', '2023-09-20 20:46:00', 'pinpinpinpum', 1),
(4, 8064454, 'cromozoma', '2023-09-21 20:46:00', 'pinpinpinpumadsssssssssssssssss', 1),
(9, 8064454, 'alogodon de azucar1', '2023-09-29 21:40:00', 'fghdjhghjghjfghjf', 1),
(11, 28019006, 'guaco', '2023-09-23 18:07:00', 'asdasdasdasdasd', 1),
(13, 28019006, 'mesoneros', '2023-09-29 13:12:00', 'asdadasda', 1),
(47, 28019006, 'a', '2023-09-28 13:14:00', 'a', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `fotos`
--

CREATE TABLE `fotos` (
  `id_foto` int(11) NOT NULL,
  `id_Evento` int(11) NOT NULL,
  `foto` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `fotos`
--

INSERT INTO `fotos` (`id_foto`, `id_Evento`, `foto`) VALUES
(12, 1, 'pics\\256px-The_Sun.jpg'),
(13, 1, 'pics\\5_1.jpg'),
(14, 1, 'pics\\5_2.jpg'),
(15, 1, 'pics\\5_3.jpg'),
(16, 9, 'pics\\base_de_datos.jfif'),
(17, 9, 'pics\\base.png'),
(18, 13, 'pics\\Acer_Wallpaper_01_3840x2400.jpg');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `login`
--

CREATE TABLE `login` (
  `cedula` int(11) NOT NULL,
  `password` text NOT NULL,
  `estado` tinyint(4) NOT NULL,
  `tipo` tinyint(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `login`
--

INSERT INTO `login` (`cedula`, `password`, `estado`, `tipo`) VALUES
(8064454, 'pbkdf2:sha256:600000$gZXjEruNBqv7guy8$23d83902d68e2f83874c2674d4b9995f99af59115f477186c1291763fca71133', 1, 1),
(15884430, 'pbkdf2:sha256:600000$0zj4IEMTblSyeXSs$46ee0351ff3673aff939bfc1b6862b2a61d8d45c65904f2ece336e7c8a2d04fc', 1, 2),
(28019006, 'pbkdf2:sha256:600000$CjBfUJnzhd9vEdL2$9b1dbd168a9c696cc4058f62c28d54ecc226d1c42ac3a063d45ea03aa5d4afb9', 1, 3);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipo_entrada`
--

CREATE TABLE `tipo_entrada` (
  `id_TipoEntrada` int(11) NOT NULL,
  `tipo` text NOT NULL,
  `Precio` decimal(11,0) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tipo_entrada`
--

INSERT INTO `tipo_entrada` (`id_TipoEntrada`, `tipo`, `Precio`) VALUES
(1, 'general', 5000),
(2, 'premium', 6000),
(3, 'ultra', 7000),
(22, 'b', 1),
(23, 'c', 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `cedula` int(11) NOT NULL,
  `nombre` text NOT NULL,
  `apellido` text NOT NULL,
  `correo` text NOT NULL,
  `telefono` bigint(12) NOT NULL,
  `direccion` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`cedula`, `nombre`, `apellido`, `correo`, `telefono`, `direccion`) VALUES
(8064454, 'inma', 'bastidas', 'inma@gmail.com', 4125217525, 'el paraiso '),
(15884430, 'nahomy', 'sequera', 'nchsequera@gmail.com', 4125217525, 'el paraisowoo'),
(28019006, 'carlos', 'sequera', 'carlos@gmail.com', 4127736602, 'el paraiso');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `compra`
--
ALTER TABLE `compra`
  ADD PRIMARY KEY (`id_Compra`),
  ADD KEY `fk_compra` (`id_Evento`),
  ADD KEY `fk_compra_usuario` (`cedula`),
  ADD KEY `id_DetallePago` (`id_DetallePago`);

--
-- Indices de la tabla `detalle_compra`
--
ALTER TABLE `detalle_compra`
  ADD PRIMARY KEY (`id_DetalleCompra`),
  ADD KEY `fk_detalle_Compra` (`id_Compra`),
  ADD KEY `fk_tipo_entrada_final` (`id_TipoEntrada`);

--
-- Indices de la tabla `detalle_pago`
--
ALTER TABLE `detalle_pago`
  ADD PRIMARY KEY (`id_DetallePago`),
  ADD KEY `fk_cedula_usuario` (`cedula`);

--
-- Indices de la tabla `entrada_evento`
--
ALTER TABLE `entrada_evento`
  ADD PRIMARY KEY (`id_Entrada_Evento`),
  ADD KEY `fk_entrada_evento` (`id_Evento`),
  ADD KEY `fk_tipo_entrada` (`id_TipoEntrada`);

--
-- Indices de la tabla `eventos`
--
ALTER TABLE `eventos`
  ADD PRIMARY KEY (`id_Evento`),
  ADD KEY `cedula` (`cedula`);

--
-- Indices de la tabla `fotos`
--
ALTER TABLE `fotos`
  ADD PRIMARY KEY (`id_foto`),
  ADD KEY `fk_id_Evento` (`id_Evento`);

--
-- Indices de la tabla `login`
--
ALTER TABLE `login`
  ADD PRIMARY KEY (`cedula`);

--
-- Indices de la tabla `tipo_entrada`
--
ALTER TABLE `tipo_entrada`
  ADD PRIMARY KEY (`id_TipoEntrada`);

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`cedula`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `compra`
--
ALTER TABLE `compra`
  MODIFY `id_Compra` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT de la tabla `detalle_compra`
--
ALTER TABLE `detalle_compra`
  MODIFY `id_DetalleCompra` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT de la tabla `detalle_pago`
--
ALTER TABLE `detalle_pago`
  MODIFY `id_DetallePago` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT de la tabla `entrada_evento`
--
ALTER TABLE `entrada_evento`
  MODIFY `id_Entrada_Evento` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de la tabla `eventos`
--
ALTER TABLE `eventos`
  MODIFY `id_Evento` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=48;

--
-- AUTO_INCREMENT de la tabla `fotos`
--
ALTER TABLE `fotos`
  MODIFY `id_foto` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT de la tabla `tipo_entrada`
--
ALTER TABLE `tipo_entrada`
  MODIFY `id_TipoEntrada` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `compra`
--
ALTER TABLE `compra`
  ADD CONSTRAINT `fk_compra` FOREIGN KEY (`id_Evento`) REFERENCES `eventos` (`id_Evento`),
  ADD CONSTRAINT `fk_compra_usuario` FOREIGN KEY (`cedula`) REFERENCES `usuario` (`cedula`),
  ADD CONSTRAINT `id_DetallePago` FOREIGN KEY (`id_DetallePago`) REFERENCES `detalle_pago` (`id_DetallePago`);

--
-- Filtros para la tabla `detalle_compra`
--
ALTER TABLE `detalle_compra`
  ADD CONSTRAINT `fk_detalle_Compra` FOREIGN KEY (`id_Compra`) REFERENCES `compra` (`id_Compra`),
  ADD CONSTRAINT `fk_tipo_entrada_final` FOREIGN KEY (`id_TipoEntrada`) REFERENCES `tipo_entrada` (`id_TipoEntrada`);

--
-- Filtros para la tabla `detalle_pago`
--
ALTER TABLE `detalle_pago`
  ADD CONSTRAINT `fk_cedula_usuario` FOREIGN KEY (`cedula`) REFERENCES `usuario` (`cedula`);

--
-- Filtros para la tabla `entrada_evento`
--
ALTER TABLE `entrada_evento`
  ADD CONSTRAINT `fk_entrada_evento` FOREIGN KEY (`id_Evento`) REFERENCES `eventos` (`id_Evento`),
  ADD CONSTRAINT `fk_tipo_entrada` FOREIGN KEY (`id_TipoEntrada`) REFERENCES `tipo_entrada` (`id_TipoEntrada`);

--
-- Filtros para la tabla `eventos`
--
ALTER TABLE `eventos`
  ADD CONSTRAINT `eventos_ibfk_1` FOREIGN KEY (`cedula`) REFERENCES `usuario` (`cedula`);

--
-- Filtros para la tabla `fotos`
--
ALTER TABLE `fotos`
  ADD CONSTRAINT `fk_id_Evento` FOREIGN KEY (`id_Evento`) REFERENCES `eventos` (`id_Evento`);

--
-- Filtros para la tabla `login`
--
ALTER TABLE `login`
  ADD CONSTRAINT `login_ibfk_1` FOREIGN KEY (`cedula`) REFERENCES `usuario` (`cedula`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
