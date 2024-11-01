
import axiosInstance from '../services/config/axios';

export const authService = {
    login: async (credentials) => {
        try {
            const response = await axiosInstance.post('/login', credentials);
            if (response.data.token) {
                localStorage.setItem('token', response.data.token);
            }
            return response.data;
        } catch (error) {
            throw error.response?.data || error.message;
        }
    },

    register: async (userData) => {
        try {
            const response = await axiosInstance.post('/register', userData);
            return response.data;
        } catch (error) {
            throw error.response?.data || error.message;
        }
    },

    logout: () => {
        localStorage.removeItem('token');
    }
};