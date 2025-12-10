from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
import streamlit as st
import datetime
from PIL import Image
import folium
from streamlit_folium import folium_static

df = pd.read_csv( 'dataset/zomato.csv')
df1 = df.copy()

st.set_page_config(
    page_title="Visão países",
    page_icon="🌎")


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
    return df

df1['Country'] = df1['Country Code'].map(COUNTRIES)
df1['Price_range'] = df1['Price range'].apply(create_price_tye)
df1["Cuisines"] = (
    df1["Cuisines"]
    .fillna("")  # substitui NaN por vazio
    .astype(str) # garante que seja string
    .apply(lambda x: x.split(",")[0])
)

#----------------------------cria grafico de barras/ restaurantes registrados por pais--------------------------------------------
def rest_reg_pais(df1):
    df1_aux = (df1.loc[:, ['Restaurant ID','Country']].groupby('Country').nunique().sort_values('Restaurant ID',ascending=False).reset_index())

    fig = px.bar(df1_aux ,x ='Country', y='Restaurant ID', text="Restaurant ID",
    labels={
            "Country": "Paises",
            "Restaurant ID": "Quantidade de Restaurantes",
        },)
    return fig
#------------------------cidades registradas por pais------------------------------------------------
def cida_reg_pais(df1):
    df1_aux = (df1.loc[:, ['City','Country']].groupby('Country').nunique().sort_values('City',ascending=False).reset_index())
    fig = px.bar(df1_aux, x='Country', y='City', text='City',
    labels={
        "Country": "Países",
        "City": "Quantidade de cidades",
        },)
    return fig
#---------------------cria um grafico de barras da media de avaliacoes por paises---------------------------------------------------
def avg_avaliacao_pais(df1):
    df1_aux = df1_aux = (df1.loc[:,['Votes','Country']].groupby('Country').mean().sort_values('Votes',ascending=False).reset_index())
    fig = px.bar(df1_aux,x='Country',y='Votes', text='Votes', text_auto=".2f",
        labels={
            "Country" : "Países",
            "Votes" : "Quantidade média de avaliações"
        },)
    return fig
#------------------cria um grafico de barras da media de prato para 2 pessoas por pais---------------------------------------------------------------------
def avg_custo_pais(df1):
    df1_aux = (df1.loc[:,['Average Cost for two','Country']].groupby('Country').mean().sort_values('Average Cost for two',ascending=False).reset_index())
    fig = px.bar(df1_aux, x='Country', y='Average Cost for two', text='Average Cost for two', text_auto=".2f",
        labels={
            "Country" : "Países",
            "Average Cost for two" : "Preço médio de prato para duas pessoas"
        },)
    return fig
#---------------------------------------------------------------------------------------
#=======================
#barra lateral
#=======================

st.header('🌎Visão Países' )

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

#===============================
#Layout
#===============================

tab1, tab2, tab3 = st.tabs( ['Visão Países', '-', '-'])

with tab1:
    with st.container():
        st.markdown('### Restaurantes registrados por país')
        fig = rest_reg_pais(df1)
        st.plotly_chart(fig, use_container_width=True) 
        st.set_page_config(layout="wide")     

    with st.container():
        st.markdown('### Cidades registradas por país')
        fig = cida_reg_pais(df1)
        st.plotly_chart(fig, use_container_width=True) 
        st.set_page_config(layout="wide")

    with st.container():
        col1,col2 = st.columns(2)
        with col1: 
            st.markdown('### Média de avaliações feitas por país')
            fig = avg_avaliacao_pais(df1)
            st.plotly_chart(fig, use_container_width=True)         

        with col2: 
            st.markdown('### Média de preço de um prato para duas pessoas por país')
            fig = avg_custo_pais(df1)
            st.plotly_chart(fig, use_container_width=True)  



            



        

    
