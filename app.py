import pandas as pd 
import geopandas as gpd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
import streamlit_js_eval
import requests
import folium
from streamlit_folium import st_folium, folium_static
import altair as alt

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
lista_crs_selectbox = sorted(dados['CRS'].unique())
lista_crs_selectbox.insert(0,'Todas')
CRS = st.selectbox("Selecione a CRS", lista_crs_selectbox, index=0, placeholder="Nenhuma CRS selecionada")
if CRS != 'Todas':
    dados = dados[dados['CRS']==CRS]

# Filtrando apenas com detecção
dados_detec = dados[dados['Detecção']>0].reset_index(drop=True)

# Filtrar as linhas com valores válidos de latitude e longitude
dados_filtrados = dados_detec.dropna(subset=["Latitude", "Longitude"])
dados_filtrados['Parametros detectados'].fillna('Verificando', inplace=True)

dados_consolid = pd.pivot_table(dados_filtrados, values='Detecção', index=['Latitude','Longitude', 'Municipio', 'Ponto de Coleta',
                                                                           'CRS', 'Parametros detectados'], aggfunc=['sum', 'count']).reset_index()

try:
    dados_consolid.columns = ['Latitude', 'Longitude', 'Municipio', 'Ponto de Coleta', 'CRS','Parametros detectados', 'Detecções_Total', 'Detecções_Contagem', ]
except:
    dados_consolid.columns = ['Latitude', 'Longitude', 'Municipio', 'Ponto de Coleta', 'CRS','Parametros detectados']

def processar_parametros(parametros):
    for parametro in parametros.split(','):
        # Remover vírgulas
        parametro_formatado = parametro.replace(',', '')
        # Criar a coluna para o parâmetro
        dados_consolid[f'{parametro_formatado}'] = dados_consolid['Parametros detectados'].map(lambda p: 
                                                                                                   any(parametro_formatado == parametro_atual for parametro_atual in p.split(',')))

dados_consolid['Parametros detectados'].apply(processar_parametros)

dados_consolid['Parametros detectados'].apply(processar_parametros)

# Adicionando métricas
col6, col7, col8, col9 = st.columns(4)

# Quantas amostras já foram coletadas
#total_amostras = len(dados_consolid)
#col6.metric("Total de Amostras Coletadas", count)

# Quantas detecções
total_deteccoes = len(dados_consolid)
col7.metric("Total de Detecções", Detecções_Total)

# Quantos municípios com detecção
#municipios_com_detec = dados_detec['Municipio'].nunique()
#col8.metric("Municípios com Detecção", municipios_com_detec)

# Quantos municípios houve coleta
#municipios_com_coleta = dados['Municipio'].nunique()
#col9.metric("Municípios com Coleta", municipios_com_coleta)

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
            color_discrete_sequence=["#f2a744"],
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


        # Supondo que 'dados_filtrados' já esteja carregado
        dados['Data da coleta'] = pd.to_datetime(dados['Data da coleta'])
        
        # Extraindo o mês das datas
        dados['Mes'] = dados['Data da coleta'].dt.month
        
        # Calcular a porcentagem de detecções > 0 por mês
        detec_perc_mes = (dados[dados['Detecção'] > 0].groupby('Mes').size() / dados.groupby('Mes').size() * 100).fillna(0)
        
        #display(detec_perc_mes.fillna(0))
        
        # Formatando os valores para exibição no gráfico
        detec_perc_mes_text = detec_perc_mes.apply(lambda x: f'{x:.1f}%')
        detec_perc_mes_total = (dados.groupby('Mes').size()).fillna(0)
        
       # Criar o gráfico de colunas para o total de detecções
        bar_trace = go.Bar(
            x=detec_perc_mes_total.index,
            y=detec_perc_mes_total,
            name='Total de Detecções',
            yaxis='y2',
            marker_color='#01133b',
            opacity=0.3,
            marker_line_width=1.5
        )
        
        # Criar o gráfico de linhas para a porcentagem de detecções
        line_trace = go.Scatter(
            x=detec_perc_mes.index,
            y=detec_perc_mes,
            mode='lines+markers+text',
            text=detec_perc_mes_text,
            name='Percentual de Detecção',
            line=dict(color='orange')
        )
        
        # Combinar os gráficos
        grafico_deteccoes_mensal = go.Figure(
            layout=dict( barcornerradius=15) 
        )
        grafico_deteccoes_mensal.add_trace(bar_trace)
        grafico_deteccoes_mensal.add_trace(line_trace)
        
        # Ajustar os rótulos dos meses
        grafico_deteccoes_mensal.update_layout(
            title='Percentual de Detecção por Mês',
            xaxis=dict(
                tickmode='array',
                tickvals=list(range(1, 13)),
                ticktext=['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
            ),
            yaxis=dict(
                title='Percentual de Detecção',
                #titlefont=dict(color='blue'),
                #tickfont=dict(color='blue')
            ),
            yaxis2=dict(
                title='Total de Detecções',
                #titlefont=dict(color='orange'),
                #tickfont=dict(color='orange'),
                overlaying='y',
                side='right'
            ),
            legend=dict(x=0.4, y=1.2, bgcolor='rgba(255, 255, 255, 0)')
        )

    
        # Mostrar o gráfico
        st.plotly_chart(grafico_deteccoes_mensal)

        soma_agrotoxicos = dados_filtrados['Parametros detectados'].str.get_dummies(sep=',').sum().sort_values(ascending=True).reset_index()
        soma_agrotoxicos.columns = ['Parametro', 'Quantidade']

                        
        grafico_top_agrotoxico = px.bar(soma_agrotoxicos.sort_values(by='Quantidade'),
                 x='Parametro', y='Quantidade', orientation='v', height=350, 
                 text='Quantidade', title = 'Quantidade de agrotóxicos encontrada', color_discrete_sequence=['#f2a744'])  # Azul muito escuro
                
        # Mostre o mapa no Streamlit
        st.plotly_chart(grafico_top_agrotoxico)
