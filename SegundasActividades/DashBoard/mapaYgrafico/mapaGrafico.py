import dash
from dash import dcc
from dash import html
import json
import plotly.graph_objects as go
import accesoDb as db

app = dash.Dash()


def generadorDeMapas(clustersEstadoParametroX, dictColoresMapaEstadoParametroX):
    estados = []

    # Lee el archivo GeoJSON
    # with open('mexico.geojson', encoding='utf-8') as f:
    with open('../mexico.geojson', encoding='utf-8') as f:
        data = json.load(f)

    # Itera sobre todas las características (features) en el archivo GeoJSON
    for feature, numCluster in zip(data['features'], clustersEstadoParametroX):
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
        estados.append(go.Scattergeo(
            locationmode = 'country names',
            lon = longitudes,
            lat = latitudes,
            mode = 'lines',
            line = dict(width = 1, color = 'blue'),
            fill = 'toself',
            fillcolor = dictColoresMapaEstadoParametroX[str(numCluster)],
            name = entidad,
            visible="legendonly"
        ))

    return estados

# Genera la figura
fig = go.Figure(data=generadorDeMapas(db.extraerClustersEstadoCancer(), db.coloresMapaEstadoCancer))

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
    title = 'Estados de México feat tipos de cancer',
    geo = dict(
        scope='world',
        showland=True,
    ),
    margin=dict(l=20, r=20, t=50, b=50),
    width=1320,  # ajusta el ancho de la figura
    height=680   # ajusta el alto de la figura
)

app.layout = html.Div([
    dcc.Graph(
        id='mapa',
        figure=fig
    )
    
    
])


if __name__ == '__main__':
    app.run_server()