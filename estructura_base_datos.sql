-- Estructura de la tabla cargos
CREATE TABLE `cargos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Estructura de la tabla categoria
CREATE TABLE `categoria` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Estructura de la tabla cliente
CREATE TABLE `cliente` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_persona` int(11) NOT NULL,
  `fecha_alta` datetime NOT NULL,
  `id_condicion_fiscal` int(11) NOT NULL,
  `observaciones` varchar(200) DEFAULT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT 1,
  `id_usuario` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id_persona` (`id_persona`),
  KEY `id_condicion_fiscal` (`id_condicion_fiscal`),
  KEY `id_usuario` (`id_usuario`),
  CONSTRAINT `cliente_ibfk_1` FOREIGN KEY (`id_persona`) REFERENCES `persona` (`id`),
  CONSTRAINT `cliente_ibfk_2` FOREIGN KEY (`id_condicion_fiscal`) REFERENCES `condicion_fiscal` (`id`),
  CONSTRAINT `cliente_ibfk_3` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Estructura de la tabla compra
CREATE TABLE `compra` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `numero` varchar(255) DEFAULT NULL,
  `fecha_compra` date NOT NULL,
  `id_proveedor` int(11) NOT NULL,
  `id_comprobante` int(11) NOT NULL,
  `id_forma_pago` int(11) DEFAULT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT 1,
  `fecha_carga` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `id_usuario` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id_proveedor` (`id_proveedor`),
  KEY `id_tipo_comprobante` (`id_comprobante`),
  KEY `id_forma_pago` (`id_forma_pago`),
  KEY `id_usuario` (`id_usuario`),
  CONSTRAINT `compra_ibfk_1` FOREIGN KEY (`id_proveedor`) REFERENCES `proveedor` (`id`),
  CONSTRAINT `compra_ibfk_2` FOREIGN KEY (`id_comprobante`) REFERENCES `comprobante` (`id`),
  CONSTRAINT `compra_ibfk_3` FOREIGN KEY (`id_forma_pago`) REFERENCES `forma_pago` (`id`),
  CONSTRAINT `compra_ibfk_4` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Estructura de la tabla comprobante
CREATE TABLE `comprobante` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Estructura de la tabla condicion_fiscal
CREATE TABLE `condicion_fiscal` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `iva` float NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Estructura de la tabla detalle_compra
CREATE TABLE `detalle_compra` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_compra` int(11) NOT NULL,
  `id_producto` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `precio_unitario` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id_compra` (`id_compra`),
  KEY `id_producto` (`id_producto`),
  CONSTRAINT `detalle_compra_ibfk_1` FOREIGN KEY (`id_compra`) REFERENCES `compra` (`id`),
  CONSTRAINT `detalle_compra_ibfk_2` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Estructura de la tabla detalle_factura
CREATE TABLE `detalle_factura` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_factura` int(11) NOT NULL,
  `id_producto` int(11) NOT NULL,
  `cantidad` int(12) DEFAULT NULL,
  `precio_unitario` int(15) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id_venta` (`id_factura`),
  KEY `detalle_factura_productos_FK` (`id_producto`),
  CONSTRAINT `detalle_factura_ibfk_1` FOREIGN KEY (`id_factura`) REFERENCES `factura` (`id`),
  CONSTRAINT `detalle_factura_productos_FK` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Estructura de la tabla dni_tipo
