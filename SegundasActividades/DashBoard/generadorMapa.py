# import plotly.graph_objects as go

# fig = go.Figure(go.Scattergeo())
# fig.update_geos(
#     visible=False, resolution=110, scope="usa",
#     showcountries=True, countrycolor="Black",
#     showsubunits=True, subunitcolor="Blue"
# )

# fig.update_layout(height=300, margin={"r":0,"t":0,"l":0,"b":0})

# fig.show()


import plotly.graph_objects as go
import json

# Cargar el archivo GeoJSON
with open('mexico2.geojson', 'r') as f:
    mexico_geojson = json.load(f)

# Crear el objeto figura de Plotly
fig = go.Figure()

# Agregar las capas de las entidades federativas (estados) de México al mapa
for feature in mexico_geojson['features']:
    geo_layer = feature['geometry']
    if geo_layer['type'] == 'Polygon':
        xs, ys = zip(*geo_layer['coordinates'][0])
        fig.add_trace(go.Scattergeo(
            lon=xs,
            lat=ys,
            mode='lines',
            line=dict(color='black', width=1),
            name=feature['properties']['name']
        ))
    elif geo_layer['type'] == 'MultiPolygon':
        for coords in geo_layer['coordinates']:
            xs, ys = zip(*coords[0])
            fig.add_trace(go.Scattergeo(
                lon=xs,
                lat=ys,
                mode='lines',
                line=dict(color='black', width=1),
                name=feature['properties']['name']
            ))

# Establecer el diseño del mapa
fig.update_geos(projection_type="mercator", 
                showcountries=True, 
                landcolor="rgb(217, 217, 217)", 
                showocean=True, 
                oceancolor="rgb(204, 204, 255)",
                center=dict(lon=-102, lat=23.6345),
                projection_scale=8.5)

# # Establecer el diseño del mapa completo
fig.update_layout(
    title_text='Mapa de México',
    showlegend=False
#     geo=dict(
#         scope='north america',
#         projection_type='mercator',
#         showland=True,
#         landcolor='rgb(217, 217, 217)',
#         showcountries=True,
#         showocean=True,
#         oceancolor="rgb(204, 204, 255)",
#         showcoastlines=True,
#         showframe=False,
#         coastlinewidth=1,
#         countrylinewidth=1,
#     )
)

# Mostrar el mapa
fig.show()

