#!/usr/bin/env python3
"""
Script de pruebas del sistema de permisos por roles.
Ejecutar con: python test_permisos.py
"""

import requests
import json

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
        print(response.text)
        return None

def hacer_request(endpoint, token=None, method='GET', data=None):
    """Hacer una request a la API con opcional token JWT."""
    url = f"{BASE_URL}{endpoint}"
    headers = {}
    
    if token:
        headers['Authorization'] = f'Bearer {token}'
    
    if method == 'GET':
        response = requests.get(url, headers=headers)
    elif method == 'POST':
        headers['Content-Type'] = 'application/json'
        response = requests.post(url, headers=headers, json=data)
    
    return response

def probar_permisos():
    """Ejecutar suite completa de pruebas de permisos."""
    
    print("🔑 PRUEBAS DEL SISTEMA DE PERMISOS")
    print("=" * 50)
    
    # Test 1: Obtener tokens
    print("\n1️⃣ Obteniendo tokens de autenticación...")
    
    token_directivo = obtener_token("directivo1", "dir123")
    token_docente = obtener_token("docente1", "doc123") 
    token_admin = obtener_token("admin_tic", "admin123")
    
    if not all([token_directivo, token_docente, token_admin]):
        print("❌ Error: No se pudieron obtener todos los tokens")
        return
    
    print("✅ Tokens obtenidos exitosamente")
    
    # Test 2: Verificar perfiles
    print("\n2️⃣ Verificando perfiles de usuario...")
    
    perfil_directivo = hacer_request("mi-perfil/", token_directivo)
    if perfil_directivo.status_code == 200:
        data = perfil_directivo.json()
        print(f"✅ Directivo: {data['usuario']['username']} - Rol: {data['perfil']['rol']['nombre_rol']}")
    
    # Test 3: Directivo crea encuesta (DEBE FUNCIONAR)
    print("\n3️⃣ Directivo intenta crear encuesta...")
    
    nueva_encuesta = {
        "titulo": "Encuesta Test Permisos",
        "descripcion": "Prueba del sistema de permisos"
    }
    
    response = hacer_request("encuestas/", token_directivo, 'POST', nueva_encuesta)
    if response.status_code == 201:
        print("✅ Directivo puede crear encuestas (CORRECTO)")
        encuesta_id = response.json()['id']
    else:
        print(f"❌ Error: Directivo no puede crear encuestas: {response.status_code}")
        print(response.text)
        encuesta_id = 1  # Usar la de ejemplo
    
    # Test 4: Docente intenta crear encuesta (DEBE FALLAR) 
    print("\n4️⃣ Docente intenta crear encuesta (debe fallar)...")
    
    response = hacer_request("encuestas/", token_docente, 'POST', nueva_encuesta)
    if response.status_code == 403:
        print("✅ Docente NO puede crear encuestas (CORRECTO)")
    else:
        print(f"❌ Error: Docente puede crear encuestas (status: {response.status_code})")
    
    # Test 5: Docente ve encuestas de su institución
    print("\n5️⃣ Docente consulta encuestas disponibles...")
    
    response = hacer_request("encuestas/", token_docente)
    if response.status_code == 200:
        encuestas = response.json()
        print(f"✅ Docente ve {len(encuestas)} encuesta(s) de su institución")
    else:
        print(f"❌ Error consultando encuestas como docente: {response.status_code}")
    
    # Test 6: Docente crea respuesta (DEBE FUNCIONAR)
    print("\n6️⃣ Docente intenta responder encuesta...")
    
    respuesta_data = {
        "encuesta": encuesta_id,
        "pregunta": 1,
        "opcion": 4
    }
    
    response = hacer_request("respuestas/", token_docente, 'POST', respuesta_data)
    if response.status_code == 201:
        print("✅ Docente puede crear respuestas (CORRECTO)")
    else:
        print(f"❌ Error: Docente no puede responder: {response.status_code}")
        print(response.text)
    
    # Test 7: Admin TIC ve reporte
    print("\n7️⃣ Admin TIC consulta reporte...")
    
    response = hacer_request("reporte-resumen/", token_admin)
    if response.status_code == 200:
        reporte = response.json()
        print(f"✅ Admin TIC ve reporte: {reporte.get('total_resultados', 0)} resultados")
    else:
        print(f"❌ Error consultando reporte: {response.status_code}")
    
    print("\n" + "=" * 50)
    print("🎉 PRUEBAS COMPLETADAS")

if __name__ == "__main__":
    try:
        probar_permisos()
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor Django")
        print("   Asegúrate de que 'python manage.py runserver' esté corriendo")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")