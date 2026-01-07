"""
Script de prueba completa para validar todos los endpoints implementados
Incluye: autenticación, reportes avanzados, módulo de IA y permisos por roles
"""

import requests
import json
import time

def test_authentication():
    """Prueba el sistema de autenticación JWT"""
    print("\n🔐 PROBANDO AUTENTICACIÓN...")
    
    # Crear usuario de prueba
    login_data = {
        "username": "admin_tic",
        "password": "admin123"
    }
    
    try:
        response = requests.post('http://127.0.0.1:8000/api/token/', json=login_data)
        
        if response.status_code == 200:
            tokens = response.json()
            print(f"✅ Autenticación exitosa")
            print(f"   Access token: {tokens['access'][:20]}...")
            print(f"   Refresh token: {tokens['refresh'][:20]}...")
            return tokens['access']
        else:
            print(f"❌ Error en autenticación: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión. ¿Está ejecutándose el servidor Django?")
        return None
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return None

def test_reporting_endpoints(token):
    """Prueba todos los endpoints de reportes avanzados"""
    print("\n📊 PROBANDO ENDPOINTS DE REPORTES AVANZADOS...")
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # 1. Dashboard general
    print("1. Probando dashboard general...")
    start_time = time.time()
    try:
        response = requests.get('http://127.0.0.1:8000/api/dashboard-metricas/', headers=headers)
        end_time = time.time()
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Dashboard OK - Tiempo: {end_time - start_time:.2f}s")
            print(f"   Total encuestas: {data.get('total_encuestas', 'N/A')}")
            print(f"   Promedio general: {data.get('promedio_general', 'N/A')}")
        else:
            print(f"❌ Error en dashboard: {response.status_code}")
            print(f"   Respuesta: {response.text[:200]}...")
    except Exception as e:
        print(f"❌ Error de conexión en dashboard: {e}")
    
    # 2. Reporte resumen
    print("2. Probando reporte resumen...")
    start_time = time.time()
    try:
        response = requests.get('http://127.0.0.1:8000/api/reporte-resumen/', headers=headers)
        end_time = time.time()
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Reporte resumen OK - Tiempo: {end_time - start_time:.2f}s")
            print(f"   Instituciones: {len(data.get('por_institucion', []))}")
        else:
            print(f"❌ Error en reporte resumen: {response.status_code}")
            print(f"   Respuesta: {response.text[:200]}...")
    except Exception as e:
        print(f"❌ Error de conexión en reporte resumen: {e}")
    
    # 3. Reporte por indicador
    print("3. Probando reporte por indicador...")
    start_time = time.time()
    try:
        response = requests.get('http://127.0.0.1:8000/api/reporte-indicador/', headers=headers)
        end_time = time.time()
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Reporte por indicador OK - Tiempo: {end_time - start_time:.2f}s")
            print(f"   Indicadores analizados: {len(data.get('indicadores', []))}")
        else:
            print(f"❌ Error en reporte por indicador: {response.status_code}")
            print(f"   Respuesta: {response.text[:200]}...")
    except Exception as e:
        print(f"❌ Error de conexión en reporte por indicador: {e}")
    
    # 4. Reporte comparativo
    print("4. Probando reporte comparativo...")
    start_time = time.time()
    try:
        response = requests.get('http://127.0.0.1:8000/api/reporte-comparativo/', headers=headers)
        end_time = time.time()
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Reporte comparativo OK - Tiempo: {end_time - start_time:.2f}s")
            print(f"   Comparaciones: {len(data.get('comparaciones', []))}")
        else:
            print(f"❌ Error en reporte comparativo: {response.status_code}")
            print(f"   Respuesta: {response.text[:200]}...")
    except Exception as e:
        print(f"❌ Error de conexión en reporte comparativo: {e}")

