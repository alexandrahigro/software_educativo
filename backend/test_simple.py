"""
Script simplificado para probar un endpoint específico
"""

import requests
import json

def test_single_endpoint():
    print("🔐 Autenticando...")
    
    # Autenticarse
    login_data = {
        "username": "admin_tic",
        "password": "admin123"
    }
    
    response = requests.post('http://127.0.0.1:8000/api/token/', json=login_data)
    if response.status_code != 200:
        print(f"❌ Error de autenticación: {response.status_code}")
        print(response.text)
        return
    
    token = response.json()['access']
    headers = {'Authorization': f'Bearer {token}'}
    
    print("✅ Autenticación exitosa")
    
    # Probar dashboard
    print("\n📊 Probando dashboard...")
    response = requests.get('http://127.0.0.1:8000/api/encuestas/dashboard-metricas/', headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print("✅ Dashboard funciona correctamente")
        print(f"Total encuestas: {data.get('total_encuestas', 'N/A')}")
        print(f"Promedio general: {data.get('promedio_general', 'N/A')}")
    else:
        print(f"❌ Error: {response.text}")
    
    # Probar IA
    print("\n🤖 Probando entrenamiento de IA...")
    response = requests.post('http://127.0.0.1:8000/api/encuestas/ia/entrenar-modelo/', headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print("✅ Entrenamiento funciona correctamente")
        print(f"Precisión: {data.get('precision', 'N/A')}")
        print(f"Mensaje: {data.get('mensaje', 'N/A')}")
    else:
        print(f"❌ Error: {response.text[:300]}...")

if __name__ == "__main__":
    test_single_endpoint()