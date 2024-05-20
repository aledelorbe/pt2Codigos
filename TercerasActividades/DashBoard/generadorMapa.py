# CARGA LAS LIBRERIAS
import json
import plotly.graph_objects as go
import plotly.offline as pyo
import plotly.express as px
import pandas as pd
import numpy as np
import pyodbc # Este modulo se tuvo que instalar de la siguiente manera: 'pip install pyodbc'

# Diccionarios con los colores para los 2 mapas
coloresEducacion = {
    "0": "#4682B4", # Azul metalico
	"1": "#FF4500", # Naranja
	"2": "#C71585", # Rosa Oscuro
	"3": "#006847", # Verde bandera
    "4": "#753a88", # Morado oscuro
    "5": "#8B4513", # Cafe
    "6": "#FF0000", # Rojo
    "7": "#00FF00", # Verde lima
    "8": "#FFFF00", # Amarillo
    "9": "#00FFFF", # Cian
}
coloresOcupacion = {
    "0": "#4682B4", # Azul metalico
	"3": "#FF4500", # Naranja
	"6": "#C71585", # Rosa Oscuro
	"1": "#006847", # Verde bandera
    "4": "#753a88", # Morado oscuro
    "5": "#8B4513", # Cafe
    "2": "#FF0000", # Rojo
    "7": "#00FF00", # Verde lima
    "8": "#FFFF00", # Amarillo
    "9": "#00FFFF", # Cian
    "10": "#FF69B4", # Rosa metalico
    "11": "#1A195D", # Azul marino
    "12": "#B22222", # Rojo metalico
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

    return aux

# Configura la cadena de conexión
# server = '192.168.0.14\MSSQL3'
server = '192.168.1.103\MSSQL3'
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

    # Prepara la consulta para traerse los datos de estado con cancer
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

    # Prepara la consulta para traerse los datos de estado con educacion
    sqlString = """
                select id_estado, cluster
                from EstadoEscolaridad
                group by id_estado, cluster
                order by 1
                """
    cursor.execute(sqlString) # Ejecuta la consulta
    consultaEstadoEducacion = cursor.fetchall()

    clustersEstadoEducacion = []
    for renglon in consultaEstadoEducacion:
        # Extra el id_pais y el numero de cluster
        _, numCluster = renglon
        clustersEstadoEducacion.append(numCluster)

    # Prepara la consulta para traerse los datos de estado con ocupacion
    sqlString = """
                select id_estado, cluster
                from EstadoOcupacion
                group by id_estado, cluster
                order by 1
                """
    cursor.execute(sqlString) # Ejecuta la consulta
    consultaEstadoOcupacion = cursor.fetchall()

    clustersEstadoOcupacion = []
    for renglon in consultaEstadoOcupacion:
        # Extra el id_pais y el numero de cluster
        _, numCluster = renglon
        clustersEstadoOcupacion.append(numCluster)

except Exception as e:
    print(f'Error: {e}')
    conn.rollback()

finally:
    # Cierra la conexión
    if 'conn' in locals():
        conn.close()

# Actualizar los clusters
clustersEstadoCancer = actualizacionClusters(clustersEstadoCancer)
clustersEstadoEducacion = actualizacionClusters(clustersEstadoEducacion)
clustersEstadoOcupacion = actualizacionClusters(clustersEstadoOcupacion)


# CREACION DE LOS MAPAS

# Creacion del mapa estado con niveles de educacion
# Crea la figura
fig = px.line()

# Itera sobre todas las características (features) en el archivo GeoJSON
for feature, numCluster in zip(data['features'], clustersEstadoEducacion):
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
        fillcolor = coloresEducacion[str(numCluster)],
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
    title = 'Estados de México feat niveles de educacion',
    geo = dict(
        scope='world',
        showland=True,
    ),
    margin=dict(l=20, r=20, t=50, b=50),
    width=1320,  # ajusta el ancho de la figura
    height=680   # ajusta el alto de la figura
)

# Oculta los números en los ejes
fig.update_xaxes(visible=False)
fig.update_yaxes(visible=False)

# Muestra el mapa
fig.show()

# pyo.plot(fig, filename="mapaMexicoEducacion.html")


# Creacion del mapa estado con categorias de empleo
# Crea la figura
# fig = px.line()

# # Itera sobre todas las características (features) en el archivo GeoJSON
# for feature, numCluster in zip(data['features'], clustersEstadoOcupacion):
#     # Extrae las coordenadas y las propiedades de la característica actual
#     coordinates = feature['geometry']['coordinates'][0]
#     properties = feature['properties']
    
#     # Extrae los datos específicos que deseas mostrar
#     entidad = properties['ENTIDAD']
#     capital = properties['CAPITAL']
#     area = properties['AREA']
#     perimetro = properties['PERIMETER']
    
#     # Extrae las longitudes y latitudes de las coordenadas
#     longitudes = [coord[0] for coord in coordinates]
#     latitudes = [coord[1] for coord in coordinates]
    
#     # Agrega la capa de polígono para el mapa
#     fig.add_trace(go.Scattergeo(
#         locationmode = 'country names',
#         lon = longitudes,
#         lat = latitudes,
#         mode = 'lines',
#         line = dict(width = 1, color = 'blue'),
#         fill = 'toself',
#         fillcolor = coloresOcupacion[str(numCluster)],
#         name = entidad,
#         visible="legendonly"
#     ))

# # Define el diseño del mapa
# fig.update_geos(
#     projection_type="equirectangular",
#     showland = True,
#     showcountries=True,
#     landcolor = "rgb(243, 243, 243)",
#     countrycolor = "rgb(204, 204, 204)",
#     showlakes = True,
#     lakecolor = "rgb(255, 255, 255)",
#     projection_scale=9.5,
#     center=dict(lon=-102, lat=23.6345)
# )

# # Ajusta el título y las leyendas
# fig.update_layout(
#     title = 'Estados de México feat Ocupacion',
#     geo = dict(
#         scope='world',
#         showland=True,
#     ),
#     margin=dict(l=20, r=20, t=50, b=50),
#     width=1320,  # ajusta el ancho de la figura
#     height=680   # ajusta el alto de la figura
# )

# # Oculta los números en los ejes
# fig.update_xaxes(visible=False)
# fig.update_yaxes(visible=False)

# # Muestra el mapa
# fig.show()

# pyo.plot(fig, filename="mapaMexicoOcupacion.html")