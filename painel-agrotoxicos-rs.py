import streamlit as st
import pandas as pd
import folium

# Carregar os dados
dados = pd.read_excel('https://docs.google.com/spreadsheets/d/e/2PACX-1vRR1E1xhXucgiQW8_cOOZ0BzBlMpfz6U9sUY9p1t8pyn3gu0NvWBYsMtCHGhJvXt2QYvCLM1rR7ZpAG/pub?output=xlsx')

# Filtrar as linhas com valores válidos de latitude e longitude
dados_filtrados = dados.dropna(subset=["Latitude", "Longitude"])

# Consolidar os dados
dados_consolid = pd.pivot_table(dados_filtrados, values='Detecção', index=['Latitude','Longitude', 'Municipio', 'Ponto de Coleta', 'CRS'], aggfunc=['sum', 'count']).reset_index()
dados_consolid.columns = ['Latitude', 'Longitude', 'Municipio', 'Ponto de Coleta', 'CRS', 'Detecções_Total', 'Detecções_Contagem']

# Crie o mapa
mapa_folium = folium.Map(location=[dados_consolid["Latitude"].mean(), dados_consolid["Longitude"].mean()], zoom_start=5)

# Adicione marcadores
for i, row in dados_consolid.iterrows():
    folium.Marker([row["Latitude"], row["Longitude"]]).add_to(mapa_folium)

# Adicione camadas (opcional)
# Adicione uma camada de azulejos com diferentes estilos
folium.TileLayer('Stamen Toner').add_to(mapa_folium)

# Mostre o mapa
# mapa_folium.save("mapa_folium.html")  # Salve o mapa como HTML
mapa_folium
