#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User

print("=== CORRIGIENDO CONTRASEÑAS ===")

# Corregir contraseñas
usuarios_fix = [
    ('docente', 'docente123'),
    ('directivo', 'directivo123'),
    ('admin', 'admin123')
]

for username, nueva_password in usuarios_fix:
    try:
        user = User.objects.get(username=username)
        user.set_password(nueva_password)
        user.save()
        print(f"✅ {username}: Contraseña actualizada")
    except User.DoesNotExist:
        print(f"❌ {username}: Usuario no existe")

print("=== CONTRASEÑAS CORREGIDAS ===")