CREATE TABLE `dni_tipo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Estructura de la tabla empleado
CREATE TABLE `empleado` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_persona` int(11) NOT NULL,
  `id_cargo` int(11) NOT NULL,
  `fecha_ingreso` date NOT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT 1,
  `id_sucursal` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id_cargo` (`id_cargo`),
  KEY `id_persona` (`id_persona`),
  KEY `empleado_sucursales_FK` (`id_sucursal`),
  CONSTRAINT `empleado_ibfk_1` FOREIGN KEY (`id_cargo`) REFERENCES `cargos` (`id`),
  CONSTRAINT `empleado_ibfk_3` FOREIGN KEY (`id_persona`) REFERENCES `persona` (`id`),
  CONSTRAINT `empleado_sucursales_FK` FOREIGN KEY (`id_sucursal`) REFERENCES `sucursales` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Estructura de la tabla factura
CREATE TABLE `factura` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `numero` varchar(255) DEFAULT NULL,
  `fecha_factura` datetime NOT NULL,
  `id_cliente` int(11) NOT NULL,
  `id_tipo_comprobante` int(11) NOT NULL,
  `id_forma_pago` int(11) DEFAULT NULL,
  `total` int(15) NOT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT 1,
  `id_empleado` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id_forma_pago` (`id_forma_pago`),
  KEY `id_tipo_comprobante` (`id_tipo_comprobante`),
  KEY `id_cliente` (`id_cliente`),
  KEY `factura_empleado_FK` (`id_empleado`),
  CONSTRAINT `factura_empleado_FK` FOREIGN KEY (`id_empleado`) REFERENCES `empleado` (`id`),
  CONSTRAINT `factura_ibfk_2` FOREIGN KEY (`id_forma_pago`) REFERENCES `forma_pago` (`id`),
  CONSTRAINT `factura_ibfk_4` FOREIGN KEY (`id_tipo_comprobante`) REFERENCES `comprobante` (`id`),
  CONSTRAINT `factura_ibfk_5` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Estructura de la tabla forma_pago
CREATE TABLE `forma_pago` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Estructura de la tabla localidad
CREATE TABLE `localidad` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(75) NOT NULL,
  `id_provincia` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id_provincia` (`id_provincia`),
  CONSTRAINT `localidad_ibfk_1` FOREIGN KEY (`id_provincia`) REFERENCES `provincia` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3560 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Estructura de la tabla marcas
CREATE TABLE `marcas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Estructura de la tabla pais
CREATE TABLE `pais` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Estructura de la tabla persona
CREATE TABLE `persona` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `apellido` varchar(50) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `direccion` varchar(75) NOT NULL,
  `fecha_nacimiento` date NOT NULL,
  `id_localidad` int(11) NOT NULL,
  `id_tipo_dni` int(11) NOT NULL,
  `dni` varchar(20) NOT NULL,
  `mail` varchar(30) DEFAULT NULL,
  `telefono` varchar(15) NOT NULL,
  `id_condicion_fiscal` int(11) NOT NULL,
  `id_sexo` int(11) NOT NULL,
  `id_pais` int(11) NOT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT 1,
  `fecha_carga` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `id_usuario` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id_razon_social` (`id_condicion_fiscal`),
  KEY `id_pais` (`id_pais`),
  KEY `id_tipo_dni` (`id_tipo_dni`),
  KEY `id_sexo` (`id_sexo`),
  KEY `id_usuario` (`id_usuario`),
  KEY `id_localidad` (`id_localidad`),
  CONSTRAINT `persona_ibfk_3` FOREIGN KEY (`id_condicion_fiscal`) REFERENCES `condicion_fiscal` (`id`),
  CONSTRAINT `persona_ibfk_4` FOREIGN KEY (`id_pais`) REFERENCES `pais` (`id`),
  CONSTRAINT `persona_ibfk_5` FOREIGN KEY (`id_tipo_dni`) REFERENCES `dni_tipo` (`id`),
  CONSTRAINT `persona_ibfk_6` FOREIGN KEY (`id_sexo`) REFERENCES `sexo` (`id`),
  CONSTRAINT `persona_ibfk_7` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id`),
  CONSTRAINT `persona_ibfk_8` FOREIGN KEY (`id_localidad`) REFERENCES `localidad` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Estructura de la tabla productos
CREATE TABLE `productos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(150) NOT NULL,
  `descripcion` varchar(200) DEFAULT NULL,
  `id_marca` int(11) NOT NULL,
  `id_categoria` int(11) NOT NULL,
  `precio_unitario` int(11) NOT NULL,
  `codigo` varchar(50) NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `fecha_carga` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `id_unidad_medida` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id_categoria` (`id_categoria`),
  KEY `id_unidad_medida` (`id_unidad_medida`),
  KEY `id_marca` (`id_marca`),
  KEY `id_usuario` (`id_usuario`),
  CONSTRAINT `productos_ibfk_1` FOREIGN KEY (`id_categoria`) REFERENCES `categoria` (`id`),
  CONSTRAINT `productos_ibfk_2` FOREIGN KEY (`id_unidad_medida`) REFERENCES `unidad_med` (`id`),
  CONSTRAINT `productos_ibfk_3` FOREIGN KEY (`id_marca`) REFERENCES `marcas` (`id`),
  CONSTRAINT `productos_ibfk_4` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Estructura de la tabla proveedor
