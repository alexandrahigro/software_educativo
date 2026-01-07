from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Institucion, Rol, UsuarioPerfil,
    Encuesta, Pregunta, OpcionRespuesta, Respuesta,
    ResultadoEncuesta, Indicador, ResultadoIndicador,
    ModeloIA, PrediccionIA, RecursoColaborativo
)

class InstitucionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institucion
        fields = "__all__"


class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = "__all__"


class UsuarioSerializer(serializers.ModelSerializer):
    """Usuario base de Django, para exponer datos básicos."""
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class UsuarioPerfilSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)
    institucion = InstitucionSerializer(read_only=True)
    rol = RolSerializer(read_only=True)

    class Meta:
        model = UsuarioPerfil
        fields = ["id", "usuario", "institucion", "rol", "estado", "fecha_registro"]


class EncuestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Encuesta
        fields = "__all__"
        read_only_fields = ["creador", "fecha_creacion"]


class PreguntaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pregunta
        fields = "__all__"


class OpcionRespuestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpcionRespuesta
        fields = "__all__"


class RespuestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Respuesta
        fields = "__all__"
        read_only_fields = ["usuario", "fecha_respuesta"]


class ResultadoEncuestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultadoEncuesta
        fields = "__all__"
        read_only_fields = ["fecha_calculo"]


class IndicadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicador
        fields = "__all__"


class ResultadoIndicadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultadoIndicador
        fields = "__all__"


class ModeloIASerializer(serializers.ModelSerializer):
    class Meta:
        model = ModeloIA
        fields = "__all__"
        read_only_fields = ["fecha_entrenamiento"]


class PrediccionIASerializer(serializers.ModelSerializer):
    class Meta:
        model = PrediccionIA
        fields = "__all__"
        read_only_fields = ["fecha_prediccion"]


class RecursoColaborativoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecursoColaborativo
        fields = "__all__"
        read_only_fields = ["autor", "fecha_publicacion"]


class UsuarioRegistroSerializer(serializers.ModelSerializer):
    """Serializer para registro de nuevos usuarios con perfil"""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    institucion_id = serializers.IntegerField(required=True)
    rol_id = serializers.IntegerField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password_confirm', 'institucion_id', 'rol_id']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        return attrs
    
    def create(self, validated_data):
        # Extraer datos de perfil
        institucion_id = validated_data.pop('institucion_id')
        rol_id = validated_data.pop('rol_id')
        validated_data.pop('password_confirm')
        
        # Crear usuario
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        
        # Crear perfil
        from .models import Institucion, Rol
        institucion = Institucion.objects.get(id=institucion_id)
        rol = Rol.objects.get(id=rol_id)
        
        UsuarioPerfil.objects.create(
            usuario=user,
            institucion=institucion,
            rol=rol
        )
        
        return user
