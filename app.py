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

# Filtrando apenas com detecção
dados_detec = dados[dados['Detecção']>0].reset_index(drop=True)

# Filtrar as linhas com valores válidos de latitude e longitude
dados_filtrados = dados_detec.dropna(subset=["Latitude", "Longitude"])
 
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

col5, col4 = st.columns([4, 4]) 
    
with col4:  
        # Configurar o token do Mapbox
        token = 'pk.eyJ1IjoiYW5kcmUtamFyZW5rb3ciLCJhIjoiY2xkdzZ2eDdxMDRmMzN1bnV6MnlpNnNweSJ9.4_9fi6bcTxgy5mGaTmE4Pw'
        px.set_mapbox_access_token(token)

    # Definindo o centro do mapa
        center_lat = -30.5  # Latitude central aproximada do Rio Grande do Sul
        center_lon = -53  # Longitude central aproximada do Rio Grande do Sul
           
        # Crie o mapa
        mapa_px = px.scatter_mapbox(
            data_frame=dados_consolid,
            lat="Latitude",
            lon="Longitude",
            title="Mapa de Pontos de Detecção de Agrotóxicos no RS",
            zoom=6,
            hover_data="Municipio",  # Use a coluna correta
            size="Detecções_Contagem",  # Use a coluna correta
            height=800,
            width=800,
            color_continuous_scale=px.colors.sequential.Sunsetdark,
            size_max=15, #tamanho maximo dos pontos
            mapbox_style="open-street-map"
        )
        
        # Adicione uma legenda
        mapa_px.update_layout(
            legend_title="Detecção de Agrotóxicos no RS",
            mapbox=dict(
                center={"lat": center_lat, "lon": center_lon},  # Reforçando a centralização
                zoom=5.7
            )
        )
        # Mostre o mapa no Streamlit
        st.plotly_chart(mapa_px)

with col5:        
        soma_agrotoxicos = dados_filtrados['Parametros detectados'].str.get_dummies(sep=',').sum().sort_values(ascending=False).reset_index()
        soma_agrotoxicos.columns = ['Parametro', 'Quantidade']

        CRS = st.selectbox("Selecione a CRS", dados_filtrados['CRS'].unique(), index=None, placeholder="Nenhuma CRS selecionada")
    #soro = st.selectbox('Soro Antiveneno', dados_geral[dados_geral['Animal']==animal]['soro'].unique(), index=None, placeholder="Selecione o Soro Antiveneno")
                
        grafico_top_agrotoxico = px.bar(soma_agrotoxicos.sort_values(by='Quantidade'),
                 y='Parametro', x='Quantidade', orientation='h', height=700,
                 text='Quantidade', title = 'Quantidade de agrotóxicos encontrada', )
                
        # Mostre o mapa no Streamlit
        st.plotly_chart(grafico_top_agrotoxico)

        # Supondo que seu dataframe seja chamado 'dados_filtrados' e que a coluna de data seja 'Data da coleta'
        # Convertendo a coluna 'Data da coleta' para datetime
        dados_filtrados = dados_filtrados.reset_index(drop=True)
        dados_filtrados['Data da coleta'] = pd.to_datetime(dados_filtrados['Data da coleta'])
        
        # Extraindo ano e mês
        dados_filtrados['Ano'] = dados_filtrados['Data da coleta'].dt.year
        dados_filtrados['Mês'] = dados_filtrados['Data da coleta'].dt.month
        
        # Agrupando os dados por ano e mês, e calculando alguma métrica (por exemplo, a média de outra coluna 'valor')
        # Aqui vou assumir que temos uma coluna 'valor' que queremos plotar
        dados_agrupados = dados_filtrados.groupby(['Ano', 'Mês'])['Detecção'].sum().reset_index()
        
        # Criando o gráfico de linhas
        grafico_tempo = px.line(dados_agrupados, x='Mês', y='Detecção', markers = True, labels={
            'Mês': 'Mês',
            'Detecção': 'Detecção',
            'Ano': 'Ano'
        }, title='Linha do Tempo com Dados Agrupados por Ano e Mês')
        
        st.plotly_chart(grafico_tempo)

