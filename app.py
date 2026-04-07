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

# límites de PlayTimeHours
horas_min = float(df_Gente_Sin_Oficio["PlayTimeHours"].min())
horas_max = float(df_Gente_Sin_Oficio["PlayTimeHours"].max())

# config. del slider en el sidebar
rango_horas = st.sidebar.slider(
    "Rango de horas de juego",
    min_value=horas_min,
    max_value=horas_max,
    value=(horas_min, horas_max), 
    step=1.0
)

# 3. filtro al DataFrame
df_filtrado = df_Gente_Sin_Oficio[
    (df_Gente_Sin_Oficio["PlayTimeHours"] >= rango_horas[0]) & 
    (df_Gente_Sin_Oficio["PlayTimeHours"] <= rango_horas[1])
]

# se agregan tabs para mostrar diferentes análisis
tab1, tab2, tab3, tab4 = st.tabs(["Análisis Regional", " Dedicación y Frecuencia", "Distribución de horas", "Tiempo de juego y Frecuencia Semanal"])

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
with tab2:
    st.subheader("📈 Comparativa: Engagement vs. Sesiones Semanales")
    
    if not df_filtrado.empty:
        # se crea el Box Plot
        fig_comp = px.box(
            df_filtrado,
            x="GameGenre",          
            y="SessionsPerWeek",    
            color="EngagementLevel",
            title="Distribución de Sesiones por Género y Nivel de Engagement",
            # Ordeno las categorías de la leyenda para que tengan sentido
            category_orders={"EngagementLevel": ["Low", "Medium", "High"]},
            # Asigno colores
            color_discrete_map={
                "Low": "#EF553B", 
                "Medium": "#FECB52", 
                "High": "#00CC96"
            },
            template="plotly_dark"
        )
        
        # configuración de la leyenda
        fig_comp.update_layout(
            showlegend=True, 
            legend_title_text='Nivel de Engagement', 
            legend=dict(
                orientation="h",    
                yanchor="bottom",
                y=1.02,             
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig_comp, use_container_width=True)
        
        st.info("💡Cada 'caja' representa el rango donde se encuentra la mayoría de los jugadores. Los puntos aislados son casos atípicos.")
        st.image("https://content.imageresizer.com/images/memes/Sonic-with-a-gun-meme-2.jpg", width = 250)
    else:
        st.image("https://www.shutterstock.com/image-vector/dino-google-chrome-abstract-game-600nw-2533959479.jpg", width=400)
        st.warning("Selecciona una ubicación en la barra lateral.")