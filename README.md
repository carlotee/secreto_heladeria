MySql usar php [secreto_helader__a.sql](https://github.com/user-attachments/files/22579828/secreto_helader__a.sql)
-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3306
-- Tiempo de generación: 28-09-2025 a las 02:44:03
-- Versión del servidor: 9.1.0
-- Versión de PHP: 8.3.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `secreto_heladería`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `accounts_usuario`
--

DROP TABLE IF EXISTS `accounts_usuario`;
CREATE TABLE IF NOT EXISTS `accounts_usuario` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `username` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `numero` varchar(15) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `accounts_usuario`
--

INSERT INTO `accounts_usuario` (`id`, `password`, `last_login`, `is_superuser`, `first_name`, `last_name`, `is_staff`, `is_active`, `date_joined`, `username`, `email`, `numero`, `created_at`, `updated_at`) VALUES
(1, 'pbkdf2_sha256$1000000$IcEL4ophPKRzaU8ob4zn17$4Nt0WNP0NGZtWi0zIDNjySKJYSq3N19qPvBKMdK2O2U=', '2025-09-27 23:37:10.751352', 0, '', '', 0, 1, '2025-09-27 23:30:21.778715', 'pato', '', NULL, '2025-09-27 23:30:21.779624', '2025-09-27 23:30:23.376916'),
(2, 'pbkdf2_sha256$1000000$nk3e5RBNOP30Ak0vgExG9B$heTuGKQ0hBzwskCmO7wsqtXDuKdxJurHn6KcKHeeyzY=', '2025-09-28 01:03:47.266309', 1, '', '', 1, 1, '2025-09-28 01:03:29.883551', 'Admin', 'alexiseba15@gmail.com', NULL, '2025-09-28 01:03:31.288574', '2025-09-28 01:03:31.288592');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `accounts_usuario_groups`
--

DROP TABLE IF EXISTS `accounts_usuario_groups`;
CREATE TABLE IF NOT EXISTS `accounts_usuario_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `usuario_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_usuario_groups_usuario_id_group_id_90f476d3_uniq` (`usuario_id`,`group_id`),
  KEY `accounts_usuario_groups_usuario_id_8eb16911` (`usuario_id`),
  KEY `accounts_usuario_groups_group_id_81d91a41` (`group_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `accounts_usuario_user_permissions`
--

DROP TABLE IF EXISTS `accounts_usuario_user_permissions`;
CREATE TABLE IF NOT EXISTS `accounts_usuario_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `usuario_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_usuario_user_pe_usuario_id_permission_id_0065a2ce_uniq` (`usuario_id`,`permission_id`),
  KEY `accounts_usuario_user_permissions_usuario_id_d048ad71` (`usuario_id`),
  KEY `accounts_usuario_user_permissions_permission_id_3de42c14` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_group_id_b120cbf9` (`group_id`),
  KEY `auth_group_permissions_permission_id_84c5c92e` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  KEY `auth_permission_content_type_id_2f476e4b` (`content_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=81 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add content type', 4, 'add_contenttype'),
(14, 'Can change content type', 4, 'change_contenttype'),
(15, 'Can delete content type', 4, 'delete_contenttype'),
(16, 'Can view content type', 4, 'view_contenttype'),
(17, 'Can add session', 5, 'add_session'),
(18, 'Can change session', 5, 'change_session'),
(19, 'Can delete session', 5, 'delete_session'),
(20, 'Can view session', 5, 'view_session'),
(21, 'Can add registro', 6, 'add_registro'),
(22, 'Can change registro', 6, 'change_registro'),
(23, 'Can delete registro', 6, 'delete_registro'),
(24, 'Can view registro', 6, 'view_registro'),
(25, 'Can add user', 7, 'add_usuario'),
(26, 'Can change user', 7, 'change_usuario'),
(27, 'Can delete user', 7, 'delete_usuario'),
(28, 'Can view user', 7, 'view_usuario'),
(29, 'Can add organization', 8, 'add_organization'),
(30, 'Can change organization', 8, 'change_organization'),
(31, 'Can delete organization', 8, 'delete_organization'),
(32, 'Can view organization', 8, 'view_organization'),
(33, 'Can add centro_ costos', 9, 'add_centro_costos'),
(34, 'Can change centro_ costos', 9, 'change_centro_costos'),
(35, 'Can delete centro_ costos', 9, 'delete_centro_costos'),
(36, 'Can view centro_ costos', 9, 'view_centro_costos'),
(37, 'Can add gastos comunes', 10, 'add_gastoscomunes'),
(38, 'Can change gastos comunes', 10, 'change_gastoscomunes'),
(39, 'Can delete gastos comunes', 10, 'delete_gastoscomunes'),
(40, 'Can view gastos comunes', 10, 'view_gastoscomunes'),
(41, 'Can add boleta gc', 11, 'add_boletagc'),
(42, 'Can change boleta gc', 11, 'change_boletagc'),
(43, 'Can delete boleta gc', 11, 'delete_boletagc'),
(44, 'Can view boleta gc', 11, 'view_boletagc'),
(45, 'Can add detalle compra', 12, 'add_detallecompra'),
(46, 'Can change detalle compra', 12, 'change_detallecompra'),
(47, 'Can delete detalle compra', 12, 'delete_detallecompra'),
(48, 'Can view detalle compra', 12, 'view_detallecompra'),
(49, 'Can add producto', 13, 'add_producto'),
(50, 'Can change producto', 13, 'change_producto'),
(51, 'Can delete producto', 13, 'delete_producto'),
(52, 'Can view producto', 13, 'view_producto'),
(53, 'Can add proveedor', 14, 'add_proveedor'),
(54, 'Can change proveedor', 14, 'change_proveedor'),
(55, 'Can delete proveedor', 14, 'delete_proveedor'),
(56, 'Can view proveedor', 14, 'view_proveedor'),
(57, 'Can add orden compra', 15, 'add_ordencompra'),
(58, 'Can change orden compra', 15, 'change_ordencompra'),
(59, 'Can delete orden compra', 15, 'delete_ordencompra'),
(60, 'Can view orden compra', 15, 'view_ordencompra'),
(61, 'Can add cliente', 16, 'add_cliente'),
(62, 'Can change cliente', 16, 'change_cliente'),
(63, 'Can delete cliente', 16, 'delete_cliente'),
(64, 'Can view cliente', 16, 'view_cliente'),
(65, 'Can add reparto', 17, 'add_reparto'),
(66, 'Can change reparto', 17, 'change_reparto'),
(67, 'Can delete reparto', 17, 'delete_reparto'),
(68, 'Can view reparto', 17, 'view_reparto'),
(69, 'Can add usuario', 18, 'add_usuario'),
(70, 'Can change usuario', 18, 'change_usuario'),
(71, 'Can delete usuario', 18, 'delete_usuario'),
(72, 'Can view usuario', 18, 'view_usuario'),
(73, 'Can add detalle venta', 19, 'add_detalleventa'),
(74, 'Can change detalle venta', 19, 'change_detalleventa'),
(75, 'Can delete detalle venta', 19, 'delete_detalleventa'),
(76, 'Can view detalle venta', 19, 'view_detalleventa'),
(77, 'Can add ventas', 20, 'add_ventas'),
(78, 'Can change ventas', 20, 'change_ventas'),
(79, 'Can delete ventas', 20, 'delete_ventas'),
(80, 'Can view ventas', 20, 'view_ventas');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `centro_costos_centro_costos`
--

DROP TABLE IF EXISTS `centro_costos_centro_costos`;
CREATE TABLE IF NOT EXISTS `centro_costos_centro_costos` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `deleted_at` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint UNSIGNED NOT NULL,
  `change_message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6` (`user_id`)
) ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=MyISAM AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(2, 'auth', 'permission'),
(3, 'auth', 'group'),
(4, 'contenttypes', 'contenttype'),
(5, 'sessions', 'session'),
(6, 'accounts', 'registro'),
(7, 'accounts', 'usuario'),
(8, 'organizations', 'organization'),
(9, 'centro_costos', 'centro_costos'),
(10, 'gastos_comunes', 'gastoscomunes'),
(11, 'gastos_comunes', 'boletagc'),
(12, 'produccion', 'detallecompra'),
(13, 'produccion', 'producto'),
(14, 'produccion', 'proveedor'),
(15, 'produccion', 'ordencompra'),
(16, 'reparto', 'cliente'),
(17, 'reparto', 'reparto'),
(18, 'reparto', 'usuario'),
(19, 'reparto', 'detalleventa'),
(20, 'reparto', 'ventas');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2025-09-27 03:43:23.152864'),
(2, 'contenttypes', '0002_remove_content_type_name', '2025-09-27 03:43:23.923601'),
(3, 'auth', '0001_initial', '2025-09-27 03:43:26.955999'),
(4, 'auth', '0002_alter_permission_name_max_length', '2025-09-27 03:43:27.228592'),
(5, 'auth', '0003_alter_user_email_max_length', '2025-09-27 03:43:27.244620'),
(6, 'auth', '0004_alter_user_username_opts', '2025-09-27 03:43:27.262965'),
(7, 'auth', '0005_alter_user_last_login_null', '2025-09-27 03:43:27.281535'),
(8, 'auth', '0006_require_contenttypes_0002', '2025-09-27 03:43:27.287463'),
(9, 'auth', '0007_alter_validators_add_error_messages', '2025-09-27 03:43:27.294629'),
(10, 'auth', '0008_alter_user_username_max_length', '2025-09-27 03:43:27.301171'),
(11, 'auth', '0009_alter_user_last_name_max_length', '2025-09-27 03:43:27.307165'),
(12, 'auth', '0010_alter_group_name_max_length', '2025-09-27 03:43:27.872249'),
(13, 'auth', '0011_update_proxy_permissions', '2025-09-27 03:43:27.889941'),
(14, 'auth', '0012_alter_user_first_name_max_length', '2025-09-27 03:43:27.905384'),
(15, 'accounts', '0001_initial', '2025-09-27 03:43:31.640230'),
(16, 'admin', '0001_initial', '2025-09-27 03:43:33.890521'),
(17, 'admin', '0002_logentry_remove_auto_add', '2025-09-27 03:43:33.923998'),
(18, 'admin', '0003_logentry_add_action_flag_choices', '2025-09-27 03:43:33.950856'),
(19, 'organizations', '0001_initial', '2025-09-27 03:43:34.003734'),
(20, 'sessions', '0001_initial', '2025-09-27 03:43:34.639994'),
(21, 'centro_costos', '0001_initial', '2025-09-27 22:38:06.956754'),
(22, 'gastos_comunes', '0001_initial', '2025-09-27 22:38:09.053630'),
(23, 'produccion', '0001_initial', '2025-09-27 22:38:10.637428'),
(24, 'reparto', '0001_initial', '2025-09-27 22:38:12.087388'),
(25, 'produccion', '0002_producto_precio', '2025-09-28 00:09:07.101740'),
(26, 'gastos_comunes', '0002_rename_name_gastoscomunes_nombre', '2025-09-28 01:16:27.314857');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_session`
--

DROP TABLE IF EXISTS `django_session`;
CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('51qevjfbkxoegl2sfpa7sqgiezng39vf', '.eJxVjEEOwiAQRe_C2hCkMxRcuu8ZyMAMUjVtUtqV8e7apAvd_vfef6lI21rj1mSJI6uLsur0uyXKD5l2wHeabrPO87QuY9K7og_a9DCzPK-H-3dQqdVvnbAUdN44D4IkbDNichACc-4DnEtARwCFDXiRvgu2gGFMQmgydFm9P-sPOBw:1v2fpL:v4aOYL_BAwWaOzSubiCG_QI0TCJib-c639-2pMn9E-s', '2025-10-12 01:03:47.332604');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `gastos_comunes_boletagc`
--

DROP TABLE IF EXISTS `gastos_comunes_boletagc`;
CREATE TABLE IF NOT EXISTS `gastos_comunes_boletagc` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `valor` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `fecha` datetime(6) NOT NULL,
  `gastosComunes_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `gastos_comunes_boletagc_gastosComunes_id_fd2f75f7` (`gastosComunes_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `gastos_comunes_gastoscomunes`
--

DROP TABLE IF EXISTS `gastos_comunes_gastoscomunes`;
CREATE TABLE IF NOT EXISTS `gastos_comunes_gastoscomunes` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `login`
--

DROP TABLE IF EXISTS `login`;
CREATE TABLE IF NOT EXISTS `login` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `usuario` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `correo` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `contraseña` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `telefono` varchar(15) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `login`
--

INSERT INTO `login` (`id`, `usuario`, `correo`, `contraseña`, `telefono`) VALUES
(1, 'pato', 'pato@gmail.com', '12345', '+5933333333');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `organizations_organization`
--

DROP TABLE IF EXISTS `organizations_organization`;
CREATE TABLE IF NOT EXISTS `organizations_organization` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `deleted_at` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `produccion_detallecompra`
--

DROP TABLE IF EXISTS `produccion_detallecompra`;
CREATE TABLE IF NOT EXISTS `produccion_detallecompra` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `valor_unitario` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `cantidad_total` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `estado` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `producto_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `produccion_detallecompra_producto_id_44872354` (`producto_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `produccion_ordencompra`
--

DROP TABLE IF EXISTS `produccion_ordencompra`;
CREATE TABLE IF NOT EXISTS `produccion_ordencompra` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `valor_total` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `estado` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `proveedor_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `produccion_ordencompra_proveedor_id_8d4f0466` (`proveedor_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `produccion_producto`
--

DROP TABLE IF EXISTS `produccion_producto`;
CREATE TABLE IF NOT EXISTS `produccion_producto` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `precio` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `produccion_producto`
--

INSERT INTO `produccion_producto` (`id`, `nombre`, `precio`) VALUES
(1, 'Helado de Vainilla', '500'),
(2, 'Helado de Chocolate', '500');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `produccion_proveedor`
--

DROP TABLE IF EXISTS `produccion_proveedor`;
CREATE TABLE IF NOT EXISTS `produccion_proveedor` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reparto_cliente`
--

DROP TABLE IF EXISTS `reparto_cliente`;
CREATE TABLE IF NOT EXISTS `reparto_cliente` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reparto_detalleventa`
--

DROP TABLE IF EXISTS `reparto_detalleventa`;
CREATE TABLE IF NOT EXISTS `reparto_detalleventa` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `valor_unitario` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ventas_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `reparto_detalleventa_ventas_id_bb08b76a` (`ventas_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reparto_reparto`
--

DROP TABLE IF EXISTS `reparto_reparto`;
CREATE TABLE IF NOT EXISTS `reparto_reparto` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `valor` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `fecha_reparto` datetime(6) NOT NULL,
  `fecha_ingreso` datetime(6) NOT NULL,
  `usuario_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `reparto_reparto_usuario_id_3db28c56` (`usuario_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reparto_usuario`
--

DROP TABLE IF EXISTS `reparto_usuario`;
CREATE TABLE IF NOT EXISTS `reparto_usuario` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reparto_ventas`
--

DROP TABLE IF EXISTS `reparto_ventas`;
CREATE TABLE IF NOT EXISTS `reparto_ventas` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `valor_total` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `estado` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

Cargar semilla (solo he hecho una) con:
python manage.py loaddata fixtures/01_productos.json

Admin
12345



contraseña compus de Incapaz: admin
