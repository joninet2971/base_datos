import mysql.connector

def create_connection():
    connection = mysql.connector.connect(
        host="143.198.156.171",
        user="BD2021",
        password="BD2021itec",
        database="db_desplats"
    )
    return connection

def create_tables():
    connection = create_connection()
    cursor = connection.cursor()

    # Tabla de Paises
    crear_paises = """
    CREATE TABLE IF NOT EXISTS Paises (
        pais_id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        codigo_iso VARCHAR(10)
    )
    """

    # Tabla de Localidades (debe estar después de crear la tabla Paises)
    crear_localidades = """
    CREATE TABLE IF NOT EXISTS Localidades (
        localidad_id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        provincia VARCHAR(100) NOT NULL,
        pais_id INT,
        FOREIGN KEY (pais_id) REFERENCES Paises(pais_id) ON DELETE CASCADE
    )
    """

    # Tabla de Clientes
    crear_clientes = """
    CREATE TABLE IF NOT EXISTS Clientes (
        cliente_id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        direccion VARCHAR(255),
        telefono VARCHAR(20),
        email VARCHAR(100),
        estado ENUM('Activo', 'Inactivo') DEFAULT 'Activo'
    )
    """

    # Tabla de Productos
    crear_productos = """
    CREATE TABLE IF NOT EXISTS Productos (
        producto_id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        precio DECIMAL(10, 2) NOT NULL,
        stock INT NOT NULL
    )
    """

    # Tabla de Facturas
    crear_facturas = """
    CREATE TABLE IF NOT EXISTS Facturas (
        factura_id INT AUTO_INCREMENT PRIMARY KEY,
        cliente_id INT,
        fecha_emision DATETIME NOT NULL,
        total DECIMAL(10, 2) NOT NULL,
        estado ENUM('Activa', 'Anulada') DEFAULT 'Activa',
        FOREIGN KEY (cliente_id) REFERENCES Clientes(cliente_id) ON DELETE CASCADE
    )
    """

    # Tabla de Detalle_Factura
    crear_detalle_factura = """
    CREATE TABLE IF NOT EXISTS Detalle_Factura (
        detalle_id INT AUTO_INCREMENT PRIMARY KEY,
        factura_id INT,
        producto_id INT,
        cantidad INT NOT NULL,
        subtotal DECIMAL(10, 2) NOT NULL,
        FOREIGN KEY (factura_id) REFERENCES Facturas(factura_id) ON DELETE CASCADE,
        FOREIGN KEY (producto_id) REFERENCES Productos(producto_id) ON DELETE CASCADE
    )
    """

    # Tabla de Pagos
    crear_pagos = """
    CREATE TABLE IF NOT EXISTS Pagos (
        pago_id INT AUTO_INCREMENT PRIMARY KEY,
        factura_id INT,
        monto DECIMAL(10, 2) NOT NULL,
        fecha_pago DATETIME NOT NULL,
        metodo_pago VARCHAR(50) NOT NULL,
        FOREIGN KEY (factura_id) REFERENCES Facturas(factura_id) ON DELETE CASCADE
    )
    """

    # Tabla de Empleados
    crear_empleados = """
    CREATE TABLE IF NOT EXISTS Empleados (
        empleado_id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        cargo VARCHAR(50) NOT NULL,
        telefono VARCHAR(20),
        email VARCHAR(100)
    )
    """

    # Crear las tablas en el orden correcto
    cursor.execute(crear_paises)
    cursor.execute(crear_clientes)
    cursor.execute(crear_productos)
    cursor.execute(crear_facturas)
    cursor.execute(crear_detalle_factura)
    cursor.execute(crear_pagos)
    cursor.execute(crear_localidades)  # Ahora se crea después de Paises
    cursor.execute(crear_empleados)

    # Confirmar cambios y cerrar conexión
    connection.commit()
    cursor.close()
    connection.close()

    print("Tablas creadas exitosamente.")

# Ejecutar la función para crear tablas
create_tables()
