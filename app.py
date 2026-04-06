# Importación de librerías necesarias
import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuración de la página
st.set_page_config(page_title="Dashboard del Online Gaming", layout="wide")

# 2. Carga de datos
@   st.cache_data
def cargar_datos():
    df_Gente_Sin_Oficio = pd.read_csv("17. Online Gaming.csv")
    return df_Gente_Sin_Oficio 

df_Gente_Sin_Oficio = cargar_datos()

# 3. Título del dashboard
st.title("Análisis del Online Gaming")
st.markdown("Comportamiento de los jugadores en función de la ubicación geográfica y el género del videojuego: Horas de uso y frecuencia de sesiones")

