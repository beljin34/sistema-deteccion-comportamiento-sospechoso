# Arquitectura Backend - Django

## 🎯 Rol del Framework Django

Django es un framework web Python de alto nivel que proporciona:

### 1. **ORM (Object-Relational Mapping)**
- Abstracción de base de datos
- Migraciones automáticas
- Queries seguras contra SQL injection

### 2. **REST API**
Con Django REST Framework:
- Serialización de datos
- Autenticación y permisos
- Rate limiting
- Documentación automática

### 3. **Sistema de Modelos**
```python
# api/models.py
from django.db import models

class SuspiciousActivity(models.Model):
    """Modelo para registrar actividades sospechosas"""
    timestamp = models.DateTimeField(auto_now_add=True)
    activity_type = models.CharField(max_length=50)
    confidence = models.FloatField()
    location = models.CharField(max_length=255)
    video_url = models.URLField()
    
    class Meta:
        ordering = ['-timestamp']
```

### 4. **Vistas y Serializers**
```python
# api/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import SuspiciousActivity
from .serializers import ActivitySerializer

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = SuspiciousActivity.objects.all()
    serializer_class = ActivitySerializer
    
    @action(detail=False, methods=['post'])
    def analyze_video(self, request):
        """Endpoint para analizar video y detectar comportamiento"""
        video_file = request.FILES.get('video')
        # Procesar con OpenCV y visión por computadora
        result = process_video_analysis(video_file)
        return Response(result, status=status.HTTP_200_OK)
```

### 5. **Rutas y URLs**
```python
# config/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import ActivityViewSet

router = DefaultRouter()
router.register(r'activities', ActivityViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
```

## 🔄 Procesamiento Asíncrono

```python
# api/tasks.py
from celery import shared_task
import cv2

@shared_task
def process_video_analysis(video_path):
    """Tarea asíncrona para análisis de video"""
    cap = cv2.VideoCapture(video_path)
    results = []
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Análisis con ML
        detection = detect_suspicious_behavior(frame)
        if detection['confidence'] > 0.7:
            results.append(detection)
    
    return results
```

## 🛡️ Seguridad

- **CORS**: Control de acceso desde frontend
- **JWT**: Autenticación tokens
- **Validación**: Serializers validan datos
- **Permisos**: Control granular de acceso

## 📊 Ventajas de Django

| Aspecto | Beneficio |
|--------|----------|
| **ORM poderoso** | Elimina SQL manual |
| **Admin panel** | Gestión de datos sin código |
| **Seguridad** | CSRF, XSS, SQL injection protección |
| **Escalabilidad** | Soporta millones de usuarios |
| **Comunidad** | Gran ecosistema de librerías |
