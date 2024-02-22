import dash
from dash import dcc
from dash import html
import json
import plotly.graph_objects as go
import accesoDb as db
import funcionesAuxiliares as funcAux
from dash.dependencies import Input, Output


def generadorDeMapas(clustersEstadoParametroX, dictColoresMapaEstadoParametroX):
    estados = []
    grupos = [] # Para que solo un estado por grupo se agregue a la leyenda
    apariciones = []

    # Lee el archivo GeoJSON
    # with open('mexico.geojson', encoding='utf-8') as f:
    with open('../mexico.geojson', encoding='utf-8') as f:
        data = json.load(f)

    ordenLegend = 0 # Para que las leyendas salgan en orden ascendente
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
        
        if numCluster not in grupos and numCluster == ordenLegend:
            # Agrega la capa de polígono para el mapa
            estados.append(go.Scattergeo(
                locationmode = 'country names',
                lon = longitudes,
                lat = latitudes,
                mode = 'lines',
                line = dict(width = 1, color = 'blue'),
                fill = 'toself',
                fillcolor = dictColoresMapaEstadoParametroX[str(numCluster)],
                name=funcAux.gruposX[str(numCluster)],
                legendgroup = funcAux.gruposX[str(numCluster)],
                hoverinfo='text',
                hovertext=entidad,
            ))

            grupos.append(numCluster)
            ordenLegend += 1
        else:
            # Agrega la capa de polígono para el mapa
            estados.append(go.Scattergeo(
                locationmode = 'country names',
                lon = longitudes,
                lat = latitudes,
                mode = 'lines',
                line = dict(width = 1, color = 'blue'),
                fill = 'toself',
                fillcolor = dictColoresMapaEstadoParametroX[str(numCluster)],
                name=funcAux.gruposX[str(numCluster)],
                legendgroup = funcAux.gruposX[str(numCluster)],
                hoverinfo='text',
                hovertext=entidad,
                showlegend=False
            ))

    return estados, apariciones


def aplicarEstilosMapa(fig, tituloX, aparicionesX):
    # Define el diseño del mapa
    fig.update_geos(
        projection_type="equirectangular",
        showland = True,
        showcountries=True,
        landcolor = "rgb(243, 243, 243)",
        countrycolor = "rgb(204, 204, 204)",
        showlakes = True,
        lakecolor = "rgb(255, 255, 255)",
        projection_scale=9.6,
        center=dict(lon=-102, lat=23.6345)
    )

    orden_personalizado = [2, 0, 3, 1]

    # Ajusta el título y las leyendas
    fig.update_layout(
        title = tituloX,
        geo = dict(
            scope='world',
            showland=True,
        ),
        margin=dict(l=20, r=20, t=50, b=50),
        width=1320,  # ajusta el ancho de la figura
        height=680,   # ajusta el alto de la figura
        # hovermode='closest' Esta por defecto asi
    )

    # Reordenar las leyendas según el orden personalizado
    print(aparicionesX)
    # aparicionesX.sort()
    # fig.data = [fig.data[i] for i in aparicionesX]
    # fig.data[aparicionesX.index(0)].showlegend=True
    # fig.data[aparicionesX.index(1)].showlegend=True
    # fig.data[aparicionesX.index(2)].showlegend=True
    # fig.data[aparicionesX.index(3)].showlegend=True
    # fig.data[aparicionesX.index(4)].showlegend=True

    return fig




app = dash.Dash()


# MAPA QUE SE MOSTRARA POR DEFECTO
# Genera la figura
mapa, apariciones = generadorDeMapas(db.extraerClustersEstadoCancer(), funcAux.coloresMapaEstadoCancer)
fig = go.Figure(data=mapa)

# Aplicar estilos
fig = aplicarEstilosMapa(fig, 'Estados de México feat tipos de cancer', apariciones)


