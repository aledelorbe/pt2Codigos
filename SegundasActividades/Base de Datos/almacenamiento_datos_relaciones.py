import pandas as pd
import numpy as np
import pyodbc # Este modulo se tuvo que instalar de la siguiente manera: 'pip install pyodbc'

# Configura la cadena de conexión
server = '192.168.0.14\MSSQL3'
database = 'Sociodemografico'
username = 'sa'
password = '123456'

# Construye la cadena de conexión
conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

# Intenta establecer la conexión
try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # Ejemplo de consulta
    cursor.execute('SELECT * FROM Estado')
    rows = cursor.fetchall()

    # Imprime los resultados
    for row in rows:
        print(row)

except Exception as e:
    print(f'Error: {e}')

finally:
    # Cierra la conexión
    if 'conn' in locals():
        conn.close()
