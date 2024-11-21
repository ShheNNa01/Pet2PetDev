// src/components/services/config/axios.jsx
import axios from 'axios';

const isDevelopment = import.meta.env.MODE === 'development';
const BASE_URL = isDevelopment 
    ? 'http://localhost:8000/api/v1'
    : 'https://pet2petbackdeploy-production.up.railway.app/api/v1';

const MEDIA_URL = isDevelopment
    ? 'http://localhost:8000'
    : 'https://pet2petbackdeploy-production.up.railway.app';

const axiosInstance = axios.create({
    baseURL: BASE_URL,
    headers: {
        'Accept': 'application/json',
    },
});

let isRefreshing = false;
let failedQueue = [];

const processQueue = (error, token = null) => {
    failedQueue.forEach(prom => {
        if (error) {
            prom.reject(error);
        } else {
            prom.resolve(token);
        }
    });
    failedQueue = [];
};

const handleTokenRefresh = async () => {
    try {
        const refreshToken = localStorage.getItem('refresh_token');
        console.log('🔄 Iniciando refresh con token:', refreshToken?.substring(0, 20) + '...');

        if (!refreshToken) {
            throw new Error('No refresh token available');
        }

        // Crear una instancia específica para el refresh
        const refreshRequest = await axios({
            method: 'post',
            url: `${BASE_URL}/auth/refresh`,
            data: { refresh_token: refreshToken },
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        });

        console.log('✅ Respuesta del refresh:', refreshRequest.data);

        if (refreshRequest.data.access_token) {
            localStorage.setItem('token', refreshRequest.data.access_token);
            if (refreshRequest.data.refresh_token) {
                localStorage.setItem('refresh_token', refreshRequest.data.refresh_token);
            }
            return refreshRequest.data;
        }

        throw new Error('No se recibió access_token en la respuesta');
    } catch (error) {
        console.error('❌ Error en refresh:', error);
        console.error('📝 Detalles del error:', {
            message: error.message,
            response: error.response?.data,
            status: error.response?.status
        });
        throw error;
    }
};

// Interceptor para las peticiones
axiosInstance.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
            console.log('📤 Enviando petición con token:', token.substring(0, 20) + '...');
        }
        return config;
    },
    (error) => {
        console.error('❌ Error en interceptor de request:', error);
        return Promise.reject(error);
    }
);

// Interceptor para las respuestas
axiosInstance.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;
        console.log('🔍 Error interceptado:', {
            status: error.response?.status,
            url: originalRequest?.url,
            isRetry: !!originalRequest._retry
        });

        if (
            error.response?.status === 401 && 
            !originalRequest._retry &&
            !originalRequest.url.includes('/auth/refresh')
        ) {
            console.log('🔄 Detectado error 401, iniciando refresh...');

            if (isRefreshing) {
                console.log('⏳ Refresh en proceso, añadiendo petición a la cola');
                return new Promise((resolve, reject) => {
                    failedQueue.push({ resolve, reject });
                }).then(token => {
                    console.log('✅ Petición recuperada de la cola, reintentando');
                    originalRequest.headers['Authorization'] = `Bearer ${token}`;
                    return axiosInstance(originalRequest);
                });
            }

            isRefreshing = true;
            originalRequest._retry = true;

            try {
                console.log('🔄 Ejecutando refresh token...');
                const response = await handleTokenRefresh();
                console.log('✅ Refresh exitoso, reintentando petición original');
                
                originalRequest.headers['Authorization'] = `Bearer ${response.access_token}`;
                processQueue(null, response.access_token);
                
                return axiosInstance(originalRequest);
            } catch (refreshError) {
                console.error('❌ Error en proceso de refresh:', refreshError);
                processQueue(refreshError, null);
                
                if (refreshError.response?.status === 401 || 
                    refreshError.message.includes('token')) {
                    console.log('🚫 Error de autenticación, redirigiendo al login');
                    localStorage.removeItem('token');
                    localStorage.removeItem('refresh_token');
                    localStorage.removeItem('user');
                    window.location.href = '/login';
                }
                
                return Promise.reject(refreshError);
            } finally {
                isRefreshing = false;
            }
        }

        return Promise.reject(error);
    }
);

export const getMediaUrl = (url) => {
    if (!url) return '/placeholder.svg';
    if (url.startsWith('http')) return url;
    const cleanUrl = url.replace(/\\/g, '/');
    return cleanUrl.startsWith('media/') 
        ? `${MEDIA_URL}/${cleanUrl}`
        : `${MEDIA_URL}/media/${cleanUrl}`;
};

export { MEDIA_URL, BASE_URL };
export default axiosInstance;