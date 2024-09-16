#Un scipt que inserte un registro en la tabla factura
from conexion import create_connection
def insertar_factura():
    numero_factura = "12s345g"
    fecha = "2022-09-10"
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

    mycursor.close()
    mydb.close()
    print(f"id:{mycursor.lastrowid}")

    return {mycursor.lastrowid}

insertar_factura()
