# 📊 Documentación Técnica: Monitoreo y Desempeño Operacional — RedConecta Telecom S. A.

## 📌 Contexto y Objetivos del Proyecto

El presente proyecto responde a la necesidad operacional de **RedConecta Telecom S. A.** de transicionar desde un modelo de gestión de red reactivo hacia uno basado en evidencia analítica y datos cuantitativos. 

### Objetivos Principales:
1. **Evaluar el Desempeño Operacional:** Analizar las métricas clave de la infraestructura (tráfico de datos, latencia, tickets de soporte y tiempos de resolución) segmentadas por región (*Centro, Norte, Sur*) y tipo de servicio (*Empresas, Internet Hogar, Móvil*).
2. **Identificar Patrones de Calidad de Servicio:** Determinar la tasa de cumplimiento de los acuerdos de nivel de servicio (SLA) e identificar los cuellos de botella técnicos.
3. **Asegurar la Reproducibilidad:** Construir un flujo de trabajo modular y documentado respaldado en un repositorio control de versiones en **Git** y un cuadro de mando interactivo en **Streamlit**.

---

## 📁 Estructura del Repositorio

El proyecto se encuentra organizado bajo una estructura estándar de ciencia de datos, garantizando la separación de responsabilidades entre datos de entrada, código fuente modular, scripts de despliegue y artefactos de salida:

```text
redconecta-telecom-analytics/
│
├── data/
│   └── dataset_set_D_telecomunicaciones.xlsx   # Dataset operacional fuente
│
├── outputs/
│   ├── output_latencia_stats.joblib          # Artefacto estadístico serializado
│   ├── output_soporte_tecnico.csv            # Salida segmentada para Soporte Técnico
│   ├── output_experiencia_clientes.csv       # Salida segmentada para Experiencia de Clientes
│   └── grafico_soporte_resolucion.png        # Gráfico exploratorio generado por script
│
├── src/
│   ├── script_principal.py                   # Script de orquestación y procesamiento
│   ├── utilidad_telecom.py                  # Módulo de funciones estadísticas y helpers
│   └── app_dashboard.py                     # Aplicación interactiva Streamlit
│
└── README.md                                 # Documentación técnica general
```

---

## 🔧 Descripción de Componentes y Código Fuente

### 1. Módulo Auxiliar (`src/utilidad_telecom.py`)
Contiene funciones desacopladas reutilizables que hacen uso de las librerías `numpy`, `scipy` y `joblib`:
* `calcular_estadisticas_latencia(serie_latencia)`: Calcula la media, desviación estándar muestral e intervalo de confianza al 95% ($t\text{-student}$) para series numéricas.
* `guardar_modelo_artefacto(objeto, nombre_archivo)`: Serializa y persiste modelos o diccionarios estadísticos en disco para asegurar la reproductibilidad.

### 2. Script Principal de Procesamiento (`src/script_principal.py`)
Ejecuta la ingesta, transformación, cálculo analítico y generación automática de los archivos entregables:
* Carga el dataset desde `data/dataset_set_D_telecomunicaciones.xlsx`.
* Calcula resúmenes por tipo de servicio y métricas inferenciales.
* Exporta los datos formateados a `outputs/output_soporte_tecnico.csv` y `outputs/output_experiencia_clientes.csv`.
* Genera la visualización gráfica `grafico_soporte_resolucion.png` y serializa `output_latencia_stats.joblib`.

### 3. Dashboard Exploratorio Interactivo (`src/app_dashboard.py`)
Construido con **Streamlit**, provee una interfaz web gráfica con:
* **Filtros dinámicos en barra lateral:** Selección múltiple por *Región* y *Tipo de Servicio*.
* **Tarjetas de KPIs:** Latencia promedio ($\text{ms}$), total de tickets, tiempo promedio de resolución ($\text{hrs}$) y $\%$ de cumplimiento de SLA.
* **Gráficos interactivos:** Diagramas de barras (`sns.barplot`) y diagramas de caja (`sns.boxplot`).

