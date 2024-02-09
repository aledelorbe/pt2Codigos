import json
import plotly.graph_objects as go

# Lee el archivo GeoJSON
with open('mexico.geojson', encoding='utf-8') as f:
    data = json.load(f)

# Crea la figura
fig = go.Figure()

# Itera sobre todas las características (features) en el archivo GeoJSON
for feature in data['features']:
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
    title = 'Áreas de los estados de México',
    geo = dict(
        scope='north america',
        showland=True,
    )
)

# Muestra el mapa
fig.show()
