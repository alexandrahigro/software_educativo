from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    api_root,
    InstitucionViewSet, RolViewSet, UsuarioPerfilViewSet,
    EncuestaViewSet, PreguntaViewSet, OpcionRespuestaViewSet,
    RespuestaViewSet, ResultadoEncuestaViewSet, IndicadorViewSet,
    ResultadoIndicadorViewSet, ModeloIAViewSet, PrediccionIAViewSet,
    RecursoColaborativoViewSet,
    mi_perfil, registrar_usuario, listar_usuarios,
    crear_usuario, editar_usuario, eliminar_usuario, listar_roles, listar_instituciones,
    crear_encuesta_completa, responder_encuesta, mis_encuestas,
    reporte_resumen, reporte_por_indicador, 
    reporte_comparativo_instituciones, dashboard_metricas, 
    predecir_nivel, entrenar_modelo_ia, analizar_tendencias, estado_modelo_ia,
    predecir_madurez,
)

router = DefaultRouter()
router.register(r"instituciones", InstitucionViewSet, basename="institucion")
router.register(r"roles", RolViewSet, basename="rol")
router.register(r"perfiles", UsuarioPerfilViewSet, basename="perfil")
router.register(r"encuestas", EncuestaViewSet, basename="encuesta")
router.register(r"preguntas", PreguntaViewSet, basename="pregunta")
router.register(r"opciones", OpcionRespuestaViewSet, basename="opcion_respuesta")
router.register(r"respuestas", RespuestaViewSet, basename="respuesta")
router.register(r"resultados", ResultadoEncuestaViewSet, basename="resultado_encuesta")
router.register(r"indicadores", IndicadorViewSet, basename="indicador")
router.register(r"resultados-indicadores", ResultadoIndicadorViewSet, basename="resultado_indicador")
router.register(r"modelos-ia", ModeloIAViewSet, basename="modelo_ia")
router.register(r"predicciones-ia", PrediccionIAViewSet, basename="prediccion_ia")
router.register(r"recursos", RecursoColaborativoViewSet, basename="recurso_colaborativo")

urlpatterns = [
    path('', api_root, name='api_root'),
    
    # Endpoints personalizados PRIMERO para evitar conflictos con router
    path("mi-perfil/", mi_perfil, name="mi_perfil"),
    
    # Gestión de Usuarios (RF-001)
    path("registro/", registrar_usuario, name="registrar_usuario"),
    path("usuarios/", listar_usuarios, name="listar_usuarios"),
    path("usuarios/crear/", crear_usuario, name="crear_usuario"),
    path("usuarios/<int:usuario_id>/editar/", editar_usuario, name="editar_usuario"),
    path("usuarios/<int:usuario_id>/eliminar/", eliminar_usuario, name="eliminar_usuario"),
    path("usuarios/roles/", listar_roles, name="listar_roles"),
    path("usuarios/instituciones/", listar_instituciones, name="listar_instituciones"),
    
    # Flujo de Encuestas (RF-002, RF-003)
    path("encuestas/crear-completa/", crear_encuesta_completa, name="crear_encuesta_completa"),
    path("encuestas/<int:encuesta_id>/responder/", responder_encuesta, name="responder_encuesta"),
    path("mis-encuestas/", mis_encuestas, name="mis_encuestas"),
    
    # Endpoints de Reportes
    path("reporte-resumen/", reporte_resumen, name="reporte_resumen"),
    path("reporte-indicador/", reporte_por_indicador, name="reporte_por_indicador"),
    path("reporte-comparativo/", reporte_comparativo_instituciones, name="reporte_comparativo"),
    path("dashboard-metricas/", dashboard_metricas, name="dashboard_metricas"),
    
    # Endpoints de IA/Analytics (Machine Learning)
    path("predecir-nivel/", predecir_nivel, name="predecir_nivel"),
    path("entrenar-modelo-ia/", entrenar_modelo_ia, name="entrenar_modelo_ia"),
    path("analizar-tendencias/", analizar_tendencias, name="analizar_tendencias"),
    path("estado-modelo-ia/", estado_modelo_ia, name="estado_modelo_ia"),
    
    # Nuevos endpoints de IA
    path("ia/entrenar-modelo/", entrenar_modelo_ia, name="ia_entrenar_modelo"),
    path("ia/predecir/", predecir_madurez, name="ia_predecir_madurez"),
    path("ia/tendencias/", analizar_tendencias, name="ia_tendencias"),
    
    # Router URLs AL FINAL
    path("", include(router.urls)),
]