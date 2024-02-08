import json
import plotly.graph_objects as go

# Lee el archivo GeoJSON
with open('aguascalientes.geojson') as f:
# with open('baja california sur.geojson') as f:
    data = json.load(f)

# Extrae las coordenadas y las propiedades
coordinates = data['geometry']['coordinates'][0]
properties = data['properties']

# Extrae los datos específicos que deseas mostrar
entidad = properties['ENTIDAD']
capital = properties['CAPITAL']
area = properties['AREA']
perimetro = properties['PERIMETER']

# Extrae las longitudes y latitudes de las coordenadas
longitudes = [coord[0] for coord in coordinates]
latitudes = [coord[1] for coord in coordinates]

# Crea la figura
fig = go.Figure()

# Agrega la capa de polígono para el mapa
fig.add_trace(go.Scattergeo(
    locationmode = 'country names',
    lon = longitudes,
    lat = latitudes,
    mode = 'lines',
    line = dict(width = 1,color = 'blue'),
    fill = 'toself',
    fillcolor = 'rgba(0, 255, 0, 0.1)',
    name = entidad
))

# Define el diseño del mapa
fig.update_geos(
    projection_type="mercator",
    showland = True,
    landcolor = "rgb(243, 243, 243)",
    countrycolor = "rgb(204, 204, 204)",
    showlakes = True,
    lakecolor = "rgb(255, 255, 255)",
)

# Ajusta el título y las leyendas
fig.update_layout(
    title = f'Datos de {entidad}',
    geo = dict(
        scope='north america',
        showland=True,
    )
)

# Muestra el mapa
fig.show()