def test_ai_endpoints(token):
    """Prueba todos los endpoints de IA"""
    print("\n🤖 PROBANDO ENDPOINTS DE IA...")
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # 1. Entrenar modelo
    print("1. Probando entrenamiento de modelo...")
    start_time = time.time()
    try:
        response = requests.post('http://127.0.0.1:8000/api/ia/entrenar-modelo/', headers=headers)
        end_time = time.time()
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Entrenamiento OK - Tiempo: {end_time - start_time:.2f}s")
            print(f"   Precisión: {data.get('precision', 'N/A')}")
            print(f"   Características: {data.get('num_caracteristicas', 'N/A')}")
        else:
            print(f"❌ Error en entrenamiento: {response.status_code}")
            print(f"   Respuesta: {response.text[:200]}...")
    except Exception as e:
        print(f"❌ Error de conexión en entrenamiento: {e}")
    
    # 2. Predicción
    print("2. Probando predicción...")
    prediction_data = {
        "valores_indicadores": [3.5, 4.0, 3.8, 4.2, 3.9]
    }
    start_time = time.time()
    try:
        response = requests.post('http://127.0.0.1:8000/api/ia/predecir/', 
                               json=prediction_data, headers=headers)
        end_time = time.time()
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Predicción OK - Tiempo: {end_time - start_time:.2f}s")
            print(f"   Nivel predicho: {data.get('nivel_predicho', 'N/A')}")
            print(f"   Confianza: {data.get('confianza', 'N/A')}")
        else:
            print(f"❌ Error en predicción: {response.status_code}")
            print(f"   Respuesta: {response.text[:200]}...")
    except Exception as e:
        print(f"❌ Error de conexión en predicción: {e}")
    
    # 3. Análisis de tendencias
    print("3. Probando análisis de tendencias...")
    start_time = time.time()
    try:
        response = requests.get('http://127.0.0.1:8000/api/ia/tendencias/', headers=headers)
        end_time = time.time()
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Análisis de tendencias OK - Tiempo: {end_time - start_time:.2f}s")
            print(f"   Periodos analizados: {len(data.get('tendencias', []))}")
        else:
            print(f"❌ Error en tendencias: {response.status_code}")
            print(f"   Respuesta: {response.text[:200]}...")
    except Exception as e:
        print(f"❌ Error de conexión en tendencias: {e}")

def test_permissions():
    """Prueba el sistema de permisos por roles"""
    print("\n🛡️ PROBANDO SISTEMA DE PERMISOS...")
    
    # Crear datos de prueba para diferentes roles
    roles_test = [
        {"username": "docente_test", "rol": "docente"},
        {"username": "directivo_test", "rol": "directivo"}, 
        {"username": "admin_test", "rol": "admin_tic"}
    ]
    
    for rol_data in roles_test:
        print(f"\nProbando rol: {rol_data['rol']}")
        
        # Intentar login con cada rol
        login_data = {
            "username": rol_data["username"],
            "password": "test123"
        }
        
        try:
            response = requests.post('http://127.0.0.1:8000/api/token/', json=login_data)
            
            if response.status_code == 200:
                token = response.json()['access']
                headers = {'Authorization': f'Bearer {token}'}
                
                # Probar acceso a dashboard
                response = requests.get('http://127.0.0.1:8000/api/dashboard-metricas/', headers=headers)
                
                if response.status_code == 200:
                    print(f"   ✅ {rol_data['rol']} - Acceso autorizado")
                else:
                    print(f"   ⚠️ {rol_data['rol']} - Acceso denegado (código: {response.status_code})")
            else:
                print(f"   ❌ {rol_data['rol']} - Usuario no existe o credenciales incorrectas")
        except Exception as e:
            print(f"   ❌ {rol_data['rol']} - Error de conexión: {e}")

def run_complete_test():
    """Ejecuta todas las pruebas"""
    print("🚀 INICIANDO PRUEBAS COMPLETAS DE LA API")
    print("=" * 60)
    
    # 1. Autenticación
    token = test_authentication()
    
    if not token:
        print("❌ No se pudo autenticar. Deteniendo pruebas.")
        return
    
    # 2. Reportes
    test_reporting_endpoints(token)
    
    # 3. IA
    test_ai_endpoints(token)
    
    # 4. Permisos
    test_permissions()
    
    print("\n🎉 PRUEBAS COMPLETADAS")
    print("=" * 60)
    print("Revisar los resultados arriba para verificar el estado de cada endpoint.")

if __name__ == "__main__":
    run_complete_test()