# =================================================
# Proyecto: redconecta-telecom-analytics-S8_TAREA
# =================================================

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Informar funciones /src/utilidad_telecom.py
from utilidad_telecom import calcular_estadisticas_latencia, guardar_modelo_artefacto

# directorios
directorio_actual = os.path.dirname(os.path.abspath(__file__)) # Ruta de /src/
raiz_proyecto = os.path.dirname(directorio_actual)             # Directorio raíz del proyecto

ruta_data = os.path.join(raiz_proyecto, 'data', 'dataset_set_D_telecomunicaciones.xlsx')
ruta_outputs = os.path.join(raiz_proyecto, 'outputs')

os.makedirs(ruta_outputs, exist_ok=True)

# Carga de datos
if not os.path.exists(ruta_data):
    print(f"[ERROR] No se encuentra el dataset en la ruta: {ruta_data}")
else:
    df = pd.read_excel(ruta_data)
    print("Dataset de RedConecta Telecom S. A. cargado exitosamente.\n")

    # Resumen por tipo de servicio
    resumen_servicio = df.groupby('tipo_servicio').agg({
        'trafico_datos_gb': 'mean',
        'latencia_ms': 'mean',
        'tickets_soporte': 'sum',
        'tiempo_resolucion_hr': 'mean'
    }).reset_index()

    print("Resumen Operacional por Servicio:")
    print(resumen_servicio)
    print("-" * 50)

    # Análisis usando el módulo externo
    stats_latencia = calcular_estadisticas_latencia(df['latencia_ms'])
    print("Estadísticas de Latencia (ms):", stats_latencia)

    # Guardar en /outputs/
    ruta_artefacto = os.path.join(ruta_outputs, 'output_latencia_stats.joblib')
    guardar_modelo_artefacto(stats_latencia, ruta_artefacto)
    print("-" * 50)

    # genera archivo para soporte técnico
    df_soporte = df[[
        'fecha_registro', 
        'region', 
        'tipo_servicio', 
        'incidencias_reportadas', 
        'tickets_soporte', 
        'tiempo_resolucion_hr'
    ]].copy()

    ruta_soporte = os.path.join(ruta_outputs, 'output_soporte_tecnico.csv')
    df_soporte.to_csv(ruta_soporte, index=False, encoding='utf-8-sig')
    print(f"[OK] Archivo de Soporte Técnico generado en: {ruta_soporte}")

    # genera archivo para experiencia de clientes
    df_clientes = df[[
        'fecha_registro', 
        'tipo_servicio', 
        'clientes_afectados', 
        'latencia_ms', 
        'cumplimiento_sla'
    ]].copy()

    ruta_clientes = os.path.join(ruta_outputs, 'output_experiencia_clientes.csv')
    df_clientes.to_csv(ruta_clientes, index=False, encoding='utf-8-sig')
    print(f"[OK] Archivo de Experiencia de Clientes generado en: {ruta_clientes}")
    print("-" * 50)

    # Genera Gráficos para el Dashboard (/outputs/)
    sns.set_theme(style="whitegrid")
    
    # grafico de Tiempo de Resolución
    plt.figure(figsize=(9, 5))
    sns.barplot(data=df, x='region', y='tiempo_resolucion_hr', hue='tipo_servicio', errorbar=None, palette="Blues")
    plt.title('Tiempo Promedio de Resolución por Región y Tipo de Servicio')
    plt.xlabel('Región')
    plt.ylabel('Tiempo de Resolución (horas)')
    plt.tight_layout()
    ruta_grafico = os.path.join(ruta_outputs, 'grafico_soporte_resolucion.png')
    plt.savefig(ruta_grafico)
    plt.close()

    print(f"[OK] Gráfico exploratorio guardado en: {ruta_grafico}")

    # Agrupación y cálculo para la tabla del Área de Soporte Técnico
    tabla_soporte = df.groupby(['region', 'tipo_servicio']).agg({
        'incidencias_reportadas': 'mean',
        'tickets_soporte': 'mean',
        'tiempo_resolucion_hr': 'mean'
    }).reset_index()

    # Redondear valor numérico
    tabla_soporte = tabla_soporte.round(2)

    print("--- TABLA RESUMEN: ÁREA DE SOPORTE TÉCNICO ---")
    print(tabla_soporte.to_string(index=False))

