from conexion import create_connection

numero_factura = "12345"
fecha = "2024-09-10"
cliente_id = 1
total = 1239.00

mydb = create_connection()
mycursor = mydb.cursor()

insert_query = """
INSERT INTO factura (numero_factura, fecha, cliente_id, total)
VALUES (%s, %s, %s, %s)
"""

values = (numero_factura, fecha, cliente_id, total)

mycursor.execute(insert_query, values)
mydb.commit()

print(f"Factura insertada con ID: {mycursor.lastrowid}")

mycursor.close()
mydb.close()
