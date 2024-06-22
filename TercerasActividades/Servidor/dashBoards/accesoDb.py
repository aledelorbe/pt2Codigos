import mysql.connector
import os
# from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
# load_dotenv()

# Configura la conexión (local)
config = {
    'user': 'root',
    'password': '12345678',
    'host': 'localhost',
    'database': 'sociodemografico',
}

# Obtener las variables de entorno
# db_user = os.getenv('MYSQLUSER')
# db_password = os.getenv('MYSQLPASSWORD')
# db_host = os.getenv('MYSQLHOST')
# db_name = os.getenv('MYSQLDATABASE')
# db_port = os.getenv('MYSQLPORT')

# Configura la conexión (nube)
# Estos datos se quitaron por seguridad
# config = {
# }

# Configurar la conexión con la base de datos
# config = {
#     'user': db_user,
#     'password': db_password,
#     'host': db_host,
#     'database': db_name,
#     'port': db_port
# }


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
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # Prepara la consulta para traerse los datos de estado con cancer
        sqlString = """
                    select id_estado, cluster
                    from estadocancer
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
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # Prepara la consulta para traerse los datos de estado con cancer
        sqlString = """
                    select id_estado, cluster
                    from estadoescolaridad
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
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # Prepara la consulta para traerse los datos de estado con cancer
        sqlString = """
                    select id_estado, cluster
                    from estadoocupacion
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
        tablaRelacion = 'estadocancer'
        tablaCatalogo = 'cancer'
        nombreId = 'id_cancer'
    elif parametro == 'Nivel Educativo':
        tablaRelacion = 'estadoescolaridad'
        tablaCatalogo = 'escolaridad'
        nombreId = 'id_escolaridad'
    else:
        tablaRelacion = 'estadoocupacion'
        tablaCatalogo = 'ocupacion'
        nombreId = 'id_ocupacion'

    try:
        # INTENTA ESTABLECER LA CONEXION
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # Prepara la consulta para traerse los datos de estado con cancer
        sqlString = f"""
                    select e.nombre, ec.cluster, c.nombre, ec.cantidad, ec.porcentaje 
                    from {tablaRelacion} ec
                    inner join estado e
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
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # Prepara la consulta para traerse los datos de estado con cancer
        sqlString = f"""
                    select e.id_estado, e.nombre, sum(ec.cantidad)
                    from estadocancer ec
                    inner join estado e
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
    
    return estado, total


# Funcion para consultar el nombre de cada estado
def consultaEstados():
    try:
        # INTENTA ESTABLECER LA CONEXION
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # Prepara la consulta para traerse el nombre de todos los estados
        sqlString = f"""
                    select nombre
                    from estado
                    """
        cursor.execute(sqlString) # Ejecuta la consulta
        consultaEstados = cursor.fetchall()

        estados = []
        for renglon in consultaEstados:
            estado = renglon[0]
            estados.append(estado)

    except Exception as e:
        print(f'Error: {e}')

    finally:
        # Cierra la conexión
        if 'conn' in locals():
            conn.close()
    
    return estados


# Funcion para extraer el id de determinado estado
def buscarIdEstado(nombreEstado):
    idEstado = None
    try:
        # INTENTA ESTABLECER LA CONEXION
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # Prepara la consulta para traerse el nombre de todos los estados
        sqlString = f"""
                    select id_estado
                    from estado
                    where nombre = '{nombreEstado}'
                    """
        cursor.execute(sqlString) # Ejecuta la consulta
        consultaIdEstado = cursor.fetchone()

        idEstado = consultaIdEstado[0]

    except Exception as e:
        print(f'Error: {e}')

    finally:
        # Cierra la conexión
        if 'conn' in locals():
            conn.close()
    
    return idEstado


# Funcion para extraer el nombre de determinado estado
def buscarNombreEstado(idEstado):
    try:
        # INTENTA ESTABLECER LA CONEXION
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # Prepara la consulta para traerse el nombre de todos los estados
        sqlString = f"""
                    select nombre
                    from estado
                    where id_estado = {idEstado}
                    """
        cursor.execute(sqlString) # Ejecuta la consulta
        consultaNombreEstado = cursor.fetchone()

        nombreEstado = consultaNombreEstado[0]

    except Exception as e:
        print(f'Error: {e}')

    finally:
        # Cierra la conexión
        if 'conn' in locals():
            conn.close()
    
    return nombreEstado
