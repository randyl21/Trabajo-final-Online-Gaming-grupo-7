# Importación de librerías necesarias
import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="Dashboard del Online Gaming", page_icon="🎮", layout="wide")

# Carga de datos
@   st.cache_data
def cargar_datos():
    df_Gente_Sin_Oficio = pd.read_csv("17. Online Gaming.csv")
    #reemplazo nombres de la columna "Location" para que estén en español
    df_Gente_Sin_Oficio["Location"] = df_Gente_Sin_Oficio["Location"].replace("Other", "Otro")
    df_Gente_Sin_Oficio["Location"] = df_Gente_Sin_Oficio["Location"].replace("USA", "EE.UU")
    df_Gente_Sin_Oficio["Location"] = df_Gente_Sin_Oficio["Location"].replace("Europe", "Europa")
    return df_Gente_Sin_Oficio 

df_Gente_Sin_Oficio = cargar_datos()

# Título del dashboard
st.title("Análisis de Jugadores de Videojuegos Online")
st.markdown("Comportamiento de los jugadores de videojuegos online en diferentes regiones del mundo.")

# Filtro por locación geográfica
st.sidebar.header("Locación Geográfica")
ubicacion = st.sidebar.multiselect("Selecciona la ubicación geográfica:", options=df_Gente_Sin_Oficio["Location"].unique(), default=df_Gente_Sin_Oficio["Location"].unique()) 
df_filtrado = df_Gente_Sin_Oficio[df_Gente_Sin_Oficio["Location"].isin(ubicacion)]

tab1, tab2, tab3, tab4 = st.tabs(["Análisis Regional", "📊 Dedicación y Frecuencia", "x", "x2"])

# se agregan tabs para mostrar diferentes análisis, el primero es el análisis de la ubicación, donde se muestra la popularidad de los géneros de videojuegos por ubicación geográfica.
with tab1:
    st.subheader("🎮 Géneros más populares por ubicación")

    # Agrupo por Ubicación y contamos la frecuencia de cada Género
    df_que_tan_virgenes_son = df_filtrado.groupby("Location")["GameGenre"].value_counts().reset_index(name="Usuarios")

    # Creo el gráfico de barras utilizando Plotly Express
    if not df_que_tan_virgenes_son.empty:
        fig_que_tan_virgenes_son = px.bar(
            df_que_tan_virgenes_son, 
            x="Location", 
            y="Usuarios", 
            color="GameGenre", 
            barmode="relative", 
            title="Comparativa de Géneros por Ubicación",
            labels={"Location": "Ubicación", "Usuarios": "Cantidad de Jugadores", "GameGenre": "Género"},
            color_discrete_sequence=px.colors.sequential.Blues_r,
            template="plotly_dark"
        )
        
        st.plotly_chart(fig_que_tan_virgenes_son, use_container_width=True)
    else:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image("https://www.shutterstock.com/image-vector/dino-google-chrome-abstract-game-600nw-2533959479.jpg", width=400)
            st.warning("Selecciona al menos una región en la barra lateral.")