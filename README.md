# Sistema de Detección de Comportamiento Sospechoso

## 📋 Descripción General
Proyecto educativo que implementa un sistema de detección de comportamiento sospechoso mediante análisis de patrones de conducta y visión por computadora, utilizando arquitectura moderna con React (Frontend) y Django (Backend).

## 🏗️ Arquitectura del Proyecto

```
sistema-deteccion-comportamiento-sospechoso/
├── frontend/                 # React Application
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── App.tsx
│   └── package.json
├── backend/                  # Django Application
│   ├── config/
│   ├── api/
│   ├── manage.py
│   └── requirements.txt
└── docker-compose.yml
```

## 🛠️ Tecnologías

### Frontend (React)
- **React 18+** - Librería UI
- **TypeScript** - Type safety
- **Axios** - HTTP client
- **React Router** - Navigation
- **TailwindCSS** - Styling

### Backend (Django)
- **Django 4.2+** - Framework web
- **Django REST Framework** - API REST
- **PostgreSQL** - Database
- **Celery** - Async tasks
- **OpenCV** - Computer vision

## 📌 Tarea 7: Frameworks de Desarrollo

### Criterios de Evaluación (Excelencia 95-100%)
✅ Ambos frameworks integrados y funcionando
✅ Explicación técnica clara
✅ Buenas prácticas de organización del código

## 🚀 Inicio Rápido

### Instalación
```bash
# Backend
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

# Frontend
cd ../frontend
npm install
npm start
```

## 📚 Documentación
- [Arquitectura Backend](./backend/ARCHITECTURE.md)
- [Arquitectura Frontend](./frontend/ARCHITECTURE.md)
- [Guía de Integración](./INTEGRATION.md)
