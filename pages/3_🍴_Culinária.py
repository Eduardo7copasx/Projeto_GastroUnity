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
    page_title="Visão culinária",
    page_icon="🍴")


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

#---------------------------------------------------------------------------------------
def metrics(df1):
    df.aux = round(df1.loc[df1['Cuisines'].str.contains('Italian', case=False, na=False) , :].groupby(['Restaurant Name','Country','City']).agg(avg_rating =('Aggregate rating','mean'), avg_cost=('Average Cost for two', 'mean'), votos=('Votes','sum')).sort_values('avg_rating', ascending=False).reset_index().iloc[0,3],1)
    df.aux1 = df1.loc[df1['Cuisines'].str.contains('Italian', case=False, na=False) , :].groupby(['Restaurant Name','Country','City']).agg(avg_rating =('Aggregate rating','mean'), avg_cost=('Average Cost for two', 'mean'), votos=('Votes','sum')).sort_values('avg_rating', ascending=False).reset_index().iloc[0,1]
    df.aux2 = df1.loc[df1['Cuisines'].str.contains('Italian', case=False, na=False) , :].groupby(['Restaurant Name','Country','City']).agg(avg_rating =('Aggregate rating','mean'), avg_cost=('Average Cost for two', 'mean'), votos=('Votes','sum')).sort_values('avg_rating', ascending=False).reset_index().iloc[0,2]
    df.aux3 = df1.loc[df1['Cuisines'].str.contains('Italian', case=False, na=False) , :].groupby(['Restaurant Name','Country','City']).agg(avg_rating =('Aggregate rating','mean'), avg_cost=('Average Cost for two', 'mean'), votos=('Votes','sum')).sort_values('avg_rating', ascending=False).reset_index().iloc[0,4]
    st.metric("", f"{df.aux}/5.0",
              help=f"""
            País: {df.aux1} \n
            Cidade: {df.aux2}\n
            Média de prato para dois: {df.aux3},(Dólar neozelandes)
              """,)
#---------------------------------------------------------------------------------------
def metrics1(df1):
    df.aux = round(df1.loc[df1['Cuisines'].str.contains('American', case=False, na=False) , :].groupby(['Restaurant Name','Country','City']).agg(avg_rating =('Aggregate rating','mean'), avg_cost=('Average Cost for two', 'mean'), votos=('Votes','sum')).sort_values('avg_rating', ascending=False).reset_index().iloc[0,3],1)
    df.aux1 = df1.loc[df1['Cuisines'].str.contains('American', case=False, na=False) , :].groupby(['Restaurant Name','Country','City']).agg(avg_rating =('Aggregate rating','mean'), avg_cost=('Average Cost for two', 'mean'), votos=('Votes','sum')).sort_values('avg_rating', ascending=False).reset_index().iloc[0,1]
    df.aux2 = df1.loc[df1['Cuisines'].str.contains('American', case=False, na=False) , :].groupby(['Restaurant Name','Country','City']).agg(avg_rating =('Aggregate rating','mean'), avg_cost=('Average Cost for two', 'mean'), votos=('Votes','sum')).sort_values('avg_rating', ascending=False).reset_index().iloc[0,2]
    df.aux3 = df1.loc[df1['Cuisines'].str.contains('American', case=False, na=False) , :].groupby(['Restaurant Name','Country','City']).agg(avg_rating =('Aggregate rating','mean'), avg_cost=('Average Cost for two', 'mean'), votos=('Votes','sum')).sort_values('avg_rating', ascending=False).reset_index().iloc[0,4]
    st.metric("", f"{df.aux}/5.0",
              help=f"""
            País: {df.aux1} \n
            Cidade: {df.aux2}\n
            Média de prato para dois: {df.aux3},(Dólar singapuriano)
              """,)
