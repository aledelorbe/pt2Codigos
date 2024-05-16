# CARGA LAS LIBRERIAS
import pandas as pd
import numpy as np
import pyodbc # Este modulo se tuvo que instalar de la siguiente manera: 'pip install pyodbc'

# CARGAR LOS DF'S
dfEducaciones0_1 = pd.read_csv('Resul (0 - 1)/dfEducaciones.csv')
dfEmpleos0_1 = pd.read_csv('Resul (0 - 1)/dfEmpleos.csv')
dfEducaciones = pd.read_csv('Resul sin escala/dfEducaciones.csv')
dfEmpleos = pd.read_csv('Resul sin escala/dfEmpleos.csv')
gruposEducaciones = pd.read_csv('gruposEducaciones.csv')
gruposEmpleos = pd.read_csv('gruposEmpleos.csv')

# Configura la cadena de conexión
server = '192.168.0.14\MSSQL3'
database = 'Sociodemografico'
username = 'sa'
password = '123456'

# Construye la cadena de conexión
conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

# Determinacion de valores distintos
nombres = dfEducaciones.columns
nivelesEscolares = nombres[0:10]
canceres = nombres[10:]
nombres = dfEmpleos.columns
empleos = nombres[0:13]
estados = ['Aguascalientes', 'Baja California', 'Baja California Sur', 'Campeche', 'Chiapas', 
           'Chihuahua', 'Coahuila de Zaragoza', 'Colima', 'Distrito Federal', 'Durango', 
           'Guanajuato', 'Guerrero', 'Hidalgo', 'Jalisco', 'Michoacán de Ocampo', 'Morelos', 
           'México', 'Nayarit', 'Nuevo León', 'Oaxaca', 'Puebla', 'Querétaro', 'Quintana Roo', 
           'San Luis Potosí', 'Sinaloa', 'Sonora', 'Tabasco', 'Tamaulipas', 'Tlaxcala', 
           'Veracruz de Ignacio de la Llave', 'Yucatán', 'Zacatecas']

try:
    # INTENTA ESTABLECER LA CONEXION
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    contador = 0
    # ITERA LOS DATOS DE ESTADO CON EDUCACION Y CON CANCER PARA SER ALMACENADOS
    for rowEdu, rowEdu0_1, grupoEdu, estado in zip(dfEducaciones.values, dfEducaciones0_1.values, gruposEducaciones.values, estados):
        numCluster = int(grupoEdu[0])
        
        for i in range(10):
            cant = int(rowEdu[i])
            porcen = round(rowEdu0_1[i], 4)
            descrip = nivelesEscolares[i]
            print(estado, descrip, cant, numCluster, round(porcen, 4))
            # Mandar a llamar el sp que inserta datos de estado con nivel escolar
            cursor.execute("{CALL sp_insertarEstadoEscolaridad (?, ?, ?, ?, ?)}", (estado, descrip, cant, numCluster, porcen))
            if cursor.rowcount == 1:
                contador += 1

        for i in range(10, 46, 1):
            cant = int(rowEdu[i])
            porcen =  round(rowEdu0_1[i], 4)
            descrip = canceres[i - 10]
            print(estado, descrip, cant, numCluster, porcen)
            # Mandar a llamar el sp que inserta datos de estado con algun tipo de cancer
            cursor.execute("{CALL sp_insertarEstadoCancer (?, ?, ?, ?, ?)}", (estado, descrip, cant, numCluster, porcen))
            if cursor.rowcount == 1:
                contador += 1

    # Solo si se hicieron las inserciones que se debieron hacer entonces...
    if contador == 1472: # (32 estado x 36 tipos de cancer = 1152 registros) + 
                        # (32 estados x 10 niveles escolares = 320 registros) = 1472
        print(f'\nSe almacenaron correctamente los {contador} registros de estado con cancer y educacion.\n')
        # Guardar las inserciones realizadas.
        conn.commit()
    else:
        print('Se almacenaron incorrectamente los datos de estado con cancer y educacion.')
        # Deshacer todo lo que se haya hecho en la db
        conn.rollback()

    contador = 0
    # ITERAR LOS DATOS DEL ESTADO CON OCUPACION Y CON CANCER PARA SER ALMACENADOS
    for rowEmp, rowEmp0_1, grupoEmp, estado in zip(dfEmpleos.values, dfEmpleos0_1.values, gruposEmpleos.values, estados):
        numCluster = int(grupoEmp[0])
        
        for i in range(13):
            cant = int(rowEmp[i])
            porcen = round(rowEmp0_1[i], 4)
            descrip = empleos[i]
            print(estado, descrip, cant, numCluster, porcen)
            # Mandar a llamar el sp que inserta datos de estado con nivel escolar
            cursor.execute("{CALL sp_insertarEstadoOcupacion (?, ?, ?, ?, ?)}", (estado, descrip, cant, numCluster, porcen))
            if cursor.rowcount == 1:
                contador += 1

    # Solo si se hicieron las inserciones que se debieron hacer entonces...
    if contador == 416: # (32 estados x 13 categorias de empleo = 416 registros)  
                    # Ya no se contemplaron los datos del cancer porque serian los mismos que ya se insertaron
        print(f'\nSe almacenaron correctamente los {contador} registros de estado con cancer y empleo.\n')
        # Guardar las inserciones realizadas.
        conn.commit()
    else:
        print('Se almacenaron incorrectamente los datos de estado con cancer y empleo.')
        # Deshacer todo lo que se haya hecho en la db
        conn.rollback()

except Exception as e:
    print(f'Error: {e}')
    conn.rollback()

finally:
    # Cierra la conexión
    if 'conn' in locals():
        conn.close()
