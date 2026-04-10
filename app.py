# Importación de librerías necesarias
import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="Análisis de Juego en Línea", page_icon="https://img.freepik.com/free-vector/globe-grid-glyph-with-mouse-cursor_78370-4904.jpg?semt=ais_hybrid&w=740&q=80", layout="wide")

# Carga de datos
@   st.cache_data
def cargar_datos():
    df_Gente_Sin_Oficio = pd.read_csv("17. Online Gaming.csv")
    #reemplazo nombres de la columna "Location" para que estén en español
    df_Gente_Sin_Oficio["Location"] = df_Gente_Sin_Oficio["Location"].replace("Other", "Otro")
    df_Gente_Sin_Oficio["Location"] = df_Gente_Sin_Oficio["Location"].replace("USA", "EE.UU")
    df_Gente_Sin_Oficio["Location"] = df_Gente_Sin_Oficio["Location"].replace("Europe", "Europa")
    # reemplazo los nombres de los géneros de juego para que estén en español
    df_Gente_Sin_Oficio["GameGenre"] = df_Gente_Sin_Oficio["GameGenre"].replace("Action", "Acción")
    df_Gente_Sin_Oficio["GameGenre"] = df_Gente_Sin_Oficio["GameGenre"].replace("Simulation", "Simulación")
    df_Gente_Sin_Oficio["GameGenre"] = df_Gente_Sin_Oficio["GameGenre"].replace("Strategy", "Estrategia")
    df_Gente_Sin_Oficio["GameGenre"] = df_Gente_Sin_Oficio["GameGenre"].replace("Sports", "Deportes")
    # reemplazo los nombres de compromiso para que estén en español
    df_Gente_Sin_Oficio["EngagementLevel"] = df_Gente_Sin_Oficio["EngagementLevel"].replace("Low", "Bajo")
    df_Gente_Sin_Oficio["EngagementLevel"] = df_Gente_Sin_Oficio["EngagementLevel"].replace("Medium", "Medio")
    df_Gente_Sin_Oficio["EngagementLevel"] = df_Gente_Sin_Oficio["EngagementLevel"].replace("High", "Alto")
    return df_Gente_Sin_Oficio 

df_Gente_Sin_Oficio = cargar_datos()

# Título y Descripción
st.title("🎮 Análisis de Juego en línea")
st.markdown("Con este Dashboard, lograrás indagar, analizar y comprender el comportamiento de los miles de usuarios que juegan diversos tipos de juegos en línea en varios continentes del mundo, explorando el tiempo invertido en ellos, la dedicación, y el género más popular por cada región.")

# sidebar
st.sidebar.title("🎮 Análisis de Juego en línea")
st.sidebar.markdown("🔴 Panel de Filtros")

# Locación
with st.sidebar.expander("📍 Locación Geográfica", expanded=True):
    ubicaciones_disponibles = df_Gente_Sin_Oficio['Location'].unique()
    ubicaciones_seleccionadas = st.multiselect(
        "Selecciona el Continente", 
        options=ubicaciones_disponibles,
        default=ubicaciones_disponibles[:4]
    )

# Género de juego
with st.sidebar.expander("🎮 Género de Juego", expanded=True):
    generos_disponibles = df_Gente_Sin_Oficio['GameGenre'].unique()
    generos_seleccionados = st.multiselect(
        "Selecciona los géneros de Juego",
        options=generos_disponibles,
        default=generos_disponibles.tolist()
    )

# Horas
with st.sidebar.expander("🕒 Horas de Juego", expanded=True):
    horas_min = float(df_Gente_Sin_Oficio["PlayTimeHours"].min())
    horas_max = float(df_Gente_Sin_Oficio["PlayTimeHours"].max())
    rango_horas = st.slider(
        "Selecciona las horas de Juego",
        min_value=horas_min,
        max_value=horas_max,
        value=(horas_min, horas_max)
    )

# filtrado
df_filtrado = df_Gente_Sin_Oficio[
    (df_Gente_Sin_Oficio["PlayTimeHours"] >= rango_horas[0]) & 
    (df_Gente_Sin_Oficio["PlayTimeHours"] <= rango_horas[1]) & 
    (df_Gente_Sin_Oficio["Location"].isin(ubicaciones_seleccionadas)) &
    (df_Gente_Sin_Oficio["GameGenre"].isin(generos_seleccionados))
]

