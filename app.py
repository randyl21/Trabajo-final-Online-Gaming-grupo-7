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

ubicaciones_disponibles = df_Gente_Sin_Oficio['Location'].unique()
ubicaciones_seleccionadas = st.sidebar.multiselect(
    "Selecciona el Continente", 
    options= ubicaciones_disponibles,
    default = ubicaciones_disponibles [:4]
    )

# límites de PlayTimeHours
horas_min = float(df_Gente_Sin_Oficio["PlayTimeHours"].min())
horas_max = float(df_Gente_Sin_Oficio["PlayTimeHours"].max())

# config. del slider en el sidebar
rango_horas = st.sidebar.slider(
    "Rango de horas de juego",
    min_value=horas_min,
    max_value=horas_max,
    value=(horas_min, horas_max), 
)

# filtro al DataFrame
df_filtrado = df_Gente_Sin_Oficio[
    (df_Gente_Sin_Oficio["PlayTimeHours"] >= rango_horas[0]) & 
    (df_Gente_Sin_Oficio["PlayTimeHours"] <= rango_horas[1]) & 
    (df_Gente_Sin_Oficio["Location"].isin(ubicaciones_seleccionadas))
]

#columnas para métricas
col1, col2, col3 = st.columns(3)
col1.metric("Total Jugadores", len(df_filtrado))
col2.metric("Horas Promedio", f"{df_filtrado['PlayTimeHours'].mean():,.1f}")
col3.metric("Promedio de Frecuencia Semanal", f"{df_filtrado['SessionsPerWeek'].mean():,.0f}")

st.markdown("---")

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
with tab3:
     with tab3:
      st.subheader("📊 Distribución de las horas de juego registradas por los usuarios para identificar niveles de dedicación")

     if not df_filtrado.empty:
        # Cálculo de Cuartiles / Q1 (25% inferior), Q2 (Mediana/50%), Q3 (75% superior)
        q1 = df_filtrado['PlayTimeHours'].quantile(0.25)
        mediana = df_filtrado['PlayTimeHours'].median()
        q3 = df_filtrado['PlayTimeHours'].quantile(0.75)

        # Categorizo los valores con la función
        def evaluar_dedicacion(h):
            if h <= q1: return "Casual"
            if h <= q3: return "Moderado"
            return "Intenso / Hardcore"

        df_eval = df_filtrado.copy()
        df_eval["Nivel"] = df_eval["PlayTimeHours"].apply(evaluar_dedicacion)

        # Gráfico de Distribución con Box Plot Marginal
        fig_eval = px.histogram(
            df_eval,
            x="PlayTimeHours",
            color="Nivel",
            marginal="box",
            title="Distribución de Horas y Segmentos de Dedicación",
            labels={"PlayTimeHours": "Horas Totales", "count": "Número de Jugadores"},
            color_discrete_map={
                "Casual": "#EF553B", 
                "Moderado": "#FECB52", 
                "Intenso / Hardcore": "#00CC96"
            },
            category_orders={"Nivel": ["Casual", "Moderado", "Intenso / Hardcore"]},
            template="plotly_dark",
            barmode="overlay"
        )

        st.plotly_chart(fig_eval, use_container_width=True)

        # 4. Resumen
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Punto de Corte Casual", f"{q1:.1f} hrs")
        with col2:
            st.metric("Punto de Corte Hardcore", f"{q3:.1f} hrs")
        with col3:
            st.metric("Máximo de Horas", f"{df_filtrado['PlayTimeHours'].max():.1f} hrs")
            
     else:
        st.image("https://www.shutterstock.com/image-vector/dino-google-chrome-abstract-game-600nw-2533959479.jpg", width=400)
        st.warning("No hay datos suficientes. Revisa los filtros del sidebar.")

    