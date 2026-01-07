"""
Script para probar endpoint específico con token válido
"""
import requests

def test_specific_endpoint():
    # Autenticarse primero
    print("Obteniendo token...")
    login_data = {
        "username": "admin_tic",
        "password": "admin123"
    }
    
    auth_response = requests.post('http://127.0.0.1:8000/api/token/', json=login_data)
    if auth_response.status_code != 200:
        print(f"Error de autenticación: {auth_response.text}")
        return
    
    token = auth_response.json()['access']
    headers = {'Authorization': f'Bearer {token}'}
    
    print("✅ Token obtenido correctamente")
    
    # Probar mi-perfil (que sabemos que debería funcionar)
    print("\n1. Probando mi-perfil...")
    response = requests.get('http://127.0.0.1:8000/api/encuestas/mi-perfil/', headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ mi-perfil funciona")
    else:
        print(f"❌ Error en mi-perfil: {response.text}")
    
    # Probar dashboard
    print("\n2. Probando dashboard...")
    response = requests.get('http://127.0.0.1:8000/api/encuestas/dashboard-metricas/', headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ dashboard funciona")
        data = response.json()
        print(f"Total encuestas: {data.get('total_encuestas', 'N/A')}")
    else:
        print(f"❌ Error en dashboard: {response.text[:200]}")
    
    # Probar endpoint sin la parte /encuestas/
    print("\n3. Probando dashboard sin /encuestas/...")
    response = requests.get('http://127.0.0.1:8000/api/dashboard-metricas/', headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ dashboard funciona sin /encuestas/")
    else:
        print(f"❌ Error: {response.text[:200]}")

if __name__ == "__main__":
    test_specific_endpoint()