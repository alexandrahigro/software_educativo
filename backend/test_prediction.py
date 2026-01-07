"""
Prueba rápida solo para predicción de IA
"""
import requests

def test_prediction_only():
    # Autenticarse
    login_data = {"username": "admin_tic", "password": "admin123"}
    auth_response = requests.post('http://127.0.0.1:8000/api/token/', json=login_data)
    
    if auth_response.status_code != 200:
        print(f"Error de autenticación: {auth_response.text}")
        return
    
    token = auth_response.json()['access']
    headers = {'Authorization': f'Bearer {token}'}
    
    print("🔮 PROBANDO PREDICCIÓN...")
    
    # Datos de prueba
    prediction_data = {
        "valores_indicadores": [3.5, 4.0, 3.8, 4.2, 3.9]
    }
    
    response = requests.post('http://127.0.0.1:8000/api/ia/predecir/', 
                           json=prediction_data, headers=headers)
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ PREDICCIÓN EXITOSA")
        print(f"   Nivel predicho: {data.get('nivel_predicho', 'N/A')}")
        print(f"   Confianza: {data.get('confianza', 'N/A')}")  
        print(f"   Probabilidad: {data.get('probabilidad', 'N/A')}")
        print(f"   Puntuación estimada: {data.get('puntuacion_estimada', 'N/A')}")
        if 'probabilidades' in data:
            print(f"   Probabilidades por nivel: {data['probabilidades']}")
    else:
        print(f"❌ Error: {response.text}")

if __name__ == "__main__":
    test_prediction_only()