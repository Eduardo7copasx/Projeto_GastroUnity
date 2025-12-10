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
    page_title="Visão cidades",
    page_icon="🏙️")


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

#--------------------------cidades com mais restaurantes-------------------------------------------------------------
def top_cidades_rest(df1):
    df1_aux = (df1.loc[:,['Restaurant ID','City','Country']].groupby(['City','Country']).nunique().sort_values('Restaurant ID', ascending=False).reset_index().head(10))
    fig = px.bar(df1_aux, x='City',y='Restaurant ID', text='Restaurant ID',color="Country",
            labels={
                    "City" : "Cidades",
                    "Restaurant ID" : "Quantidade de restaurantes",
                    "Country" : "Países"
                 },)
    return fig
#------------------------restaurantes com media acima de 4---------------------------------------------------------------
def top_rest_4(df1):
    df1_aux = df1.aux = (df1.loc[df1['Aggregate rating'] >= 4,['Restaurant ID','City','Country']].groupby(['City','Country']).nunique().sort_values(['Restaurant ID','City'],ascending=[False,True]).reset_index().head(7))
    fig = px.bar(df1_aux, x='City', y='Restaurant ID',text='Restaurant ID', text_auto=".2f", color='Country',
            labels={
                "City" : "Cidades",
                "Country" : "Países",            
                "Restaurant ID" : "Quantidade de restaurantes"
            }, )
    return fig
#----------------------restaurantes com media abaixo de 2.5-----------------------------------------------------------------
def top_rest_2_5(df1):
    df1_aux = (df1.loc[df1['Aggregate rating'] <= 2.5,['Restaurant ID','City','Country']].groupby(['City','Country']).nunique().sort_values(['Restaurant ID','City'],ascending=[False,True]).reset_index().head(7))
    fig = px.bar(df1_aux, x='City', y='Restaurant ID',text='Restaurant ID', text_auto=".2f", color='Country',
        labels={
            "City" : "Cidades",
            "Country" : "Países",            
            "Restaurant ID" : "Quantidade de restaurantes"
        }, )
    return fig   
#---------------------------------------------------------------------------------------
def top_rest_25_cluina_dist(df1):
    df1_aux = (df1.loc[:, ['Cuisines','City','Country']].groupby(['City','Country']).nunique().sort_values(['City','Cuisines'], ascending=[True,False]).reset_index().head(15))
    fig = px.bar(df1_aux, x='City', y='Cuisines',text='Cuisines', text_auto=".2f", color='Country',
        labels={
            "City" : "Cidades",
            "Country" : "Países",            
            "Cuisines" : "Quantidade de restaurantes"
        },)
    return fig
#---------------------------------------------------------------------------------------


#=======================
#barra lateral
#=======================

st.header('🏙️Visão Cidades' )

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

tab1, tab2, tab3 = st.tabs( ['Visão Cidades','-', '-'])

with tab1:
    with st.container():
        st.markdown('### Top 10 cidades com mais restaurantes na base de dados')
        fig = top_cidades_rest(df1)
        st.plotly_chart(fig, use_container_width=True) 
        st.set_page_config(layout="wide") 

with tab1:
    col1,col2 = st.columns(2)
    with col1:
        st.markdown('### Top 7 cidades com restaurantes com média acima de 4')
        fig = top_rest_4(df1)
        st.plotly_chart(fig, use_container_width=True) 
        st.set_page_config(layout="wide") 

    with col2:
        st.markdown('### Top 7 cidades com restaurantes com média abaixo de 2.5')
        fig = top_rest_2_5(df1)
        st.plotly_chart(fig, use_container_width=True) 
        st.set_page_config(layout="wide")         

with tab1:
    with st.container():
        st.markdown('### Top 15 cidades com mais restaurantes de tipos culinários distintos')
        fig = top_rest_25_cluina_dist(df1)
        st.plotly_chart(fig, use_container_width=True) 
        st.set_page_config(layout="wide")  