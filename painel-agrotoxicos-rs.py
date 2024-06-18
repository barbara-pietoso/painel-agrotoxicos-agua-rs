import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.express as px
import folium

# Carregar os dados
dados = pd.read_excel('https://docs.google.com/spreadsheets/d/e/2PACX-1vRR1E1xhXucgiQW8_cOOZ0BzBlMpfz6U9sUY9p1t8pyn3gu0NvWBYsMtCHGhJvXt2QYvCLM1rR7ZpAG/pub?output=xlsx')

# Filtrar as linhas com valores válidos de latitude e longitude
dados_filtrados = dados.dropna(subset=["Latitude", "Longitude"])

# Consolidar os dados
dados_consolid = pd.pivot_table(dados_filtrados, values='Detecção', index=['Latitude','Longitude', 'Municipio', 'Ponto de Coleta', 'CRS'], aggfunc=['sum', 'count']).reset_index()
dados_consolid.columns = ['Latitude', 'Longitude', 'Municipio', 'Ponto de Coleta', 'CRS', 'Detecções_Total', 'Detecções_Contagem']

# Configurar o token do Mapbox
px.set_mapbox_access_token('pk.eyJ1IjoiYW5kcmUtamFyZW5rb3ciLCJhIjoiY2xkdzZ2eDdxMDRmMzN1bnV6MnlpNnNweSJ9.4_9fi6bcTxgy5mGaTmE4Pw')

# Crie o mapa
mapa_px = px.scatter_mapbox(
    data_frame=dados_consolid,
    lat="Latitude",
    lon="Longitude",
    title="Mapa de Pontos de Detecção de Agrotóxicos no RS",
    zoom=6,
    color="Detecções_Total",
    size="Detecções_Contagem",
    height=800,
    color_continuous_scale=px.colors.sequential.Sunsetdark,
    size_max=15,
    mapbox_style="open-street-map"
)

# Adicione uma legenda
mapa_px.update_layout(legend_title="Detecção de Agrotóxicos no RS")

# Mostre o mapa no Streamlit
st.plotly_chart(mapa_px)
