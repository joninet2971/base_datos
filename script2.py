from conexion import create_connection
from datetime import datetime, timedelta, date
"""-Un scrpt que obtenga el id Máximo O ultimo de la tabla factura"""
def ultimo_id():
    mydb = create_connection()
    mycursor = mydb.cursor()

    select_query = "SELECT max(id) FROM factura"

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
def insertar_detallefactura(ultimoId, productoId, cantidad, precioUnitario):

    mydb = create_connection()
    mycursor = mydb.cursor()

    insert_query = """
    INSERT INTO detalle_factura (id_factura, id_producto, cantidad, precio_unitario)
    VALUES (%s, %s, %s, %s)
    """

    values = (ultimoId, productoId, cantidad, precioUnitario)

    mycursor.execute(insert_query, values)
    mydb.commit()

    mycursor.close()
    mydb.close()

    return f"Insertado correctamente, factura_id: {ultimoId}"

#insertar = insertar_detallefactura(13, 8, 3, 259.00)
#print(insertar)

"""Un script que obtenga la suma*producto de las cantidades y precios de los registros insertados en el punto anterior."""

def obtener_suma_detalle(factura_id):
    connection = create_connection()
    cursor = connection.cursor()
    
    sql = """
    SELECT SUM(d.cantidad * p.precio_unitario) AS Total
    FROM detalle_factura d 
    JOIN productos p ON d.id_producto = p.id 
    WHERE d.id_factura = %s
    """

    cursor.execute(sql, (factura_id,))
    result = cursor.fetchone()

    total = result[0]

    return total

numero_detalle_factura = 13
resultado_suma_detalle = obtener_suma_detalle(numero_detalle_factura)
#print(resultado_suma_detalle)

"""-Un script que actualice la tabla factura campo (Total) con el monto obtenido del script anterior"""

def actualizar_total_factura(factura_id, total):
    connection = create_connection()
    cursor = connection.cursor()
    
    sql = "UPDATE factura SET total = %s WHERE id = %s"
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
    JOIN factura f ON d.id_factura = f.id
    JOIN productos p ON d.id_producto = p.id
    WHERE f.activo != '2'
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
        id_pais = pais[0]
    else:
        cursor.execute("INSERT INTO pais (nombre) VALUES (%s)", (pais_nombre,))
        id_pais = cursor.lastrowid
        connection.commit()
        print(f"Nuevo pais '{pais_nombre}' agregado")

    # Verificar si la provincia existe
    cursor.execute("SELECT id FROM provincia WHERE nombre = %s AND id_pais = %s", (provincia_nombre, id_pais))
    provincia = cursor.fetchone()

    if provincia:
        id_provincia = provincia[0]
    else:
        cursor.execute("INSERT INTO provincia (nombre, id_pais) VALUES (%s, %s)", (provincia_nombre, id_pais))
        id_provincia = cursor.lastrowid
        connection.commit()
        print(f"Nueva provincia {provincia_nombre}")

    # Verificar si la localidad existe
    cursor.execute("SELECT id FROM localidad WHERE nombre = %s AND id_provincia = %s", (localidad_nombre, id_provincia))
    localidad = cursor.fetchone()

    if localidad:
        print(f"La localidad '{localidad_nombre}' ya existe.")
    else:
        cursor.execute("INSERT INTO localidad (nombre, id_provincia) VALUES (%s, %s)", (localidad_nombre, id_provincia))
        connection.commit()
        print(f"Nueva ciudad {localidad_nombre} agregada con éxito.")

    cursor.close()
    connection.close()

#agregar_localidad('santa clara', 'mardel plata', 'argentina')

"""Un script que muestro al cliente con mas ventas del año."""

