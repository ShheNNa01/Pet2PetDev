import api from './config/axios';

export const AuthService = {
    async register(userData) {
        try {
            const response = await api.post('/auth/register', {
                user_name: userData.userName,
                user_last_name: userData.userLastName,
                user_email: userData.userEmail,
                user_city: userData.userCity,
                user_country: userData.userCountry,
                user_number: userData.userNumber,
                user_bio: userData.userBio,
                password: userData.password
            });
            return response.data;
        } catch (error) {
            throw error.response?.data || error.message;
        }
    },

    async login(credentials) {
        try {
            // Crear URLSearchParams en lugar de FormData
            const formData = new URLSearchParams();
            formData.append('username', credentials.username);
            formData.append('password', credentials.password);
    
            const response = await api.post('/auth/login', formData, {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
            });
    
            if (response.data.access_token) {
                localStorage.setItem('token', response.data.access_token);
                localStorage.setItem('user', JSON.stringify(response.data.user));
            }
    
            return response.data;
        } catch (error) {
            throw error.response?.data || error.message;
        }
    },

    logout() {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
    },

    getCurrentUser() {
        return JSON.parse(localStorage.getItem('user'));
    },

    isAuthenticated() {
        return !!localStorage.getItem('token');
    }
};