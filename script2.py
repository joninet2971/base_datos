from conexion import create_connection

def ultimo_id():
    mydb = create_connection()
    mycursor = mydb.cursor()

    select_query = "SELECT max(id) FROM factura"

    mycursor.execute(select_query)

    resultados = mycursor.fetchall()

    id_obtenido = None
    for (id,) in resultados:
        id_obtenido = id  # Aquí usas id_obtenido en lugar de id

    mycursor.close()
    mydb.close()

    print(f"Último id: {id_obtenido}")
    return id_obtenido  # Retorna el id obtenido

# Llama a la función para obtener el último ID
ultimoID = ultimo_id()

def insertar_detallefactura(ultimoId, productoId, cantidad, precio):

    mydb = create_connection()
    mycursor = mydb.cursor()

    insert_query = """
    INSERT INTO detalle_factura (factura_id, producto_id, cantidad, precio_unitario)
    VALUES (%s, %s, %s, %s)
    """

    values = (ultimoId, productoId, cantidad, precio)

    mycursor.execute(insert_query, values)
    mydb.commit()

    mycursor.close()
    mydb.close()

    return f"Insertado correctamente, factura_id: {ultimoId}"

# Llama a la función para insertar el detalle de la factura
insertar = insertar_detallefactura(ultimoID, 2, 200, 234.00)
print(insertar)
