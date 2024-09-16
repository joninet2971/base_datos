from conexion import create_connection

def create_detalle_factura_table():
    mydb = create_connection()
    
    if mydb:
        mycursor = mydb.cursor()

        # Definir la consulta para crear la tabla 'detalle_factura' con las claves foráneas
        create_table_query = """
        CREATE TABLE IF NOT EXISTS detalle_factura (
            id INT(11) AUTO_INCREMENT PRIMARY KEY,
            factura_id INT(11) NOT NULL,
            producto_id INT(11) UNSIGNED NOT NULL,
            cantidad INT NOT NULL,
            precio_unitario DECIMAL(10, 2) NOT NULL,
            FOREIGN KEY (factura_id) REFERENCES factura(id) ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (producto_id) REFERENCES producto(id) ON DELETE CASCADE ON UPDATE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
        """
        
        try:
            mycursor.execute(create_table_query)
            mydb.commit()
            print("Tabla 'detalle_factura' creada exitosamente con relación a 'factura' y 'producto'.")
        except Exception as e:
            print(f"Error al crear la tabla: {e}")
        
        mycursor.close()
        mydb.close()

if __name__ == "__main__":
    create_detalle_factura_table()