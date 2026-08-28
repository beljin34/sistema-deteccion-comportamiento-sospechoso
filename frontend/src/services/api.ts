import axios, { AxiosInstance } from 'axios';
import { Activity, PaginatedResponse } from '../types';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const apiClient: AxiosInstance = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para agregar token JWT
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Interceptor para manejar errores
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('authToken');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Activities endpoints
export const fetchActivities = () =>
  apiClient.get<PaginatedResponse<Activity>>('/activities/').then(r => r.data);

export const fetchActivityById = (id: number) =>
  apiClient.get<Activity>(`/activities/${id}/`).then(r => r.data);

export const analyzeVideo = (file: File, location: string = 'Unknown') => {
  const formData = new FormData();
  formData.append('video', file);
  formData.append('location', location);
  return apiClient.post('/activities/analyze_video/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  }).then(r => r.data);
};

export const deleteActivity = (id: number) =>
  apiClient.delete(`/activities/${id}/`);

export default apiClient;
