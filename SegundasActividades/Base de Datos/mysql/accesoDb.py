import mysql.connector

# Configura la conexión
config = {
    'user': 'root',
    'password': '12345678',
    'host': 'localhost',
    'database': 'Sociodemografico',
}

def insertarEstadoParametro(parametro, idEstado, idParametro, cant, numCluster, porcen):
    tabla = None
    rowAfectados = None
    if parametro == 'escolaridad':
        tabla = 'EstadoEscolaridad'
    elif parametro == 'ocupacion':
        tabla = 'EstadoOcupacion'
    else:
        tabla = 'EstadoCancer'

    try:
        # INTENTA ESTABLECER LA CONEXION
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        sql = f"""
            INSERT INTO {tabla}
            VALUES ({idEstado}, {idParametro}, {cant}, {numCluster}, {porcen});
            """
        cursor.execute(sql)
        rowAfectados = cursor.rowcount

        conn.commit()
    except Exception as e:
        print(f'Error: {e}')
        conn.rollback()

        return 0

    finally:
        # Cierra la conexión
        if 'conn' in locals():
            conn.close()

    return rowAfectados


def buscarId(tabla, nombre):
    id_name = None
    id_num = None
    if tabla == 'escolaridad':
        id_name = 'id_escolaridad'
    elif tabla == 'ocupacion':
        id_name = 'id_ocupacion'
    elif tabla == 'estado':
        id_name = 'id_estado'
    else:
        id_name = 'id_cancer'

    try:
        # INTENTA ESTABLECER LA CONEXION
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        sql = f"""
            SELECT {id_name} 
            FROM {tabla} 
            WHERE nombre = "{nombre}";
            """
        cursor.execute(sql)

        consulta = cursor.fetchone()
        id_num = consulta[0]

    except Exception as e:
        print(f'Error: {e}')
        conn.rollback()

    finally:
        # Cierra la conexión
        if 'conn' in locals():
            conn.close()
    
    return id_num