---

## 📊 Principales Resultados Operacionales

### Resumen Consolidado: Área de Soporte Técnico

| Región | Tipo de Servicio | Promedio Incidencias | Promedio Tickets Soporte | Tiempo Promedio Resolución (hr) |
| :--- | :--- | :---: | :---: | :---: |
| **Centro** | Empresas | 14.29 | 28.38 | 27.95 |
| **Centro** | Internet Hogar | 12.52 | 36.63 | 21.67 |
| **Centro** | Móvil | 10.65 | 28.65 | 24.26 |
| **Norte** | Empresas | 12.72 | 26.94 | 20.57 |
| **Norte** | Internet Hogar | 13.83 | 29.87 | 22.48 |
| **Norte** | Móvil | 12.00 | 35.29 | 27.28 |
| **Sur** | Empresas | 13.77 | 34.00 | 27.03 |
| **Sur** | Internet Hogar | 16.36 | 33.36 | 30.60 |
| **Sur** | Móvil | 14.61 | 28.61 | 27.03 |

*Nota.* Cuadro resumen de carga operativa y tiempos de respuesta. Elaboración propia a partir del dataset procesado (2026).

### Hallazgos Clave:
1. **Brecha de SLA:** El cumplimiento global del SLA se encuentra por debajo del $50\%$ ($48.4\%$ en Empresas, $46.8\%$ en Internet Hogar y $49.1\%$ en Móvil).
2. **Cuellos de Botella Regionales:** La zona **Sur** en el servicio de **Internet Hogar** registra el mayor tiempo promedio de resolución de incidencias ($30.60\text{ horas}$) y la mayor tasa de incidencias reportadas ($16.36$).
3. **Latencia Operacional:** La latencia promedio global se ubica en $64.86\text{ ms}$ ($\text{IC } 95\%: [60.28, 69.44]\text{ ms}$), con valores máximos de $119.9\text{ ms}$, sobrepasando los umbrales ideales de calidad de red.

---

## 🛠️ Evaluación de Calidad de Datos e Impacto Operativo

### Evaluación Técnica del Dataset:
* **Integridad:** 200 registros completos. No presenta valores nulos ni duplicados explícitos.
* **Coherencia de Dominio:** Rangos de tráfico ($50.5 - 497.9\text{ GB}$), latencia ($11.2 - 119.9\text{ ms}$) y tiempos de resolución ($1.2 - 47.2\text{ hrs}$) dentro de límites operacionales válidos.
* **Limitaciones Identificadas:** El dataset representa un corte estático/sintético acotado a 200 registros, lo que impide análisis de series de tiempo de alta frecuencia u ondas de congestión por horario punta.

### Consecuencias Operativas de Datos de Baja Confiabilidad:
* **Asignación Ineficiente de Cuadrillas:** Reportes con latencia o tickets mal categorizados llevarían a despliegue innecesario de soporte en zonas de baja prioridad.
* **Multas y Sanciones por SLA:** Indicadores inexactos ocultan incumplimientos contractuales con clientes corporativos, generando pérdidas financieras directas.

---

## 🚀 Guía de Instalación y Ejecución

### 1. Clonar el repositorio e instalar dependencias
```bash
git clone https://github.com/kikevike/redconecta-telecom-analytics-S8_TAREA.git
cd redconecta-telecom-analytics-S8_TAREA
pip install pandas numpy scipy joblib matplotlib seaborn streamlit openpyxl
```

### 2. Ejecutar el Procesamiento Principal
Para procesar la data y generar todos los artefactos en la carpeta `outputs/`:
```bash
python src/script_principal.py
```

### 3. Iniciar el Dashboard Exploratorio
Para desplegar la aplicación interactiva en el navegador web:
```bash
streamlit run src/app_dashboard.py
```

