#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
sys.path.append('/path/to/your/project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User
from encuestas.models import Institucion, Rol, UsuarioPerfil

def fix_users_and_profiles():
    """
    Corrige usuarios y perfiles según TFM:
    1. Crea instituciones de prueba
    2. Crea roles
    3. Vincula usuarios con UsuarioPerfil completo
    """
    
    print("🏗️ Creando instituciones de prueba...")
    inst1, _ = Institucion.objects.get_or_create(
        nombre="UNIR Universidad",
        defaults={
            'nivel_educativo': "Universidad",
            'ciudad': "Madrid",
            'pais': "España",
            'estado': "activa"
        }
    )
    
    inst2, _ = Institucion.objects.get_or_create(
        nombre="IES Madrid Centro", 
        defaults={
            'nivel_educativo': "Instituto",
            'ciudad': "Madrid",
            'pais': "España", 
            'estado': "activa"
        }
    )
    
    print("👥 Creando roles...")
    rol_docente, _ = Rol.objects.get_or_create(
        nombre_rol="docente"
    )
    
    rol_directivo, _ = Rol.objects.get_or_create(
        nombre_rol="directivo"
    )
    
    rol_admin, _ = Rol.objects.get_or_create(
        nombre_rol="admin_tic"
    )
    
    print("🔧 Creando/actualizando usuarios...")
    
    # Usuario admin_tic
    user_admin, created = User.objects.get_or_create(
        username="admin_tic",
        defaults={
            'email': 'admin@unir.net',
            'first_name': 'Admin',
            'last_name': 'TIC',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        user_admin.set_password('admin123')
        user_admin.save()
    
    # Perfil admin_tic
    perfil_admin, _ = UsuarioPerfil.objects.get_or_create(
        usuario=user_admin,
        defaults={
            'rol': rol_admin,
            'institucion': inst1,
            'estado': 'activo'
        }
    )
    
    # Usuario docente
    user_docente, created = User.objects.get_or_create(
        username="docente",
        defaults={
            'email': 'docente@unir.net',
            'first_name': 'María',
            'last_name': 'García',
            'is_staff': False
        }
    )
    if created:
        user_docente.set_password('docente123')
        user_docente.save()
        
    # Perfil docente
    perfil_docente, _ = UsuarioPerfil.objects.get_or_create(
        usuario=user_docente,
        defaults={
            'rol': rol_docente,
            'institucion': inst1,
            'estado': 'activo'
        }
    )
    
    # Usuario directivo
    user_directivo, created = User.objects.get_or_create(
        username="directivo",
        defaults={
            'email': 'directivo@iesmadrid.edu',
            'first_name': 'Carlos',
            'last_name': 'Rodríguez',
            'is_staff': True
        }
    )
    if created:
        user_directivo.set_password('directivo123')
        user_directivo.save()
        
    # Perfil directivo  
    perfil_directivo, _ = UsuarioPerfil.objects.get_or_create(
        usuario=user_directivo,
        defaults={
            'rol': rol_directivo,
            'institucion': inst2,
            'estado': 'activo'
        }
    )
    
    print("✅ USUARIOS CREADOS CORRECTAMENTE:")
    for user in User.objects.all():
        try:
            perfil = user.perfil  # Cambio: usuarioperfil -> perfil (según related_name)
            print(f"  - {user.username}: {perfil.rol.nombre_rol} en {perfil.institucion.nombre}")
        except:
            print(f"  - {user.username}: SIN PERFIL ❌")
    
    return True

if __name__ == "__main__":
    fix_users_and_profiles()