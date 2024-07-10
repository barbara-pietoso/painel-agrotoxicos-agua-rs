import pandas as pd 
import geopandas as gpd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
import requests
import folium
from streamlit_folium import st_folium, folium_static
import altair as alt
from unidecode import unidecode
import textwrap
import extra_streamlit_components as stx

# Configurações da página
st.set_page_config(
    page_title="Detecção de Agrotóxicos no Rio Grande do Sul",
    page_icon="	:skull:",
    layout="wide",
    initial_sidebar_state='collapsed'
)

col1, col2, col3 = st.columns([2,5,1], vertical_alignment="center")

col3.image('https://github.com/andrejarenkow/csv/blob/master/logo_cevs%20(2).png?raw=true', width=200)
col2.title('Detecção de Agrotóxicos no Rio Grande do Sul')
col1.image('https://github.com/andrejarenkow/csv/blob/master/logo_estado%20(3)%20(1).png?raw=true', width=300)

#Dicionario CRS
substituicoes_crs = {
    1: "01ª CRS", 
    2: "02ª CRS", 
    3: "03ª CRS", 
    4: "04ª CRS", 
    5: "05ª CRS", 
    6: "06ª CRS", 
    7: "07ª CRS", 
    8: "08ª CRS", 
    9: "09ª CRS", 
    10: "10ª CRS", 
    11: "11ª CRS", 
    12: "12ª CRS", 
    13: "13ª CRS", 
    14: "14ª CRS", 
    15: "15ª CRS", 
    16: "16ª CRS", 
    17: "17ª CRS", 
    18: "18ª CRS"
}
# Adicionando métricas
col10, col6, col7, col8, col9 = st.columns([2,1,1,1,1])

# Carregar dados de referencias
# Planilha com referencias de municipios
dados_municipios = pd.read_csv('https://raw.githubusercontent.com/andrejarenkow/csv/master/Munic%C3%ADpios%20RS%20IBGE6%20Popula%C3%A7%C3%A3o%20CRS%20Regional%20-%20P%C3%A1gina1.csv')
dados_municipios['Município'] = dados_municipios['Município'].apply(lambda x: unidecode(x).upper())
dados_municipios['Município'] = dados_municipios['Município'].replace("SANT'ANA DO LIVRAMENTO", 'SANTANA DO LIVRAMENTO', regex=True)
dados_municipios['CRS'] = dados_municipios['CRS'].replace(substituicoes_crs)

# Carregar os dados
dados = pd.read_excel('https://docs.google.com/spreadsheets/d/e/2PACX-1vRR1E1xhXucgiQW8_cOOZ0BzBlMpfz6U9sUY9p1t8pyn3gu0NvWBYsMtCHGhJvXt2QYvCLM1rR7ZpAG/pub?output=xlsx')
dados['detectado'] = dados['Detecção']>0
	
dados['Municipio'] = dados['Municipio'].replace("SANT'ANA DO LIVRAMENTO", 'SANTANA DO LIVRAMENTO', regex=True)

dados['CRS'] = dados['CRS'].replace(substituicoes_crs)

# Converter a coluna 'Tipo de manancial' para string
dados['Tipo de manancial'] = dados['Tipo de manancial'].astype(str)

# Substituir espaços em branco por "Sem informação" na coluna 'Tipo de manancial'
dados['Tipo de manancial'] = dados['Tipo de manancial'].replace('nan', 'Sem informação até o momento', regex=True)

# Substituir os valores NaN por "Sem informação"
#dados['Tipo de manancial'] = dados['Tipo de manancial'].fillna('Sem informação até o momento')

#Arquivo com geojson municipios

def load_geodata(url):
    gdf = gpd.read_file(url)
    return gdf

municipios = load_geodata('https://raw.githubusercontent.com/andrejarenkow/geodata/main/municipios_rs_CRS/RS_Municipios_2021.json')
# Remover acentos e converter para maiúsculo
municipios['NM_MUN'] = municipios['NM_MUN'].apply(lambda x: unidecode(x).upper())