# Métricas estáticas
st.subheader("Referencia Global")
with st.container(border=True):
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Base de Datos", f"{len(df_Gente_Sin_Oficio):,}")
    c2.metric("Promedio Global", f"{df_Gente_Sin_Oficio['PlayTimeHours'].mean():.1f} h")
    c3.metric("Frecuencia Base", f"{df_Gente_Sin_Oficio['SessionsPerWeek'].mean():.0f}")


st.markdown("---")

# se agregan tabs para mostrar diferentes análisis de los objetivos
tab1, tab2, tab3, tab4 = st.tabs(["🌎Análisis Regional", "📈Dedicación y Frecuencia", "📊Distribución de horas", "⏱️Tiempo de juego y Frecuencia Semanal"])

with tab1:
    st.subheader("🌎Géneros más populares por Región")

    # Agrupo por Ubicación y contamos la frecuencia de cada Género
    df_que_tan_virgenes_son = df_filtrado.groupby("Location")["GameGenre"].value_counts().reset_index(name="Usuarios")


    col_grafico, col_texto = st.columns([2, 1])

    # Creo el gráfico de barras
    with col_grafico:
        with st.container(border=True):
         if not df_que_tan_virgenes_son.empty:
          fig_que_tan_virgenes_son = px.bar(
          df_que_tan_virgenes_son, 
          x="Location", 
          y="Usuarios", 
          color="GameGenre", 
          barmode="relative", 
          title="Comparativa de Géneros por Ubicación",
          labels={"Location": "Región", "Usuarios": "Cantidad de Jugadores", "GameGenre": "Género"},
          color_discrete_sequence=px.colors.sequential.Blues_r,
          template="plotly_dark"
        )
        
         st.plotly_chart(fig_que_tan_virgenes_son, use_container_width=True)

    with col_texto:
            with st.container(border=True):
                st.markdown("### 📈 Análisis")
                st.write("Esta gráfica muestra cómo se distribuyen los géneros. En las regiones seleccionadas, observamos que:")
                for r in df_filtrado['Location'].unique()[:5]:
                    top = df_filtrado[df_filtrado['Location']==r]['GameGenre'].mode()[0]
                    st.caption(f"**{r}**: Domina el género {top}")
                   #Se filtra para el resúmen
                regiones_populares = df_filtrado['Location'].unique()[:5]
                cols = st.columns(len(regiones_populares))
                
        
with tab2:
    st.subheader("📈Comparativa de Compromiso y Sesiones Semanales")

    col_grafico, col_texto = st.columns([2, 1])
    with col_grafico:
        with st.container(border=True):
         if not df_filtrado.empty:
        # se crea el Box Plot
          fig_comp = px.box(
            df_filtrado,
            x="GameGenre",          
            y="SessionsPerWeek",    
            color="EngagementLevel",
            labels={"GameGenre": "Género de Juego",
                    "SessionsPerWeek": "Sesiones Semanales"},
            title="Distribución de Sesiones por Género y Nivel de Compromiso",
            # Ordeno las categorías de la leyenda para que tengan sentido
            category_orders={"EngagementLevel": ["Bajo", "Medio", "Alto"]},
            # Asigno colores
            color_discrete_map={
                "Bajo": "#EF553B", 
                "Medio": "#FECB52", 
                "Alto": "#00CC96"
            },
            template="plotly_dark"
        )
        
        # configuración de la leyenda
         fig_comp.update_layout(
            showlegend=True, 
            legend_title_text='Nivel de Compromiso', 
            legend=dict(
                orientation="h",    
                yanchor="bottom",
                y=1.02,             
                xanchor="right",
                x=1
            )
        )
        
         st.plotly_chart(fig_comp, use_container_width=True)
    with col_texto:
        with st.container(border=True):
            st.markdown("### 📈 Análisis de Sesiones")
            st.write("Se Observan tres secciones, cada una representa un rango de sesiones semanales, agrupados por el género del juego. Puede observarse que:")
            st.write("Los jugadores con nivel **Alto** de compromiso mantienen una frecuencia constante, independientemente del género.")
            st.write("Esto sugiere que la lealtad al juego no depende del tipo de contenido, sino de la mecánica de retención.")
    
with tab3:
    st.subheader("📊Distribución de las horas de juego, identificando niveles de dedicación")

    col_grafico, col_texto = st.columns([2, 1])

