#Un scipt que inserte un registro en la tabla factura
from conexion import create_connection
def insertar_factura():
    numero = "12s345g"
    fecha_factura = "2022-09-10"
    id_cliente = 4
    id_tipo_comprobante = 3
    id_forma_pago = 2
    total = 1239.00
    id_empleado = 4
    activo = 1

    mydb = create_connection()
    mycursor = mydb.cursor()

    insert_query = """
    INSERT INTO factura (numero, fecha_factura, id_cliente, id_tipo_comprobante, id_forma_pago,  total, id_empleado, activo)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (numero, fecha_factura,  id_cliente, id_tipo_comprobante, id_forma_pago, total, id_empleado, activo)

    mycursor.execute(insert_query, values)
    mydb.commit()

    mycursor.close()
    mydb.close()
    print(f"id:{mycursor.lastrowid}")

    return {mycursor.lastrowid}

insertar_factura()
