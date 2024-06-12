import dash
from dash import dcc
from dash import html
import json
import plotly.graph_objects as go
import dashBoards.accesoDb as db
import dashBoards.funcionesAuxiliares as funcAux
from dash.dependencies import Input, Output



def generadorDeMapas(clustersEstadoParametroX, dictColoresMapaEstadoParametroX):
    estados = []
    grupos = [] # Para que solo un estado por grupo se agregue a la leyenda
    longitudesCentrales = []
    latitudesCentrales = []
    nombresEstados = []

    # Nombre resumido de los 32 estados
    nombresEstados = ['Ags.', 'BC', 'BCS', 'Camp.', 'Coah.', 'Col.', 'Chis.', 'Chih.', 'CDMX', 'Dgo.', 'Gto.', 'Gro.', 'Hgo.', 'Jal.', 'Mor.', 'Mich.', 'Edo. Méx.', 'Nay.', 'NL', 'Oax.', 'Pue.', 'Qro.', 'QR', 'SLP', 'Sin.', 'Son.', 'Tab.', 'Tamps.', 'Tlax.', 'Ver.', 'Yuc.', 'Zac.']

    # Lee el archivo GeoJSON
    with open('dashBoards/mexico.geojson', encoding='utf-8') as f:
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
                marker=dict(size=20, opacity=1)
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
                marker=dict(size=20, opacity=1),
                showlegend=False
            ))
        
        # Almacenar el centro de cada region
        # nombresEstados.append(entidad)
        longitudesCentrales.append(sum(longitudes) / len(longitudes))
        latitudesCentrales.append(sum(latitudes) / len(latitudes))

    for i in range(32):
        # Agrega la etiqueta de texto sobre el área geográfica
        estados.append(go.Scattergeo(
            locationmode = 'country names',
            lon = [longitudesCentrales[i]],
            lat = [latitudesCentrales[i]],
            mode = 'text',
            text = nombresEstados[i],
            showlegend=False,
            hoverinfo='skip',  # Desactiva el cuadro de texto al pasar el cursor
            textfont=dict(size=13, family="Verdana Bold")
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
        # width=1320,  # ajusta el ancho de la figura
        height=470,   # ajusta el alto de la figura
    )

    return fig


# Función para insertar un salto de línea
def insertar_salto_de_linea(lista_de_cadenas):
    lista_modificada = []

    for cadena in lista_de_cadenas:
        if len(cadena) > 30:
            punto_medio = len(cadena) // 2
            cadena_modificada = cadena[:punto_medio] + "<br>" + cadena[punto_medio:]
            lista_modificada.append(cadena_modificada)
        else:
            lista_modificada.append(cadena)
    
    return lista_modificada


def generadorGraficos(parametroVerda, numeroId, diccColores):
    # Consultar los datos que permiten la creacion de los graficos referentes al parametro seleccionado
    estado, numCluster, etiquetasParam, cantidadesParam, porcentajesParam = db.consultaBarras(parametroVerda, numeroId)

    # Consultar los datos que permiten la creacion de los graficos referentes a los tipos de cáncer
    estado, _, etiquetasCancer, cantidadesCancer, porcentajesCancer = db.consultaBarras('Tipo de Cancer', numeroId)

    # Aplicar la función a cada etiqueta en la lista etiquetasParam
    etiquetasParam = insertar_salto_de_linea(etiquetasParam)
    alturaFiguras = 780

    # Crear la grafica de barras para el parametro seleccionado (forma cruda)
    dataBarraParam = [go.Bar(x=etiquetasParam, 
                        y=cantidadesParam,
                        marker=dict(
                            color=diccColores[str(numCluster)],  
                            line=dict(color='black')  
                        ))] 
    estilosFiguraParam = go.Layout(
        title=f"""         Cantidad de personas con cáncer en los años 2010 a 2019 por cada 
                <br>       {parametroVerda} en el estado de {estado}""",
        xaxis=dict(title=parametroVerda,
                    showgrid=True,  
                    gridcolor='lightgray', 
                    gridwidth=1,
                    tickangle=-45  
        ),
        yaxis=dict(title="Cantidad",
                    showgrid=True,  
                    gridcolor='lightgray', 
                    gridwidth=1,
        ),
        font=dict(
            family='Verdana',
            size=16,
            color='black'
        ),
        height=alturaFiguras 
    )
    figuraParam = go.Figure(data=dataBarraParam, layout=estilosFiguraParam)

    # Crear la grafica de barras para los tipos de cancer (forma cruda)
    dataBarraCancer = [go.Bar(x=etiquetasCancer, 
                        y=cantidadesCancer,
                        marker=dict(
                            color=diccColores[str(numCluster)],  
                            line=dict(color='black')  
                        ))] 
    estilosFiguraCancer = go.Layout(
        title=f"""Cantidad de personas con cáncer en los años 2010 a 2019 por cada 
                <br>       Tipo de Cáncer en el estado de {estado}""",
        xaxis=dict(title='Tipos de Cáncer',
                    showgrid=True,  
                    gridcolor='lightgray', 
                    gridwidth=1,
                    tickangle=-45 
        ),
        yaxis=dict(title="Cantidad",
                    showgrid=True,  
                    gridcolor='lightgray', 
                    gridwidth=1  
        ),
        font=dict(
            family='Verdana',
            size=16,
            color='black'
        ),
        height=alturaFiguras 
    )
    figuraCancer = go.Figure(data=dataBarraCancer, layout=estilosFiguraCancer)

    # Crear la grafica de barras para el parametro seleccionado (forma porcentual)
    if parametroVerda == 'Nivel Educativo':
        increParam = 0.025
        maxiParam = 0.36
    else:
        increParam = 0.025
        maxiParam = 0.63
    yticksValores = [i*increParam for i in range(0, int(maxiParam/increParam)+1)]
    yticksTexto = [str(round(i, 3)) for i in yticksValores]

    dataBarraParam_0_1 = [go.Bar(x=etiquetasParam, 
                        y=porcentajesParam,
                        marker=dict(
                            color=diccColores[str(numCluster)],  
                            line=dict(color='black')  
                        ))] 
    estilosFiguraParam_0_1 = go.Layout(
        title=f"""Porcentaje de la cantidad de personas con cáncer en los años 2010 a 2019 
                <br>    por cada {parametroVerda} en el estado de {estado}""",
        xaxis=dict(title=parametroVerda,
                    showgrid=True,  
                    gridcolor='lightgray', 
                    gridwidth=2,
                    tickangle=-45
        ),
        yaxis=dict(title="Porcentaje",
                    showgrid=True,  
                    gridcolor='lightgray', 
                    gridwidth=2,
                    tickvals=yticksValores,  
                    ticktext=yticksTexto,
                    range=[0, maxiParam] 
        ),
        font=dict(
            family='Verdana',
            size=16,
            color='black'
        ),
        height=alturaFiguras 
    )
    figuraParam_0_1 = go.Figure(data=dataBarraParam_0_1, layout=estilosFiguraParam_0_1)

    # Crear la grafica de barras para los tipo de cancer (forma porcentual)
    increCancer = 0.01
    maxiCancer = 0.16
    yticksValores = [i*increCancer for i in range(0, int(maxiCancer/increCancer)+1)]
    yticksTexto = [str(round(i, 3)) for i in yticksValores]

    dataBarraCancer_0_1 = [go.Bar(x=etiquetasCancer, 
                        y=porcentajesCancer,
                        marker=dict(
                            color=diccColores[str(numCluster)],  
                            line=dict(color='black')  
                        ))] 
    estilosFiguraCancer_0_1 = go.Layout(
        title=f"""Porcentaje de la cantidad de personas con cáncer en los años 2010 a 2019 
                <br>    por cada Tipo de Cáncer en el estado de {estado}""",
        xaxis=dict(title='Tipo de Cáncer',
                    showgrid=True,  
                    gridcolor='lightgray', 
                    gridwidth=2,
                    tickangle=-45
        ),
        yaxis=dict(title="Porcentaje",
                    showgrid=True,  
                    gridcolor='lightgray', 
                    gridwidth=2,  
                    tickvals=yticksValores,  
                    ticktext=yticksTexto,
                    range=[0, maxiCancer] 
        ),
        font=dict(
            family='Verdana',
            size=16,
            color='black'
        ),
        height=alturaFiguras 
    )
    figuraCancer_0_1 = go.Figure(data=dataBarraCancer_0_1, layout=estilosFiguraCancer_0_1)

    return figuraParam, figuraCancer, figuraParam_0_1, figuraCancer_0_1


def generadorTotal(numeroId):
    estado, total = db.consultaTotal(numeroId)
    totalString = f'En los años 2010 a 2019 en {estado} se registrarón un total de {total:,} personas con algun tipo de cáncer'

    return totalString


# app = dash.Dash()

def crearDashApp(flask_app):
    app = dash.Dash(__name__, server=flask_app, url_base_pathname='/dash/')

    # MAPA QUE SE MOSTRARA POR DEFECTO
    # Genera la figura
    mapaDefecto = go.Figure(data=generadorDeMapas(db.extraerClustersEstadoEducacion(), funcAux.coloresEducacion))
    # Aplicar estilos
    mapaDefecto = aplicarEstilosMapa(mapaDefecto, 'Estados de México')

    # CANTIDAD TOTAL QUE SE MOSTRARA POR DEFECTO
    totalString = generadorTotal(1)

    # GRAFICOS QUE SE MOSTRARAN POR DEFECTO
    # Graficos crudos y porcentuales
    figuraParam, figuraCancer, figuraParam_0_1, figuraCancer_0_1 = generadorGraficos('Nivel Educativo', 1, funcAux.coloresEducacion)

    # Para extraer el nombre de todos las entidades federativas
    nombresEstados = db.consultaEstados()

    # LAYOUT
    app.layout = html.Div([
        html.Section(
            id='global',
            children=[
                html.Header(
                    children=[
                        # IMAGENES
                        html.Div(
                            id='content-logos',
                            children=[
                                html.Span(className='flotador', id='renglon1', children="d "),
                                html.Span(className='flotador', id='separadorImg1', children="d "),
                                html.Img(className='flotador', id='imgHeaderPol', src='/static/img/ipnLogo.png'),
                                html.Span(className='flotador', id='separadorEntreImg', children="d "),
                                html.Img(className='flotador', id='imgHeaderUpiita', src='https://www.upiita.ipn.mx/images/logo_upiita_ipn_varios_colores_logo_upiita_oro.png', alt='imagen'),
                                html.Div(className='limpiador')
                            ]
                        ),

                        # TITULO
                        html.Div(
                            id='content-titulo',
                            className='color',
                            children=[
                                html.H1('Impacto de variables sociodemográficas en cáncer usando técnicas de Ciencia de Datos')
                            ]
                        ),

                        # MENU
                        html.Nav(
                            id='menu',
                            children=[
                                html.Ul(
                                    children=[
                                        html.Li(html.A('Inicio', href='/inicio')),
                                        html.Li(html.A('Correlación', href='/correlacion')),
                                        html.Li(html.A('Características', href='/caracteristicasGrupos')),
                                        html.Li(html.A('Aplicación', href='/dash'))
                                    ]
                                )
                            ]
                        )
                    ]
                ),

                # APLICACION
                # Contenedor de los dropdowns
                html.Div(
                    id="content-controles",
                    children=[
                        # Parametro y su respectivo dropdown
                        html.Div(
                            id="contenedor",
                            children=[
                                html.Div(
                                    [
                                        html.H4("Seleccione una opción:", className="hijo")
                                    ],
                                    className="padre flotador2 textosControles",
                                    id="textoControl-par"
                                ),
                                dcc.Dropdown(id='parametro', 
                                        className="flotador2 drop-par",
                                        options=['Nivel Educativo y Cáncer', 'Categoría de Empleo y Cáncer'], 
                                        value='Nivel Educativo y Cáncer',
                                        clearable=False
                                )
                            ]
                        ),

                        # Estado y su respectivo dropdown
                        html.Div(
                            id="contenedor2",
                            children=[
                                html.Div(
                                    [
                                        html.H4("Estado:", className="hijo")
                                    ],
                                    className="padre flotador2 textosControles",
                                    id="textoControl-state"
                                ),
                                dcc.Dropdown(
                                    id='dropEstado',
                                    options=nombresEstados,
                                    value=nombresEstados[0],
                                    className="flotador2 drop-state",
                                    clearable=False
                                )
                        ]),

                        html.Div(className="limpiador")
                    ]
                ),

                # MAPA
                dcc.Graph(
                    id='mapa',
                    figure=mapaDefecto
                ),
                # html.Div([
                #     html.Pre(id='informacionClick')
                # ]),
                html.Div([
                    html.Pre(id='prueba')
                ]),

                # TOTAL DE PERSONAS CON CANCER
                html.H1(
                    id='totalEstado',
                    children=totalString
                ),

                # GRAFICOS CRUDOS
                dcc.Graph(
                    id='barraParametro',
                    figure=figuraParam
                ),
                dcc.Graph(
                    id='barraCancer',
                    figure=figuraCancer
                ),

                # GRAFICOS PORCENTUALES
                html.H2(
                    id="tituloPorcenData",
                    children=' - Representacion porcentual de los datos - '
                ),
                dcc.Graph(
                    id='barraParametro_0_1',
                    figure=figuraParam_0_1
                ),
                dcc.Graph(
                    id='barraCancer_0_1',
                    figure=figuraCancer_0_1
                ),
            ]
        ),

        html.Div(
            id="footerId",
            children="Derechos Reservados por Alejandro Granados ©"
        )
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
            titulo = 'Estados de México'
            indicesClustersX = db.extraerClustersEstadoEducacion()
            coloresMapa = funcAux.coloresEducacion 
        else:
            titulo = 'Estados de México'
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
    # @app.callback(
    #     [Output('barraParametro', 'figure'), Output('barraCancer', 'figure'), Output('barraParametro_0_1', 'figure'), Output('barraCancer_0_1', 'figure')],
    #     [Input('parametro', 'value'), Input('mapa', 'clickData')]
    # )
    # def actualizarBarra(parametro, informacion):
    #     # Seleccionar el diccionario de colores que le toque segun el parametro
    #     diccColores = None
    #     parametroVerda = None
    #     if parametro == 'Nivel Educativo y Cáncer':
    #         diccColores = funcAux.coloresEducacion
    #         parametroVerda = 'Nivel Educativo'
    #     else:
    #         diccColores = funcAux.coloresOcupacion
    #         parametroVerda = 'Categoria de Empleo'

    #     # De la informacion del click, extraer el id del pais
    #     numeroId = informacion['points'][0]['curveNumber'] + 1 # El +1 porque el primer estado es 0 pero en la db es 1
    #     numeroId = funcAux.corregirIndice(numeroId) # Corregir indice

    #     return generadorGraficos(parametroVerda, numeroId, diccColores)


    # ACTUALIZADOR DE CANTIDAD TOTAL
    # Cambia cantidad total de personas con cancer dependientemente del estado que se seleccione en el mapa
    # @app.callback(
    #     Output('totalEstado', 'children'),
    #     Input('mapa', 'clickData')
    # )
    # def cantidadTotal(informacion):
    #     # De la informacion del click, extraer el id del pais
    #     numeroId = informacion['points'][0]['curveNumber'] + 1 # El +1 porque el primer estado es 0 pero en la db es 1
    #     numeroId = funcAux.corregirIndice(numeroId) # Corregir indice

    #     # Almacenar total
    #     totalString = generadorTotal(numeroId)
        
    #     return totalString
    

    # EVENTOS PARA LA VERSION 2 (CON DROPDOWN ESTADO) ---------------------------------------------------

    # ACTUALIZADOR DE BARRA (VERSION 2)
    # Cambia las graficas de barras dependientemenete del estado que se seleccione en el drop down
    # y el parametro que se seleccione en el drop down
    @app.callback(
        [Output('barraParametro', 'figure'), Output('barraCancer', 'figure'), Output('barraParametro_0_1', 'figure'), Output('barraCancer_0_1', 'figure')],
        [Input('parametro', 'value'), Input('dropEstado', 'value')]
    )
    def actualizarBarraVersion2(parametro, nombreEstado):
        # Seleccionar el diccionario de colores que le toque segun el parametro
        diccColores = None
        parametroVerda = None
        if parametro == 'Nivel Educativo y Cáncer':
            diccColores = funcAux.coloresEducacion
            parametroVerda = 'Nivel Educativo'
        else:
            diccColores = funcAux.coloresOcupacion
            parametroVerda = 'Categoria de Empleo'

        # Del estado que se seleccione en el dropDown, extraer el id del pais
        numeroId = db.buscarIdEstado(nombreEstado) 

        return  generadorGraficos(parametroVerda, numeroId, diccColores)
    

    # ACTUALIZADOR DE CANTIDAD TOTAL (VERSION 2)
    # Cambia cantidad total de personas con cancer dependientemente del estado que se seleccione 
    # en el dropDown estado
    @app.callback(
        Output('totalEstado', 'children'),
        Input('dropEstado', 'value')
    )
    def cantidadTotalVersion2(nombreEstado):
        # Del estado que se seleccione en el dropDown, extraer el id del pais
        numeroId = db.buscarIdEstado(nombreEstado) 

        # Almacenar total
        totalString = generadorTotal(numeroId)
        
        return totalString
    

    # ACTUALIZADOR DE BARRA (VERSION 1)
    # Cambia las graficas de barras dependientemenete del estado que se seleccione en el mapa
    @app.callback(
        Output('dropEstado', 'value'),
        Input('mapa', 'clickData')
    )
    def actualizarBarra(informacion):
        # De la informacion del click, extraer el id del pais
        numeroId = informacion['points'][0]['curveNumber'] + 1 # El +1 porque el primer estado es 0 pero en la db es 1
        numeroId = funcAux.corregirIndice(numeroId) # Corregir indice

        return db.buscarNombreEstado(numeroId)

    return app


   