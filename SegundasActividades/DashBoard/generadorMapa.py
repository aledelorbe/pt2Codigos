# CARGA LAS LIBRERIAS
import json
import plotly.graph_objects as go
import plotly.offline as pyo
import plotly.express as px
import pandas as pd
import numpy as np
import pyodbc # Este modulo se tuvo que instalar de la siguiente manera: 'pip install pyodbc'

# Diccionario de colores para el mapa de estado - cancer
coloresMapaEstadoCancer = {
    "0": "#870000",
	"1": "#215f00",
	"2": "#c21500",
	"3": "#4b6cb7",
    "4": "#753a88"
}

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

    # print(aux)
    return aux

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

    # Lee el archivo GeoJSON
    with open('mexico.geojson', encoding='utf-8') as f:
        data = json.load(f)

    # Prepara la consulta
    sqlString = """
                select id_estado, cluster
                from EstadoCancer
                group by id_estado, cluster
                order by 1
                """
    cursor.execute(sqlString) # Ejecuta la consulta
    consultaEstadoCancer = cursor.fetchall()

    clustersEstadoCancer = []
    for renglon in consultaEstadoCancer:
        # Extra el id_pais y el numero de cluster
        _, numCluster = renglon
        clustersEstadoCancer.append(numCluster)

except Exception as e:
    print(f'Error: {e}')
    conn.rollback()

finally:
    # Cierra la conexión
    if 'conn' in locals():
        conn.close()

# Actuliazar los clusters
clustersEstadoCancer = actualizacionClusters(clustersEstadoCancer)

# Crea la figura
fig = px.line()

# Itera sobre todas las características (features) en el archivo GeoJSON
for feature, numCluster in zip(data['features'], clustersEstadoCancer):
# for feature in data['features']:
    # Extrae las coordenadas y las propiedades de la característica actual
    coordinates = feature['geometry']['coordinates'][0]
    properties = feature['properties']
    
    # Extrae los datos específicos que deseas mostrar
    entidad = properties['ENTIDAD']
    capital = properties['CAPITAL']
    area = properties['AREA']
    perimetro = properties['PERIMETER']
    
    # Extrae las longitudes y latitudes de las coordenadas
    longitudes = [coord[0] for coord in coordinates]
    latitudes = [coord[1] for coord in coordinates]
    
    # Agrega la capa de polígono para el mapa
    fig.add_trace(go.Scattergeo(
        locationmode = 'country names',
        lon = longitudes,
        lat = latitudes,
        mode = 'lines',
        line = dict(width = 1, color = 'blue'),
        fill = 'toself',
        # fillcolor = 'rgba(0, 255, 0, 0.1)',
        fillcolor = coloresMapaEstadoCancer[str(numCluster)],
        name = entidad,
        visible="legendonly"
    ))

# Define el diseño del mapa
fig.update_geos(
    projection_type="equirectangular",
    showland = True,
    showcountries=True,
    landcolor = "rgb(243, 243, 243)",
    countrycolor = "rgb(204, 204, 204)",
    showlakes = True,
    lakecolor = "rgb(255, 255, 255)",
    projection_scale=9.5,
    center=dict(lon=-102, lat=23.6345)
)

# Ajusta el título y las leyendas
fig.update_layout(
    title = 'Áreas de los estados de México',
    geo = dict(
        scope='world',
        showland=True,
    ),
    margin=dict(l=20, r=20, t=50, b=50),
    width=1320,  # ajusta el ancho de la figura
    height=680   # ajusta el alto de la figura
)

# Muestra el mapa
fig.show()

# pyo.plot(fig, filename="mapaMexico.html")

# colores
#870000
#215f00
#c21500
#ffc500
#7a2828
#4b6cb7
#182848
#753a88



# print(coloresMapaEstadoCancer["0"])