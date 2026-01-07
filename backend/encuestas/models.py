from django.db import models
from django.contrib.auth.models import User

class Institucion(models.Model):
    # INSTITUCION
    nombre = models.CharField(max_length=200)
    nivel_educativo = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    estado = models.CharField(max_length=50, default="activa")

    class Meta:
        db_table = "institucion"

    def __str__(self):
        return self.nombre


class Rol(models.Model):
    # ROL
    nombre_rol = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = "rol"

    def __str__(self):
        return self.nombre_rol


class UsuarioPerfil(models.Model):
    """
    Implementa la entidad USUARIO del modelo E-R,
    enlazada con el usuario de Django (auth.User).
    Relaciones:
    - 1 institución tiene N usuarios
    - 1 usuario pertenece a 1 institución
    - 1 rol se asigna a muchos usuarios
    - 1 usuario tiene 1 rol
    """
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil")
    institucion = models.ForeignKey(Institucion, on_delete=models.SET_NULL, null=True, blank=True)
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, blank=True)
    estado = models.CharField(max_length=50, default="activo")
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "usuario"

    def __str__(self):
        return f"{self.usuario.username} ({self.rol})"



#  ENCUESTAS, PREGUNTAS Y RESPUESTAS


class Encuesta(models.Model):
    """
    Relaciones:
    - 1 institución puede tener muchas encuestas
    - 1 encuesta pertenece a 1 institución
    - 1 usuario (creador) crea muchas encuestas
    - 1 encuesta es creada por 1 usuario
    """
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE, null=True, blank=True)
    creador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="encuestas_creadas")
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=50, default="activa")

    class Meta:
        db_table = "encuesta"

    def __str__(self):
        return self.titulo


class Pregunta(models.Model):
    """
    - 1 encuesta contiene muchas preguntas
    - 1 pregunta pertenece a 1 encuesta
    """
    encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE, related_name="preguntas")
    texto = models.CharField(max_length=255)
    tipo = models.CharField(max_length=50, default="escala_1_5")  # escala, opción múltiple, abierta...
    orden = models.IntegerField()

    class Meta:
        db_table = "pregunta"
        ordering = ["encuesta", "orden"]

    def __str__(self):
        return f"{self.encuesta.titulo} - {self.texto}"


class OpcionRespuesta(models.Model):
    """
    - 1 pregunta puede tener muchas opciones
    - 1 opción pertenece a 1 pregunta
    """
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, related_name="opciones")
    etiqueta = models.CharField(max_length=100)
    valor_numerico = models.IntegerField()

    class Meta:
        db_table = "opcion_respuesta"

    def __str__(self):
        return f"{self.pregunta.texto} -> {self.etiqueta} ({self.valor_numerico})"


class Respuesta(models.Model):
    """
    Implementa la entidad RESPUESTA del modelo E-R.
    Relaciones:
    - 1 usuario puede registrar muchas respuestas
    - 1 respuesta pertenece a 1 usuario
    - 1 pregunta tiene muchas respuestas
    - 1 respuesta corresponde a 1 pregunta
    - 1 encuesta tiene muchas respuestas
    - 1 respuesta pertenece a 1 encuesta
    """
    encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    opcion = models.ForeignKey(OpcionRespuesta, on_delete=models.SET_NULL, null=True, blank=True)
    valor_abierto = models.TextField(blank=True, null=True)
    fecha_respuesta = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "respuesta"

    def __str__(self):
        return f"{self.usuario.username} - {self.encuesta.titulo} - {self.pregunta.texto}"



#  RESULTADOS E INDICADORES


class ResultadoEncuesta(models.Model):
    """
    Relaciones:
    - 1 encuesta puede tener varios resultados
    - 1 resultado se calcula para 1 encuesta
    - 1 institución puede tener muchos resultados
    - 1 resultado corresponde a 1 institución
    """
    encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE)
    nivel_madurez = models.CharField(max_length=50)
    puntuacion_global = models.FloatField()
    fecha_calculo = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "resultado_encuesta"

    def __str__(self):
        return f"{self.encuesta.titulo} - {self.institucion.nombre} ({self.nivel_madurez})"


class Indicador(models.Model):
    # INDICADOR
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    categoria = models.CharField(max_length=100)

    class Meta:
        db_table = "indicador"

    def __str__(self):
        return self.nombre


class ResultadoIndicador(models.Model):
    """
    RESULTADO_ENCUESTA – RESULTADO_INDICADOR – INDICADOR
    - 1 resultado de encuesta tiene muchos valores de indicadores
    - 1 indicador aparece en muchos resultados
    """
    resultado = models.ForeignKey(ResultadoEncuesta, on_delete=models.CASCADE, related_name="valores_indicadores")
    indicador = models.ForeignKey(Indicador, on_delete=models.CASCADE)
    valor = models.FloatField()
    nivel_indicador = models.CharField(max_length=50)

    class Meta:
        db_table = "resultado_indicador"

    def __str__(self):
        return f"{self.resultado} - {self.indicador.nombre} ({self.nivel_indicador})"



#  IA: MODELO Y PREDICCIONES


class ModeloIA(models.Model):
    """
    MODELO_IA
    """
    nombre_modelo = models.CharField(max_length=100)
    version = models.CharField(max_length=20)
    metrica_precision = models.FloatField()
    fecha_entrenamiento = models.DateTimeField(auto_now_add=True)
    ruta_fichero = models.CharField(max_length=255)  # ruta al .pkl del modelo

    class Meta:
        db_table = "modelo_ia"

    def __str__(self):
        return f"{self.nombre_modelo} v{self.version}"


class PrediccionIA(models.Model):
    """
    MODELO_IA – PREDICCION_IA – RESULTADO_ENCUESTA
    - 1 modelo IA genera muchas predicciones
    - 1 predicción se asocia a 1 resultado de encuesta
    """
    modelo = models.ForeignKey(ModeloIA, on_delete=models.CASCADE)
    resultado = models.ForeignKey(ResultadoEncuesta, on_delete=models.CASCADE)
    nivel_pred = models.CharField(max_length=50)
    probabilidad = models.FloatField()
    fecha_prediccion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "prediccion_ia"

    def __str__(self):
        return f"{self.modelo} -> {self.nivel_pred} ({self.probabilidad})"



#  MÓDULO COLABORATIVO


class RecursoColaborativo(models.Model):
    """
    USUARIO – RECURSO_COLABORATIVO
    - 1 usuario publica muchos recursos
    - 1 recurso tiene 1 autor
    """
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "recurso_colaborativo"

    def __str__(self):
        return self.titulo