with col_grafico:
    with st.container(border=True):
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
    
   
          # Resumen
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Punto de Corte Casual", f"{q1:.1f} hrs")
            with col2:
              st.metric("Punto de Corte Hardcore", f"{q3:.1f} hrs")
            with col3:
              st.metric("Máximo de Horas", f"{df_filtrado['PlayTimeHours'].max():.1f} hrs")
     
     with col_texto:
        with st.container(border=True):
          st.markdown("### 📈 Análisis")
          st.write("Se observa que los jugadores que tienen más horas son 'hardcore' o intensos, mientras que los jugadores que tienen menos horas son moderados o casuales.")
          st.write("Esto nos dice que los jugadores intensos tienen un nivel muy alto de compromiso, nivel que se va degradando a medida que retrocedemos en el gráfico.")
            
with tab4:
    st.subheader("⏱️Frecuencia y Tiempo de juego (por región)")

    if not df_filtrado.empty:
        # Muestra para el gráfico, total para el cálculo
        df_muestra = df_filtrado.sample(n=min(1000, len(df_filtrado)), random_state=42)
        
        # Gráfico de Violín (optimizado para evitar lag)
        fig_regional = px.violin(
            df_muestra,
            x="SessionsPerWeek",
            y="PlayTimeHours",
            color="Location",
            labels= {"SessionsPerWeek": "Sesiones Semanales",
                     "PlayTimeHours": "Horas de Juego"},
            facet_col="Location",
            box=True,
            points="outliers", 
            template="plotly_dark",
            title="Distribución de Tiempo de Juego por Sesiones Semanales",
            category_orders={"Location": ubicaciones_seleccionadas}
        )
        fig_regional.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
        st.plotly_chart(fig_regional, use_container_width=True)

           
        st.markdown("---")

        # se prepara la tabla
        st.markdown("### Resumen de Correlación")
        # se filtra por grupos
        df_correlaciones = df_filtrado.groupby('Location').apply(
            lambda x: x['SessionsPerWeek'].corr(x['PlayTimeHours']),
            include_groups=False
        ).reset_index()

        df_correlaciones.columns = ['Región', 'Valor_Corr'] 
        # Se asigna etiqueta por fuerza de relación
        df_correlaciones['Fuerza de Relación'] = df_correlaciones['Valor_Corr'].apply(
            lambda r: "Nula / Inexistente" if abs(r) < 0.1 else ("Débil" if abs(r) < 0.3 else "Moderada")
        )

        df_correlaciones = df_correlaciones.rename(columns={'Valor_Corr': 'Coeficiente Pearson (r)'})
        # se muestra la tabla
        st.table(df_correlaciones)
        
        st.markdown("""
         Si los coeficientes son cercanos a 0, significa que el tiempo de juego 
        es independiente de cuántas veces se conectan a la semana. Esto sugiere que hay jugadores 
        que se conectan poco pero juegan sesiones larguísimas, y viceversa.
        """)

    else:
     st.image("https://www.shutterstock.com/image-vector/dino-google-chrome-abstract-game-600nw-2533959479.jpg", width=400)
     st.warning("Selecciona ubicaciones en la barra lateral.")

# Métricas que cambian con selección
st.subheader("Estadísticas de selección")

df_filtrado = df_Gente_Sin_Oficio[
    (df_Gente_Sin_Oficio["PlayTimeHours"] >= rango_horas[0]) & 
    (df_Gente_Sin_Oficio["PlayTimeHours"] <= rango_horas[1]) & 
    (df_Gente_Sin_Oficio["Location"].isin(ubicaciones_seleccionadas)) &
    (df_Gente_Sin_Oficio["GameGenre"].isin(generos_seleccionados))
]

with st.container(border=True):
    if not df_filtrado.empty:
        col1, col2, col3 = st.columns(3)
        
        col1.metric("Jugadores", f"{len(df_filtrado):,}", 
                  help="Número de personas que cumplen con tus filtros")
        
        avg_playtime = df_filtrado['PlayTimeHours'].mean()
        col2.metric("Horas", f"{avg_playtime:.1f} h")
        
        avg_freq = df_filtrado['SessionsPerWeek'].mean()
        col3.metric("Frecuencia", f"{avg_freq:.1f}")
    else:
        st.warning("No hay coincidencias para los filtros actuales.")

#  Expansor de los datos
with st.expander("Ver los datos de los jugadores completos"):
    st.dataframe(df_filtrado)