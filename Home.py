import streamlit as st 
from PIL import Image
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
import streamlit as st
import datetime
from PIL import Image
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster


df = pd.read_csv( 'dataset/zomato.csv')
df1 = df.copy()

COUNTRIES = {
1: "India",
14: "Australia",
30: "Brazil",
37: "Canada",
94: "Indonesia",
148: "New Zeland",
162: "Philippines",
166: "Qatar",
184: "Singapure",
189: "South Africa",
191: "Sri Lanka",
208: "Turkey",
214: "United Arab Emirates",
215: "England",
216: "United States of America"}

def country_name (country_id): 
    return COUNTRIES [country_id]


def create_price_tye(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"
    
COLORS = {
"3F7E00": "darkgreen",
"5BA829": "green",
"9ACD32": "lightgreen",
"CDD614": "orange",
"FFBA00": "red",
"CBCBC8": "darkred",
"FF7800": "darkred",
}
def color_name(color_code):
    return COLORS[color_code]

def rename_columns(dataframe):
    df1 = df.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df1

df1['COLORS'] = df1['Rating color']  # ou o nome correto da sua coluna
df1['cores'] = df1['COLORS'].map(COLORS).fillna("unknown")
df1['Country'] = df1['Country Code'].map(COUNTRIES)
df1['Price_range'] = df1['Price range'].apply(create_price_tye)
df1['cores'] = df1['COLORS'].map(COLORS).fillna("unknown")
df1["Cuisines"] = (
    df1["Cuisines"]
    .fillna("")  # substitui NaN por vazio
    .astype(str) # garante que seja string
    .apply(lambda x: x.split(",")[0])
)

#-------------------------restaurantes cadastrados-----------------------------------------------------------------
def rest(df1):
    rest_cad = df1.loc[:,'Restaurant ID'].nunique()
    st.metric("",rest_cad)
#------------------------paises cadastrados------------------------------------------------------------------
def country(df1):
    countrye = df1.loc[:,'Country'].nunique()
    st.metric("",countrye)
#-----------------------cidades cadastradas-------------------------------------------------------------------
def city(df1):
    cityes = df1.loc[:,'City'].nunique()
    st.metric("",cityes)
#----------------------votos--------------------------------------------------------------------
def vote(df1):
    votes = df1.loc[:,'Votes'].sum()
    votes = f"{votes:,.0f}".replace(",", ".") 
    st.metric("",str(votes))
#----------------------tipo de culinaria--------------------------------------------------------------------
def culi(df1):
    culina = df1.loc[:,'Cuisines'].nunique()
    st.metric("",culina)
#------------------------criacao do mapa------------------------------------------------------------------
def create_mapa(df1):
    f = folium.Figure(width=1920, height=1080) # cria o mapa
    m = folium.Map(max_bounds=True).add_to(f) # adiciona os marcadores
    market_cluster = MarkerCluster().add_to(m) # junta todos os marcadores

    for _, line in df1.iterrows():   # pega todos os restaurantes e as colunas que selecionamos logo abaixo, pegando os dados das linhas que escrevemos abaixo

        name = line['Restaurant Name']
        price_for_two = line["Average Cost for two"]
        cuisine = line["Cuisines"]
        currency = line["Currency"]
        rating = line["Aggregate rating"]
        color = line["cores"]
#essa parte de baixo representa a janela que aparece quando clicamos no pin do mapa, dessa forma ele pega o nome do restaurante, preco, tipo e pontuacao
        html = f"""
        <p><strong>{name}</strong></p>
        <p>Price: {price_for_two},00 ({currency}) para dois</p>
        <p>Type: {cuisine}</p>
        <p>Aggregate Rating: {rating}/5.0</p>
        """

        popup = folium.Popup(html, max_width=500) #a propria janelinha do popup
# abaixo colocamos o marcador no mapa
        folium.Marker(
            [line["Latitude"], line["Longitude"]],
            popup=popup,
            icon=folium.Icon(
                color=color,
                icon="cutlery",#essa parte define o icone que vai aparecer no mapa, nesse caso cutlery quer dizer talher
                prefix="fa" # biblioteca do folium que possui inumeros icones
            ),
        ).add_to(market_cluster)

    # exibe o mapa
    folium_static(m, width=1024, height=768)





#------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------

st.set_page_config(
    page_title="Home",
    page_icon="📊")

#=======================
#barra lateral
#=======================

st.header('GastroUnity' )
st.markdown(" ### O Melhor lugar para encontrar seu mais novo restaurante favorito!")
st.markdown('### Temos as seguintes marcas dentro da nossa plataforma:')

#image_path = 'Logo.jpeg'
#image = Image.open('Logo.jpeg')
#st.sidebar.image(image, width=120)

st.sidebar.markdown('# Origem Food Group' )
st.sidebar.markdown('## Fastest Delivery in Town' )

st.sidebar.markdown ("""---""" )

st.sidebar.markdown('### Selecione o país que deseja visualizar as informações ' )

traffic_options = st.sidebar.multiselect('Países',
[ "India","Australia", "Brazil", "Canada", "Indonesia","New Zeland",
"Philippines", "Qatar", "Singapure", "South Africa", "Sri Lanka", "Turkey",
"United Arab Emirates", "England", "United States of America"],
default=['India', 'Brazil', 'Canada', 'Indonesia'])

st.sidebar.markdown ("""---""" )
st.sidebar.markdown('### Powered by Comunidade DS' )

tab1,tab2,tab3 = st.tabs( ['Visão geral','-','-'])

with tab1:
    with st.container():        
        col1,col2,col3,col4,col5 = st.columns(5)
        with col1:
            st.text('Restaurantes cadastrados')            
            rest(df1)
        with col2:
            st.text('Países cadastrados')
            country(df1)
        with col3:
            st.text('Cidades cadastradas')
            city(df1)
        with col4:
            st.text('Avaliações feitas na plataforma')
            vote(df1)
        with col5:
            st.text('Tipos de culinárias oferecidas')
            culi(df1)
            
with tab1:
    with st.container():
        st.markdown("### Distribuição de restaurantes por países")
        create_mapa(df1)