with col10:
    filtro_container = st.container(border=True)
    with filtro_container:
	    coluna_crs, coluna_captacao = st.columns([1,1])
	    with coluna_crs:
		#Filtro de CRS
		    lista_crs_selectbox = sorted(dados['CRS'].unique())
		    lista_crs_selectbox.insert(0,'Todas')
		    CRS = st.selectbox("Selecione a CRS", lista_crs_selectbox, index=0, placeholder="Nenhuma CRS selecionada")
		    lista_munipios_crs = dados_municipios['Município']
		    zoom_ini=5.5
		    if CRS != 'Todas':
			    dados = dados[dados['CRS']==CRS]
			    lista_munipios_crs = dados_municipios[dados_municipios['CRS']==CRS]['Município']
			    zoom_ini=7
		
    
	    with coluna_captacao:
                #Filtro de área
                # Lista de opções na ordem desejada
                captacao_opcoes = ['Subterrânea', 'Superficial', 'Sem informação até o momento']

                # Filtra a lista para incluir apenas as opções presentes nos dados e adiciona "Todas"
                captacao_selectbox = ['Todas'] + [opcao for opcao in captacao_opcoes if opcao in dados['Tipo de manancial'].unique()]
                Captação = st.selectbox("Selecione o tipo de captação", captacao_selectbox, index=0, placeholder="Nenhuma captação selecionada")
                if Captação != 'Todas':
                    dados = dados[dados['Tipo de manancial']==Captação]
			
                    
                # Filtrando apenas com detecção
                dados_detec = dados[dados['Detecção']>0].reset_index(drop=True)
                
                # Filtrar as linhas com valores válidos de latitude e longitude
                dados_filtrados = dados_detec.dropna(subset=["Latitude", "Longitude"])
                dados_filtrados['Parametros detectados'] = dados_filtrados['Parametros detectados'].fillna('Verificando')
                
                dados_consolid = pd.pivot_table(dados_filtrados, values='Detecção', index=['Latitude','Longitude', 'Municipio', 'Ponto de Coleta',
                                                                                           'CRS', 'Parametros detectados', 'Tipo de manancial'], aggfunc=['sum', 'count']).reset_index()
                try:
                    dados_consolid.columns = ['Latitude', 'Longitude', 'Municipio', 'Ponto de Coleta', 'CRS','Parametros detectados', 'Tipo de manancial', 'Detecções_Total', 'Detecções_Contagem', ]
                except:
                    dados_consolid.columns = ['Latitude', 'Longitude', 'Municipio', 'Ponto de Coleta', 'CRS','Parametros detectados', 'Tipo de manancial']
                
                def processar_parametros(parametros):
                    for parametro in parametros.split(','):
                        # Remover vírgulas
                        parametro_formatado = parametro.replace(',', '')
                        # Criar a coluna para o parâmetro
                        dados_consolid[f'{parametro_formatado}'] = dados_consolid['Parametros detectados'].map(lambda p: 
                                                                                                                   any(parametro_formatado == parametro_atual for parametro_atual in p.split(',')))
                
                dados_consolid['Parametros detectados'].apply(processar_parametros)

# Quantas amostras já foram coletadas
with col6:
    total_amostras = len(dados)
    with st.container(border=True):
        st.metric("Total de Amostras Coletadas", total_amostras)

# Quantas detecções
with col7:
    total_deteccoes = dados_detec['Detecção'].sum()
    with st.container(border=True):
        st.metric("Total de Detecções", total_deteccoes)

# Quantos municípios com detecção
with col8:
    municipios_com_detec = dados_detec['Municipio'].nunique()
    with st.container(border=True):
        st.metric("Municípios com Detecção", municipios_com_detec)

# Quantos municípios houve coleta
with col9:
    municipios_com_coleta = dados['Municipio'].nunique()
    with st.container(border=True):
        st.metric("Municípios com Coleta", municipios_com_coleta)

col5, col4 = st.columns([4, 4]) 
    
