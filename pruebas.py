import mysql.connector
import json

# Conectar a la base de datos
db_config = {
    'host': "143.198.156.171",
    'user': "BD2021",
    'password': "BD2021itec",
    'database': "db_mas_30"
}

def get_db_structure():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Obtener todas las tablas
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        db_structure = {}

        for (table_name,) in tables:
            # Obtener columnas de cada tabla
            cursor.execute(f"DESCRIBE {table_name}")
            columns = cursor.fetchall()

            # Obtener relaciones (claves foráneas)
            cursor.execute(f"""
                SELECT 
                    COLUMN_NAME, 
                    REFERENCED_TABLE_NAME, 
                    REFERENCED_COLUMN_NAME 
                FROM 
                    INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
                WHERE 
                    TABLE_NAME = '{table_name}' 
                    AND CONSTRAINT_SCHEMA = '{db_config['database']}' 
                    AND REFERENCED_TABLE_NAME IS NOT NULL;
            """)
            relations = cursor.fetchall()

            db_structure[table_name] = {
                'columns': [{'Field': col[0], 'Type': col[1], 'Null': col[2], 'Key': col[3], 'Default': col[4], 'Extra': col[5]} for col in columns],
                'relations': [{'column': rel[0], 'referenced_table': rel[1], 'referenced_column': rel[2]} for rel in relations]
            }

        # Exportar estructura a formato JSON
        with open('db_structure.json', 'w') as json_file:
            json.dump(db_structure, json_file, indent=4)

        print("La estructura de la base de datos ha sido exportada a 'db_structure.json'.")

    except mysql.connector.Error as error:
        print(f"Error al conectarse a la base de datos: {error}")
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    get_db_structure()