def cliente_con_mas_compras():
    connection = create_connection()
    cursor = connection.cursor()

    anio_actual = datetime.now().year

    sql = """
    SELECT c.id, p.nombre, COUNT(f.id) AS total_compras
    FROM factura f
    JOIN cliente c ON f.id_cliente = c.id
    JOIN persona p ON c.id_persona = p.id
    WHERE YEAR(f.fecha_factura) = %s 
    AND f.activo = 1
    GROUP BY c.id, p.nombre
    ORDER BY total_compras DESC
    LIMIT 1
    """

    cursor.execute(sql, (anio_actual,))
    resultado = cursor.fetchone()
    cursor.close()
    connection.close()

    if resultado:
        id_cliente, nombre, total_compras = resultado
        return f"El cliente con más compras es {nombre} con un total de {total_compras} compras en el año {anio_actual}."
    else:
        return f"No se encontraron compras en el año {anio_actual}."

#print(cliente_con_mas_compras())

"""Un script que diga la cantidad de clientes masculinos y femeninos que compraron en el ultimo mes."""

def clientes_por_sexo_ultimo_mes():
    connection = create_connection()
    cursor = connection.cursor()

    # Calculamos la fecha de hace un mes
    fecha_un_mes_atras = datetime.now() - timedelta(days=30)

    sql = """
    SELECT s.nombre AS sexo, COUNT(DISTINCT c.id) AS cantidad_clientes
    FROM factura f
    JOIN cliente c ON f.id_cliente = c.id
    JOIN persona p ON c.id_persona = p.id
    JOIN sexo s ON p.id_sexo = s.id
    WHERE f.fecha_factura >= %s
    AND f.activo = 1
    GROUP BY s.nombre
    """

    cursor.execute(sql, (fecha_un_mes_atras,))
    resultados = cursor.fetchall()
    cursor.close()
    connection.close()

    if resultados:
        resumen = "Clientes que compraron en el último mes:\n"
        for sexo, cantidad in resultados:
            resumen += f"{sexo}: {cantidad}\n"
        return resumen
    else:
        return "No se encontraron compras en el último mes."

#print(clientes_por_sexo_ultimo_mes())

"""Un scpit muestre las ventas por provincia (cantidad y suma)."""
def ventas_por_provincia():
    connection = create_connection()
    cursor = connection.cursor()

    sql = """
    SELECT 
        pr.nombre AS provincia, 
        COUNT(f.id) AS cantidad_ventas, 
        SUM(f.total) AS suma_total
    FROM factura f
    JOIN cliente c ON f.id_cliente = c.id
    JOIN persona pe ON c.id_persona = pe.id
    JOIN localidad l ON pe.id_localidad = l.id
    JOIN provincia pr ON l.id_provincia = pr.id
    WHERE f.activo = 1
    GROUP BY pr.id, pr.nombre
    ORDER BY suma_total DESC
    """

    cursor.execute(sql)
    resultados = cursor.fetchall()
    cursor.close()
    connection.close()

    if resultados:
        print("Ventas por provincia:")
        for provincia, cantidad, total in resultados:
            print(f"provincia: {provincia} - cantidad: {cantidad} - total: ${total}")
    else:
        print("No se encontraron ventas.")

#ventas_por_provincia()

"""Un script que diga la cantidad de clientes masculinos y femeninos que compraron en el ultimo mes."""

def clientes_por_sexo_ultimomes():
    connection = create_connection()
    cursor = connection.cursor()

    # Calculamos la fecha de hace un mes
    fecha_un_mes_atras = datetime.now() - timedelta(days=30)

    sql = """
    SELECT 
        s.nombre AS sexo, 
        COUNT(DISTINCT c.id) AS cantidad_clientes
    FROM factura f
    JOIN cliente c ON f.id_cliente = c.id
    JOIN persona p ON c.id_persona = p.id
    JOIN sexo s ON p.id_sexo = s.id
    WHERE f.fecha_factura >= %s
    AND f.activo = 1
    GROUP BY s.nombre
    """

    cursor.execute(sql, (fecha_un_mes_atras,))
    resultados = cursor.fetchall()
    cursor.close()
    connection.close()

    if resultados:
        print("Clientes que compraron en el último mes:")
        for sexo, cantidad in resultados:
            print(f"{sexo}: {cantidad}")
    else:
        print("No se encontraron compras en el último mes.")

