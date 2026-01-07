#!/usr/bin/env python3
import requests
import json

def probar_api_completa():
    print("🧪 PROBANDO API COMPLETA TFM...")
    
    base_url = "http://127.0.0.1:8000/api"
    
    # 1. Login con cada usuario
    usuarios_prueba = [
        {"username": "admin_tic", "password": "admin123"},
        {"username": "directivo", "password": "admin123"},
        {"username": "docente", "password": "admin123"}
    ]
    
    for credenciales in usuarios_prueba:
        print(f"\n👤 Probando login: {credenciales['username']}")
        
        try:
            # Login
            login_response = requests.post(
                f"{base_url}/token/",
                json=credenciales,
                headers={"Content-Type": "application/json"}
            )
            
            if login_response.status_code == 200:
                token_data = login_response.json()
                token = token_data['access']
                print(f"✅ Login exitoso")
                
                # Headers con token
                headers = {"Authorization": f"Bearer {token}"}
                
                # 2. Probar dashboard-metricas
                dashboard_response = requests.get(f"{base_url}/dashboard-metricas/", headers=headers)
                if dashboard_response.status_code == 200:
                    metricas = dashboard_response.json()
                    print(f"✅ Dashboard: Encuestas={metricas.get('total_encuestas', 0)}, "
                          f"Promedio={metricas.get('promedio_general', 'N/A')}, "
                          f"Instituciones={metricas.get('total_instituciones', 0)}")
                else:
                    print(f"❌ Error dashboard: {dashboard_response.status_code}")
                
                # 3. Probar perfil
                perfil_response = requests.get(f"{base_url}/mi-perfil/", headers=headers)
                if perfil_response.status_code == 200:
                    perfil = perfil_response.json()
                    print(f"✅ Perfil: {perfil.get('usuario', {}).get('username')} - "
                          f"Rol: {perfil.get('rol', {}).get('nombre_rol')}")
                else:
                    print(f"❌ Error perfil: {perfil_response.status_code}")
                
                # 4. Probar reporte-resumen
                reporte_response = requests.get(f"{base_url}/reporte-resumen/", headers=headers)
                if reporte_response.status_code == 200:
                    reporte = reporte_response.json()
                    print(f"✅ Reporte: {reporte.get('total_resultados', 0)} resultados")
                else:
                    print(f"❌ Error reporte: {reporte_response.status_code}")
            
            else:
                print(f"❌ Login falló: {login_response.status_code}")
                print(f"    Response: {login_response.text}")
        
        except Exception as e:
            print(f"❌ Error de conexión: {e}")

if __name__ == "__main__":
    probar_api_completa()