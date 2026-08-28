# Arquitectura Frontend - React

## 🎯 Rol del Framework React

React es una librería JavaScript para construir interfaces de usuario componibles:

### 1. **Componentes Reutilizables**
```tsx
// src/components/ActivityCard.tsx
import React from 'react';
import { Activity } from '../types';

interface ActivityCardProps {
  activity: Activity;
  onViewDetails: (id: number) => void;
}

const ActivityCard: React.FC<ActivityCardProps> = ({ activity, onViewDetails }) => (
  <div className="border rounded-lg p-4 bg-white shadow-md hover:shadow-lg transition">
    <h3 className="text-lg font-bold">{activity.activity_type}</h3>
    <p className="text-gray-600">Confianza: {(activity.confidence * 100).toFixed(2)}%</p>
    <p className="text-sm text-gray-500">{activity.location}</p>
    <button 
      onClick={() => onViewDetails(activity.id)}
      className="mt-3 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
    >
      Ver Detalles
    </button>
  </div>
);

export default ActivityCard;
```

### 2. **Gestión de Estado**
```tsx
// src/hooks/useActivities.ts
import { useState, useEffect } from 'react';
import { Activity } from '../types';
import { fetchActivities } from '../services/api';

const useActivities = () => {
  const [activities, setActivities] = useState<Activity[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadActivities = async () => {
      try {
        const data = await fetchActivities();
        setActivities(data);
      } catch (err) {
        setError((err as Error).message);
      } finally {
        setLoading(false);
      }
    };

    loadActivities();
  }, []);

  return { activities, loading, error };
};

export default useActivities;
```

### 3. **Comunicación con Backend**
```tsx
// src/services/api.ts
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para agregar token
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const fetchActivities = () => apiClient.get('/activities/').then(r => r.data);
export const analyzeVideo = (file: File) => {
  const formData = new FormData();
  formData.append('video', file);
  return apiClient.post('/activities/analyze_video/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};
```

### 4. **Routing**
```tsx
// src/App.tsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import VideoUpload from './pages/VideoUpload';
import ActivityDetails from './pages/ActivityDetails';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/upload" element={<VideoUpload />} />
        <Route path="/activity/:id" element={<ActivityDetails />} />
      </Routes>
    </Router>
  );
}

export default App;
```

### 5. **Renderizado Dinámico**
```tsx
// src/pages/Dashboard.tsx
import React from 'react';
import useActivities from '../hooks/useActivities';
import ActivityCard from '../components/ActivityCard';
import LoadingSpinner from '../components/LoadingSpinner';

const Dashboard: React.FC = () => {
  const { activities, loading, error } = useActivities();

  if (loading) return <LoadingSpinner />;
  if (error) return <div className="text-red-500">Error: {error}</div>;

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-6">Dashboard de Actividades</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {activities.map(activity => (
          <ActivityCard 
            key={activity.id} 
            activity={activity}
            onViewDetails={(id) => console.log(`Ver: ${id}`)}
          />
        ))}
      </div>
    </div>
  );
};

export default Dashboard;
```

## 🔄 Flujo de Datos

```
Usuario → Componente React
   ↓
Maneja evento (click, submit)
   ↓
Llama API (axios)
   ↓
Backend Django procesa
   ↓
Retorna JSON
   ↓
Actualiza estado (useState)
   ↓
Re-renderiza componente
   ↓
Usuario ve cambios
```

## 🎨 Ventajas de React

| Aspecto | Beneficio |
|--------|----------|
| **Virtual DOM** | Renderizado eficiente |
| **Componentes** | Código reutilizable |
| **Unidireccional** | Fácil debugging |
| **Comunidad** | Ecosistema enorme |
| **Performance** | Lazy loading, code splitting |
| **Herramientas** | DevTools, testing frameworks |
