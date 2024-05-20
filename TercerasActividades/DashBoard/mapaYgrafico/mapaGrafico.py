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

    # Lee el archivo GeoJSON
    with open('mexico.geojson', encoding='utf-8') as f:
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
        
        if numCluster not in grupos:
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

    return estados


def aplicarEstilosMapa(fig, tituloX):
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
    )

    return fig




app = dash.Dash()


# MAPA QUE SE MOSTRARA POR DEFECTO
# Genera la figura
fig = go.Figure(data=generadorDeMapas(db.extraerClustersEstadoEducacion(), funcAux.coloresEducacion))

# Aplicar estilos
fig = aplicarEstilosMapa(fig, 'Estados de México feat Nivel Educativo y Cáncer')


app.layout = html.Div([
    # APLICACION
    dcc.Dropdown(id='parametro', 
                 options=['Nivel Educativo y Cáncer', 'Categoria de Empleo y Cáncer'], 
                 value='Nivel Educativo y Cáncer'),
    dcc.Graph(
        id='mapa',
        figure=fig
    ),
    html.Div([
        html.Pre(id='informacionClick')
    ]),
    dcc.Graph(
        id='barraParametro',
        # figure=fig
    ),
    # dcc.Graph(
    #     id='barraCancer',
    #     # figure=fig
    # ),
    dcc.Graph(
        id='barraParametro_0_1',
        # figure=fig
    ),
    # dcc.Graph(
    #     id='barraCancer_0_1',
    #     # figure=fig
    # ),
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
    if parametro == 'Nivel Educativo y Cáncer':
        titulo = 'Estados de México feat Nivel Educativo'
        indicesClustersX = db.extraerClustersEstadoEducacion()
        coloresMapa = funcAux.coloresEducacion 
    else:
        titulo = 'Estados de México feat Ocupacion'
        indicesClustersX = db.extraerClustersEstadoOcupacion()
        coloresMapa = funcAux.coloresOcupacion 

    # MAPA QUE SE MOSTRARA TRAS LA ACTUALIZACION
    # Genera una nueva figura
    fig = go.Figure(data=generadorDeMapas(indicesClustersX, coloresMapa))

    # Aplicar los nuevos estilos
    fig = aplicarEstilosMapa(fig, titulo)
        
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
# Cambia las graficas de barras dependientemenete del estado que se seleccione en el mapa
@app.callback(
    [Output('barraParametro', 'figure'), Output('barraParametro_0_1', 'figure')],
    [Input('parametro', 'value'), Input('mapa', 'clickData')]
)
def actualizarBarra(parametro, informacion):
    # Seleccionar el diccionario de colores que le toque segun el parametro
    diccColores = None
    parametroVerda = None
    if parametro == 'Nivel Educativo y Cáncer':
        diccColores = funcAux.coloresEducacion
        parametroVerda = 'Nivel Educativo'
    else:
        diccColores = funcAux.coloresOcupacion
        parametroVerda = 'Categoria de Empleo'

    # De la informacion del click, extraer el id del pais
    numeroId = informacion['points'][0]['curveNumber'] + 1 # El +1 porque el primer estado es 0 pero en la db es 1
    numeroId = funcAux.corregirIndice(numeroId) # Corregir indice

    # Consultar los datos que permiten la creacion del grafico
    estado, numCluster, etiquetas, cantidades, porcentajes = db.consultaBarras(parametroVerda, numeroId)
    # print(estado, numCluster, etiquetas, cantidades)

    # Crear la grafica de barras para el parametro seleccionado (forma cruda)
    dataBarraParam = [go.Bar(x=etiquetas, 
                        y=cantidades,
                        marker=dict(
                            color=diccColores[str(numCluster)],  
                            line=dict(color='black')  
                        ))] 
    estilosFiguraParam = go.Layout(
        title=f"Cantidad de personas con cáncer en los años 2010 a 2019 por cada {parametroVerda} en el \n \testado de {estado}",
        xaxis=dict(title=parametroVerda),
        yaxis=dict(title="Cantidad"),
        font=dict(
            family='Verdana',
            size=16,
            color='black'
        )
    )
    figuraParam = go.Figure(data=dataBarraParam, layout=estilosFiguraParam)

    # Crear la grafica de barras para el parametro seleccionado (forma porcentual)
    dataBarraParam_0_1 = [go.Bar(x=etiquetas, 
                        y=porcentajes,
                        marker=dict(
                            color=diccColores[str(numCluster)],  
                            line=dict(color='black')  
                        ))] 
    estilosFiguraParam_0_1 = go.Layout(
        title=f"Porcentaje de la cantidad de personas con cáncer en los años 2010 a 2019 por cada {parametroVerda} \n \ten el estado de {estado}",
        xaxis=dict(title=parametroVerda),
        yaxis=dict(title="Porcentaje"),
        font=dict(
            family='Verdana',
            size=16,
            color='black'
        )
    )
    figuraParam_0_1 = go.Figure(data=dataBarraParam_0_1, layout=estilosFiguraParam_0_1)

    return figuraParam, figuraParam_0_1

if __name__ == '__main__':
    app.run_server()