app.layout = html.Div([
    # APLICACION
    dcc.Dropdown(id='parametro', 
                 options=['Tipo de Cancer', 'Nivel Educativo', 'Categoria de Empleo'], 
                 value='Tipo de Cancer'),
    dcc.Graph(
        id='mapa',
        figure=fig
    ),
    html.Div([
        html.Pre(id='informacionClick')
    ]),
    dcc.Graph(
        id='barra',
        # figure=fig
    ),

    # CONJUNTOS DE DATOS
    html.Span("Conjunto de Datos del año 2010"),
    html.Button("Download", id="btn-download-set-2010"),
    dcc.Download(id="download-set-2010"),

])


# ACTUALIZADOR DE MAPA
# Cambia el mapa dependientemenete del valor que se selccione en el dropdown
@app.callback(
    Output('mapa', 'figure'),
    [Input('parametro', 'value')]
)
def actualizarMapa(parametro):
    titulo = None
    indicesClustersX = None
    coloresMapa = None 

    if parametro == 'Tipo de Cancer':
        titulo = 'Estados de México feat tipos de cancer'
        indicesClustersX = db.extraerClustersEstadoCancer()
        coloresMapa = funcAux.coloresMapaEstadoCancer 
    elif parametro == 'Nivel Educativo':
        titulo = 'Estados de México feat Nivel Educativo'
        indicesClustersX = db.extraerClustersEstadoEducacion()
        coloresMapa = funcAux.coloresMapaEstadoEducacion 
    else:
        titulo = 'Estados de México feat Ocupacion'
        indicesClustersX = db.extraerClustersEstadoOcupacion()
        coloresMapa = funcAux.coloresMapaEstadoOcupacion 

    # MAPA QUE SE MOSTRARA TRAS LA ACTUALIZACION
    # Genera una nueva figura
    mapa, apariciones = generadorDeMapas(indicesClustersX, coloresMapa)
    fig = go.Figure(data=mapa)

    # Aplicar los nuevos estilos
    fig = aplicarEstilosMapa(fig, titulo, apariciones)
        
    return fig

# EVENTO CLICK
# Cuando se le de click sobre el mapa se extraera informacion util, especialmente
# sobre cual estado se dio click para mostrar la informacion de dicho estado.
@app.callback(
    Output('informacionClick', 'children'),
    [Input('mapa', 'clickData'), Input('parametro', 'value')]
)
def extractorInformacionClick(informacion, parametro):
    # return json.dumps(informacion, indent=2)
    curve_number = informacion['points'][0]['curveNumber'] + 1
    return curve_number, parametro, funcAux.corregirIndice(curve_number)

# ACTUALIZADOR DE BARRA
# Cambia la grafica de barras dependientemenete del estado que se selccione en el mapa
@app.callback(
    Output('barra', 'figure'),
    [Input('parametro', 'value'), Input('mapa', 'clickData')]
)
def actualizarBarra(parametro, informacion):

    # Seleccionar el diccionario de colores que le toque segun el parametro
    diccColores = None
    if parametro == 'Tipo de Cancer':
        diccColores = funcAux.coloresMapaEstadoCancer
    elif parametro == 'Nivel Educativo':
        diccColores = funcAux.coloresMapaEstadoEducacion
    else:
        diccColores = funcAux.coloresMapaEstadoOcupacion

    # De la informacion del click, extraer el id del pais
    numeroId = informacion['points'][0]['curveNumber'] + 1 # El +1 porque el primer estado es 0 pero en la db es 1
    numeroId = funcAux.corregirIndice(numeroId) # Corregir indice

    # Consultar los datos que permiten la creacion del grafico
    estado, numCluster, etiquetas, cantidades = db.consultaBarras(parametro, numeroId)
    # print(estado, numCluster, etiquetas, cantidades)

    dataBarra = [go.Bar(x=etiquetas, 
                        y=cantidades,
                        marker=dict(
                            color=diccColores[str(numCluster)],  
                            line=dict(color='black')  
                        ))] 
    estilosFigura = go.Layout(
        title=f"Cantidad de personas con cancer por cada {parametro} en el estado de {estado}",
        xaxis=dict(title=parametro),
        yaxis=dict(title="cantidad"),
        font=dict(
            family='Verdana',
            size=16,
            color='black'
        )
    )
    figura = go.Figure(data=dataBarra, layout=estilosFigura)

    return figura

if __name__ == '__main__':
    app.run_server()