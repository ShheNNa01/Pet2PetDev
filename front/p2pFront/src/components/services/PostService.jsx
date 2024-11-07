// services/postService.js
import axiosInstance from './config/axios';

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
    }
};