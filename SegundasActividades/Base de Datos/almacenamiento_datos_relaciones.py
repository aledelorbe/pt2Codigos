# CARGA LAS LIBRERIAS
import pandas as pd
import numpy as np
import pyodbc # Este modulo se tuvo que instalar de la siguiente manera: 'pip install pyodbc'

# CARGAR LOS DF'S
dfEstados = pd.read_csv('df.csv')
gruposEducaciones = pd.read_csv('gruposEducaciones.csv')
gruposEmpleos = pd.read_csv('gruposEmpleos.csv')
gruposCanceres = pd.read_csv('gruposCanceres.csv')

# Configura la cadena de conexión
server = '192.168.0.14\MSSQL3'
database = 'Sociodemografico'
username = 'sa'
password = '123456'

# Construye la cadena de conexión
conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

try:
    # INTENTA ESTABLECER LA CONEXION
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # contador = 0
    # # ITERAR LOS DATOS DEL ESTADO CON CANCER PARA SER ALMACENADOS
    # for index, row in dfEstados.iterrows():
    #     estado = row["estado"]
    #     numCluster = int(gruposCanceres.iloc[index].values)
    #     print(f'Índice: {index}, Estado: {estado}, numCluster: {numCluster}')
    #     for i in range(0, 72, 2): # 36*2 = 72. 36 tipos de cancer y de 2 en dos.
    #         descrip = dfEstados.iloc[index, 1 + i]
    #         cant = int(dfEstados.iloc[index, 2 + i])
    #         print(f'Descrip: {descrip}, Cant: {cant}')
    #         # Mandar a llamar el sp que inserta datos de estado con cancer
    #         cursor.execute("{CALL sp_insertarEstadoCancer (?, ?, ?, ?)}", (estado, descrip, cant, numCluster))
    #         if cursor.rowcount == 1:
    #             contador += 1
    
    # # Solo si se hicieron las inserciones que se debieron hacer entonces...
    # if contador == 1152: # 32 estado x 36 tipos de cancer = 1152 registros
    #     print('Se almacenaron correctamente los datos de estado con cancer.')
    #     # Guardar las inserciones realizadas.
    #     conn.commit()
    # else:
    #     print('Se almacenaron incorrectamente los datos de estado con cancer.')
    #     # Deshacer todo lo que se haya hecho en la db
    #     conn.rollback()



    contador = 0
    # ITERAR LOS DATOS DEL ESTADO CON OCUPACION PARA SER ALMACENADOS
    for index, row in dfEstados.iterrows():
        estado = row["estado"]
        numCluster = int(gruposEmpleos.iloc[index].values)
        print(f'Índice: {index}, Estado: {estado}, numCluster: {numCluster}')
        for i in range(0, 26, 2): # 13*2 = 26. 13 categorias de empleos y de 2 en dos.
            descrip = dfEstados.iloc[index, 73 + i]
            cant = int(dfEstados.iloc[index, 74 + i])
            print(f'Descrip: {descrip}, Cant: {cant}')
            # Mandar a llamar el sp que inserta datos de estado con cancer
            cursor.execute("{CALL sp_insertarEstadoOcupacion (?, ?, ?, ?)}", (estado, descrip, cant, numCluster))
            if cursor.rowcount == 1:
                contador += 1
    
    # Solo si se hicieron las inserciones que se debieron hacer entonces...
    if contador == 416: # 32 estado x 13 categorias de ocupacion = 1152 registros
        print('Se almacenaron correctamente los datos de estado con categoria de ocupacion.')
        # Guardar las inserciones realizadas.
        conn.commit()
    else:
        print('Se almacenaron incorrectamente los datos de estado con categoria de ocupacion.')
        # Deshacer todo lo que se haya hecho en la db
        conn.rollback()


except Exception as e:
    print(f'Error: {e}')
    conn.rollback()

finally:
    # Cierra la conexión
    if 'conn' in locals():
        conn.close()
