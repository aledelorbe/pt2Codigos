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

app.layout = html.Div([
    dcc.Graph(
        id='mapa',
        figure={
            'data': generadorDeMapas(db.extraerClustersEstadoCancer(), db.coloresMapaEstadoCancer)
        }
    )
    
    
])


if __name__ == '__main__':
    app.run_server()