#clientes_por_sexo_ultimomes()

"""Un script que sirva para la insercion de un nuevo empleado ( tener en cuenta que se necesita que se le genere usuario)"""

def generar_usuario(nombre, apellido):
    inicial = nombre[0].lower()  
    apellido = apellido.lower()  
    return f"{inicial}{apellido}"

def generar_contraseña_aleatoria():
    contrasena = "12345"
    return contrasena

def insertar_empleado(id_persona, id_cargo, fecha_ingreso, id_sucursal):
    
    mydb = create_connection()
    mycursor = mydb.cursor()

    select_persona_query = "SELECT nombre, apellido FROM persona WHERE id = %s"
    mycursor.execute(select_persona_query, (id_persona,))
    resultado_persona = mycursor.fetchone()

    nombre_persona, apellido_persona = resultado_persona

    nombre_usuario = generar_usuario(nombre_persona, apellido_persona)
    contrasena = generar_contraseña_aleatoria()

    insert_usuario_query = """
    INSERT INTO usuario (nombre, password, id_rol)
    VALUES (%s, %s, 2)  -- Asumiendo que el rol 2 es 'empleado'
    """
    mycursor.execute(insert_usuario_query, (nombre_usuario, contrasena))
    id_usuario = mycursor.lastrowid

    insert_empleado_query = """
    INSERT INTO empleado (id_persona, id_cargo, fecha_ingreso, activo, id_sucursal)
    VALUES (%s, %s, %s, 1, %s)
    """
    mycursor.execute(insert_empleado_query, (id_persona, id_cargo, fecha_ingreso, id_sucursal))
    mydb.commit()

    mycursor.close()
    mydb.close()

    print(f"Empleado insertado con éxito. Usuario: {nombre_usuario}, Contraseña: {contrasena}")
    return id_usuario

id_persona = 9  
id_cargo = 1    
fecha_ingreso = "2023-10-26"  
id_sucursal = 1    

#insertar_empleado(id_persona, id_cargo, fecha_ingreso, id_sucursal)

"""Un scrip que permita ingresar una compra completa."""
def insertar_compra(numero, fecha_compra, id_proveedor, id_comprobante, id_forma_pago, id_usuario, detalles_compra):
    
    mydb = create_connection()
    mycursor = mydb.cursor()

    insert_compra_query = """
    INSERT INTO compra (numero, fecha_compra, id_proveedor, id_comprobante, id_forma_pago, id_usuario)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    mycursor.execute(insert_compra_query, (numero, fecha_compra, id_proveedor, id_comprobante, id_forma_pago, id_usuario))
    id_compra = mycursor.lastrowid

    insert_detalle_compra_query = """
    INSERT INTO detalle_compra (id_compra, id_producto, cantidad, precio_unitario)
    VALUES (%s, %s, %s, %s)
    """
    
    for detalle in detalles_compra:
        id_producto = detalle['id_producto']
        cantidad = detalle['cantidad']
        precio_unitario = detalle['precio_unitario']
        mycursor.execute(insert_detalle_compra_query, (id_compra, id_producto, cantidad, precio_unitario))
    
    mydb.commit()

    mycursor.close()
    mydb.close()

    print(f"Compra insertada con éxito. ID de la compra: {id_compra}")
    return id_compra

numero_compra = "C-2023-001"
fecha_compra = "2023-09-28"  
id_proveedor = 3             
id_comprobante = 2           
id_forma_pago = 3            
id_usuario = 2               

detalles_compra = [
    {'id_producto': 8, 'cantidad': 10, 'precio_unitario': 100},
    {'id_producto': 9, 'cantidad': 5, 'precio_unitario': 200}
]

insertar_compra(numero_compra, fecha_compra, id_proveedor, id_comprobante, id_forma_pago, id_usuario, detalles_compra)


