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
        # Parte 1: Agrupa os dados pela coluna 'CRS' e soma as outras colunas para cada grupo
        soma_agrotoxicos = dados_consolid.groupby('CRS').sum().reset_index()
        
        # Seleciona as colunas de parâmetros a partir da oitava coluna
        parametros = soma_agrotoxicos.iloc[:, 8:]
        
        # Combina a coluna 'CRS' com as colunas de parâmetros selecionadas
        dados_tabela = pd.concat([dados_consolid['CRS'], parametros], axis=1)
        
        # Transforma o DataFrame em formato longo
        dados_tabela = dados_tabela.melt(id_vars=['CRS'], var_name='Parametro', value_name='Quantidade')
        
        # Converte a coluna 'CRS' para tipo de dado categórico
        dados_tabela['CRS'] = dados_tabela['CRS'].astype('category')
        
        # Cria o gráfico de barras com Plotly
        fig1 = px.bar(dados_tabela, x='CRS', y='Valor', color='Parametro', barmode='group', title='Soma dos Parâmetros por CRS')
        
        # Ajusta o layout para garantir que todos os rótulos sejam exibidos
        fig1.update_layout(
            xaxis={'categoryorder': 'total descending'},
            xaxis_tickangle=-45  # Ajusta o ângulo dos rótulos do eixo X para melhor legibilidade
        )
        
        # Parte 2: Somando as colunas de dados_consolid e filtrando a partir da oitava linha
        soma_agrotoxicos_total = dados_consolid.sum().reset_index().loc[8:].reset_index(drop=True)
        # Renomeando as colunas do DataFrame para 'Parametro' e 'Quantidade'
        soma_agrotoxicos_total.columns = ['Parametro', 'Quantidade']
        
        # Criando um gráfico de barras horizontal usando Plotly
        fig2 = px.bar(
            soma_agrotoxicos_total.sort_values(by='Quantidade'),  # Ordena os dados pelo valor de 'Quantidade'
            y='Parametro',  # Define 'Parametro' como o eixo Y
            x='Quantidade',  # Define 'Quantidade' como o eixo X
            orientation='h',  # Define a orientação do gráfico para horizontal
            text='Quantidade',  # Adiciona os valores de 'Quantidade' como texto nas barras
            title='Quantidade de agrotóxicos encontrada'  # Define o título do gráfico
        )
        
        # Configurar o layout do aplicativo Streamlit
        st.title('Análise de Agrotóxicos')
        
        # Exibir os gráficos no Streamlit
        st.plotly_chart(fig1)
        st.plotly_chart(fig2)
        # a partir daqui
        #soma_agrotoxicos = dados_consolid.sum().reset_index().loc[8:].reset_index(drop=True)
        #soma_agrotoxicos.columns = ['Parametro', 'Quantidade']

        #CRS = st.selectbox("Selecione a CRS", dados_consolid['CRS'].unique(), index=None, placeholder="Nenhuma CRS selecionada")
        #soro = st.selectbox('Soro Antiveneno', dados_geral[dados_geral['Animal']==animal]['soro'].unique(), index=None, placeholder="Selecione o Soro Antiveneno")
                
        #grafico_top_agrotoxico = px.bar(soma_agrotoxicos.sort_values(by='Quantidade'),
                 #y='Parametro', x='Quantidade', orientation='h',
                 #text='Quantidade', title = 'Quantidade de agrotóxicos encontrada')
                
        # Mostre o mapa no Streamlit
        #st.plotly_chart(grafico_top_agrotoxico)

