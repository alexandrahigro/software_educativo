#!/usr/bin/env python3
"""
Script de pruebas para los reportes avanzados.
Ejecutar con: python test_reportes.py
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000/api/"

def obtener_token(username, password):
    """Obtener token JWT para un usuario."""
    url = f"{BASE_URL}token/"
    data = {"username": username, "password": password}
    
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()['access']
    else:
        print(f"Error obteniendo token para {username}: {response.status_code}")
        return None

def hacer_request(endpoint, token=None, method='GET', params=None):
    """Hacer una request a la API con token JWT."""
    url = f"{BASE_URL}{endpoint}"
    headers = {}
    
    if token:
        headers['Authorization'] = f'Bearer {token}'
    
    start_time = time.time()
    response = requests.get(url, headers=headers, params=params)
    end_time = time.time()
    
    return response, round(end_time - start_time, 3)

def probar_reportes_avanzados():
    """Ejecutar suite de pruebas para reportes avanzados."""
    
    print("📊 PRUEBAS DE REPORTES AVANZADOS")
    print("=" * 60)
    
    # Obtener token admin_tic para todas las pruebas
    print("\n🔑 Obteniendo token de admin_tic...")
    token_admin = obtener_token("admin_tic", "admin123")
    
    if not token_admin:
        print("❌ Error: No se pudo obtener token de admin_tic")
        return
    
    print("✅ Token obtenido exitosamente")
    
    # Test 1: Dashboard de métricas (debe ser rápido < 3s)
    print("\n📈 Test 1: Dashboard de métricas principales...")
    
    response, tiempo = hacer_request("dashboard-metricas/", token_admin)
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Dashboard cargado en {tiempo}s")
        print(f"   📊 Total evaluaciones: {data['metricas_principales']['total_evaluaciones']}")
        print(f"   📊 Promedio madurez: {data['metricas_principales']['promedio_madurez']}")
        print(f"   📊 Nivel predominante: {data['metricas_principales']['nivel_predominante']}")
        
        # Verificar objetivo de rendimiento
        cumple_objetivo = data['rendimiento']['cumple_objetivo_3s']
        if cumple_objetivo:
            print(f"   🚀 Rendimiento: ✅ Cumple objetivo < 3s ({tiempo}s)")
        else:
            print(f"   ⚠️ Rendimiento: ❌ No cumple objetivo de 3s ({tiempo}s)")
    else:
        print(f"❌ Error en dashboard: {response.status_code}")
        print(response.text)
    
    # Test 2: Reporte resumen completo
    print(f"\n📋 Test 2: Reporte resumen completo...")
    
    response, tiempo = hacer_request("reporte-resumen/", token_admin)
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Reporte generado en {tiempo}s")
        print(f"   📊 Resumen ejecutivo:")
        for key, value in data['resumen_ejecutivo'].items():
            print(f"      {key}: {value}")
        
        print(f"   📊 Indicadores analizados: {len(data['indicadores_detalle'])}")
        for nombre, stats in list(data['indicadores_detalle'].items())[:3]:  # Mostrar solo los primeros 3
            print(f"      {nombre}: promedio {stats['promedio']} ({stats['total_evaluaciones']} evaluaciones)")
        
        print(f"   📊 Distribución por madurez:")
        for nivel in data['distribucion_madurez']['por_nivel']:
            print(f"      {nivel['nivel']}: {nivel['cantidad']} ({nivel['porcentaje']}%)")
            
    else:
        print(f"❌ Error en reporte resumen: {response.status_code}")
        print(response.text)
    
    # Test 3: Reporte por indicador específico
    print(f"\n🎯 Test 3: Reporte por indicador específico...")
    
    response, tiempo = hacer_request("reporte-indicador/", token_admin, params={'indicador_id': 1})
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Reporte de indicador generado en {tiempo}s")
        print(f"   📊 Indicador: {data['indicador']['nombre']}")
        print(f"   📊 Categoría: {data['indicador']['categoria']}")
        if data['estadisticas']:
            stats = data['estadisticas']
            print(f"   📊 Estadísticas:")
            print(f"      Promedio: {stats['promedio_general']}")
            print(f"      Rango: {stats['valor_minimo']} - {stats['valor_maximo']}")
            print(f"      Total evaluaciones: {stats['total_evaluaciones']}")
    else:
        print(f"❌ Error en reporte por indicador: {response.status_code}")
        print(response.text)
    
    # Test 4: Reporte comparativo instituciones
    print(f"\n🏢 Test 4: Reporte comparativo instituciones...")
    
    response, tiempo = hacer_request("reporte-comparativo/", token_admin)
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Comparativa generada en {tiempo}s")
        print(f"   📊 Total instituciones: {data['total_instituciones']}")
        print(f"   📊 Promedio del sistema: {data['promedio_sistema']}")
        if data['mejor_institucion']:
            mejor = data['mejor_institucion']
            print(f"   🏆 Mejor institución: {mejor['institucion']} ({mejor['promedio_general']})")
    else:
        print(f"❌ Error en comparativa: {response.status_code}")
        print(response.text)
    
    # Test 5: Probar con usuario docente (acceso limitado)
    print(f"\n👨‍🏫 Test 5: Acceso de docente (limitado)...")
    
    token_docente = obtener_token("docente1", "doc123")
    if token_docente:
        # Dashboard para docente
        response, tiempo = hacer_request("dashboard-metricas/", token_docente)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Docente puede ver dashboard (filtrado por institución)")
            print(f"   📊 Vista: {data['usuario_contexto']['vista_global']}")
            print(f"   📊 Institución: {data['usuario_contexto']['institucion']}")
        
        # Comparativa (debe fallar)
        response, tiempo = hacer_request("reporte-comparativo/", token_docente)
        if response.status_code == 403:
            print(f"✅ Docente NO puede ver comparativa global (correcto)")
        else:
            print(f"❌ Error: Docente puede ver comparativa global")
    
    print("\n" + "=" * 60)
    print("🎉 PRUEBAS DE REPORTES COMPLETADAS")

if __name__ == "__main__":
    try:
        probar_reportes_avanzados()
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor Django")
        print("   Asegúrate de que 'python manage.py runserver' esté corriendo")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")