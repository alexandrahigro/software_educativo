"""
Módulo de Inteligencia Artificial para análisis de madurez digital.
Implementa clasificación con Scikit-learn y análisis con Pandas.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os
from datetime import datetime
import logging

from django.conf import settings
from .models import (
    ResultadoEncuesta, ResultadoIndicador, Indicador, 
    ModeloIA, PrediccionIA, Respuesta
)

logger = logging.getLogger(__name__)

class AnalizadorMadurezDigital:
    """
    Analizador de madurez digital con ML.
    Utiliza RandomForest para clasificar niveles de madurez.
    """
    
    def __init__(self):
        self.modelo = None
        self.scaler = StandardScaler()
        self.indicadores_orden = []
        self.niveles_madurez = ['Inicial', 'En desarrollo', 'Competente', 'Avanzado', 'Experto']
        self.model_path = os.path.join(settings.BASE_DIR, 'ml_models')
        
        # Crear directorio de modelos si no existe
        os.makedirs(self.model_path, exist_ok=True)
    
    def extraer_datos_entrenamiento(self):
        """
        Extrae datos de la BD para entrenamiento del modelo.
        Convierte ResultadoIndicador en un dataset de Pandas.
        """
        # Obtener todos los resultados con sus indicadores
        resultados = ResultadoEncuesta.objects.prefetch_related(
            'valores_indicadores__indicador'
        ).filter(
            valores_indicadores__isnull=False
        ).distinct()
        
        if not resultados.exists():
            logger.warning("No hay datos suficientes para entrenamiento")
            return None, None
        
        # Crear lista de datos
        datos = []
        labels = []
        
        # Obtener lista ordenada de indicadores
        self.indicadores_orden = list(
            Indicador.objects.values_list('nombre', flat=True).order_by('id')
        )
        
        for resultado in resultados:
            # Crear vector de características por indicador
            caracteristicas = {}
            
            for valor_ind in resultado.valores_indicadores.all():
                caracteristicas[valor_ind.indicador.nombre] = valor_ind.valor
            
            # Solo incluir si tiene todos los indicadores
            if len(caracteristicas) == len(self.indicadores_orden):
                # Crear fila de datos en orden consistente
                fila = [caracteristicas.get(ind, 0) for ind in self.indicadores_orden]
                
                # Añadir características adicionales
                fila.extend([
                    resultado.puntuacion_global,
                    len(resultado.valores_indicadores.all()),  # cantidad de indicadores evaluados
                ])
                
                datos.append(fila)
                labels.append(resultado.nivel_madurez)
        
        if not datos:
            logger.warning("No se pudieron extraer datos válidos para entrenamiento")
            return None, None
        
        # Crear DataFrame
        columnas = self.indicadores_orden + ['puntuacion_global', 'num_indicadores']
        df = pd.DataFrame(datos, columns=columnas)
        
        logger.info(f"Datos extraídos: {len(df)} muestras, {len(columnas)} características")
        
        return df, labels
    
    def entrenar_modelo(self, test_size=0.2, random_state=42):
        """
        Entrena el modelo de clasificación de madurez digital.
        """
        logger.info("Iniciando entrenamiento del modelo...")
        
        # Extraer datos
        X, y = self.extraer_datos_entrenamiento()
        if X is None:
            return {"error": "No hay datos suficientes para entrenar el modelo"}
        
        # Dividir en entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        # Normalizar características
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Entrenar RandomForest
        self.modelo = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=random_state,
            class_weight='balanced'  # Balancear clases automáticamente
        )
        
        self.modelo.fit(X_train_scaled, y_train)
        
        # Evaluar modelo
        y_pred = self.modelo.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        reporte_clasificacion = classification_report(y_test, y_pred, output_dict=True)
        
        # Guardar modelo entrenado
        self.guardar_modelo()
        
        # Guardar info del modelo en BD
        modelo_bd = ModeloIA.objects.create(
            nombre_modelo="RandomForest_MadurezDigital",
            version=f"v{datetime.now().strftime('%Y%m%d_%H%M')}",
            metrica_precision=round(accuracy, 4),
            ruta_fichero=os.path.join(self.model_path, 'modelo_madurez.pkl')
        )
        
        logger.info(f"Modelo entrenado con precisión: {accuracy:.4f}")
        
        return {
            "modelo_id": modelo_bd.id,
            "precision": accuracy,
            "num_muestras_entrenamiento": len(X_train),
            "num_muestras_prueba": len(X_test),
            "reporte_detallado": reporte_clasificacion,
            "importancia_caracteristicas": dict(
                zip(X.columns, self.modelo.feature_importances_)
            )
        }
    
    def guardar_modelo(self):
        """Guardar modelo entrenado en disco."""
        modelo_data = {
            'modelo': self.modelo,
            'scaler': self.scaler,
            'indicadores_orden': self.indicadores_orden,
            'niveles_madurez': self.niveles_madurez
        }
        
        ruta_modelo = os.path.join(self.model_path, 'modelo_madurez.pkl')
        joblib.dump(modelo_data, ruta_modelo)
        logger.info(f"Modelo guardado en: {ruta_modelo}")
    
    def cargar_modelo(self):
        """Cargar modelo desde disco."""
        ruta_modelo = os.path.join(self.model_path, 'modelo_madurez.pkl')
        
        if not os.path.exists(ruta_modelo):
            logger.warning("No existe modelo guardado, entrenando nuevo modelo...")
            resultado_entrenamiento = self.entrenar_modelo()
            if "error" in resultado_entrenamiento:
                return False
        
        try:
            modelo_data = joblib.load(ruta_modelo)
            self.modelo = modelo_data['modelo']
            self.scaler = modelo_data['scaler']
            self.indicadores_orden = modelo_data['indicadores_orden']
            self.niveles_madurez = modelo_data['niveles_madurez']
            logger.info("Modelo cargado exitosamente")
            return True
        except Exception as e:
            logger.error(f"Error cargando modelo: {e}")
            return False
    
    def predecir_madurez(self, valores_indicadores, resultado_id=None):
        """
        Predecir nivel de madurez digital basado en valores de indicadores.
        
        Args:
            valores_indicadores: dict con {nombre_indicador: valor}
            resultado_id: ID del resultado para guardar predicción
        
        Returns:
            dict con nivel predicho y probabilidades
        """
        if not self.cargar_modelo():
            return {"error": "No se pudo cargar el modelo de IA"}
        
        # Crear vector de características
        caracteristicas = []
        for indicador in self.indicadores_orden:
            caracteristicas.append(valores_indicadores.get(indicador, 0))
        
        # Añadir características adicionales
        puntuacion_global = np.mean(list(valores_indicadores.values()))
        caracteristicas.extend([
            puntuacion_global,
            len(valores_indicadores)
        ])
        
        # Convertir a array y normalizar
        X = np.array(caracteristicas).reshape(1, -1)
        X_scaled = self.scaler.transform(X)
        
        # Realizar predicción
        nivel_predicho = self.modelo.predict(X_scaled)[0]
        probabilidades = self.modelo.predict_proba(X_scaled)[0]
        
        # Crear diccionario de probabilidades por nivel
        prob_por_nivel = dict(zip(self.modelo.classes_, probabilidades))
        probabilidad_maxima = prob_por_nivel.get(nivel_predicho, 0)
        
        # Guardar predicción en BD si se proporciona resultado_id
        if resultado_id:
            try:
                resultado = ResultadoEncuesta.objects.get(id=resultado_id)
                modelo_bd = ModeloIA.objects.order_by('-fecha_entrenamiento').first()
                
                if modelo_bd:
                    PrediccionIA.objects.create(
                        modelo=modelo_bd,
                        resultado=resultado,
                        nivel_pred=nivel_predicho,
                        probabilidad=probabilidad_maxima
                    )
            except Exception as e:
                logger.error(f"Error guardando predicción: {e}")
        
        return {
            "nivel_predicho": nivel_predicho,
            "probabilidad": round(probabilidad_maxima, 4),
            "probabilidades_todas": {
                nivel: round(prob, 4) 
                for nivel, prob in prob_por_nivel.items()
            },
            "puntuacion_estimada": round(puntuacion_global, 2),
            "confianza": "alta" if probabilidad_maxima > 0.7 else "media" if probabilidad_maxima > 0.5 else "baja"
        }
    
    def analizar_tendencias(self, institucion_id=None):
        """
        Analizar tendencias de madurez digital usando Pandas.
        """
        # Filtrar por institución si se especifica
        filtro = {}
        if institucion_id:
            filtro['institucion_id'] = institucion_id
        
        # Obtener resultados
        resultados = ResultadoEncuesta.objects.filter(**filtro).prefetch_related(
            'valores_indicadores__indicador'
        )
        
        if not resultados.exists():
            return {"error": "No hay datos suficientes para análisis de tendencias"}
        
        # Crear DataFrame con datos temporales
        datos_temporales = []
        
        for resultado in resultados:
            fila = {
                'fecha': resultado.fecha_calculo,
                'puntuacion_global': resultado.puntuacion_global,
                'nivel_madurez': resultado.nivel_madurez,
                'institucion': resultado.institucion.nombre if resultado.institucion else 'Sin institución'
            }
            
            # Añadir valores de indicadores
            for valor_ind in resultado.valores_indicadores.all():
                fila[f"ind_{valor_ind.indicador.nombre}"] = valor_ind.valor
            
            datos_temporales.append(fila)
        
        df = pd.DataFrame(datos_temporales)
        
        # Análisis con Pandas
        analisis = {
            "resumen_estadistico": df.describe().to_dict(),
            "tendencia_temporal": self._calcular_tendencia_temporal(df),
            "correlaciones_indicadores": self._calcular_correlaciones(df),
            "distribucion_niveles": df['nivel_madurez'].value_counts().to_dict(),
            "evolucion_promedio": self._calcular_evolucion_promedio(df)
        }
        
        return analisis
    
    def _calcular_tendencia_temporal(self, df):
        """Calcular tendencia temporal de puntuaciones."""
        if 'fecha' not in df.columns:
            return {}
        
        df_temporal = df.copy()
        df_temporal['fecha'] = pd.to_datetime(df_temporal['fecha'])
        df_temporal = df_temporal.sort_values('fecha')
        
        # Agrupar por mes
        df_temporal['mes_año'] = df_temporal['fecha'].dt.to_period('M')
        tendencia_mensual = df_temporal.groupby('mes_año')['puntuacion_global'].mean()
        
        return {
            "tendencia_mensual": tendencia_mensual.to_dict(),
            "pendiente_general": float(
                np.polyfit(range(len(tendencia_mensual)), tendencia_mensual.values, 1)[0]
            )
        }
    
    def _calcular_correlaciones(self, df):
        """Calcular correlaciones entre indicadores."""
        columnas_indicadores = [col for col in df.columns if col.startswith('ind_')]
        
        if len(columnas_indicadores) < 2:
            return {}
        
        correlaciones = df[columnas_indicadores + ['puntuacion_global']].corr()
        
        # Correlaciones con puntuación global
        corr_con_puntuacion = correlaciones['puntuacion_global'].drop('puntuacion_global')
        
        return {
            "con_puntuacion_global": corr_con_puntuacion.to_dict(),
            "matriz_completa": correlaciones.to_dict()
        }
    
    def _calcular_evolucion_promedio(self, df):
        """Calcular evolución del promedio en el tiempo."""
        if 'fecha' not in df.columns:
            return {}
        
        df_evol = df.copy()
        df_evol['fecha'] = pd.to_datetime(df_evol['fecha'])
        df_evol = df_evol.sort_values('fecha')
        
        # Promedio móvil de 30 días
        df_evol['promedio_movil'] = df_evol['puntuacion_global'].rolling(window=3, min_periods=1).mean()
        
        return {
            "valores": df_evol[['fecha', 'promedio_movil']].to_dict('records'),
            "promedio_inicial": float(df_evol['puntuacion_global'].iloc[0]),
            "promedio_final": float(df_evol['puntuacion_global'].iloc[-1]),
            "mejora_absoluta": float(df_evol['puntuacion_global'].iloc[-1] - df_evol['puntuacion_global'].iloc[0])
        }
