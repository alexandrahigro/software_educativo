# 📚 Software Educativo - Sistema de Gestión y Analytics

Un sistema completo de gestión educativa con Dashboard interactivo, análisis de tendencias con IA y módulos especializados para instituciones educativas.

## 🚀 Características Principales

### 🎯 **Dashboard Interactivo**
- Métricas en tiempo real de instituciones y encuestas
- Diseño responsive optimizado para PC y móvil
- Interfaz moderna con gradientes y animaciones

### 🤖 **Inteligencia Artificial**
- Entrenamiento de modelos ML con RandomForest
- Predicciones de madurez digital
- Análisis de tendencias automatizado
- Recomendaciones inteligentes

### 👥 **Gestión de Usuarios**
- Sistema de roles (admin_tic, directivo, docente)
- CRUD completo para usuarios
- Autenticación JWT segura
- Control de permisos granular

### 📊 **Reportes Avanzados**
- Análisis comparativo entre instituciones
- Reportes de indicadores de madurez
- Visualización de datos interactiva
- Exportación de métricas

### 📝 **Sistema de Encuestas**
- Creación y gestión de encuestas
- Seguimiento de respuestas en tiempo real
- Estados configurables (activa/inactiva/cerrada)
- Análisis de resultados

### 🤝 **Módulo Colaborativo**
- Recursos compartidos entre instituciones
- Sistema de discusiones
- Intercambio de metodologías
- Valoraciones y feedback

## 🛠️ Tecnologías Utilizadas

### Backend
- **Django 4.x** - Framework web principal
- **Django REST Framework** - API REST
- **PostgreSQL/SQLite** - Base de datos
- **Scikit-learn** - Machine Learning
- **Pandas** - Análisis de datos
- **JWT** - Autenticación

### Frontend
- **React 18** - Biblioteca de UI
- **JavaScript ES6+** - Lenguaje principal
- **CSS3** - Estilos modernos
- **Responsive Design** - Adaptable a todos los dispositivos

## 📁 Estructura del Proyecto

```
software_educativo/
├── backend/                    # Django API Backend
│   ├── backend/               # Configuración principal
│   ├── encuestas/            # App principal
│   │   ├── models.py         # Modelos de BD
│   │   ├── views.py          # Vistas de API
│   │   ├── serializers.py    # Serializadores DRF
│   │   ├── urls.py           # URLs de la app
│   │   ├── ml.py             # Algoritmos ML
│   │   └── permissions.py    # Permisos personalizados
│   ├── manage.py             # Comando Django
│   └── ml_models/            # Modelos ML entrenados
├── frontend/                  # React Frontend
│   ├── src/
│   │   ├── Dashboard.js      # Componente principal
│   │   ├── api.js            # Cliente API
│   │   ├── login.js          # Sistema de login
│   │   └── App.js            # Componente raíz
│   └── public/               # Archivos estáticos
├── Docs/                     # Documentación
└── README.md                 # Este archivo
```

## ⚡ Instalación y Configuración

### Prerrequisitos
- Python 3.8+
- Node.js 16+
- npm o yarn
- Git

### 🔧 Configuración del Backend

```bash
# Clonar el repositorio
git clone https://github.com/alexandrahigro/software_educativo.git
cd software_educativo

# Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Instalar dependencias
cd backend
pip install django djangorestframework django-cors-headers
pip install scikit-learn pandas numpy joblib
pip install djangorestframework-simplejwt

# Configurar base de datos
python manage.py migrate
python manage.py createsuperuser

# Crear datos iniciales
python manage.py shell
>>> exec(open('crear_usuarios.py').read())

# Ejecutar servidor
python manage.py runserver
```

### 🎨 Configuración del Frontend

```bash
# En otra terminal
cd frontend
npm install
npm start
```

## 🔐 Usuarios de Prueba

```
Admin TIC:     admin_tic / admin123
Directivo:     directivo / admin123  
Docente:       docente / admin123
```

## 📋 Funcionalidades por Rol

### 🔧 **Admin TIC**
- ✅ Gestión completa de usuarios
- ✅ Entrenamiento de modelos IA
- ✅ Acceso a todos los reportes
- ✅ Configuración del sistema

### 🎯 **Directivo**
- ✅ Creación y gestión de encuestas
- ✅ Visualización de reportes
- ✅ Análisis de tendencias
- ✅ Gestión de recursos colaborativos

### 👨‍🏫 **Docente**
- ✅ Respuesta a encuestas
- ✅ Consulta de métricas básicas
- ✅ Participación en colaborativo
- ✅ Visualización de tendencias

## 🤖 Características de IA

### Algoritmo de Machine Learning
- **RandomForest Classifier** para predicciones de madurez
- **Entrenamiento automático** con datos históricos
- **Validación cruzada** para optimización
- **Métricas de precisión** en tiempo real

### Análisis de Tendencias
- Detección automática de patrones
- Recomendaciones basadas en IA
- Indicadores de madurez digital
- Predicciones de evolución

## 📊 API Endpoints

### Autenticación
- `POST /api/token/` - Login
- `POST /api/token/refresh/` - Refresh token

### Dashboard
- `GET /api/dashboard-metricas/` - Métricas principales

### IA y Analytics
- `POST /api/ia/entrenar-modelo/` - Entrenar modelo
- `POST /api/ia/predecir/` - Realizar predicción
- `GET /api/ia/tendencias/` - Análisis tendencias

### Usuarios
- `GET /api/usuarios/` - Listar usuarios
- `POST /api/usuarios/` - Crear usuario
- `PUT /api/usuarios/{id}/` - Actualizar usuario

## 🎨 Diseño Visual

### Características del UI
- **Diseño moderno** con gradientes y sombras
- **Responsive design** adaptable a cualquier dispositivo
- **Animaciones suaves** para mejor UX
- **Código de colores** para diferentes tipos de datos
- **Iconos emoji** para identificación rápida

### Layout Responsive
- **PC**: Layout en dos columnas sin scroll externo
- **Tablet**: Adaptación automática del contenido
- **Móvil**: Una columna con scroll optimizado

## 🔄 Estados de Desarrollo

- ✅ **Backend API** - Completado
- ✅ **Frontend Dashboard** - Completado  
- ✅ **Sistema de Usuarios** - Completado
- ✅ **Machine Learning** - Completado
- ✅ **Diseño Responsive** - Completado
- ✅ **Integración completa** - Completado

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 👩‍💻 Autor

**Alexandra Higuera**
- GitHub: [@alexandrahigro](https://github.com/alexandrahigro)
- Proyecto: [Software Educativo](https://github.com/alexandrahigro/software_educativo)

---

⭐ **¡Dale una estrella al proyecto si te ha sido útil!** ⭐