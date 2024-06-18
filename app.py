import pandas as pd
import geopandas as gpd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
import streamlit_js_eval
import requests
import folium
from streamlit_folium import st_folium, folium_static

# Carregar os dados
dados = pd.read_excel('https://docs.google.com/spreadsheets/d/e/2PACX-1vRR1E1xhXucgiQW8_cOOZ0BzBlMpfz6U9sUY9p1t8pyn3gu0NvWBYsMtCHGhJvXt2QYvCLM1rR7ZpAG/pub?output=xlsx')

# Filtrar as linhas com valores válidos de latitude e longitude
dados_filtrados = dados.dropna(subset=["Latitude", "Longitude"])

# Consolidar os dados
dados_consolid = pd.pivot_table(dados_filtrados, values='Detecção', index=['Latitude','Longitude', 'Municipio', 'Ponto de Coleta', 'CRS'], aggfunc=['sum', 'count']).reset_index()
dados_consolid.columns = ['Latitude', 'Longitude', 'Municipio', 'Ponto de Coleta', 'CRS', 'Detecções_Total', 'Detecções_Contagem']

# Crie o mapa
#mapa_folium = folium.Map(location=[dados_consolid["Latitude"].mean(), dados_consolid["Longitude"].mean()], zoom_start=5)

# Adicione marcadores
#for i, row in dados_consolid.iterrows():
#    folium.Marker([row["Latitude"], row["Longitude"]]).add_to(mapa_folium)

# Adicione camadas (opcional)
# Adicione uma camada de azulejos com diferentes estilos
#folium.TileLayer('Stamen Toner', attr='Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL.').add_to(mapa_folium)

# Mostre o mapa
#folium_static(mapa_folium)
# Configurar o token do Mapbox
token = 'pk.eyJ1IjoiYW5kcmUtamFyZW5rb3ciLCJhIjoiY2xkdzZ2eDdxMDRmMzN1bnV6MnlpNnNweSJ9.4_9fi6bcTxgy5mGaTmE4Pw'
px.set_mapbox_access_token(token)

# Crie o mapa
mapa_px = px.scatter_mapbox(
    data_frame = dados_consolid,
    lat="Latitude",
    lon="Longitude",
    title="Mapa de Pontos de Detecção de Agrotóxicos no RS",
    zoom=6,
    color = "sum",
    size = "count",
    height = 800,
    color_continuous_scale=px.colors.sequential.Sunsetdark,
    size_max=15,
    mapbox_style="open-street-map"
)

# Adicione uma legenda
mapa_px.update_layout(legend_title="Detecção de Agrotóxicos no RS")

# Mostre o mapa
mapa_px.show()
