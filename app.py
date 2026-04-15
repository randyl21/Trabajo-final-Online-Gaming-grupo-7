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
st.markdown("¡Bienvenido a nuestro Dashboard!")
st.markdown("Aquí, lograrás indagar, analizar y comprender el comportamiento de miles de usuarios que juegan en línea diversos géneros de juego en algunos continentes del mundo, explorando el tiempo, la dedicación invertida en ellos, así como también el género más popular por cada región.")

# sidebar
st.sidebar.title("🎮 Análisis de Juego en Línea")
st.sidebar.markdown("🔴 Panel de Filtros")

# Desplegable interactivo para la locación
with st.sidebar.expander("📍 Locación Geográfica", expanded=True):
    ubicaciones_disponibles = df_Gente_Sin_Oficio['Location'].unique()
    ubicaciones_seleccionadas = st.multiselect(
        "Selecciona el Continente", 
        options=ubicaciones_disponibles,
        default=ubicaciones_disponibles[:4]
    )

# Desplegable interactivo para el Género de juego
with st.sidebar.expander("🎮 Género de Juego", expanded=True):
    generos_disponibles = df_Gente_Sin_Oficio['GameGenre'].unique()
    generos_seleccionados = st.multiselect(
        "Selecciona los géneros de Juego",
        options=generos_disponibles,
        default=generos_disponibles.tolist()
    )

# Slider para el rango de horas de juego
with st.sidebar.expander("🕒 Horas de Juego", expanded=True):
    horas_min = float(df_Gente_Sin_Oficio["PlayTimeHours"].min())
    horas_max = float(df_Gente_Sin_Oficio["PlayTimeHours"].max())
    rango_horas = st.slider(
        "Selecciona las horas de Juego",
        min_value=horas_min,
        max_value=horas_max,
        value=(horas_min, horas_max)
    )
 # Se agregan autores del trabajo
st.sidebar.markdown("🎮 Análisis por: Aziel González y Estefani Carreño")

# filtrado importante
df_filtrado = df_Gente_Sin_Oficio[
    (df_Gente_Sin_Oficio["PlayTimeHours"] >= rango_horas[0]) & 
    (df_Gente_Sin_Oficio["PlayTimeHours"] <= rango_horas[1]) & 
    (df_Gente_Sin_Oficio["Location"].isin(ubicaciones_seleccionadas)) &
    (df_Gente_Sin_Oficio["GameGenre"].isin(generos_seleccionados))
]

# generación de las Métricas estáticas con los datos globales
st.subheader("Referencia Global")
with st.container(border=True):
    c1, c2, c3 = st.columns(3)
    # Total de jugadores (en general)
    c1.metric("Total de Jugadores", f"{len(df_Gente_Sin_Oficio):,}")
    # Horas en promedio
    c2.metric("Promedio Global de Horas", f"{df_Gente_Sin_Oficio['PlayTimeHours'].mean():.1f} h")
    # Promedio de las sesiones semanales
    c3.metric("Promedio Frecuencia (sesiones semanales)", f"{df_Gente_Sin_Oficio['SessionsPerWeek'].mean():.1f}")


st.markdown("---")

# se agregan tabs para mostrar diferentes análisis de los objetivos
tab1, tab2, tab3, tab4 = st.tabs(["🌎Análisis Regional", "📈Dedicación y Frecuencia", "📊Distribución de horas", "⏱️Tiempo de juego y Frecuencia Semanal"])
 # Objetivo 1: Identificar los géneros más populares por región
