from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from encuestas.models import (
    Institucion, Rol, UsuarioPerfil, Indicador, Encuesta, 
    Pregunta, OpcionRespuesta
)

class Command(BaseCommand):
    help = 'Crea datos iniciales básicos para el software educativo'

    def handle(self, *args, **options):
        self.stdout.write('Creando datos iniciales...')
        
        # 1. Crear roles básicos
        self.crear_roles()
        
        # 2. Crear institución de ejemplo
        institucion = self.crear_institucion_ejemplo()
        
        # 3. Crear usuarios de ejemplo
        self.crear_usuarios_ejemplo(institucion)
        
        # 4. Crear indicadores predefinidos
        self.crear_indicadores()
        
        # 5. Crear encuesta básica de ejemplo
        self.crear_encuesta_ejemplo(institucion)
        
        # 6. Crear resultados de ejemplo para reportes
        self.crear_resultados_ejemplo(institucion)
        
        self.stdout.write(
            self.style.SUCCESS('¡Datos iniciales creados exitosamente!')
        )
        self.mostrar_credenciales()

    def crear_roles(self):
        """Crear los 3 roles principales del sistema."""
        roles_data = [
            'docente',
            'directivo', 
            'admin_tic'
        ]
        
        for nombre_rol in roles_data:
            rol, created = Rol.objects.get_or_create(nombre_rol=nombre_rol)
            if created:
                self.stdout.write(f'✓ Rol creado: {nombre_rol}')
            else:
                self.stdout.write(f'- Rol ya existe: {nombre_rol}')

    def crear_institucion_ejemplo(self):
        """Crear una institución de ejemplo."""
        institucion, created = Institucion.objects.get_or_create(
            nombre='IES Ejemplo TFM',
            defaults={
                'nivel_educativo': 'Educación Secundaria',
                'ciudad': 'Madrid',
                'pais': 'España',
                'estado': 'activa'
            }
        )
        if created:
            self.stdout.write('✓ Institución creada: IES Ejemplo TFM')
        else:
            self.stdout.write('- Institución ya existe: IES Ejemplo TFM')
        return institucion

    def crear_usuarios_ejemplo(self, institucion):
        """Crear usuarios de ejemplo para cada rol."""
        usuarios_data = [
            {
                'username': 'admin_tic',
                'email': 'admin@ejemplo.com',
                'password': 'admin123',
                'rol': 'admin_tic',
                'is_staff': True
            },
            {
                'username': 'directivo1', 
                'email': 'directivo@ejemplo.com',
                'password': 'dir123',
                'rol': 'directivo',
                'is_staff': False
            },
            {
                'username': 'docente1',
                'email': 'docente1@ejemplo.com', 
                'password': 'doc123',
                'rol': 'docente',
                'is_staff': False
            },
            {
                'username': 'docente2',
                'email': 'docente2@ejemplo.com',
                'password': 'doc123', 
                'rol': 'docente',
                'is_staff': False
            }
        ]
        
        for user_data in usuarios_data:
            # Crear usuario Django
            user, user_created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'is_staff': user_data['is_staff'],
                    'is_active': True
                }
            )
            
            if user_created:
                user.set_password(user_data['password'])
                user.save()
                self.stdout.write(f'✓ Usuario creado: {user_data["username"]}')
            else:
                self.stdout.write(f'- Usuario ya existe: {user_data["username"]}')
            
            # Crear perfil
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
                self.stdout.write(f'✓ Perfil creado para: {user_data["username"]} ({user_data["rol"]})')

    def crear_indicadores(self):
        """Crear indicadores predefinidos según el TFM."""
        indicadores_data = [
            {
                'nombre': 'Infraestructura tecnológica',
                'descripcion': 'Nivel de infraestructura TIC disponible en el centro',
                'categoria': 'infraestructura'
            },
            {
                'nombre': 'Competencia digital docente',
                'descripcion': 'Nivel de competencias digitales del profesorado',
                'categoria': 'competencias'
            },
            {
                'nombre': 'Uso pedagógico de TIC', 
                'descripcion': 'Integración de las TIC en la práctica docente',
                'categoria': 'pedagogia'
            },
            {
                'nombre': 'Gestión y organización digital',
                'descripcion': 'Procesos de gestión digitalizada del centro',
                'categoria': 'gestion'
            },
            {
                'nombre': 'Proyección y liderazgo digital',
                'descripcion': 'Visión estratégica y liderazgo en transformación digital',
                'categoria': 'liderazgo'
            }
        ]
        
        for ind_data in indicadores_data:
            indicador, created = Indicador.objects.get_or_create(
                nombre=ind_data['nombre'],
                defaults={
                    'descripcion': ind_data['descripcion'],
                    'categoria': ind_data['categoria']
                }
            )
            if created:
                self.stdout.write(f'✓ Indicador creado: {ind_data["nombre"]}')

    def crear_encuesta_ejemplo(self, institucion):
        """Crear una encuesta básica de ejemplo."""
        # Obtener usuario directivo
        directivo_user = User.objects.filter(
            perfil__rol__nombre_rol='directivo'
        ).first()
        
        if not directivo_user:
            self.stdout.write('- No se puede crear encuesta: no hay usuario directivo')
            return
            
        # Crear encuesta
        encuesta, created = Encuesta.objects.get_or_create(
            titulo='Evaluación Madurez Digital - Ejemplo',
            defaults={
                'institucion': institucion,
                'creador': directivo_user,
                'descripcion': 'Encuesta de ejemplo para evaluar el nivel de madurez digital del centro educativo',
                'estado': 'activa'
            }
        )
        
        if not created:
            self.stdout.write('- Encuesta de ejemplo ya existe')
            return
            
        self.stdout.write('✓ Encuesta de ejemplo creada')
        
        # Crear preguntas de ejemplo
        preguntas_data = [
            {
                'texto': '¿Cómo evalúa la infraestructura tecnológica de su centro?',
                'tipo': 'escala_1_5',
                'orden': 1
            },
            {
                'texto': '¿Cuál es su nivel de competencia digital como docente?',
                'tipo': 'escala_1_5',
                'orden': 2
            },
            {
                'texto': '¿Con qué frecuencia utiliza herramientas TIC en sus clases?',
                'tipo': 'escala_1_5',
                'orden': 3
            }
        ]
        
        # Opciones de respuesta estándar (escala 1-5)
        opciones_escala = [
            {'etiqueta': 'Muy bajo', 'valor_numerico': 1},
            {'etiqueta': 'Bajo', 'valor_numerico': 2},
            {'etiqueta': 'Medio', 'valor_numerico': 3},
            {'etiqueta': 'Alto', 'valor_numerico': 4},
            {'etiqueta': 'Muy alto', 'valor_numerico': 5}
        ]
        
        for preg_data in preguntas_data:
            pregunta = Pregunta.objects.create(
                encuesta=encuesta,
                texto=preg_data['texto'],
                tipo=preg_data['tipo'],
                orden=preg_data['orden']
            )
            
            # Crear opciones para cada pregunta
            for opcion_data in opciones_escala:
                OpcionRespuesta.objects.create(
                    pregunta=pregunta,
                    etiqueta=opcion_data['etiqueta'],
                    valor_numerico=opcion_data['valor_numerico']
                )
        
        self.stdout.write(f'✓ {len(preguntas_data)} preguntas creadas con sus opciones')

    def crear_resultados_ejemplo(self, institucion):
        """Crear resultados de ejemplo para probar los reportes."""
        from encuestas.models import ResultadoEncuesta, ResultadoIndicador
        import random
        from datetime import datetime, timedelta
        
        # Obtener la encuesta de ejemplo
        encuesta = Encuesta.objects.filter(institucion=institucion).first()
        if not encuesta:
            self.stdout.write('- No se puede crear resultados: no hay encuesta')
            return
        
        # Obtener indicadores
        indicadores = list(Indicador.objects.all())
        if not indicadores:
            self.stdout.write('- No se puede crear resultados: no hay indicadores')
            return
        
        # Definir niveles de madurez posibles
        niveles_madurez = ['Inicial', 'En desarrollo', 'Competente', 'Avanzado', 'Experto']
        
        # Crear 10 resultados de ejemplo con fechas variadas
        resultados_creados = 0
        
        for i in range(10):
            # Generar puntuación aleatoria (1.0 - 5.0)
            puntuacion = round(random.uniform(1.5, 4.8), 2)
            
            # Asignar nivel basado en puntuación
            if puntuacion < 2.0:
                nivel = 'Inicial'
            elif puntuacion < 2.8:
                nivel = 'En desarrollo'
            elif puntuacion < 3.6:
                nivel = 'Competente'
            elif puntuacion < 4.2:
                nivel = 'Avanzado'
            else:
                nivel = 'Experto'
            
            # Crear resultado con fecha aleatoria (últimos 3 meses)
            fecha_base = datetime.now() - timedelta(days=random.randint(1, 90))
            
            resultado = ResultadoEncuesta.objects.create(
                encuesta=encuesta,
                institucion=institucion,
                nivel_madurez=nivel,
                puntuacion_global=puntuacion
            )
            
            # Actualizar fecha_calculo manualmente para simular fechas variadas
            resultado.fecha_calculo = fecha_base
            resultado.save()
            
            # Crear valores para cada indicador
            for indicador in indicadores:
                # Generar valor del indicador (relacionado con la puntuación global)
                base_valor = puntuacion + random.uniform(-0.5, 0.5)
                valor_indicador = max(1.0, min(5.0, round(base_valor, 2)))
                
                # Asignar nivel del indicador
                if valor_indicador < 2.0:
                    nivel_ind = 'Bajo'
                elif valor_indicador < 3.0:
                    nivel_ind = 'Medio-bajo'
                elif valor_indicador < 3.5:
                    nivel_ind = 'Medio'
                elif valor_indicador < 4.0:
                    nivel_ind = 'Medio-alto'
                else:
                    nivel_ind = 'Alto'
                
                ResultadoIndicador.objects.create(
                    resultado=resultado,
                    indicador=indicador,
                    valor=valor_indicador,
                    nivel_indicador=nivel_ind
                )
            
            resultados_creados += 1
        
        self.stdout.write(f'✓ {resultados_creados} resultados de ejemplo creados')
        self.stdout.write(f'✓ {resultados_creados * len(indicadores)} valores de indicadores creados')

    def mostrar_credenciales(self):
        """Mostrar las credenciales de los usuarios creados."""
        self.stdout.write('\n' + '='*50)
        self.stdout.write('CREDENCIALES DE ACCESO:')
        self.stdout.write('='*50)
        self.stdout.write('Admin TIC:  admin_tic / admin123')
        self.stdout.write('Directivo:  directivo1 / dir123')
        self.stdout.write('Docente 1:  docente1 / doc123')
        self.stdout.write('Docente 2:  docente2 / doc123')
        self.stdout.write('='*50)
        self.stdout.write('URL API: http://localhost:8000/api/')
        self.stdout.write('Admin Django: http://localhost:8000/admin/')
        self.stdout.write('='*50)