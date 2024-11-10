import axiosInstance from './config/axios';

const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB en bytes

export const postService = {
    // Obtener todos los posts con paginación y filtros opcionales
    getPosts: async (params = {}) => {
        try {
            const { skip = 0, limit = 10, pet_id, location, from_date, to_date, has_media } = params;
            const response = await axiosInstance.get('/posts', {
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

    // Obtener un post específico
    getPostById: async (postId) => {
        try {
            const response = await axiosInstance.get(`/posts/${postId}`);
            return response.data;
        } catch (error) {
            console.error('Error obteniendo post:', error);
            throw error;
        }
    },

    // Crear un nuevo post
    createPost: async (postData) => {
        try {
            const formData = new FormData();
            formData.append('content', postData.content);
            formData.append('location', postData.location || '');
            formData.append('pet_id', postData.pet_id);

            if (postData.files && postData.files.length > 0) {
                postData.files.forEach(file => {
                    formData.append('files', file);
                });
            }

            const response = await axiosInstance.post('/posts', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            return response.data;
        } catch (error) {
            console.error('Error creando post:', error);
            throw error;
        }
    },

    // Validar archivo
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