with tab1:
    st.subheader("🌎 Géneros más populares por Región")

    if not df_filtrado.empty:
        df_counts = df_filtrado.groupby(["Location", "GameGenre"]).size().reset_index(name="Usuarios")
        # columnas para organizar
        col_grafico, col_texto = st.columns([2, 1])
        # para el gráfico
        with col_grafico:
            with st.container(border=True):
                fig_regional = px.bar(
                    df_counts, 
                    x="Location", y="Usuarios", color="GameGenre", 
                    barmode="relative", 
                    title="Comparativa de Géneros por Ubicación",
                    labels={"Location": "Región", "Usuarios": "Cantidad de Jugadores", "GameGenre": "Género"},
                    color_discrete_sequence=px.colors.sequential.Blues_r,
                    template="plotly_dark"
                )
                st.plotly_chart(fig_regional, use_container_width=True)
        # texto desplegable con análisis
        with col_texto:
            with st.container(border=True):
                st.markdown("### 📊 Tops por región")
                # se crean tabs para mostrar los géneros más jugados y menos jugados por ubicación
                tab_top, tab_bottom = st.tabs(["🏆 Más Jugados", "⚠️ Menos Jugados"])
                
                regiones_ordenadas = sorted(df_filtrado['Location'].unique())

                with tab_top:
                    st.write("Más jugados:")
                    for r in regiones_ordenadas:
                        top_genre = df_filtrado[df_filtrado['Location'] == r]['GameGenre'].mode()[0]
                        count_top = len(df_filtrado[(df_filtrado['Location'] == r) & (df_filtrado['GameGenre'] == top_genre)])
                        st.caption(f"**{r}**: {top_genre} ({count_top})")
                
                with tab_bottom:
                    st.write("Menos jugados:")
                    for r in regiones_ordenadas:
                        counts = df_filtrado[df_filtrado['Location'] == r]['GameGenre'].value_counts()
                        bottom_genre = counts.index[-1]
                        count_bottom = counts.values[-1]
                        st.caption(f"**{r}**: {bottom_genre} ({count_bottom})")
    else:
        st.error("⚠️ Selecciona al menos una región para ver el desglose.")
    #Objetivo 2: Comparar las horas de dedicación y frecuencia de sesiones semanales entre distintos géneros de videojuegos.
with tab2:
    st.subheader("📈Comparativa de Compromiso y Sesiones Semanales")
    if not df_filtrado.empty:
         # columnas para organizar x2
        col_grafico, col_texto = st.columns([2, 1])
        with col_grafico:
            with st.container(border=True):
                fig_comp = px.box(
                    df_filtrado, x="GameGenre", y="SessionsPerWeek", color="EngagementLevel",
                    labels={"GameGenre": "Género de Juego", "SessionsPerWeek": "Sesiones Semanales", "EngagementLevel": "Nivel de Compromiso"},
                    title="Distribución de Sesiones por Género",
                    category_orders={"EngagementLevel": ["Bajo", "Medio", "Alto"]},
                    color_discrete_map={"Bajo": "#EF553B", "Medio": "#FECB52", "Alto": "#00CC96"},
                    template="plotly_dark"
                )
                st.plotly_chart(fig_comp, use_container_width=True)
        with col_texto:
            with st.container(border=True):
             with st.expander("📈 Información", expanded=True):
                st.write("Se Observan tres secciones, cada una representa un rango de sesiones semanales, agrupados por el género del juego.")

    else:
        st.error("⚠️ No hay datos para mostrar la comparativa de compromiso. Revisa los filtros.")

with tab3:
    st.subheader("📊Distribución de horas y niveles de dedicación")
    if not df_filtrado.empty:
        q1 = df_filtrado['PlayTimeHours'].quantile(0.25)
        q3 = df_filtrado['PlayTimeHours'].quantile(0.75)

        def evaluar_dedicacion(h):
            if h <= q1: return "Casual"
            if h <= q3: return "Moderado"
            return "Intenso / Hardcore"

        df_eval = df_filtrado.copy()
        df_eval["Nivel"] = df_eval["PlayTimeHours"].apply(evaluar_dedicacion)
        # columnas para organizar x3
        col_grafico, col_texto = st.columns([2, 1])
        with col_grafico:
            with st.container(border=True):
                fig_eval = px.histogram(
                    df_eval, x="PlayTimeHours", color="Nivel", marginal="box",
                    labels={"PlayTimeHours": "Horas de Juego"},
                    title="Distribución de Horas y Segmentos",
                    color_discrete_map={"Casual": "#EF553B", "Moderado": "#FECB52", "Intenso / Hardcore": "#00CC96"},
                    template="plotly_dark", barmode="overlay"
                )
                st.plotly_chart(fig_eval, use_container_width=True)
        
        with col_texto:
            with st.container(border=True):
                st.metric("Corte Casual", f"{q1:.1f} hrs")
                st.metric("Corte Hardcore", f"{q3:.1f} hrs")
                with st.expander("📈 Información", expanded=True):
                  st.write("Se observa que los jugadores que tienen más horas son 'hardcore' o intensos, mientras que los jugadores que tienen menos horas son moderados o casuales.")

    else:
        st.error("⚠️ Selecciona un rango de horas o ubicación válida para ver la distribución.")
        