with col4:  
	# Número de coletas por município
	municipios_coletados = pd.pivot_table(dados, index='Municipio', aggfunc='size').reset_index()
	municipios_coletados.columns = ['Municipio', 'Coletas']
	
	# Filtrando o geodataframe
	municipios = municipios[municipios['NM_MUN'].isin(lista_munipios_crs)]
	
	# Juntando tudo no mesmo geodataframe
	dados_mapa_final = municipios.merge(municipios_coletados, how='left', right_on='Municipio', left_on='NM_MUN').fillna(0)
	
	# Configurar o token do Mapbox
	token = 'pk.eyJ1IjoiYW5kcmUtamFyZW5rb3ciLCJhIjoiY2xkdzZ2eDdxMDRmMzN1bnV6MnlpNnNweSJ9.4_9fi6bcTxgy5mGaTmE4Pw'
	px.set_mapbox_access_token(token)
	
	# Seu link GeoJSON
	geojson_url = "https://raw.githubusercontent.com/andrejarenkow/geodata/main/RS_por_CRS/RS_por_CRS.json"
	
	# Definindo o centro do mapa
	center_lat = -30.5  # Latitude central aproximada do Rio Grande do Sul
	center_lon = -53  # Longitude central aproximada do Rio Grande do Sul
	
	# Pontos máximos e mínimos
	latitude_max = dados_mapa_final['geometry'].centroid.y.max()
	latitude_min = dados_mapa_final['geometry'].centroid.y.min()
	longitude_max = dados_mapa_final['geometry'].centroid.x.max()
	longitude_min = dados_mapa_final['geometry'].centroid.x.min()
	
	center_lat = (latitude_max + latitude_min) / 2
	center_lon = (longitude_max + longitude_min) / 2
	
	# Configurando o TabBar
	tab = stx.tab_bar(data=[
	    stx.TabBarItemData(id="mapa_coropletico", title="Mapa de Municípios com Coleta", description=""),
	    stx.TabBarItemData(id="mapa_pontos", title="Mapa de Detecção de Agrotóxicos", description="")
	])
	
	if tab == 'mapa_coropletico':
	    # Defina os intervalos e os rótulos
	    bins = [0, 1, 3, 6, 9, float('inf')]
	    labels = ['0', '1 a 2', '3 a 5', '6 a 8', 'mais de 8']
	    
	    # Crie a nova coluna de intervalos
	    dados_mapa_final['Intervalo Coletas'] = pd.cut(dados_mapa_final['Coletas'], bins=bins, labels=labels, right=False)
	
	    # Crie o mapa choropleth
	    map_fig = px.choropleth_mapbox(
	        dados_mapa_final,
	        geojson=dados_mapa_final.geometry,
	        locations=dados_mapa_final.index,
	        color='Intervalo Coletas', 
	        color_discrete_map={'0': 'rgba(51, 7, 8, 0.65)', 
                                    '1 a 2': 'rgba(212, 90, 60, 0.65)', 
                                    '3 a 5': 'rgba(228, 132, 74, 0.65)',
	                            '6 a 8': 'rgba(232, 191, 86, 0.65)',
	                            'mais de 8': 'rgba(255, 232, 162, 0.65)'},
	        center={'lat': center_lat, 'lon': center_lon},
	        category_orders={'Intervalo Coletas': ['0', '1 a 2', '3 a 5', '6 a 8', 'mais de 8']},
	        zoom=zoom_ini,  # Defina seu nível de zoom inicial
	        mapbox_style="open-street-map",
	        hover_name='NM_MUN',
	        width=800,
	        height=700
	    )
            # Diminuir a grossura da linha
	    map_fig.update_traces(marker_line_width=0.3)  # Ajuste o valor conforme desejado	
	    map_fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
	    map_fig.update_layout(mapbox_layers = [dict(sourcetype = 'geojson',
                                        source = geojson_url,
                                        color='black',
                                        type = 'line',   
                                        line=dict(width=1)
                                   )]);
	    st.plotly_chart(map_fig)
	
	if tab == 'mapa_pontos':
	    # Crie o mapa
	    mapa_px = px.scatter_mapbox(
	        data_frame=dados_consolid,
	        lat="Latitude",
	        lon="Longitude",
	        center={'lat': center_lat, 'lon': center_lon},
	        zoom=zoom_ini,  # Defina seu nível de zoom inicial
	        hover_data=["Municipio"],  # Use a coluna correta
	        size="Detecções_Contagem",  # Use a coluna correta
	        width=800,
	        height=700,
	        color_discrete_sequence=["#f2a744"],
	        size_max=15,  # Tamanho máximo dos pontos
	        mapbox_style="open-street-map"
	    )
	    
	    # Adicione o GeoJSON ao mapa
	    mapa_px.update_layout(
	        mapbox=dict(
	            layers=[{
	                'source': geojson_url,
	                'type': 'line',
	                'color': 'black',
			 'line': dict(width=1)
	            }],
	            center={"lat": center_lat, "lon": center_lon},
	            zoom=zoom_ini
	        )
	    )
	
	    mapa_px.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
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
            name='Total de Amostras',
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
                title='Total de Amostras',
                #titlefont=dict(color='orange'),
                #tickfont=dict(color='orange'),
                overlaying='y',
                side='right'
            ),
            height=300,
            legend=dict(x=0.4, y=1.2, bgcolor='rgba(255, 255, 255, 0)')
        )

    
        # Mostrar o gráfico
        st.plotly_chart(grafico_deteccoes_mensal)
    
        soma_agrotoxicos = dados_filtrados['Parametros detectados'].str.get_dummies(sep=',').sum().sort_values(ascending=True).reset_index()
        soma_agrotoxicos.columns = ['Parametro', 'Quantidade']
                        
        grafico_top_agrotoxico = px.bar(soma_agrotoxicos.sort_values(by='Quantidade', ascending=False),
                 x='Parametro', y='Quantidade', orientation='v', height=350, 
                 text='Quantidade', title = 'Quantidade de agrotóxicos encontrada', color_discrete_sequence=['#f2a744'])  # Azul muito escuro
                
        # Mostre o mapa no Streamlit
        st.plotly_chart(grafico_top_agrotoxico)
	