CREATE TABLE `proveedor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_persona` int(11) NOT NULL,
  `razon_social` varchar(50) NOT NULL,
  `id_condicion_fiscal` int(11) NOT NULL,
  `cuit` varchar(25) NOT NULL,
  `id_localidad` int(11) NOT NULL,
  `observaciones` varchar(200) DEFAULT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT 1,
  `fecha_carga` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `id_usuario` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id_persona` (`id_persona`),
  KEY `id_condicion_fiscal` (`id_condicion_fiscal`),
  KEY `id_usuario` (`id_usuario`),
  KEY `id_localidad` (`id_localidad`),
  CONSTRAINT `proveedor_ibfk_1` FOREIGN KEY (`id_persona`) REFERENCES `persona` (`id`),
  CONSTRAINT `proveedor_ibfk_2` FOREIGN KEY (`id_condicion_fiscal`) REFERENCES `condicion_fiscal` (`id`),
  CONSTRAINT `proveedor_ibfk_4` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id`),
  CONSTRAINT `proveedor_ibfk_5` FOREIGN KEY (`id_localidad`) REFERENCES `localidad` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Estructura de la tabla provincia
CREATE TABLE `provincia` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `id_pais` int(11) NOT NULL,
  KEY `id` (`id`),
  KEY `id_pais` (`id_pais`),
  CONSTRAINT `provincia_ibfk_1` FOREIGN KEY (`id_pais`) REFERENCES `pais` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=96 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Estructura de la tabla roles
CREATE TABLE `roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Estructura de la tabla sexo
CREATE TABLE `sexo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Estructura de la tabla sucursales
CREATE TABLE `sucursales` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `id_localidad` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `sucursales_localidad_FK` (`id_localidad`),
  CONSTRAINT `sucursales_localidad_FK` FOREIGN KEY (`id_localidad`) REFERENCES `localidad` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Estructura de la tabla unidad_med
CREATE TABLE `unidad_med` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `sigla` varchar(15) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Estructura de la tabla usuario
CREATE TABLE `usuario` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `id_rol` int(11) NOT NULL,
  `password` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `usuario_roles_FK` (`id_rol`),
  CONSTRAINT `usuario_roles_FK` FOREIGN KEY (`id_rol`) REFERENCES `roles` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Estructura de la tabla vista_articulos_no_vendidos_mes
CREATE ALGORITHM=UNDEFINED DEFINER=`BD2021`@`%` SQL SECURITY DEFINER VIEW `vista_articulos_no_vendidos_mes` AS select `p`.`id` AS `id_producto`,`p`.`nombre` AS `nombre_producto` from ((`productos` `p` left join `detalle_factura` `df` on(`p`.`id` = `df`.`id_producto`)) left join `factura` `f` on(`df`.`id_factura` = `f`.`id` and month(`f`.`fecha_factura`) = month(curdate()) and year(`f`.`fecha_factura`) = year(curdate()))) where `f`.`id` is null group by `p`.`id`;

-- Estructura de la tabla vista_bono_fin_anio
CREATE ALGORITHM=UNDEFINED DEFINER=`BD2021`@`%` SQL SECURITY DEFINER VIEW `vista_bono_fin_anio` AS select `e`.`id` AS `id_empleado`,`p`.`nombre` AS `nombre_empleado`,`s`.`nombre` AS `sexo_empleado`,`c`.`nombre` AS `cargo`,sum(`df`.`cantidad` * `df`.`precio_unitario`) AS `total_ventas`,case when `c`.`nombre` = 'Vendedor' and sum(`df`.`cantidad` * `df`.`precio_unitario`) > 10000 then 2000 when `c`.`nombre` <> 'Vendedor' then 1000 else 0 end AS `bono` from (((((`empleado` `e` join `persona` `p` on(`e`.`id_persona` = `p`.`id`)) join `cargos` `c` on(`e`.`id_cargo` = `c`.`id`)) join `sexo` `s` on(`p`.`id_sexo` = `s`.`id`)) left join `factura` `f` on(`e`.`id` = `f`.`id_empleado` and `f`.`activo` = 1)) left join `detalle_factura` `df` on(`f`.`id` = `df`.`id_factura`)) group by `e`.`id`,`p`.`nombre`,`s`.`nombre`,`c`.`nombre` having `bono` > 0;