#---------------------------------------------------------------------------------------
def metrics2(df1):
    df.aux = round(df1.loc[df1['Cuisines'].str.contains('Arabian', case=False, na=False) , :].groupby(['Restaurant Name','Country','City']).agg(avg_rating =('Aggregate rating','mean'), avg_cost=('Average Cost for two', 'mean'), votos=('Votes','sum')).sort_values('avg_rating', ascending=False).reset_index().iloc[0,3],1)
    df.aux1 = df1.loc[df1['Cuisines'].str.contains('Arabian', case=False, na=False) , :].groupby(['Restaurant Name','Country','City']).agg(avg_rating =('Aggregate rating','mean'), avg_cost=('Average Cost for two', 'mean'), votos=('Votes','sum')).sort_values('avg_rating', ascending=False).reset_index().iloc[0,1]
    df.aux2 = df1.loc[df1['Cuisines'].str.contains('Arabian', case=False, na=False) , :].groupby(['Restaurant Name','Country','City']).agg(avg_rating =('Aggregate rating','mean'), avg_cost=('Average Cost for two', 'mean'), votos=('Votes','sum')).sort_values('avg_rating', ascending=False).reset_index().iloc[0,2]
    df.aux3 = df1.loc[df1['Cuisines'].str.contains('Arabian', case=False, na=False) , :].groupby(['Restaurant Name','Country','City']).agg(avg_rating =('Aggregate rating','mean'), avg_cost=('Average Cost for two', 'mean'), votos=('Votes','sum')).sort_values('avg_rating', ascending=False).reset_index().iloc[0,4]
    st.metric("", f"{df.aux}/5.0",
              help=f"""
            País: {df.aux1} \n
            Cidade: {df.aux2}\n
            Média de prato para dois: {df.aux3},(Rupia indiana)
              """,)
#---------------------------------------------------------------------------------------
def metrics3(df1):
    df.aux = round(df1.loc[df1['Cuisines'].str.contains('Japanese', case=False, na=False) , :].groupby(['Restaurant Name','Country','City']).agg(avg_rating =('Aggregate rating','mean'), avg_cost=('Average Cost for two', 'mean'), votos=('Votes','sum')).sort_values('avg_rating', ascending=False).reset_index().iloc[0,3],1)
    df.aux1 = df1.loc[df1['Cuisines'].str.contains('Japanese', case=False, na=False) , :].groupby(['Restaurant Name','Country','City']).agg(avg_rating =('Aggregate rating','mean'), avg_cost=('Average Cost for two', 'mean'), votos=('Votes','sum')).sort_values('avg_rating', ascending=False).reset_index().iloc[0,1]
    df.aux2 = df1.loc[df1['Cuisines'].str.contains('Japanese', case=False, na=False) , :].groupby(['Restaurant Name','Country','City']).agg(avg_rating =('Aggregate rating','mean'), avg_cost=('Average Cost for two', 'mean'), votos=('Votes','sum')).sort_values('avg_rating', ascending=False).reset_index().iloc[0,2]
    df.aux3 = df1.loc[df1['Cuisines'].str.contains('Japanese', case=False, na=False) , :].groupby(['Restaurant Name','Country','City']).agg(avg_rating =('Aggregate rating','mean'), avg_cost=('Average Cost for two', 'mean'), votos=('Votes','sum')).sort_values('avg_rating', ascending=False).reset_index().iloc[0,4]
    st.metric("", f"{df.aux}/5.0",
              help=f"""
            País: {df.aux1} \n
            Cidade: {df.aux2}\n
            Média de prato para dois: {df.aux3},(Libra esterlina)
              """,)
#------------------------------melhores culinarias---------------------------------------------------------
def metrics4(df1):
    df.aux = round(df1.loc[df1['Cuisines'].str.contains('Brazilian', case=False, na=False) , :].groupby(['Restaurant Name','Country','City']).agg(avg_rating =('Aggregate rating','mean'), avg_cost=('Average Cost for two', 'mean'), votos=('Votes','sum')).sort_values('avg_rating', ascending=False).reset_index().iloc[0,3],1)
    df.aux1 = df1.loc[df1['Cuisines'].str.contains('Brazilian', case=False, na=False) , :].groupby(['Restaurant Name','Country','City']).agg(avg_rating =('Aggregate rating','mean'), avg_cost=('Average Cost for two', 'mean'), votos=('Votes','sum')).sort_values('avg_rating', ascending=False).reset_index().iloc[0,1]
    df.aux2 = df1.loc[df1['Cuisines'].str.contains('Brazilian', case=False, na=False) , :].groupby(['Restaurant Name','Country','City']).agg(avg_rating =('Aggregate rating','mean'), avg_cost=('Average Cost for two', 'mean'), votos=('Votes','sum')).sort_values('avg_rating', ascending=False).reset_index().iloc[0,2]
    df.aux3 = df1.loc[df1['Cuisines'].str.contains('Brazilian', case=False, na=False) , :].groupby(['Restaurant Name','Country','City']).agg(avg_rating =('Aggregate rating','mean'), avg_cost=('Average Cost for two', 'mean'), votos=('Votes','sum')).sort_values('avg_rating', ascending=False).reset_index().iloc[0,4]
    st.metric("", f"{df.aux}/5.0",
              help=f"""
            País: {df.aux1} \n
            Cidade: {df.aux2}\n
            Média de prato para dois: {df.aux3},(Real)
              """,)
