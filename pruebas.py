import mysql.connector

def create_connection():
    connection = mysql.connector.connect(
        host="143.198.156.171",
        user="BD2021",
        password="BD2021itec",
        database="db_desplats"
    )
    return connection

def modificar_base_datos():
    connection = create_connection()
    cursor = connection.cursor()
    crear_persona = """
    CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    empleado_id INT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    rol VARCHAR(50),
    FOREIGN KEY (empleado_id) REFERENCES empleados(id)
    );
    """
    
    try:
        # Ejecutar las consultas SQL
        cursor.execute(crear_persona)

        
        connection.commit()  # Confirmar los cambios en la base de datos
        print("Modificaciones realizadas con éxito.")
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    
    finally:
        cursor.close()
        connection.close()

# Llamada a la función para realizar las modificaciones
modificar_base_datos()