-- Estructura de la tabla vista_cantidad_clientes_por_condicion_fiscal
CREATE ALGORITHM=UNDEFINED DEFINER=`BD2021`@`%` SQL SECURITY DEFINER VIEW `vista_cantidad_clientes_por_condicion_fiscal` AS select `cf`.`id` AS `condicion_fiscal_id`,`cf`.`nombre` AS `condicion_fiscal_nombre`,count(`c`.`id`) AS `cantidad_clientes` from (`cliente` `c` join `condicion_fiscal` `cf` on(`c`.`id_condicion_fiscal` = `cf`.`id`)) group by `cf`.`id`,`cf`.`nombre` order by `cf`.`nombre`;

-- Estructura de la tabla vista_cantidad_productos_por_unidad_y_peso
CREATE ALGORITHM=UNDEFINED DEFINER=`BD2021`@`%` SQL SECURITY DEFINER VIEW `vista_cantidad_productos_por_unidad_y_peso` AS select `um`.`nombre` AS `unidad_med`,coalesce(count(`p`.`id`),0) AS `cantidad_productos` from (`unidad_med` `um` left join `productos` `p` on(`p`.`id_unidad_medida` = `um`.`id`)) where `um`.`nombre` = 'Unidades' group by `um`.`nombre`;

-- Estructura de la tabla vista_clientes_activos
CREATE ALGORITHM=UNDEFINED DEFINER=`BD2021`@`%` SQL SECURITY DEFINER VIEW `vista_clientes_activos` AS select `c`.`id` AS `id_cliente`,`p`.`nombre` AS `nombre_cliente`,`p`.`apellido` AS `apellido_cliente`,`c`.`fecha_alta` AS `fecha_alta`,`c`.`observaciones` AS `observaciones` from (`cliente` `c` join `persona` `p` on(`c`.`id_persona` = `p`.`id`)) where `c`.`activo` = 1;

-- Estructura de la tabla vista_empleados_usuarios
CREATE ALGORITHM=UNDEFINED DEFINER=`BD2021`@`%` SQL SECURITY DEFINER VIEW `vista_empleados_usuarios` AS select `e`.`id` AS `id_empleado`,`p`.`nombre` AS `nombre_empleado`,`p`.`apellido` AS `apellido_empleado`,`u`.`nombre` AS `usuario_login` from ((`empleado` `e` join `persona` `p` on(`e`.`id_persona` = `p`.`id`)) join `usuario` `u` on(`p`.`id_usuario` = `u`.`id`));

-- Estructura de la tabla vista_ganancia_mensual_producto
CREATE ALGORITHM=UNDEFINED DEFINER=`BD2021`@`%` SQL SECURITY DEFINER VIEW `vista_ganancia_mensual_producto` AS select `p`.`id` AS `id_producto`,`p`.`nombre` AS `nombre_producto`,date_format(`f`.`fecha_factura`,'%Y-%m') AS `mes_anio`,sum(`df`.`cantidad` * `df`.`precio_unitario`) AS `total_venta`,sum(`dc`.`cantidad` * `dc`.`precio_unitario`) AS `total_costo`,sum(`df`.`cantidad` * `df`.`precio_unitario`) - sum(`dc`.`cantidad` * `dc`.`precio_unitario`) AS `ganancia_mensual` from ((((`productos` `p` join `detalle_factura` `df` on(`df`.`id_producto` = `p`.`id`)) join `factura` `f` on(`df`.`id_factura` = `f`.`id`)) join `detalle_compra` `dc` on(`dc`.`id_producto` = `p`.`id`)) join `compra` `c` on(`dc`.`id_compra` = `c`.`id`)) where `f`.`activo` = 1 group by `p`.`id`,date_format(`f`.`fecha_factura`,'%Y-%m');

