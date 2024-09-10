from conexion import create_connection

def create_factura_table():
    mydb = create_connection()
    
    if mydb:
        mycursor = mydb.cursor()

        # Definir la consulta para crear la tabla 'factura' con la clave foránea
        create_table_query = """
        CREATE TABLE factura (
            id INT AUTO_INCREMENT PRIMARY KEY,
            numero_factura VARCHAR(255) NOT NULL,
            fecha DATE NOT NULL,
            cliente_id INT NOT NULL,
            total DECIMAL(10, 2) NOT NULL,
            FOREIGN KEY (cliente_id) REFERENCES cliente(id)
        )
        """
        
        # Ejecutar la consulta para crear la tabla
        mycursor.execute(create_table_query)
        mydb.commit()
        
        print("Tabla 'factura' creada exitosamente con relación a 'cliente'.")
        
        mycursor.close()
        mydb.close()

if __name__ == "__main__":
    create_factura_table()

