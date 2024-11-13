// src/components/services/config/axios.jsx
import axios from 'axios';

// Determinar el entorno y establecer la URL base
const isDevelopment = import.meta.env.MODE === 'development';
const BASE_URL = isDevelopment 
    ? 'http://localhost:8000/api/v1'
    : 'https://pet2petbackdeploy-production.up.railway.app/api/v1';  // Cambia esto por tu URL de producción

// Determinar la URL de medios
const MEDIA_URL = isDevelopment
    ? 'http://localhost:8000'
    : 'https://pet2petbackdeploy-production.up.railway.app';  // Cambia esto por tu URL de producción

const axiosInstance = axios.create({
    baseURL: BASE_URL,
    headers: {
        'Accept': 'application/json',
    },
});

// Interceptor para añadir el token a las peticiones
axiosInstance.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        // No establecer Content-Type por defecto, dejarlo para cada petición
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Exportar tanto la instancia como las URLs
export const getMediaUrl = (url) => {
    if (!url) return '/placeholder.svg';
    if (url.startsWith('http')) return url;
    
    // Limpiar y normalizar la URL
    const cleanUrl = url.replace(/\\/g, '/');
    
    // Si la URL ya empieza con media/, simplemente añadir el BASE_URL
    if (cleanUrl.startsWith('media/')) {
        return `${MEDIA_URL}/${cleanUrl}`;
    }
    
    // Si no, asegurarse de que tenga el prefijo media/
    return `${MEDIA_URL}/media/${cleanUrl}`;
};

export { MEDIA_URL, BASE_URL };
export default axiosInstance;