#-------------------------------dataframe top 10 restaurantes--------------------------------------------------------
def metrics5(df1):
    cols = [
        "Restaurant ID",
        "Restaurant Name",
        "Country",
        "City",
        "Cuisines",
        "Average Cost for two",
        "Aggregate rating",
        "Votes",
    ]
    df_aux = (df1.loc[:, cols].sort_values('Aggregate rating',ascending=False).head(top_n))
    st.dataframe(df_aux, use_container_width=True)

#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
def top_10_cul(df1):
    df1_aux = (df1.loc[:, ['Aggregate rating','Cuisines','Restaurant ID']].groupby('Cuisines')
       .agg(
            media_rating = ('Aggregate rating', 'mean'),
            qtd_rest = ('Restaurant ID', 'count')
       ).query('qtd_rest >= 10').sort_values('media_rating', ascending=False).reset_index().head(top_n))
    fig = px.bar(df1_aux, x='Cuisines', y='media_rating', text='media_rating', text_auto='.2f', title=f'Top {top_n} piores tipos de culinária',
                 labels={
                 "media_rating" : "Média das avaliações",
                 "Cuisines" : "Tipo de culinária",                 
                 },)
    return fig
#---------------------------piores culinarias------------------------------------------------------------
def top_10_cul_ruim(df1):
    df1_aux = (df1.loc[:, ['Aggregate rating','Cuisines','Restaurant ID']].groupby('Cuisines')
       .agg(
            media_rating = ('Aggregate rating', 'mean'),
            qtd_rest = ('Restaurant ID', 'count')
       ).query('qtd_rest >= 10').sort_values('media_rating', ascending=True).reset_index().head(top_n))
    fig = px.bar(df1_aux, x='Cuisines', y='media_rating', text='media_rating', text_auto='.2f', title=f'Top {top_n} piores tipos de culinária',
                 labels={
                 "media_rating" : "Média das avaliações",
                 "Cuisines" : "Tipo de culinária",                 
                 },)
    return fig

#=======================
#barra lateral
#=======================

st.header('🏙️Visão Culinária' )

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

top_n = st.sidebar.slider('### Selecione a quantidade de restaurantes que deseja visualizar', 1,20,10 )

culinaria = st.sidebar.multiselect('Escolha os tipos de culinária',
                                    df1.loc[:,'Cuisines'].unique().tolist(),
                                    default=[
                                    "Home-made",
                                    "BBQ",
                                    "Japanese",
                                    "Brazilian",
                                    "Arabian",
                                    "American",
                                    "Italian",
                                            ],
)

st.sidebar.markdown ("""---""" )
st.sidebar.markdown('### Powered by Comunidade DS' )

#===============================
#Layout
#===============================

tab1, tab2, tab3 = st.tabs( ['Visão Culinária','-','-'])

with tab1:
    with st.container():
        st.markdown('### Melhores restaurantes dos principais tipos culinários')
        col1,col2,col3,col4,col5 = st.columns(5)
        with col1:
            st.text('Italiana:Ombra')
            metrics(df1)
        with col2:
            st.text('Americana:Wild Honey')
            metrics1(df1)
        with col3:
            st.text('Árabe:Barbeque Nation')
            metrics2(df1)
        with col4:
            st.text('Japonesa:Chotto Matte')
            metrics3(df1)
        with col5:
            st.text('Brasileira:Braseiro da Gávea')
            metrics4(df1)
with tab1:
    with st.container():
        st.markdown(f"### Top {top_n} restaurantes")
        metrics5(df1)
with tab1:
    with st.container():
        col1,col2 = st.columns(2)
        with col1:            
            fig = top_10_cul(df1)
            st.plotly_chart(fig, use_container_width=True) 
        with col2:
           fig = top_10_cul_ruim(df1)
           st.plotly_chart(fig, use_container_width=True) 