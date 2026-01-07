from rest_framework import permissions

class EsDocente(permissions.BasePermission):
    """
    Permiso para usuarios con rol de docente.
    Los docentes pueden responder encuestas y ver sus propios resultados.
    """
    def has_permission(self, request, view):
        return (request.user.is_authenticated and 
                hasattr(request.user, 'perfil') and 
                request.user.perfil.rol and
                request.user.perfil.rol.nombre_rol == 'docente')

class EsDirectivo(permissions.BasePermission):
    """
    Permiso para usuarios con rol de directivo.
    Los directivos pueden crear/gestionar encuestas y ver reportes de su institución.
    """
    def has_permission(self, request, view):
        return (request.user.is_authenticated and 
                hasattr(request.user, 'perfil') and 
                request.user.perfil.rol and
                request.user.perfil.rol.nombre_rol == 'directivo')

class EsAdminTIC(permissions.BasePermission):
    """
    Permiso para usuarios con rol de administrador TIC.
    Los admin TIC pueden gestionar todo el sistema y ver reportes globales.
    """
    def has_permission(self, request, view):
        return (request.user.is_authenticated and 
                hasattr(request.user, 'perfil') and 
                request.user.perfil.rol and
                request.user.perfil.rol.nombre_rol == 'admin_tic')

class PropietarioODirectivo(permissions.BasePermission):
    """
    Permiso para el creador del objeto o directivos de la misma institución.
    """
    def has_object_permission(self, request, view, obj):
        user = request.user
        # Si el usuario es el creador
        if hasattr(obj, 'creador') and obj.creador == user:
            return True
        if hasattr(obj, 'autor') and obj.autor == user:
            return True
            
        # Si el usuario es directivo de la misma institución
        if (hasattr(user, 'perfil') and user.perfil.rol and 
            user.perfil.rol.nombre_rol == 'directivo'):
            
            # Para encuestas, verificar institución
            if hasattr(obj, 'institucion') and obj.institucion == user.perfil.institucion:
                return True
                
        return False

class MismaInstitucion(permissions.BasePermission):
    """
    Permiso para usuarios de la misma institución.
    """
    def has_object_permission(self, request, view, obj):
        user = request.user
        if not (hasattr(user, 'perfil') and user.perfil.institucion):
            return False
            
        # Verificar si el objeto pertenece a la misma institución
        if hasattr(obj, 'institucion'):
            return obj.institucion == user.perfil.institucion
        elif hasattr(obj, 'encuesta') and hasattr(obj.encuesta, 'institucion'):
            return obj.encuesta.institucion == user.perfil.institucion
            
        return False