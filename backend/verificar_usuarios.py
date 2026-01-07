#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from encuestas.models import UsuarioPerfil, Rol, Institucion

print("=== VERIFICACIÓN RÁPIDA DE USUARIOS ===")

# Verificar usuarios existentes
print("\n1. USUARIOS EN BASE DE DATOS:")
users = User.objects.all()
for user in users:
    print(f"   - {user.username} (ID: {user.id})")

# Verificar perfiles
print("\n2. PERFILES DE USUARIO:")
perfiles = UsuarioPerfil.objects.all()
for perfil in perfiles:
    print(f"   - {perfil.usuario.username}: Rol={perfil.rol}, Institución={perfil.institucion}")

# Verificar autenticación
print("\n3. PRUEBA DE LOGIN:")
credenciales = [
    ('admin_tic', 'admin123'),
    ('docente', 'docente123'),
    ('directivo', 'directivo123')
]

for username, password in credenciales:
    user = authenticate(username=username, password=password)
    if user:
        print(f"   ✅ {username}: LOGIN OK")
    else:
        print(f"   ❌ {username}: LOGIN FALLO")
        # Verificar si existe el usuario
        try:
            u = User.objects.get(username=username)
            print(f"      Usuario existe pero contraseña incorrecta")
        except User.DoesNotExist:
            print(f"      Usuario NO existe")

print("\n=== VERIFICACIÓN COMPLETADA ===")