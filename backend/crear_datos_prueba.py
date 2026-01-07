#!/usr/bin/env python3
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User
from encuestas.models import *
from datetime import datetime, timedelta

def crear_datos_prueba():
    print("📊 Creando datos de prueba para TFM...")
    
    # Obtener objetos necesarios
    institucion = Institucion.objects.first()
    admin_user = User.objects.get(username='admin_tic')
    directivo_user = User.objects.get(username='directivo') 
    docente_user = User.objects.get(username='docente')
    
    # 1. Crear encuesta de prueba
    encuesta, created = Encuesta.objects.get_or_create(
        titulo="Evaluación de Madurez Digital - TFM",
        defaults={
            'institucion': institucion,
            'creador': admin_user,
            'descripcion': 'Encuesta de prueba para evaluar la madurez digital institucional',
            'estado': 'activa'
        }
    )
    if created:
        print(f"✅ Encuesta creada: {encuesta.titulo}")
    else:
        print(f"✅ Encuesta existente: {encuesta.titulo}")
    
    # 2. Crear preguntas si no existen
    preguntas_data = [
        "¿Cómo evalúa el nivel de tecnología educativa en su institución?",
        "¿Qué tan capacitado se siente en herramientas digitales?", 
        "¿Cómo califica la infraestructura tecnológica?",
        "¿Qué tan eficaz es la gestión digital de recursos?",
        "¿Cómo evalúa la seguridad digital institucional?"
    ]
    
    for i, texto_pregunta in enumerate(preguntas_data):
        pregunta, created = Pregunta.objects.get_or_create(
            encuesta=encuesta,
            orden=i+1,
            defaults={
                'texto': texto_pregunta,
                'tipo': 'escala_1_5'
            }
        )
        
        if created:
            print(f"✅ Pregunta {i+1} creada")
            
            # Crear opciones para cada pregunta (escala 1-5)
            for valor in range(1, 6):
                etiquetas = {
                    1: "Muy bajo",
                    2: "Bajo", 
                    3: "Medio",
                    4: "Alto",
                    5: "Muy alto"
                }
                OpcionRespuesta.objects.create(
                    pregunta=pregunta,
                    etiqueta=etiquetas[valor],
                    valor_numerico=valor
                )
        else:
            print(f"✅ Pregunta {i+1} existente")
    
    # 3. Crear respuestas simuladas
    usuarios_respuesta = [directivo_user, docente_user]
    preguntas = encuesta.preguntas.all()
    
    for usuario in usuarios_respuesta:
        for pregunta in preguntas:
            # Verificar si ya existe respuesta
            if not Respuesta.objects.filter(encuesta=encuesta, pregunta=pregunta, usuario=usuario).exists():
                # Simular respuesta aleatoria entre 3-5 (buenas evaluaciones)
                import random
                valor_respuesta = random.randint(3, 5)
                opcion = pregunta.opciones.get(valor_numerico=valor_respuesta)
                
                Respuesta.objects.create(
                    encuesta=encuesta,
                    pregunta=pregunta,
                    usuario=usuario,
                    opcion=opcion
                )
        
        print(f"✅ Respuestas creadas para: {usuario.username}")
    
    # 4. Crear resultados e indicadores
    # Crear indicadores si no existen
    indicadores_data = [
        {"nombre": "Infraestructura Tecnológica", "categoria": "Tecnología"},
        {"nombre": "Competencias Digitales", "categoria": "Capacidades"},
        {"nombre": "Gestión Digital", "categoria": "Procesos"},
        {"nombre": "Seguridad Digital", "categoria": "Seguridad"},
        {"nombre": "Innovación Pedagógica", "categoria": "Educación"}
    ]
    
    for ind_data in indicadores_data:
        indicador, created = Indicador.objects.get_or_create(
            nombre=ind_data["nombre"],
            defaults={
                'categoria': ind_data["categoria"],
                'descripcion': f'Indicador de {ind_data["nombre"].lower()}'
            }
        )
        if created:
            print(f"✅ Indicador creado: {indicador.nombre}")
    
    # 5. Crear resultado de encuesta
    if not ResultadoEncuesta.objects.filter(encuesta=encuesta, institucion=institucion).exists():
        # Calcular promedio de respuestas
        respuestas = Respuesta.objects.filter(encuesta=encuesta)
        suma_valores = sum(r.opcion.valor_numerico for r in respuestas if r.opcion)
        promedio = suma_valores / len(respuestas) if respuestas else 0
        
        # Determinar nivel según promedio
        if promedio >= 4.5:
            nivel = "Avanzado"
        elif promedio >= 3.5:
            nivel = "Intermedio Alto"
        elif promedio >= 2.5:
            nivel = "Intermedio"
        elif promedio >= 1.5:
            nivel = "Básico"
        else:
            nivel = "Inicial"
        
        resultado = ResultadoEncuesta.objects.create(
            encuesta=encuesta,
            institucion=institucion,
            nivel_madurez=nivel,
            puntuacion_global=round(promedio, 2)
        )
        
        # Crear valores de indicadores
        for indicador in Indicador.objects.all():
            import random
            valor_indicador = random.uniform(3.0, 5.0)
            ResultadoIndicador.objects.create(
                resultado=resultado,
                indicador=indicador,
                valor=round(valor_indicador, 2),
                nivel_indicador=nivel
            )
        
        print(f"✅ Resultado creado: {nivel} ({promedio:.2f})")
    else:
        print(f"✅ Resultado existente")
    
    print("\n🎯 RESUMEN DE DATOS:")
    print(f"📊 Total encuestas: {Encuesta.objects.count()}")
    print(f"❓ Total preguntas: {Pregunta.objects.count()}")
    print(f"💬 Total respuestas: {Respuesta.objects.count()}")
    print(f"📈 Total resultados: {ResultadoEncuesta.objects.count()}")
    print(f"📋 Total indicadores: {Indicador.objects.count()}")
    print(f"🔢 Total valores indicadores: {ResultadoIndicador.objects.count()}")

if __name__ == "__main__":
    crear_datos_prueba()