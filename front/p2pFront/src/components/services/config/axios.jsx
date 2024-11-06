import axios from 'axios';

const axiosInstance = axios.create({
    baseURL: 'http://localhost:8000/api/v1/auth',
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

export default axiosInstance;