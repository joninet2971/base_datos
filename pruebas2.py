import mysql.connector

def create_connection():
    connection = mysql.connector.connect(
        host="143.198.156.171",
        user="BD2021",
        password="BD2021itec",
        database="db_desplats"
    )
    return connection

def drop_all_tables():
    try:
        # Crear conexión
        connection = create_connection()
        cursor = connection.cursor()

        # Obtener el nombre de todas las tablas
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        # Deshabilitar temporalmente las verificaciones de clave externa (opcional)
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")

        # Borrar cada tabla
        for table in tables:
            table_name = table[0]
            cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
            print(f"Tabla {table_name} eliminada.")

        # Habilitar de nuevo las verificaciones de clave externa (opcional)
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

        # Confirmar cambios
        connection.commit()

    except mysql.connector.Error as e:
        print(f"Error al eliminar tablas: {e}")
    finally:
        # Cerrar la conexión
        cursor.close()
        connection.close()

# Llamada a la función para borrar las tablas
drop_all_tables()
