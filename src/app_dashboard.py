import os
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Configuración de la página del Dashboard
st.set_page_config(page_title="Dashboard RedConecta Telecom", page_icon="📊", layout="wide")

st.title("📊 Dashboard Exploratorio: Monitoreo y Desempeño Operacional")
st.markdown("**Empresa:** RedConecta Telecom S. A. | **Objetivo:** Analizar latencia, tickets de soporte y cumplimiento de SLA.")


directorio_actual = os.path.dirname(os.path.abspath(__file__)) # Ruta de /src/ o actual
raiz_proyecto = os.path.dirname(directorio_actual)             # Directorio raíz del proyecto
ruta_data = os.path.join(raiz_proyecto, 'data', 'dataset_set_D_telecomunicaciones.xlsx')

# 2. Carga de datos con caché de Streamlit
@st.cache_data
def cargar_datos():
    if not os.path.exists(ruta_data):
        st.error(f"No se encuentra el dataset en la ruta: {ruta_data}")
        return pd.DataFrame()
    return pd.read_excel(ruta_data)

df = cargar_datos()

# 3. Creación de Filtros en la Barra Lateral (Sidebar)
st.sidebar.header("Filtros de Análisis")

# Filtro por Región
regiones_disponibles = df['region'].unique().tolist()
region_seleccionada = st.sidebar.multiselect("Seleccione la(s) Región(es):", regiones_disponibles, default=regiones_disponibles)

# Filtro por Tipo de Servicio
servicios_disponibles = df['tipo_servicio'].unique().tolist()
servicio_seleccionado = st.sidebar.multiselect("Seleccione el Tipo de Servicio:", servicios_disponibles, default=servicios_disponibles)

# Filtrado del DataFrame según los selectores
df_filtrado = df[(df['region'].isin(region_seleccionada)) & (df['tipo_servicio'].isin(servicio_seleccionado))]

# 4. Métricas Principales (KPIs) en la parte superior
st.subheader("Indicadores Clave de Desempeño (KPIs)")
col1, col2, col3, col4 = st.columns(4)

with col1:
    latencia_prom = df_filtrado['latencia_ms'].mean()
    st.metric("Latencia Promedio", f"{latencia_prom:.2f} ms")

with col2:
    total_tickets = df_filtrado['tickets_soporte'].sum()
    st.metric("Total Tickets Soporte", f"{total_tickets:,}")

with col3:
    tiempo_res_prom = df_filtrado['tiempo_resolucion_hr'].mean()
    st.metric("Tiempo Prom. Resolución", f"{tiempo_res_prom:.2f} hrs")

with col4:
    # Cálculo del porcentaje de cumplimiento de SLA
    cumple_sla = (df_filtrado['cumplimiento_sla'] == 'Cumple').mean() * 100
    st.metric("Cumplimiento SLA", f"{cumple_sla:.1f}%")

st.markdown("---")

# 5. Visualizaciones Gráficas
st.subheader("Análisis Gráfico del Desempeño")

col_g1, col_g2 = st.columns(2)

with col_g1:
    st.markdown("##### Tiempo de Resolución por Región y Servicio")
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(data=df_filtrado, x='region', y='tiempo_resolucion_hr', hue='tipo_servicio', ax=ax, palette="Blues", errorbar=None)
    ax.set_xlabel("Región")
    ax.set_ylabel("Tiempo Resolución (hr)")
    st.pyplot(fig)

with col_g2:
    st.markdown("##### Distribución de Latencia vs SLA")
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    sns.boxplot(data=df_filtrado, x='cumplimiento_sla', y='latencia_ms', hue='cumplimiento_sla', ax=ax2, palette="Set2", legend=False)
    ax2.set_xlabel("Estado de SLA")
    ax2.set_ylabel("Latencia (ms)")
    st.pyplot(fig2)

# 6. Tabla de Datos Filtrados
st.markdown("---")
st.subheader("Vista Detallada de los Datos Operacionales Filtrados")
st.dataframe(df_filtrado)