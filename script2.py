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

#numero_detalle_factura = 2
#resultado_suma_detalle = obtener_suma_detalle(numero_detalle_factura)
#print(resultado_suma_detalle)

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

#print(actualizar_total_factura(numero_detalle_factura, resultado_suma_detalle))

"""-Un script con el resultado de lo vendido por cada articulo de las facturas que no esten anuladas."""
def vendidos_no_anuladas():
    connection = create_connection()
    cursor = connection.cursor()
    sql = """
    SELECT p.nombre, SUM(d.cantidad) AS total_vendido
    FROM detalle_factura d
    JOIN facturas f ON d.factura_id = f.id
    JOIN productos p ON d.producto_id = p.id
    WHERE f.estado != 'Anulada'
    GROUP BY p.nombre
    """
    cursor.execute(sql)
    
    resultados = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return resultados

#print(vendidos_no_anuladas())

"""-Un script que permita agregar una nueva Localidad, de una nueva provincia de un pais que no Esta cargado en la tabla paises."""

def agregar_localidad(localidad_nombre, provincia_nombre, pais_nombre):
    connection = create_connection()
    cursor = connection.cursor()

    # Verificar si el país existe
    cursor.execute("SELECT id FROM pais WHERE nombre = %s", (pais_nombre,))
    pais = cursor.fetchone()

    if pais:
        pais_id = pais[0]
    else:
        cursor.execute("INSERT INTO pais (nombre) VALUES (%s)", (pais_nombre,))
        pais_id = cursor.lastrowid
        connection.commit()
        print(f"Nuevo pais '{pais_nombre}' agregado")

    # Verificar si la provincia existe
    cursor.execute("SELECT id FROM provincia WHERE nombre = %s AND pais_id = %s", (provincia_nombre, pais_id))
    provincia = cursor.fetchone()

    if provincia:
        provincia_id = provincia[0]
    else:
        cursor.execute("INSERT INTO provincia (nombre, pais_id) VALUES (%s, %s)", (provincia_nombre, pais_id))
        provincia_id = cursor.lastrowid
        connection.commit()
        print(f"Nueva provincia {provincia_nombre}")

    # Verificar si la localidad existe
    cursor.execute("SELECT id FROM ciudad WHERE nombre = %s AND provincia_id = %s", (localidad_nombre, provincia_id))
    localidad = cursor.fetchone()

    if localidad:
        print(f"La localidad '{localidad_nombre}' ya existe.")
    else:
        cursor.execute("INSERT INTO ciudad (nombre, provincia_id) VALUES (%s, %s)", (localidad_nombre, provincia_id))
        connection.commit()
        print(f"Nueva ciudad {localidad_nombre} agregada con éxito.")

    cursor.close()
    connection.close()

#agregar_localidad('santa clara', 'mardel plata', 'argentina')

"""Un script que muestro al cliente con mas ventas del año."""
from datetime import datetime, timedelta
def cliente_con_mas_ventas():
    connection = create_connection()
    cursor = connection.cursor()

    anio_actual = datetime.now().year

    sql = """
    SELECT c.id, c.nombre, SUM(f.total) AS total_ventas
    FROM facturas f
    JOIN clientes c ON f.cliente_id = c.id
    WHERE YEAR(f.fecha_emision) = %s 
    GROUP BY c.id
    ORDER BY total_ventas DESC
    LIMIT 1
    """

    cursor.execute(sql, (anio_actual,))
    resultado = cursor.fetchone()
    cursor.close()
    connection.close()
    cliente_id, nombre, total_ventas = resultado
    return f"El cliente con más ventas es {nombre} con un total de {total_ventas} en el año {anio_actual}."

# Ejemplo de uso
#print(cliente_con_mas_ventas())

"""Un script que diga la cantidad de clientes masculinos y femeninos que compraron en el ultimo mes."""
def contar_clientes_por_sexo():

    connection = create_connection()
    cursor = connection.cursor()

    hoy = datetime.now()
    hace_un_mes = hoy - timedelta(days=30)

    sql = """
    SELECT c.sexo, COUNT(DISTINCT c.id) AS cantidad
    FROM facturas f
    JOIN clientes c ON f.cliente_id = c.id
    WHERE f.fecha_emision BETWEEN %s AND %s
    GROUP BY c.sexo
    """
    cursor.execute(sql, (hace_un_mes, hoy))
    resultados = cursor.fetchall()

    # Cerrar la conexión
    cursor.close()
    connection.close()

    # Preparar los resultados
    conteo_sexos = {
        'Masculino': 0,
        'Femenino': 0
    }

    for sexo, cantidad in resultados:
        conteo_sexos[sexo] = cantidad

    return f"Clientes Masculinos: {conteo_sexos['Masculino']}, Clientes Femeninos: {conteo_sexos['Femenino']}"

#print(contar_clientes_por_sexo())

"""Un scpit muestre las ventas por provincia (cantidad y suma)."""
def ventas_por_provincia():
    connection = create_connection()
    cursor = connection.cursor()

    query = """
    SELECT 
    provincia.nombre AS provincia,
    COUNT(facturas.id) AS cantidad_ventas,
    SUM(detalle_factura.subtotal) AS total_ventas
    FROM facturas
    JOIN empleados ON facturas.id = empleados.id  -- Relación facturas-empleados
    JOIN persona ON empleados.persona_id = persona.id
    JOIN ciudad ON persona.ciudad_id = ciudad.id
    JOIN provincia ON ciudad.provincia_id = provincia.id
    JOIN detalle_factura ON facturas.id = detalle_factura.factura_id
    GROUP BY provincia.nombre;
    """

    cursor.execute(query)
    resultados = cursor.fetchall()

    for row in resultados:
        print(f"Provincia: {row[0]}, Cantidad de Ventas: {row[1]}, Total Ventas: {row[2]}")

    cursor.close()
    connection.close()

#ventas_por_provincia()

"""Un script que diga la cantidad de clientes masculinos y femeninos que compraron en el ultimo mes."""
def clientes_por_genero_ultimo_mes():
    connection = create_connection()
    cursor = connection.cursor()

    query = """
    SELECT 
    clientes.sexo,
    COUNT(DISTINCT clientes.id) AS cantidad_clientes
    FROM facturas
    JOIN clientes ON facturas.cliente_id = clientes.id
    GROUP BY clientes.sexo;
    """

    cursor.execute(query)
    resultados = cursor.fetchall()

    for row in resultados:
        if row[0] == 'Masculino':
            genero = "Masculino"
        elif row[0] == 'Femenino':
            genero = "Femenino"
        else:
            genero = "Otro"
        
        print(f"Género: {genero}, Cantidad de Clientes: {row[1]}")

    cursor.close()
    connection.close()

#clientes_por_genero_ultimo_mes()