-- Estructura de la tabla vista_localidades_argentina
CREATE ALGORITHM=UNDEFINED DEFINER=`BD2021`@`%` SQL SECURITY DEFINER VIEW `vista_localidades_argentina` AS select `l`.`id` AS `id`,`l`.`nombre` AS `nombre` from ((`localidad` `l` join `provincia` `pr` on(`l`.`id_provincia` = `pr`.`id`)) join `pais` `p` on(`pr`.`id_pais` = `p`.`id`)) where `p`.`nombre` = 'Argentina';

-- Estructura de la tabla vista_mayor_venta_mes
CREATE ALGORITHM=UNDEFINED DEFINER=`BD2021`@`%` SQL SECURITY DEFINER VIEW `vista_mayor_venta_mes` AS select year(`f`.`fecha_factura`) AS `anio`,month(`f`.`fecha_factura`) AS `mes`,max(`f`.`total`) AS `mayor_venta` from `factura` `f` where `f`.`activo` <> '0' group by year(`f`.`fecha_factura`),month(`f`.`fecha_factura`) order by year(`f`.`fecha_factura`),month(`f`.`fecha_factura`);

-- Estructura de la tabla vista_menor_venta_mes
CREATE ALGORITHM=UNDEFINED DEFINER=`BD2021`@`%` SQL SECURITY DEFINER VIEW `vista_menor_venta_mes` AS select year(`f`.`fecha_factura`) AS `anio`,month(`f`.`fecha_factura`) AS `mes`,min(`f`.`total`) AS `menor_venta` from `factura` `f` where `f`.`activo` <> '0' group by year(`f`.`fecha_factura`),month(`f`.`fecha_factura`) order by year(`f`.`fecha_factura`),month(`f`.`fecha_factura`);

-- Estructura de la tabla vista_productos_mas_vendidos
CREATE ALGORITHM=UNDEFINED DEFINER=`BD2021`@`%` SQL SECURITY DEFINER VIEW `vista_productos_mas_vendidos` AS select `p`.`id` AS `id_producto`,`p`.`nombre` AS `nombre_producto`,sum(`df`.`cantidad`) AS `total_vendido` from ((`productos` `p` join `detalle_factura` `df` on(`p`.`id` = `df`.`id_producto`)) join `factura` `f` on(`df`.`id_factura` = `f`.`id`)) where `f`.`activo` = 1 group by `p`.`id` order by sum(`df`.`cantidad`) desc;

-- Estructura de la tabla vista_resumen_ventas_mensuales
CREATE ALGORITHM=UNDEFINED DEFINER=`BD2021`@`%` SQL SECURITY DEFINER VIEW `vista_resumen_ventas_mensuales` AS select year(`f`.`fecha_factura`) AS `anio`,month(`f`.`fecha_factura`) AS `mes`,sum(`f`.`total`) AS `total_ventas` from `factura` `f` where `f`.`activo` <> '0' group by year(`f`.`fecha_factura`),month(`f`.`fecha_factura`) order by year(`f`.`fecha_factura`),month(`f`.`fecha_factura`);

-- Estructura de la tabla vista_sucursal_mas_ventas
CREATE ALGORITHM=UNDEFINED DEFINER=`BD2021`@`%` SQL SECURITY DEFINER VIEW `vista_sucursal_mas_ventas` AS select `s`.`id` AS `id_sucursal`,`s`.`nombre` AS `nombre_sucursal`,count(`f`.`id`) AS `cantidad_ventas`,sum(`f`.`total`) AS `total_ventas` from ((`factura` `f` join `empleado` `e` on(`f`.`id_empleado` = `e`.`id`)) join `sucursales` `s` on(`e`.`id_sucursal` = `s`.`id`)) where `f`.`activo` <> 0 group by `s`.`id`,`s`.`nombre` order by sum(`f`.`total`) desc limit 1;

