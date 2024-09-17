from conexion import create_connection
"""-Un scrpt que obtenga el id Máximo O ultimo de la tabla factura"""
def ultimo_id():
    mydb = create_connection()
    mycursor = mydb.cursor()

    select_query = "SELECT max(id) FROM facturas"

    mycursor.execute(select_query)

    resultados = mycursor.fetchall()

    id_obtenido = None
    for (id,) in resultados:
        id_obtenido = id

    mycursor.close()
    mydb.close()

    print(f"Último id: {id_obtenido}")
    return id_obtenido 

#ultimoID = ultimo_id()

"""-Un script que inserte registros en la tabla detalle_factura usando el id obtenido en el script anterior."""
def insertar_detallefactura(ultimoId, productoId, cantidad, subtotal):

    mydb = create_connection()
    mycursor = mydb.cursor()

    insert_query = """
    INSERT INTO detalle_factura (factura_id, producto_id, cantidad, subtotal)
    VALUES (%s, %s, %s, %s)
    """

    values = (ultimoId, productoId, cantidad, subtotal)

    mycursor.execute(insert_query, values)
    mydb.commit()

    mycursor.close()
    mydb.close()

    return f"Insertado correctamente, factura_id: {ultimoId}"

#insertar = insertar_detallefactura(ultimoID, 2, 200, 234.00)
#print(insertar)

"""Un script que obtenga la suma*producto de las cantidades y precios de los registros insertados en el punto anterior."""

def obtener_suma_detalle(factura_id):
    connection = create_connection()
    cursor = connection.cursor()
    
    sql = """
    SELECT SUM(d.cantidad * p.precio) AS Total
    FROM detalle_factura d 
    JOIN productos p ON d.producto_id = p.id 
    WHERE d.factura_id = %s
    """

    cursor.execute(sql, (factura_id,))
    result = cursor.fetchone()

    total = result[0]

    return total

numero_detalle_factura = 2
resultado_suma_detalle = obtener_suma_detalle(numero_detalle_factura)
print(resultado_suma_detalle)

"""-Un script que actualice la tabla factura campo (Total) con el monto obtenido del script anterior"""

def actualizar_total_factura(factura_id, total):
    connection = create_connection()
    cursor = connection.cursor()
    
    sql = "UPDATE facturas SET total = %s WHERE id = %s"
    cursor.execute(sql, (total, factura_id))
    
    connection.commit()
    cursor.close()
    connection.close()
    
    return f"se actualizo el total de la factura con el id: {factura_id} a un total de {total}"

print(actualizar_total_factura(numero_detalle_factura, resultado_suma_detalle))