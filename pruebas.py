
import mysql.connector
from mysql.connector import Error

def create_connection():
    """Establish a connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(
            host="143.198.156.171",
            user="BD2021",
            password="BD2021itec",
            database="db_desplats2"
        )
        if connection.is_connected():
            print("Connection successful.")
        return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

def rename_column(connection, table_name, old_column_name, new_column_name, column_type):
    """Rename a column in the specified table."""
    try:
        cursor = connection.cursor()
        # Generar la sentencia SQL para renombrar la columna
        sql = f"ALTER TABLE {table_name} CHANGE COLUMN {old_column_name} {new_column_name} {column_type}"
        cursor.execute(sql)
        connection.commit()
        print(f"Column `{old_column_name}` has been renamed to `{new_column_name}`.")
    except Error as e:
        print(f"Error while renaming the column: {e}")
    finally:
        cursor.close()

def main():
    connection = create_connection()
    if connection:
        # Especificar la tabla, el nombre antiguo de la columna, el nuevo nombre y su tipo
        rename_column(connection, "factura", "numero_factura", "numero", "VARCHAR(255)")
        connection.close()

if __name__ == "__main__":
    main()
