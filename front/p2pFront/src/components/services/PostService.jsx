import axiosInstance from './config/axios';

const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB en bytes

export const postService = {
    getPosts: async (params = {}) => {
        try {
            const { skip = 0, limit = 10, pet_id, location, from_date, to_date, has_media } = params;
            const response = await axiosInstance.get('/posts/', {
                params: {
                    skip,
                    limit,
                    pet_id,
                    location,
                    from_date,
                    to_date,
                    has_media
                }
            });
            return response.data;
        } catch (error) {
            console.error('Error obteniendo posts:', error);
            throw error;
        }
    },

    getPostById: async (postId) => {
        try {
            const response = await axiosInstance.get(`/posts/${postId}`);
            return response.data;
        } catch (error) {
            console.error('Error obteniendo post:', error);
            throw error;
        }
    },

    createPost: async (postData, onSuccess) => {
        try {
            console.log('Datos recibidos en createPost:', postData);
            const formData = new FormData();
            formData.append('content', postData.content || '');
            formData.append('location', postData.location); // Usamos la ciudad del usuario
            formData.append('pet_id', postData.pet_id);
            
            if (postData.files && postData.files.length > 0) {
                postData.files.forEach(file => {
                    formData.append('files', file);
                });
            }

            const response = await axiosInstance.post('/posts/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            
            console.log('Respuesta del servidor:', response.data);
            
            // Llamamos al callback de éxito si se proporciona
            if (onSuccess && typeof onSuccess === 'function') {
                onSuccess(response.data);
            }
            
            return response.data;
        } catch (error) {
            console.error('Error completo al crear post:', {
                message: error.message,
                response: error.response?.data,
                status: error.response?.status
            });
            throw error;
        }
    },

    validateFile: (file) => {
        if (file.size > MAX_FILE_SIZE) {
            throw new Error(`El archivo ${file.name} excede el límite de 5MB`);
        }
        const validTypes = ['image/jpeg', 'image/png', 'image/gif', 'video/mp4'];
        if (!validTypes.includes(file.type)) {
            throw new Error(`El archivo ${file.name} no es un tipo válido. Se permiten jpg, png, gif y mp4`);
        }
        return true;
    }
};