with tab4:
    st.subheader("⏱️Frecuencia y Tiempo de juego (por región)")
    
    # columnas para organizar x4
    if not df_filtrado.empty:
        col_grafico, col_texto = st.columns([2, 1]) 

        with col_grafico:
            with st.container(border=True):
                df_muestra = df_filtrado.sample(n=min(1000, len(df_filtrado)), random_state=42)
                
                # Se genera gráfico de dispersión ordenado por ubicación
                fig_regional = px.scatter(
                    df_muestra,
                    x="SessionsPerWeek",
                    y="PlayTimeHours",
                    color="Location",
                    facet_col="Location",
                    labels={
                        "SessionsPerWeek": "Sesiones Sem.",
                        "PlayTimeHours": "Horas de Juego",
                        "Location": "Ubicación"
                    },
                    opacity=0.6,
                    template="plotly_dark",
                    title="Relación entre Sesiones Semanales y Horas de Juego",
                    category_orders={"Location": ubicaciones_seleccionadas}
                )

                # Ajuste de títulos de las facetas y visualización
                fig_regional.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
                st.plotly_chart(fig_regional, use_container_width=True)

                st.markdown("### Resumen de Correlación")
                # Para una mejor comprensión del resultado.
                df_correlaciones = df_filtrado.groupby('Location').apply(
                    lambda x: x['SessionsPerWeek'].corr(x['PlayTimeHours']),
                    include_groups=False
                ).reset_index()

                df_correlaciones.columns = ['Región', 'Valor_Corr'] 
                df_correlaciones['Fuerza de Relación'] = df_correlaciones['Valor_Corr'].apply(
                    lambda r: "Nula / Inexistente" if abs(r) < 0.1 else ("Débil" if abs(r) < 0.3 else "Moderada")
                )

                df_correlaciones = df_correlaciones.rename(columns={'Valor_Corr': 'Coeficiente Pearson (r)'})
                st.table(df_correlaciones)    

        with col_texto:
            with st.container(border=True):
                
                with st.expander("📈 Información", expanded=True):
                    st.markdown("""Se presenta un gráfico de dispersión agrupado por región, que muestra la relación individual de cada usuario entre sus sesiones semanales y horas de juego.
            """)
                    st.write("""Para este análisis, se realizan cálculos de correlación de Pearson para cuantificar la fuerza de dicha relación.
                                 """)
    else:
        st.error("⚠️ No hay datos suficientes para mostrar el análisis. Ajusta los filtros en la sidebar.")


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
        
        col1.metric("Jugadores seleccionados", f"{len(df_filtrado):,}", 
                  help="Número de personas que cumplen con tus filtros")
        
        avg_playtime = df_filtrado['PlayTimeHours'].mean()
        col2.metric("Horas seleccionadas", f"{avg_playtime:.1f} h")
        
        avg_freq = df_filtrado['SessionsPerWeek'].mean()
        col3.metric("Frecuencia de sesiones", f"{avg_freq:.1f}")
    else:
        st.warning("No hay coincidencias para los filtros actuales.")

#  Expansor de los datos
with st.expander("Ver los datos de los jugadores completos"):
    st.dataframe(df_filtrado)