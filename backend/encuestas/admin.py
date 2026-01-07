from django.contrib import admin
from .models import (
    Institucion, Rol, UsuarioPerfil,
    Encuesta, Pregunta, OpcionRespuesta, Respuesta,
    ResultadoEncuesta, Indicador, ResultadoIndicador,
    ModeloIA, PrediccionIA, RecursoColaborativo
)

admin.site.register(Institucion)
admin.site.register(Rol)
admin.site.register(UsuarioPerfil)
admin.site.register(Encuesta)
admin.site.register(Pregunta)
admin.site.register(OpcionRespuesta)
admin.site.register(Respuesta)
admin.site.register(ResultadoEncuesta)
admin.site.register(Indicador)
admin.site.register(ResultadoIndicador)
admin.site.register(ModeloIA)
admin.site.register(PrediccionIA)
admin.site.register(RecursoColaborativo)