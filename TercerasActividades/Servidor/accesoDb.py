import pyodbc 
import json


# Configura la cadena de conexión
server = '192.168.0.14\MSSQL3'
# server = '192.168.1.103\MSSQL3'
# server = '192.168.1.101\MSSQL3'
database = 'Sociodemografico'
username = 'sa'
password = '123456'

# Construye la cadena de conexión
conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

# METODOS QUE NO SE MANDAN A LLAMAR FUERA DEL ARCHIVO

# Lo que sucede es que en la db los paises estan ordenados alfabeticamente (A - Z)
# pero el archivo geojson tambien estan ordenados alfabeticamente pero solo utilizando
# la primera letra del estado, es decir, que estados que empiezan con c la segunda letra
# no esta ordenada.
def actualizacionClusters(lista):
    aux = [elemento for elemento in lista]

    # Ordenar los estados que inician con la letra 'c'
    aux[4] = lista[6]
    aux[5] = lista[7]
    aux[6] = lista[4]
    aux[7] = lista[5]
    # Ordenar los estados que inician con la letra 'm'
    aux[14] = lista[16]
    aux[15] = lista[14]
    aux[16] = lista[15]

    return aux


# METODOS QUE SE MANDAN A LLAMAR FUERA DEL ARCHIVO PARA CONECTARSE CON LA DB
def extraerClustersEstadoCancer():
    clustersEstadoCancer = []

    try:
        # INTENTA ESTABLECER LA CONEXION
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Prepara la consulta para traerse los datos de estado con cancer
        sqlString = """
                    select id_estado, cluster
                    from EstadoCancer
                    group by id_estado, cluster
                    order by 1
                    """
        cursor.execute(sqlString) # Ejecuta la consulta
        consultaEstadoCancer = cursor.fetchall()

        for renglon in consultaEstadoCancer:
            # Extrae el id_pais y el numero de cluster
            _, numCluster = renglon
            clustersEstadoCancer.append(numCluster)

        # Actuliazar los clusters
        clustersEstadoCancer = actualizacionClusters(clustersEstadoCancer)

    except Exception as e:
        print(f'Error: {e}')
        conn.rollback()

    finally:
        # Cierra la conexión
        if 'conn' in locals():
            conn.close()
    
    return clustersEstadoCancer


def extraerClustersEstadoEducacion():
    clustersEstadoEducacion = []
    
    try:
        # INTENTA ESTABLECER LA CONEXION
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Prepara la consulta para traerse los datos de estado con cancer
        sqlString = """
                    select id_estado, cluster
                    from EstadoEscolaridad
                    group by id_estado, cluster
                    order by 1
                    """
        cursor.execute(sqlString) # Ejecuta la consulta
        consultaEstadoEducacion = cursor.fetchall()

        for renglon in consultaEstadoEducacion:
            # Extrae el id_pais y el numero de cluster
            _, numCluster = renglon
            clustersEstadoEducacion.append(numCluster)

        # Actuliazar los clusters
        clustersEstadoEducacion = actualizacionClusters(clustersEstadoEducacion)

    except Exception as e:
        print(f'Error: {e}')
        conn.rollback()

    finally:
        # Cierra la conexión
        if 'conn' in locals():
            conn.close()
    
    return clustersEstadoEducacion


def extraerClustersEstadoOcupacion():
    clustersEstadoOcupacion = []

    try:
        # INTENTA ESTABLECER LA CONEXION
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Prepara la consulta para traerse los datos de estado con cancer
        sqlString = """
                    select id_estado, cluster
                    from EstadoOcupacion
                    group by id_estado, cluster
                    order by 1
                    """
        cursor.execute(sqlString) # Ejecuta la consulta
        consultaEstadoOcupacion = cursor.fetchall()

        for renglon in consultaEstadoOcupacion:
            # Extra el id_pais y el numero de cluster
            _, numCluster = renglon
            clustersEstadoOcupacion.append(numCluster)

        # Actuliazar los clusters
        clustersEstadoOcupacion = actualizacionClusters(clustersEstadoOcupacion)

    except Exception as e:
        print(f'Error: {e}')
        conn.rollback()

    finally:
        # Cierra la conexión
        if 'conn' in locals():
            conn.close()
    
    return clustersEstadoOcupacion


# Funcion para consultar datos que permiten la creacion de la grafica de barras
def consultaBarras(parametro, numeroId):
    
    tablaRelacion = None
    tablaCatalogo = None
    nombreId = None
    if parametro == 'Tipo de Cancer':
        tablaRelacion = 'EstadoCancer'
        tablaCatalogo = 'Cancer'
        nombreId = 'id_cancer'
    elif parametro == 'Nivel Educativo':
        tablaRelacion = 'EstadoEscolaridad'
        tablaCatalogo = 'Escolaridad'
        nombreId = 'id_escolaridad'
    else:
        tablaRelacion = 'EstadoOcupacion'
        tablaCatalogo = 'Ocupacion'
        nombreId = 'id_ocupacion'

    try:
        # INTENTA ESTABLECER LA CONEXION
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Prepara la consulta para traerse los datos de estado con cancer
        sqlString = f"""
                    select e.nombre, ec.cluster, c.nombre, ec.cantidad, ec.porcentaje 
                    from {tablaRelacion} ec
                    inner join Estado e
                    on e.id_estado = ec.id_estado
                    inner join {tablaCatalogo} c
                    on c.{nombreId} = ec.{nombreId}
                    where e.id_estado = {numeroId}
                    """
        cursor.execute(sqlString) # Ejecuta la consulta
        consultaEstadoParametro = cursor.fetchall()

        estado = None
        numCluster = None
        etiquetas = []
        cantidades = []
        porcentajes = []
        for renglon in consultaEstadoParametro:
            estado, numCluster, etiqueta, cantidad, porcentaje = renglon
            etiquetas.append(etiqueta)
            cantidades.append(cantidad)
            porcentajes.append(porcentaje)

    except Exception as e:
        print(f'Error: {e}')
        conn.rollback()

    finally:
        # Cierra la conexión
        if 'conn' in locals():
            conn.close()
    
    return estado, numCluster, etiquetas, cantidades, porcentajes


# Funcion para consultar la cantidad total de personas que hay con cancer
def consultaTotal(numeroId):
    try:
        # INTENTA ESTABLECER LA CONEXION
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Prepara la consulta para traerse los datos de estado con cancer
        sqlString = f"""
                    select e.id_estado, e.nombre, sum(ec.cantidad)
                    from EstadoCancer ec
                    inner join Estado e
                    on e.id_estado = ec.id_estado
                    group by e.id_estado, e.nombre
                    having e.id_estado = {numeroId}
                    """
        cursor.execute(sqlString) # Ejecuta la consulta
        consultaTotalEstado = cursor.fetchone()

        _, estado, total = consultaTotalEstado

    except Exception as e:
        print(f'Error: {e}')

    finally:
        # Cierra la conexión
        if 'conn' in locals():
            conn.close()
    
    print(f'idEstado: {numeroId}, Estado: {estado}, Total: {total}')
    return estado, total
