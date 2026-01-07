#!/usr/bin/env python3
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User
from encuestas.models import Institucion, Rol, UsuarioPerfil

def crear_usuarios_prueba():
    print("🚀 Creando usuarios de prueba para TFM...")
    
    # 1. Crear institución de prueba si no existe
    institucion, created = Institucion.objects.get_or_create(
        nombre="Universidad de Prueba",
        defaults={
            'nivel_educativo': 'Universitario',
            'ciudad': 'Madrid',
            'pais': 'España',
            'estado': 'activa'
        }
    )
    if created:
        print(f"✅ Institución creada: {institucion.nombre}")
    else:
        print(f"✅ Institución existente: {institucion.nombre}")
    
    # 2. Crear roles si no existen
    roles_data = [
        {'nombre_rol': 'admin_tic'},
        {'nombre_rol': 'directivo'},
        {'nombre_rol': 'docente'}
    ]
    
    for rol_data in roles_data:
        rol, created = Rol.objects.get_or_create(**rol_data)
        if created:
            print(f"✅ Rol creado: {rol.nombre_rol}")
        else:
            print(f"✅ Rol existente: {rol.nombre_rol}")
    
    # 3. Crear usuarios
    usuarios_data = [
        {
            'username': 'admin_tic',
            'password': 'admin123',
            'email': 'admin@test.com',
            'rol': 'admin_tic'
        },
        {
            'username': 'directivo', 
            'password': 'admin123',
            'email': 'directivo@test.com',
            'rol': 'directivo'
        },
        {
            'username': 'docente',
            'password': 'admin123', 
            'email': 'docente@test.com',
            'rol': 'docente'
        }
    ]
    
    for user_data in usuarios_data:
        # Crear o obtener usuario de Django
        user, user_created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={
                'email': user_data['email'],
                'is_active': True
            }
        )
        
        if user_created:
            user.set_password(user_data['password'])
            user.save()
            print(f"✅ Usuario Django creado: {user.username}")
        else:
            # Asegurar que la contraseña esté correcta
            user.set_password(user_data['password'])
            user.save()
            print(f"✅ Usuario Django existente (contraseña actualizada): {user.username}")
        
        # Crear perfil si no existe
        rol = Rol.objects.get(nombre_rol=user_data['rol'])
        perfil, perfil_created = UsuarioPerfil.objects.get_or_create(
            usuario=user,
            defaults={
                'institucion': institucion,
                'rol': rol,
                'estado': 'activo'
            }
        )
        
        if perfil_created:
            print(f"✅ Perfil creado para: {user.username} - Rol: {rol.nombre_rol}")
        else:
            # Actualizar rol e institución
            perfil.rol = rol
            perfil.institucion = institucion
            perfil.save()
            print(f"✅ Perfil actualizado para: {user.username} - Rol: {rol.nombre_rol}")
    
    print("\n🎯 RESUMEN:")
    print(f"📊 Total usuarios: {User.objects.count()}")
    print(f"👥 Total perfiles: {UsuarioPerfil.objects.count()}")
    print(f"🏢 Total instituciones: {Institucion.objects.count()}")
    print(f"🔑 Total roles: {Rol.objects.count()}")
    
    print("\n🔐 CREDENCIALES DE PRUEBA:")
    for perfil in UsuarioPerfil.objects.all():
        print(f"   {perfil.usuario.username} / admin123 - {perfil.rol.nombre_rol}")

if __name__ == "__main__":
    crear_usuarios_prueba()