import pandas as pd 
import geopandas as gpd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
import streamlit_js_eval
import requests
import folium
from streamlit_folium import st_folium, folium_static

# Configurações da página
st.set_page_config(
    page_title="Detecção de Agrotóxicos no Rio Grande do Sul",
    page_icon="	:skull:",
    layout="wide",
    initial_sidebar_state='collapsed'
)
col1, col2, col3 = st.columns([1,4,1])

col1.image('https://github.com/andrejarenkow/csv/blob/master/logo_cevs%20(2).png?raw=true', width=200)
col2.title('Detecção de Agrotóxicos no Rio Grande do Sul')
col3.image('https://github.com/andrejarenkow/csv/blob/master/logo_estado%20(3)%20(1).png?raw=true', width=300)

# Carregar os dados
dados = pd.read_excel('https://docs.google.com/spreadsheets/d/e/2PACX-1vRR1E1xhXucgiQW8_cOOZ0BzBlMpfz6U9sUY9p1t8pyn3gu0NvWBYsMtCHGhJvXt2QYvCLM1rR7ZpAG/pub?output=xlsx')

# Filtrar as linhas com valores válidos de latitude e longitude
dados_filtrados = dados.dropna(subset=["Latitude", "Longitude"])
dados_filtrados['Parametros detectados'].fillna('Verificando', inplace=True)

dados_consolid = pd.pivot_table(dados_filtrados, values='Detecção', index=['Latitude','Longitude', 'Municipio', 'Ponto de Coleta', 'CRS', 'Parametros detectados'], aggfunc=['sum', 'count']).reset_index()
dados_consolid.columns = ['Latitude', 'Longitude', 'Municipio', 'Ponto de Coleta', 'CRS','Parametros detectados', 'Detecções_Total', 'Detecções_Contagem', ]

def processar_parametros(parametros):
    for parametro in parametros.split(','):
        # Remover vírgulas
        parametro_formatado = parametro.replace(',', '')
        # Criar a coluna para o parâmetro
        dados_consolid[f'{parametro_formatado}'] = dados_consolid['Parametros detectados'].map(lambda p: 
                                                                                                   any(parametro_formatado == parametro_atual for parametro_atual in p.split(',')))

dados_consolid['Parametros detectados'].apply(processar_parametros)

col5, col4 = st.columns([3, 4]) 
    
with col4:  
        # Configurar o token do Mapbox
        token = 'pk.eyJ1IjoiYW5kcmUtamFyZW5rb3ciLCJhIjoiY2xkdzZ2eDdxMDRmMzN1bnV6MnlpNnNweSJ9.4_9fi6bcTxgy5mGaTmE4Pw'
        px.set_mapbox_access_token(token)

    # Definindo o centro do mapa
        center_lat = -30  # Latitude central aproximada do Rio Grande do Sul
        center_lon = -53  # Longitude central aproximada do Rio Grande do Sul
           
        # Crie o mapa
        mapa_px = px.scatter_mapbox(
            data_frame=dados_consolid,
            lat="Latitude",
            lon="Longitude",
            title="Mapa de Pontos de Detecção de Agrotóxicos no RS",
            zoom=4,
            hover_data="Municipio",  # Use a coluna correta
            size="Detecções_Contagem",  # Use a coluna correta
            height=800,
            color_continuous_scale=px.colors.sequential.Sunsetdark,
            size_max=15,
            mapbox_style="open-street-map"
        )
        
        # Adicione uma legenda
        mapa_px.update_layout(
            legend_title="Detecção de Agrotóxicos no RS",
            mapbox=dict(
                center={"lat": center_lat, "lon": center_lon},  # Reforçando a centralização
                zoom=6
            )
        )
        # Mostre o mapa no Streamlit
        st.plotly_chart(mapa_px)

with col5:                 
        soma_agrotoxicos = dados_consolid.sum().reset_index().loc[8:].reset_index(drop=True)
        soma_agrotoxicos.columns = ['Parametro', 'Quantidade']
            
        grafico_top_agrotoxico = px.bar(soma_agrotoxicos.sort_values(by='Quantidade'),
                y='Parametro', x='Quantidade', orientation='h',
                text='Quantidade', title = 'Quantidade de agrotóxicos encontrada')
            
        # Mostre o mapa no Streamlit
        st.plotly_chart(grafico_top_agrotoxico)

