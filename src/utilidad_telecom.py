# Archivo externo: utils_telecom.py
import numpy as np
from scipy import stats
import joblib

def calcular_estadisticas_latencia(serie_latencia):
    """Calcula la media, desviación estándar e intervalo de confianza del 95% para la latencia."""
    media = np.mean(serie_latencia)
    std_dev = np.std(serie_latencia, ddof=1)
    n = len(serie_latencia)
    ic_95 = stats.t.interval(0.95, df=n-1, loc=media, scale=stats.sem(serie_latencia))
    return {"media": media, "desv_std": std_dev, "ic_95": ic_95}

def guardar_modelo_artefacto(objeto, nombre_archivo):
    """Guarda un artefacto o resultado usando joblib para asegurar reproducibilidad."""
    joblib.dump(objeto, nombre_archivo)
    print(f"Artefacto guardado exitosamente como: {nombre_archivo}")