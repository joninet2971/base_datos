import mysql.connector


def exportar_estructura_bd(host, user, password, database, output_file):
    # Conectar a la base de datos
    mydb = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    
    mycursor = mydb.cursor()

    # Obtener todas las tablas de la base de datos
    mycursor.execute("SHOW TABLES")
    tablas = mycursor.fetchall()

    with open(output_file, 'w') as f:
        for (tabla,) in tablas:
            f.write(f"-- Estructura de la tabla {tabla}\n")
            
            # Obtener la estructura de la tabla
            mycursor.execute(f"SHOW CREATE TABLE {tabla}")
            resultado = mycursor.fetchone()
            
            # Escribir el SQL de creación de la tabla en el archivo
            f.write(f"{resultado[1]};\n\n")

    print(f"Estructura exportada a {output_file}")

# Configuración de la base de datos
host = "143.198.156.171"
user = "BD2021"
password = "BD2021itec"
database = "db_desplats2"
output_file = "estructura_base_datos.sql"

# Ejecutar la exportación
exportar_estructura_bd(host, user, password, database, output_file)
