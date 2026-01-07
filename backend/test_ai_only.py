"""
Script para probar solo los endpoints de IA después de agregar más datos
"""
import requests

def test_ai_only():
    # Autenticarse
    print("🔐 Autenticando...")
    login_data = {
        "username": "admin_tic",
        "password": "admin123"
    }
    
    auth_response = requests.post('http://127.0.0.1:8000/api/token/', json=login_data)
    if auth_response.status_code != 200:
        print(f"❌ Error de autenticación: {auth_response.text}")
        return
    
    token = auth_response.json()['access']
    headers = {'Authorization': f'Bearer {token}'}
    print("✅ Token obtenido")
    
    # 1. Entrenar modelo
    print("\n🤖 1. PROBANDO ENTRENAMIENTO...")
    response = requests.post('http://127.0.0.1:8000/api/ia/entrenar-modelo/', headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print("✅ Entrenamiento exitoso")
        print(f"   Precisión: {data.get('precision', 'N/A')}")
        print(f"   Mensaje: {data.get('mensaje', 'N/A')}")
        print(f"   Tiempo: {data.get('tiempo_entrenamiento', 'N/A')}s")
        print(f"   Características: {data.get('num_caracteristicas', 'N/A')}")
    else:
        print(f"❌ Error en entrenamiento: {response.text[:300]}")
    
    # 2. Predicción
    print("\n🔮 2. PROBANDO PREDICCIÓN...")
    prediction_data = {
        "valores_indicadores": [3.5, 4.0, 3.8, 4.2, 3.9]
    }
    response = requests.post('http://127.0.0.1:8000/api/ia/predecir/', 
                           json=prediction_data, headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print("✅ Predicción exitosa")
        print(f"   Nivel predicho: {data.get('nivel_predicho', 'N/A')}")
        print(f"   Confianza: {data.get('confianza', 'N/A')}")
        if 'probabilidades' in data:
            print(f"   Probabilidades: {data['probabilidades']}")
    else:
        print(f"❌ Error en predicción: {response.text[:300]}")
    
    # 3. Tendencias
    print("\n📈 3. PROBANDO TENDENCIAS...")
    response = requests.get('http://127.0.0.1:8000/api/ia/tendencias/', headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print("✅ Tendencias exitosas")
        print(f"   Periodos analizados: {len(data.get('tendencias', []))}")
        if 'resumen' in data:
            print(f"   Resumen: {data['resumen']}")
    else:
        print(f"❌ Error en tendencias: {response.text[:300]}")

if __name__ == "__main__":
    test_ai_only()