# Função para adicionar quebras de linha aos nomes longos
def wrap_labels(label, width=10):
    return '<br>'.join(textwrap.wrap(label, width))

# Agrupar os dados por Município e CRS e somar as detecções
municipios_detec = dados.groupby(['Municipio', 'CRS'])['Detecção'].sum().reset_index()

# Ordenar os dados pelo número de detecções em ordem decrescente
municipios_detec = municipios_detec.sort_values(by='Detecção', ascending=False)

# Filtrar os municípios com detecções maiores que zero
municipios_com_detecção = municipios_detec[municipios_detec['Detecção'] > 0]

# Aplicar a função de quebra de linha aos nomes dos municípios
municipios_com_detecção['Municipio'] = municipios_com_detecção['Municipio'].apply(wrap_labels)

# Criar um gráfico de árvore (treemap) usando Plotly Express, agrupando por CRS
grafico_mun_detec = px.treemap(municipios_com_detecção, path=['CRS', 'Municipio'], values='Detecção', height = 800, 
			       hover_name = 'Municipio', color_discrete_sequence=px.colors.qualitative.Set2, 
			       labels={'labels': 'Município', 'Detecção': 'Número de Detecções', 'parent': 'CRS'},
                 	       title='Municípios com mais detecção de agrotóxicos agrupados por CRS')

# Atualizar o layout para alterar o tamanho da fonte
grafico_mun_detec.update_layout(
    title_font_size=20,  # Tamanho da fonte do título
    font=dict(
        size=14  # Tamanho da fonte geral
    )
)
for data in grafico_mun_detec.data:
    data.textinfo = 'label+text+value'
    custom_text = "Custom Info"  # Texto personalizado que você deseja adicionar
    data.customdata = [custom_text] * len(data.labels)  # Adiciona o texto personalizado para cada item
    data.hovertemplate = '<b>%{label}</b><br>Detecção: %{value}<br>'
    data.texttemplate = '<b>%{label}</b><br>Detecção: %{value}<br>'
    
#grafico_mun_detec.layout.hovermode = False
st.plotly_chart(grafico_mun_detec, theme = None)
