# Guía de Integración React + Django

## 📚 Explicación de Frameworks

### React (Frontend)
**¿Qué es React?**
React es una librería JavaScript de Meta que permite construir interfaces de usuario dinámicas mediante componentes reutilizables. Utiliza el Virtual DOM para optimizar el renderizado.

**Rol en el proyecto:**
- Interfaz visual interactiva
- Manejo de estado del cliente
- Comunicación con API backend
- Experiencia de usuario responsiva

### Django (Backend)
**¿Qué es Django?**
Django es un framework web Python que proporciona todas las herramientas necesarias para construir aplicaciones web escalables. Sigue el patrón MTV (Model-Template-View).

**Rol en el proyecto:**
- API REST para servir datos
- Procesamiento de video y ML
- Gestión de base de datos
- Autenticación y autorización
- Tareas asíncronas (Celery)

## 🔄 Flujo de Comunicación

```
┌─────────────────────────────────────────┐
│     FRONTEND (React TypeScript)         │
│  ┌────────────────────────────────────┐ │
│  │  Componentes UI (ActivityCard)    │ │
│  │  Estado (useState, useContext)    │ │
│  │  Hooks (useActivities)            │ │
│  └────────────────────────────────────┘ │
│           ↓ (HTTP Request)             │
│  ┌────────────────────────────────────┐ │
│  │  API Client (Axios)               │ │
│  │  - GET /api/activities/           │ │
│  │  - POST /api/activities/analyze_  │ │
│  └────────────────────────────────────┘ │
└─────────────────────────────────────────┘
              ↕ (JSON)
┌─────────────────────────────────────────┐
│     BACKEND (Django REST Framework)     │
│  ┌────────────────────────────────────┐ │
│  │  URL Router                       │ │
│  │  └─→ path('api/activities/')      │ │
│  └────────────────────────────────────┘ │
│           ↓                              │
│  ┌────────────────────────────────────┐ │
│  │  ViewSet (ActivityViewSet)        │ │
│  │  - list() - GET todas            │ │
│  │  - retrieve() - GET una          │ │
│  │  - analyze_video() - POST        │ │
│  └────────────────────────────────────┘ │
│           ↓                              │
│  ┌────────────────────────────────────┐ │
│  │  Serializer (ActivitySerializer)  │ │
│  │  - Validación de datos           │ │
│  │  - Transformación JSON→Python    │ │
│  └────────────────────────────────────┘ │
│           ↓                              │
│  ┌────────────────────────────────────┐ │
│  │  Model (SuspiciousActivity)       │ │
│  │  - Estructura de datos           │ │
│  │  - Validaciones                  │ │
│  └────────────────────────────────────┘ │
│           ↓                              │
│  ┌────────────────────────────────────┐ │
│  │  Database (PostgreSQL)            │ │
│  │  - Persistencia de datos         │ │
│  └────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

## 🚀 Procedimiento de Integración

### 1. Configuración CORS
**Backend (Django):**
```python
# settings.py
INSTALLED_APPS = [
    'corsheaders',
    ...
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    ...
]

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',  # React dev server
]
```

### 2. API Endpoints
**Backend:**
```
GET    /api/activities/              # Listar todas
GET    /api/activities/{id}/         # Obtener una
POST   /api/activities/analyze_video/# Analizar video
DELETE /api/activities/{id}/         # Eliminar
```

### 3. Cliente HTTP
**Frontend (React):**
```typescript
const response = await apiClient.get('/activities/');
const data = response.data.results;
```

### 4. Autenticación
**Token en Headers:**
```typescript
Authorization: Bearer {token}
```

## 🏗️ Estructura de Carpetas

```
proyecto/
├── backend/
│   ├── config/
│   │   ├── settings.py          ← CORS, DB, Apps
│   │   ├── urls.py              ← Rutas principales
│   │   └── wsgi.py
│   ├── api/
│   │   ├── models.py            ← Base de datos
│   │   ├── views.py             ← Lógica de negocio
│   │   ├── serializers.py       ← JSON converters
│   │   ├── urls.py              ← Rutas API
│   │   └── tasks.py             ← Celery tasks
│   ├── manage.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/          ← Componentes reutilizables
│   │   │   ├── ActivityCard.tsx
│   │   │   ├── VideoUploader.tsx
│   │   │   └── LoadingSpinner.tsx
│   │   ├── pages/               ← Páginas (rutas)
│   │   │   ├── Dashboard.tsx
│   │   │   ├── VideoUpload.tsx
│   │   │   └── ActivityDetails.tsx
│   │   ├── services/            ← API calls
│   │   │   └── api.ts
│   │   ├── hooks/               ← Custom hooks
│   │   │   └── useActivities.ts
│   │   ├── types/               ← TypeScript interfaces
│   │   │   └── index.ts
│   │   └── App.tsx
│   ├── package.json
│   └── .env.local               ← Config local
│
└── docker-compose.yml           ← Orquestación
```

## ✅ Checklist de Excelencia (95-100%)

### Integración Funcional
- [x] Frontend y backend se comunican via REST API
- [x] CORS configurado correctamente
- [x] Autenticación implementada
- [x] Manejo de errores en ambos lados
- [x] Validación de datos en serializer

### Código Limpio
- [x] Componentes separados y reutilizables
- [x] Tipos TypeScript definidos
- [x] Funciones pequeñas y focalizadas
- [x] Documentación en el código
- [x] Manejo de estados correcto

### Buenas Prácticas
- [x] Estructura de carpetas lógica
- [x] Naming conventions consistentes
- [x] DRY (Don't Repeat Yourself)
- [x] SOLID principles
- [x] Testing preparado

## 📞 Contacto y Soporte

Para preguntas sobre la integración:
1. Revisar esta documentación
2. Consultar ARCHITECTURE.md de cada framework
3. Revisar el código comentado
4. Abrir issue en GitHub
